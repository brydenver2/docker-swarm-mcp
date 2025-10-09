"""
FastAPI MCP Integration with Dynamic Tool Gating

This module provides MCP JSON-RPC protocol handlers with integrated tool gating,
schema validation, and enhanced observability.
"""

import json
import logging
import uuid
from typing import Any

import jsonschema
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core.auth import verify_token_with_scopes
from app.mcp.tool_gating import FilterContext, ToolGateController
from app.mcp.tool_registry import ToolRegistry
from app.services import container_service, network_service, service_service, stack_service, volume_service

logger = logging.getLogger(__name__)

router = APIRouter()


class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request structure"""
    jsonrpc: str = Field(default="2.0", pattern="^2\\.0$")
    method: str
    params: dict[str, Any] | None = None
    id: str | int | None = None


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response structure"""
    jsonrpc: str = "2.0"
    result: Any | None = None
    error: dict[str, Any] | None = None
    id: str | int | None = None


class JSONRPCError:
    """JSON-RPC error codes"""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603

    @staticmethod
    def create_error(code: int, message: str, data: Any | None = None) -> dict[str, Any]:
        error = {"code": code, "message": message"}
        if data is not None:
            error["data"] = data
        return error


class DynamicToolGatingMCP:
    """MCP server with dynamic tool gating and schema validation"""

    def __init__(
        self,
        tool_registry: ToolRegistry,
        tool_gate_controller: ToolGateController
    ):
        self.tool_registry = tool_registry
        self.tool_gate_controller = tool_gate_controller
        self.service_map = self._build_service_map()

        # Validate schemas at startup
        self._validate_schemas_at_startup()

    def _build_service_map(self) -> dict[str, Any]:
        """Map tool names to service functions"""
        return {
            # Container operations
            "list-containers": container_service.list_containers,
            "create-container": container_service.create_container,
            "start-container": container_service.start_container,
            "stop-container": container_service.stop_container,
            "remove-container": container_service.remove_container,
            "get-logs": container_service.get_logs,

            # Stack operations
            "deploy-compose": stack_service.deploy_compose,
            "list-stacks": stack_service.list_stacks,
            "remove-compose": stack_service.remove_compose,

            # Service operations
            "list-services": service_service.list_services,
            "scale-service": service_service.scale_service,
            "remove-service": service_service.remove_service,

            # Network operations
            "list-networks": network_service.list_networks,
            "create-network": network_service.create_network,
            "remove-network": network_service.remove_network,

            # Volume operations
            "list-volumes": volume_service.list_volumes,
            "create-volume": volume_service.create_volume,
            "remove-volume": volume_service.remove_volume,
        }

    def _validate_schemas_at_startup(self) -> None:
        """Validate that all tools have valid JSON schemas"""
        all_tools = self.tool_registry.get_all_tools()
        schema_mismatches = []

        for tool_name, tool in all_tools.items():
            # Validate request schema if present
            if tool.request_schema:
                try:
                    jsonschema.Draft7Validator.check_schema(tool.request_schema)
                except jsonschema.SchemaError as e:
                    schema_mismatches.append(f"{tool_name} request_schema: {e}")

            # Validate response schema
            try:
                jsonschema.Draft7Validator.check_schema(tool.response_schema)
            except jsonschema.SchemaError as e:
                schema_mismatches.append(f"{tool_name} response_schema: {e}")

        if schema_mismatches:
            logger.error(f"Schema validation failures at startup: {schema_mismatches}")
            raise ValueError(f"Schema validation failures: {schema_mismatches}")

        logger.info(f"Successfully validated schemas for {len(all_tools)} tools")

    async def handle_initialize(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str
    ) -> dict[str, Any]:
        """Handle MCP initialize request"""
        logger.info(
            "MCP initialize request",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "client_info": params.get("clientInfo") if params else None
            }
        )

        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "docker-mcp-server",
                "version": "0.1.0"
            },
            "capabilities": {
                "tools": {
                    "gating": True,
                    "context_size_enforcement": True,
                    "task_type_filtering": True
                }
            }
        }

    async def handle_tools_list(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str,
        scopes: set[str]
    ) -> dict[str, Any]:
        """Handle tools/list with integrated gating"""
        task_type = params.get("task_type") if params else None

        context = FilterContext(
            task_type=task_type,
            client_id=None,
            session_id=session_id,
            request_id=request_id
        )

        # Apply gating filters
        filtered_tools = self.tool_gate_controller.get_available_tools(context)

        # Apply scope-based filtering
        if scopes and "admin" not in scopes:
            filtered_tools = {
                name: tool
                for name, tool in filtered_tools.items()
                if not any(blocked in tool.task_types for blocked in ["remove", "delete"])
                or any(scope in scopes for scope in tool.task_types)
            }

        # Compute context size
        context_size = self.tool_gate_controller.get_context_size(filtered_tools)

        logger.info(
            f"tools/list: {len(filtered_tools)} tools returned",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "task_type": task_type,
                "tool_count": len(filtered_tools),
                "context_size": context_size,
                "scopes": list(scopes)
            }
        )

        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.request_schema or {"type": "object"},
                }
                for tool in filtered_tools.values()
            ],
            "_metadata": {
                "context_size": context_size,
                "filters_applied": self._get_applied_filters(context)
            }
        }

    async def handle_tools_call(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str,
        scopes: set[str],
        docker_client: Any
    ) -> dict[str, Any]:
        """Handle tools/call with gating enforcement and schema validation"""
        if not params or "name" not in params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing 'name' parameter"
            )

        tool_name = params["name"]
        tool_params = params.get("arguments", {})

        # Re-build context for gating check
        context = FilterContext(
            task_type=None,  # Could extract from session if needed
            client_id=None,
            session_id=session_id,
            request_id=request_id
        )

        # Get gated tools
        filtered_tools = self.tool_gate_controller.get_available_tools(context)

        # Check if tool is in gated set
        if tool_name not in filtered_tools:
            logger.warning(
                f"Tool '{tool_name}' blocked by gating",
                extra={"request_id": request_id, "session_id": session_id, "tool": tool_name}
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=JSONRPCError.create_error(
                    JSONRPCError.METHOD_NOT_FOUND,
                    f"Tool '{tool_name}' not available or blocked",
                    {"available_tools": list(filtered_tools.keys())}
                )
            )

        tool = filtered_tools[tool_name]

        # Scope-based validation
        if scopes and "admin" not in scopes:
            if not any(scope in scopes for scope in tool.task_types):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions for this tool"
                )

        # Validate input parameters against request_schema
        if tool.request_schema:
            try:
                jsonschema.validate(instance=tool_params, schema=tool.request_schema)
            except jsonschema.ValidationError as e:
                logger.warning(
                    f"Input validation failed for '{tool_name}'",
                    extra={
                        "request_id": request_id,
                        "session_id": session_id,
                        "tool": tool_name,
                        "error": str(e)
                    }
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=JSONRPCError.create_error(
                        JSONRPCError.INVALID_PARAMS,
                        f"Invalid parameters: {e.message}",
                        {"path": list(e.absolute_path), "schema_path": list(e.absolute_schema_path)}
                    )
                )

        # Call service function
        service_func = self.service_map.get(tool_name)
        if not service_func:
            logger.error(
                f"Service function not found for '{tool_name}'",
                extra={"request_id": request_id, "session_id": session_id, "tool": tool_name}
            )
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"Service function for '{tool_name}' not implemented"
            )

        # Execute service function
        try:
            result = await service_func(docker_client, tool_params)
        except Exception as e:
            logger.error(
                f"Service execution failed for '{tool_name}'",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "tool": tool_name,
                    "error": str(e)
                },
                exc_info=True
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=JSONRPCError.create_error(
                    JSONRPCError.INTERNAL_ERROR,
                    f"Tool execution failed: {str(e)}"
                )
            )

        # Validate output against response_schema
        try:
            jsonschema.validate(instance=result, schema=tool.response_schema)
        except jsonschema.ValidationError as e:
            logger.error(
                f"Output validation failed for '{tool_name}'",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "tool": tool_name,
                    "error": str(e)
                }
            )
            # Log but don't fail the request - this is a server-side schema issue

        logger.info(
            f"tools/call: '{tool_name}' executed successfully",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "jsonrpc_method": "tools/call",
                "tool_name": tool_name
            }
        )

        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

    def _get_applied_filters(self, context: FilterContext) -> list[str]:
        """Get list of applied filters based on context"""
        filters = []
        if context.task_type:
            filters.append("TaskTypeFilter")
        if len(self.tool_gate_controller.all_tools) > self.tool_gate_controller.config.max_tools:
            filters.append("ResourceFilter")
        if self.tool_gate_controller.config.blocklist:
            filters.append("SecurityFilter")
        return filters


@router.post("/", dependencies=[Depends(verify_token_with_scopes)])
async def mcp_endpoint(
    request: Request,
    jsonrpc_request: JSONRPCRequest,
    scopes: set[str] = Depends(verify_token_with_scopes)
) -> JSONRPCResponse:
    """
    Main MCP JSON-RPC endpoint with integrated gating and observability

    Handles:
    - initialize
    - tools/list (with task_type parameter and gating)
    - tools/call (with gating enforcement and schema validation)
    """
    request_id = str(uuid.uuid4())
    session_id = request.headers.get("X-Session-ID", str(uuid.uuid4()))

    # Enhanced logging with session context
    logger.info(
        f"MCP JSON-RPC request: {jsonrpc_request.method}",
        extra={
            "request_id": request_id,
            "session_id": session_id,
            "jsonrpc_method": jsonrpc_request.method,
            "has_params": jsonrpc_request.params is not None
        }
    )

    tool_registry: ToolRegistry = request.app.state.tool_registry
    tool_gate_controller: ToolGateController = request.app.state.tool_gate_controller
    docker_client = request.app.state.docker_client

    mcp_server = DynamicToolGatingMCP(tool_registry, tool_gate_controller)

    try:
        if jsonrpc_request.method == "initialize":
            result = await mcp_server.handle_initialize(
                jsonrpc_request.params,
                request_id,
                session_id
            )
        elif jsonrpc_request.method == "tools/list":
            result = await mcp_server.handle_tools_list(
                jsonrpc_request.params,
                request_id,
                session_id,
                scopes
            )
        elif jsonrpc_request.method == "tools/call":
            result = await mcp_server.handle_tools_call(
                jsonrpc_request.params,
                request_id,
                session_id,
                scopes,
                docker_client
            )
        else:
            logger.warning(
                f"Unknown JSON-RPC method: {jsonrpc_request.method}",
                extra={"request_id": request_id, "session_id": session_id}
            )
            return JSONRPCResponse(
                id=jsonrpc_request.id,
                error=JSONRPCError.create_error(
                    JSONRPCError.METHOD_NOT_FOUND,
                    f"Method '{jsonrpc_request.method}' not found"
                )
            )

        return JSONRPCResponse(id=jsonrpc_request.id, result=result)

    except HTTPException as e:
        logger.error(
            f"HTTP exception in MCP handler",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "status_code": e.status_code,
                "detail": e.detail
            }
        )
        return JSONRPCResponse(
            id=jsonrpc_request.id,
            error=e.detail if isinstance(e.detail, dict) else JSONRPCError.create_error(
                JSONRPCError.INTERNAL_ERROR,
                str(e.detail)
            )
        )

    except Exception as e:
        logger.error(
            f"Unexpected error in MCP handler",
            extra={"request_id": request_id, "session_id": session_id},
            exc_info=True
        )
        return JSONRPCResponse(
            id=jsonrpc_request.id,
            error=JSONRPCError.create_error(
                JSONRPCError.INTERNAL_ERROR,
                f"Internal server error: {str(e)}"
            )
        )
