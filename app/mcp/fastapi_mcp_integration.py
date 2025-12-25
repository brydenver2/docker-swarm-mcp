"""
FastAPI MCP Integration with Dynamic Tool Gating

This module provides MCP JSON-RPC protocol handlers with integrated tool gating,
schema validation, and enhanced observability.
"""

import asyncio
import hashlib
import json
import logging
import uuid
from typing import Any

import jsonschema
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from app.core.auth import verify_token_with_scopes
from app.core.config import settings
from app.mcp.tool_gating import FilterContext, Tool, ToolGateController
from app.mcp.tool_registry import ToolRegistry
from app.services import (
    container_service,
    meta_service,
    network_service,
    service_service,
    stack_service,
    system_service,
    volume_service,
)

logger = logging.getLogger(__name__)

router = APIRouter()


class JSONRPCRequest(BaseModel):
    """JSON-RPC 2.0 request structure"""
    jsonrpc: str = Field(default="2.0", pattern="^2\\.0$")
    method: str
    params: dict[str, Any] | None = None
    id: str | int | None = None  # None for notifications


class JSONRPCResponse(BaseModel):
    """JSON-RPC 2.0 response structure"""
    model_config = ConfigDict(exclude_none=True)

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
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return error


class DynamicToolGatingMCP:
    """MCP server with dynamic tool gating and schema validation"""

    def __init__(
        self,
        tool_registry: ToolRegistry,
        tool_gate_controller: ToolGateController,
        intent_classifier: Any = None
    ):
        """
        Initialize the MCP server with the tool registry, gate controller, and optional intent classifier.
        
        Builds the internal service map, initializes per-session gating state, and validates all tool request/response schemas at startup.
        
        Parameters:
            tool_registry: Registry that provides available tools and their metadata.
            tool_gate_controller: Controller used to compute which tools are allowed given a filter context.
            intent_classifier: Optional component used to classify natural-language queries into task types (may be None).
        
        Raises:
            ValueError: If schema validation finds mismatches in tool request/response schemas.
        """
        self.tool_registry = tool_registry
        self.tool_gate_controller = tool_gate_controller
        self.intent_classifier = intent_classifier
        self.service_map = self._build_service_map()

        # Session-based tool gating: store last filtered tool set per session
        self.session_tools: dict[str, dict[str, Tool]] = {}

        # Validate schemas at startup
        self._validate_schemas_at_startup()

    def _build_service_map(self) -> dict[str, Any]:
        """Map tool names to service functions"""
        return {
            # System operations
            "ping": system_service.ping,
            "info": system_service.info,

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

            # Meta operations - wrap with config
            "discover-tools": lambda docker_client, params: meta_service.discover_tools(docker_client, params, self.tool_gate_controller.config),
            "list-task-types": lambda docker_client, params: meta_service.list_task_types(docker_client, params, self.tool_gate_controller.config),
            "intent-query-help": lambda docker_client, params: meta_service.intent_query_help(docker_client, params),
        }

    def _validate_schemas_at_startup(self) -> None:
        """
        Validate JSON request and response schemas for all registered tools and warn if destructive tools lack required security scopes.
        
        Validates each tool's request_schema (if present) and response_schema using JSON Schema Draft 7. If any schema is invalid, logs the failures and raises a ValueError listing the mismatches. Detects tool names containing the substrings 'remove', 'delete', 'scale', or 'stop' and emits a warning when such destructive tools have no required_scopes configured. Logs a summary info message on successful validation.
        
        Raises:
            ValueError: If one or more request or response schemas are invalid.
        """
        all_tools = self.tool_registry.get_all_tools()
        schema_mismatches = []
        security_warnings = []

        # Destructive operation patterns
        destructive_patterns = ['remove', 'delete', 'scale', 'stop']

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

            # Security validation for destructive tools
            tool_name_lower = tool_name.lower()
            is_destructive = any(pattern in tool_name_lower for pattern in destructive_patterns)

            if is_destructive and not tool.required_scopes:
                security_warnings.append(
                    f"Destructive tool '{tool_name}' lacks required_scopes. "
                    f"Consider adding 'required_scopes: [\"admin\"]' for security."
                )

        if schema_mismatches:
            logger.error(f"Schema validation failures at startup: {schema_mismatches}")
            raise ValueError(f"Schema validation failures: {schema_mismatches}")

        if security_warnings:
            logger.warning(f"Security warnings at startup: {security_warnings}")
            # In production, you might want to raise an error instead of just warning
            # raise ValueError(f"Security issues found: {security_warnings}")

        logger.info(f"Successfully validated schemas for {len(all_tools)} tools")

    @staticmethod
    def _build_input_schema(tool_schema: dict[str, Any] | None) -> dict[str, Any]:
        schema: dict[str, Any] = {
            "type": "object",
            "properties": (tool_schema.get("properties") if tool_schema else {}),
            "required": (tool_schema.get("required") if tool_schema else []),
        }

        if not tool_schema:
            return schema

        for key, value in tool_schema.items():
            if key in {"type", "properties", "required"}:
                continue
            schema[key] = value

        return schema

    async def handle_initialize(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str
    ) -> dict[str, Any]:
        """
        Provide the server protocol version, capabilities, and server information for the MCP initialize request.
        
        Parameters:
            params (dict[str, Any] | None): Optional initialize parameters from the client (ignored by this handler).
            request_id (str): Unique identifier for the incoming JSON-RPC request.
            session_id (str): Identifier for the client session.
        
        Returns:
            dict[str, Any]: A payload containing:
                - protocolVersion (str): MCP protocol version string.
                - capabilities (dict): Feature flags for tools and prompts (gating, context enforcement, task-type filtering, prompt list status).
                - serverInfo (dict): Server metadata with `name` and `version`.
        """
        from app.core.constants import APP_VERSION

        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "gating": True,
                    "context_size_enforcement": True,
                    "task_type_filtering": True
                },
                "prompts": {
                    "listChanged": False
                }
            },
            "serverInfo": {
                "name": "docker-swarm-mcp",
                "version": APP_VERSION
            }
        }

    async def handle_tools_list(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str,
        scopes: set[str],
        task_type_header: str | None = None
    ) -> dict[str, Any]:
        """
        Handle a tools/list request by applying intent classification, gating, and scope-based filtering, then return the matching tools and metadata.
        
        This method:
        - Resolves an effective task type from the task_type_header or params and optionally uses an intent classifier to detect task types from a natural-language query.
        - Enforces strict no-match behavior when intent classification yields no task types and fallback is disabled, returning an empty tool set with a warning.
        - Builds a FilterContext and obtains available tools from the tool gate controller.
        - Applies scope-based filtering (unless the caller has the "admin" scope) and records the filtered tool set for the session.
        - Computes context size and returns a list of tools (with name, description, and inputSchema) plus a _metadata object describing context size, filters applied, classification details, and optional warnings.
        
        Parameters:
            params (dict[str, Any] | None): Request parameters; may contain "task_type" (str) and/or "query" (str).
            request_id (str): Correlation ID for the request, used for logging and metadata.
            session_id (str): Session identifier used to persist session-specific filtered tools.
            scopes (set[str]): Authorization scopes for the caller; used for scope-based tool filtering.
            task_type_header (str | None): Optional task type provided via request header; takes precedence over params when present.
        
        Returns:
            dict[str, Any]: Response payload containing:
              - "tools": list of objects with keys "name", "description", and "inputSchema" (schema derived from the tool's request_schema).
              - "_metadata": object with "context_size", "filters_applied", "classification_method", and when applicable "query", "detected_task_types", and "warning".
        """
        # Support both header and param for backward compatibility
        task_type = task_type_header or (params.get("task_type") if params else None)
        query = params.get("query") if params else None

        # Intent classification
        detected_task_types = None
        classification_method = "none"

        if query and self.intent_classifier and settings.INTENT_CLASSIFICATION_ENABLED:
            detected_task_types = self.intent_classifier.classify_intent(query)
            classification_method = "intent"
            # Query takes precedence over explicit task_type based on INTENT_PRECEDENCE setting
            if settings.INTENT_PRECEDENCE == "intent":
                task_type = None
            logger.info(
                f"Intent classifier detected task types: {detected_task_types}",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "detected_task_types": detected_task_types,
                    "precedence": settings.INTENT_PRECEDENCE
                }
            )
        elif query and not settings.INTENT_CLASSIFICATION_ENABLED:
            classification_method = "none"
            logger.info(
                "Intent classification disabled, treating query as no-op",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "query": query[:100] + "..." if len(query) > 100 else query
                }
            )
        elif task_type:
            classification_method = "explicit"

        # Check for strict no-match behavior
        no_match_strict = (
            query is not None and
            classification_method == "intent" and
            detected_task_types is not None and
            len(detected_task_types) == 0 and
            (settings.STRICT_CONTEXT_LIMIT or not settings.INTENT_FALLBACK_TO_ALL)
        )

        if no_match_strict:
            # Return empty tool set with warning
            filtered_tools = {}
            filters_applied = []

            metadata = {
                "classification_method": "intent",
                "query": query,
                "detected_task_types": [],
                "warning": "No task types detected from query and fallback disabled",
                "context_size": 0
            }

            logger.info(
                "Strict no-match mode: returning empty tool set",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "strict_mode": True,
                    "fallback_disabled": not settings.INTENT_FALLBACK_TO_ALL
                }
            )

            return {
                "tools": [],
                "_metadata": metadata
            }

        context = FilterContext(
            task_type=task_type,
            client_id=None,
            session_id=session_id,
            request_id=request_id,
            query=query,
            detected_task_types=detected_task_types
        )

        # Apply gating filters
        filtered_tools, filters_applied = self.tool_gate_controller.get_available_tools(context)

        # Apply scope-based filtering using required_scopes if available, else task_types
        if scopes and "admin" not in scopes:
            filtered_tools = {
                name: tool
                for name, tool in filtered_tools.items()
                if any(scope in scopes for scope in (tool.required_scopes or tool.task_types))
            }
            # Add scope filtering to applied filters if it changed the tool set
            if len(filtered_tools) < len(self.tool_gate_controller.all_tools):
                filters_applied.append("ScopeFilter")

        # Store filtered tools for this session (for tools/call validation)
        self.session_tools[session_id] = filtered_tools.copy()

        # Compute context size
        context_size = self.tool_gate_controller.get_context_size(filtered_tools)

        logger.info(
            f"tools/list: {len(filtered_tools)} tools returned",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "task_type": task_type,
                "query": query[:50] + "..." if query and len(query) > 50 else query,
                "detected_task_types": detected_task_types,
                "classification_method": classification_method,
                "tool_count": len(filtered_tools),
                "context_size": context_size,
                "scopes": list(scopes)
            }
        )

        # Build metadata
        metadata = {
            "context_size": context_size,
            "filters_applied": filters_applied,
            "classification_method": classification_method
        }

        if query:
            metadata["query"] = query
            # Always include detected_task_types when query is present, even if empty
            metadata["detected_task_types"] = detected_task_types or []

            # Add warning if classification returned no matches and fallback is disabled
            if (detected_task_types is not None and
                len(detected_task_types) == 0 and
                (settings.STRICT_CONTEXT_LIMIT or not settings.INTENT_FALLBACK_TO_ALL)):
                metadata["warning"] = "No task types detected from query and fallback disabled"

        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": self._build_input_schema(tool.request_schema)
                }
                for tool in filtered_tools.values()
            ],
            "_metadata": metadata
        }

    async def handle_prompts_list(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str
    ) -> dict[str, Any]:
        """Handle prompts/list request"""
        logger.info(
            "prompts/list request",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "jsonrpc_method": "prompts/list"
            }
        )

        return {
            "prompts": [
                {
                    "name": "discover-tools",
                    "title": "Discover Tools Guide",
                    "description": "Learn how to discover tools by task type",
                    "arguments": []
                },
                {
                    "name": "list-task-types",
                    "title": "Task Types List",
                    "description": "View all available task types and their tools",
                    "arguments": []
                },
                {
                    "name": "intent-query-help",
                    "title": "Natural Language Query Help",
                    "description": "Learn how to use natural language queries for tool discovery",
                    "arguments": []
                }
            ]
        }

    async def handle_prompts_get(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str,
        jsonrpc_id: str | int | None = None
    ) -> JSONRPCResponse:
        """
        Retrieve a predefined prompt by name and return it formatted as a JSON-RPC response.
        
        Supported prompt names:
        - "discover-tools": Returns a brief guide describing available tools and task types, with examples for tools/list.
        - "list-task-types": Returns a detailed listing of task types and example tools (derived from configuration if available, otherwise from the tool registry).
        - "intent-query-help": Returns guidance and examples for using natural language queries with tools/list.
        
        Parameters:
            params (dict[str, Any] | None): Must include a "name" key with the prompt name to retrieve.
            request_id (str): Correlation ID for logging.
            session_id (str): Session identifier for logging and session-scoped behavior.
            jsonrpc_id (str | int | None): The JSON-RPC id to include in the response.
        
        Returns:
            JSONRPCResponse: On success, contains a `result` with `description` and `messages` (user-facing text content). If `params` is missing or the prompt name is unknown, returns an `error` with `INVALID_PARAMS`.
        """
        if not params or "name" not in params:
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INVALID_PARAMS,
                    "Missing 'name' parameter"
                )
            )

        prompt_name = params["name"]

        logger.info(
            f"prompts/get request: {prompt_name}",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "jsonrpc_method": "prompts/get",
                "prompt_name": prompt_name
            }
        )

        if prompt_name == "discover-tools":
            # Load config and compute dynamic values
            task_type_allowlists = self.tool_gate_controller.config.task_type_allowlists
            max_tools = getattr(self.tool_gate_controller.config, "max_tools", 10)
            total_tools = len(self.tool_registry.get_all_tools())

            if not task_type_allowlists:
                # Edge case: no config available - derive from registry
                all_tools = self.tool_registry.get_all_tools()
                task_type_groups = {}

                for tool_name, tool in all_tools.items():
                    for task_type in tool.task_types:
                        if task_type not in task_type_groups:
                            task_type_groups[task_type] = []
                        task_type_groups[task_type].append(tool_name)

                total_task_types = len(task_type_groups)
                task_type_source = task_type_groups
            else:
                # Normal case: use config
                total_task_types = len(task_type_allowlists)
                task_type_source = task_type_allowlists

            # Build task_types_text with truncation for token efficiency
            task_type_lines = []
            for task_type, tool_names in sorted(task_type_source.items()):
                tool_count = len(tool_names)
                sorted_tools = sorted(tool_names)
                if tool_count > 5:
                    tools_str = ", ".join(sorted_tools[:5]) + f" ... (and {tool_count-5} more)"
                else:
                    tools_str = ", ".join(sorted_tools)
                task_type_lines.append(f"- {task_type}: {tool_count} tools (e.g., {tools_str})")

            task_types_text = "\n".join(task_type_lines)

            # Compose concise message
            message_text = (
                f"This server exposes {total_tools} Docker tools organized into {total_task_types} task types. "
                f"By default, only {max_tools} tools are shown. To access specific tools, use the task_type parameter in tools/list.\n\n"
                f"Available task types:\n{task_types_text}\n\n"
                'Example: {"method": "tools/list", "params": {"task_type": "container-ops"}}'
            )

            return JSONRPCResponse(
                id=jsonrpc_id,
                result={
                    "description": "Guide to discovering Docker tools by task type",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": message_text
                            }
                        }
                    ]
                }
            )
        elif prompt_name == "list-task-types":
            # Dynamically generate from config with edge case guard
            task_type_allowlists = self.tool_gate_controller.config.task_type_allowlists

            if not task_type_allowlists:
                # Edge case: no config available - enumerate all tools from registry grouped by task_types
                all_tools = self.tool_registry.get_all_tools()
                task_type_groups = {}

                for tool_name, tool in all_tools.items():
                    for task_type in tool.task_types:
                        if task_type not in task_type_groups:
                            task_type_groups[task_type] = []
                        task_type_groups[task_type].append(tool_name)

                task_types_info = []
                for task_type, tool_names in sorted(task_type_groups.items()):
                    tool_count = len(tool_names)
                    if tool_count > 5:
                        # Show first 5 tools and note about truncation
                        first_five = sorted(tool_names)[:5]
                        tools_str = ", ".join(first_five) + f" ... (and {tool_count - 5} more)"
                    else:
                        tools_str = ", ".join(sorted(tool_names))
                    task_types_info.append(f"Task Type: {task_type} ({tool_count} tools)\nTools: {tools_str}")

                content_text = "No task type configuration found. Showing all tools from registry grouped by task types:\n\n" + "\n\n".join(task_types_info)
                content_text += "\n\nNote: Use tools/list for complete details on all available tools."
            else:
                # Normal case: use config with truncation for long lists
                task_types_info = []
                for task_type, tool_names in task_type_allowlists.items():
                    tool_count = len(tool_names)
                    if tool_count > 5:
                        # Show first 5 tools and note about truncation
                        first_five = tool_names[:5]
                        tools_str = ", ".join(first_five) + f" ... (and {tool_count - 5} more)"
                    else:
                        tools_str = ", ".join(tool_names)
                    task_types_info.append(f"Task Type: {task_type} ({tool_count} tools)\nTools: {tools_str}")

                content_text = "\n\n".join(task_types_info)
                content_text += "\n\nNote: Use tools/list for complete details on all available tools."

            return JSONRPCResponse(
                id=jsonrpc_id,
                result={
                    "description": "Complete list of task types and tools",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": content_text
                            }
                        }
                    ]
                }
            )
        elif prompt_name == "intent-query-help":
            return JSONRPCResponse(
                id=jsonrpc_id,
                result={
                    "description": "Guide to using natural language queries",
                    "messages": [
                        {
                            "role": "user",
                            "content": {
                                "type": "text",
                                "text": (
                                    "Instead of specifying task_type, you can use natural language queries. "
                                    "The server will automatically detect relevant task types.\n\n"
                                    "Examples:\n"
                                    "- 'Show me running containers' → container-ops tools\n"
                                    "- 'Deploy a compose stack' → compose-ops tools\n"
                                    "- 'Scale a service' → service-ops tools\n"
                                    "- 'Create a network' → network-ops tools\n"
                                    "- 'Check Docker status' → system-ops tools\n\n"
                                    'Use the query parameter: {"method": "tools/list", "params": {"query": "your natural language request"}}'
                                )
                            }
                        }
                    ]
                }
            )
        else:
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INVALID_PARAMS,
                    f"Unknown prompt name: {prompt_name}"
                )
            )

    async def handle_tools_call(
        self,
        params: dict[str, Any] | None,
        request_id: str,
        session_id: str,
        scopes: set[str],
        docker_client: Any,
        jsonrpc_id: str | int | None = None
    ) -> JSONRPCResponse:
        """
        Handle a tools/call request: enforce session gating and scopes, validate input/output schemas, execute the tool, and return a JSON-RPC response.
        
        Validates presence of the tool name, ensures the tool is allowed for the session, checks caller scopes against the tool's required scopes or task types, validates input parameters against the tool's request schema, executes the tool service with an operation-based timeout, validates the tool output against the response schema (optionally enforcing it), and returns a JSONRPCResponse containing either an error or the tool result serialized as a text content payload.
        
        Parameters:
            params (dict | None): RPC parameters; must include "name" and may include "arguments" for the tool.
            request_id (str): Internal request identifier used for logging and tracing.
            session_id (str): Session identifier used to look up session-filtered tools from prior tools/list calls.
            scopes (set[str]): Caller scopes to validate permission to invoke the tool.
            docker_client (Any): Client used by service functions to perform Docker operations (omitted from detailed docs as a passed service).
            jsonrpc_id (str | int | None): The JSON-RPC request id to include in the response.
        
        Returns:
            JSONRPCResponse: A JSON-RPC 2.0 response containing either an `error` (with standard JSONRPCError fields) or a `result` whose `content` is a list with a single text entry containing the serialized tool output.
        """
        if not params or "name" not in params:
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INVALID_PARAMS,
                    "Missing 'name' parameter"
                )
            )

        tool_name = params["name"]
        tool_params = params.get("arguments", {})

        # Get session-specific filtered tools (from last tools/list call)
        session_filtered_tools = self.session_tools.get(session_id, {})

        # Fallback to all tools if no session tools found (backward compatibility)
        if not session_filtered_tools:
            logger.warning(
                f"No session tools found for session '{session_id}', falling back to all tools",
                extra={"request_id": request_id, "session_id": session_id}
            )
            session_filtered_tools = self.tool_registry.get_all_tools()

        # Check if tool is in session-filtered set - return JSON-RPC error instead of HTTP exception
        if tool_name not in session_filtered_tools:
            logger.warning(
                f"Tool '{tool_name}' blocked by session gating",
                extra={"request_id": request_id, "session_id": session_id, "tool": tool_name}
            )
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.METHOD_NOT_FOUND,
                    f"Tool '{tool_name}' not available or blocked by session gating",
                    {"available_tools": list(session_filtered_tools.keys())}
                )
            )

        tool = session_filtered_tools[tool_name]

        # Scope-based validation using explicit required_scopes if available
        required_scopes = tool.required_scopes if tool.required_scopes else tool.task_types

        if scopes and "admin" not in scopes:
            if not any(scope in scopes for scope in required_scopes):
                return JSONRPCResponse(
                    id=jsonrpc_id,
                    error=JSONRPCError.create_error(
                        JSONRPCError.METHOD_NOT_FOUND,
                        f"Insufficient permissions. Required scopes: {required_scopes}"
                    )
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
                return JSONRPCResponse(
                    id=jsonrpc_id,
                    error=JSONRPCError.create_error(
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
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.METHOD_NOT_FOUND,
                    f"Service function for '{tool_name}' not implemented"
                )
            )

        # Determine timeout based on operation type
        tool_name_lower = tool_name.lower()
        if any(op in tool_name_lower for op in ['list', 'get', 'info', 'ping']):
            timeout = settings.MCP_TIMEOUT_READ_OPS
        elif any(op in tool_name_lower for op in ['remove', 'delete']):
            timeout = settings.MCP_TIMEOUT_DELETE_OPS
        else:
            timeout = settings.MCP_TIMEOUT_WRITE_OPS

        # Execute service function with timeout
        try:
            result = await asyncio.wait_for(
                service_func(docker_client, tool_params),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            logger.error(
                f"Service execution timeout for '{tool_name}'",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "tool": tool_name,
                    "timeout": timeout,
                    "docker_op": tool_name_lower
                }
            )
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INTERNAL_ERROR,
                    f"Tool execution timeout after {timeout}s",
                    {"timeout": timeout, "operation_type": "docker_op"}
                )
            )
        except HTTPException as e:
            # Extract error details from HTTPException
            error_message = e.detail if e.detail else f"HTTP {e.status_code} error"
            logger.error(
                f"Service execution failed for '{tool_name}': {error_message}",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "tool": tool_name,
                    "status_code": e.status_code,
                    "error": error_message
                },
                exc_info=True
            )
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INTERNAL_ERROR,
                    error_message,
                    {"status_code": e.status_code}
                )
            )
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
            return JSONRPCResponse(
                id=jsonrpc_id,
                error=JSONRPCError.create_error(
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
                    "error": str(e),
                    "validation_path": list(e.absolute_path)
                }
            )

            # If enforcement is enabled, fail the request
            if settings.ENFORCE_OUTPUT_SCHEMA:
                return JSONRPCResponse(
                    id=jsonrpc_id,
                    error=JSONRPCError.create_error(
                        JSONRPCError.INTERNAL_ERROR,
                        f"Output validation failed for '{tool_name}': {e.message}",
                        {"path": list(e.absolute_path), "schema_path": list(e.absolute_schema_path)}
                    )
                )
            # Otherwise log but don't fail - this is a server-side schema issue

        logger.info(
            f"tools/call: '{tool_name}' executed successfully",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "jsonrpc_method": "tools/call",
                "tool_name": tool_name
            }
        )

        return JSONRPCResponse(
            id=jsonrpc_id,
            result={"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        )



def _serialize_jsonrpc_response(response: JSONRPCResponse) -> JSONResponse:
    """Serialize JSON-RPC response excluding None values per JSON-RPC 2.0 spec"""
    response_dict = {"jsonrpc": response.jsonrpc}

    # Only include result OR error, not both (JSON-RPC 2.0 spec)
    if response.error is not None:
        response_dict["error"] = response.error
    else:
        response_dict["result"] = response.result

    # Always include id (can be None for notifications)
    response_dict["id"] = response.id

    return JSONResponse(content=response_dict)


@router.post("/")
async def mcp_endpoint(
    request: Request,
    jsonrpc_request: JSONRPCRequest,
    scopes: set[str] = Depends(verify_token_with_scopes),
    x_task_type: str | None = None
) -> JSONResponse:
    """
    Dispatch incoming MCP JSON-RPC requests to the MCP server handlers and return the appropriate JSON-RPC 2.0 response.
    
    Supports the JSON-RPC methods: "initialize", "tools/list", "tools/call", "prompts/list", and "prompts/get". JSON-RPC notifications (requests with no `id`) are accepted and return an empty HTTP 200 response with no JSON-RPC body. When an X-Session-ID header is not provided, a deterministic session id is derived from the presented Authorization token or X-Access-Token (SHA-256 based) when available; otherwise a new UUID is generated. Authentication scopes are provided via the `scopes` dependency and are used for gating and permission checks. The handler obtains the MCP server instance and docker client from the FastAPI app state and forwards requests to the corresponding MCP handlers.
    
    Parameters:
        x_task_type (str | None): Optional X-Task-Type header override used for backward compatibility.
    
    Returns:
        JSONResponse: A JSON-RPC 2.0 response containing either a `result` or an `error` field; notifications return an empty HTTP 200 response with no JSON-RPC body.
    """
    request_id = str(uuid.uuid4())

    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        # Derive a deterministic session id from the presented auth token when available.
        token_source = None
        auth_header = request.headers.get("Authorization")
        if auth_header:
            parts = auth_header.split()
            token_source = parts[1] if len(parts) == 2 else auth_header
        if not token_source:
            token_source = request.headers.get("X-Access-Token")

        if token_source:
            digest = hashlib.sha256(token_source.encode("utf-8")).hexdigest()
            session_id = f"token-{digest[:16]}"
        else:
            session_id = str(uuid.uuid4())

    # Handle notification requests (no id field)
    is_notification = jsonrpc_request.id is None

    # Enhanced logging with session context (avoid logging raw params)
    logger.info(
        f"MCP JSON-RPC request: {jsonrpc_request.method}{' (notification)' if is_notification else ''}",
        extra={
            "request_id": request_id,
            "session_id": session_id,
            "jsonrpc_method": jsonrpc_request.method,
            "has_params": jsonrpc_request.params is not None,
            "is_notification": is_notification
        }
    )

    # Debug logging with redacted params (only in DEBUG mode)
    if settings.DEBUG and jsonrpc_request.params:
        from app.core.logging import redact_secrets
        redacted_params = redact_secrets(jsonrpc_request.params.copy())
        logger.debug(
            "MCP request params (redacted)",
            extra={
                "request_id": request_id,
                "session_id": session_id,
                "params": redacted_params
            }
        )

    docker_client = request.app.state.docker_client

    # Reuse MCP server from app state (initialized at startup)
    mcp_server: DynamicToolGatingMCP = request.app.state.mcp_server

    # Extract task_type from header for backward compatibility
    task_type_header = request.headers.get("X-Task-Type")

    try:
        if is_notification:
            # JSON-RPC notifications should not receive responses
            # Just log and return HTTP 200 with empty body
            logger.info(
                f"JSON-RPC notification received: {jsonrpc_request.method}",
                extra={
                    "request_id": request_id,
                    "session_id": session_id,
                    "method": jsonrpc_request.method
                }
            )
            # Return empty response for notifications
            from fastapi import Response
            return Response(content="", media_type="application/json")

        if jsonrpc_request.method == "initialize":
            result = await mcp_server.handle_initialize(
                jsonrpc_request.params,
                request_id,
                session_id
            )
            return _serialize_jsonrpc_response(
                JSONRPCResponse(id=jsonrpc_request.id, result=result)
            )

        elif jsonrpc_request.method == "tools/list":
            result = await mcp_server.handle_tools_list(
                jsonrpc_request.params,
                request_id,
                session_id,
                scopes,
                task_type_header
            )
            return _serialize_jsonrpc_response(
                JSONRPCResponse(id=jsonrpc_request.id, result=result)
            )

        elif jsonrpc_request.method == "tools/call":
            response = await mcp_server.handle_tools_call(
                jsonrpc_request.params,
                request_id,
                session_id,
                scopes,
                docker_client,
                jsonrpc_request.id
            )
            # handle_tools_call now returns JSONRPCResponse directly
            return _serialize_jsonrpc_response(response)

        elif jsonrpc_request.method == "prompts/list":
            result = await mcp_server.handle_prompts_list(
                jsonrpc_request.params,
                request_id,
                session_id
            )
            return _serialize_jsonrpc_response(
                JSONRPCResponse(id=jsonrpc_request.id, result=result)
            )

        elif jsonrpc_request.method == "prompts/get":
            response = await mcp_server.handle_prompts_get(
                jsonrpc_request.params,
                request_id,
                session_id,
                jsonrpc_request.id
            )
            # handle_prompts_get now returns JSONRPCResponse directly
            return _serialize_jsonrpc_response(response)

        else:
            logger.warning(
                f"Unknown JSON-RPC method: {jsonrpc_request.method}",
                extra={"request_id": request_id, "session_id": session_id}
            )
            return _serialize_jsonrpc_response(
                JSONRPCResponse(
                    id=jsonrpc_request.id,
                    error=JSONRPCError.create_error(
                        JSONRPCError.METHOD_NOT_FOUND,
                        f"Method '{jsonrpc_request.method}' not found"
                    )
                )
            )

    except Exception as e:
        logger.error(
            "Unexpected error in MCP handler",
            extra={"request_id": request_id, "session_id": session_id},
            exc_info=True
        )
        return _serialize_jsonrpc_response(
            JSONRPCResponse(
                id=jsonrpc_request.id,
                error=JSONRPCError.create_error(
                    JSONRPCError.INTERNAL_ERROR,
                    f"Internal server error: {str(e)}"
                )
            )
        )