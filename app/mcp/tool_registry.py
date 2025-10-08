import logging
import uuid
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, Depends, Query, Request

from app.core.auth import verify_token
from app.mcp.tool_gating import FilterContext, Tool

logger = logging.getLogger(__name__)

router = APIRouter()


class ToolRegistry:
    def __init__(self, tools_yaml_path: str = "tools.yaml"):
        self.tools_yaml_path = tools_yaml_path
        self.tools: dict[str, Tool] = {}
        self._load_tools()
    
    def _load_tools(self) -> None:
        tools_file = Path(self.tools_yaml_path)
        
        if not tools_file.exists():
            logger.warning(f"Tools file not found: {self.tools_yaml_path}")
            return
        
        with tools_file.open() as f:
            data = yaml.safe_load(f)
        
        tools_list = data.get("tools", [])
        
        for tool_data in tools_list:
            try:
                tool = Tool(**tool_data)
                self.tools[tool.name] = tool
            except Exception as e:
                logger.error(f"Failed to load tool {tool_data.get('name')}: {e}")
        
        logger.info(f"Loaded {len(self.tools)} tools from {self.tools_yaml_path}")
    
    def get_all_tools(self) -> dict[str, Tool]:
        return self.tools.copy()
    
    def get_tool(self, name: str) -> Tool | None:
        return self.tools.get(name)


@router.get("/tools", dependencies=[Depends(verify_token)])
async def get_available_tools(
    request: Request,
    task_type: str | None = Query(None, description="Task category to filter tools")
) -> dict[str, Any]:
    request_id = str(uuid.uuid4())
    
    tool_gate_controller = request.app.state.tool_gate_controller
    
    context = FilterContext(
        task_type=task_type,
        request_id=request_id
    )
    
    filtered_tools = tool_gate_controller.get_available_tools(context)
    
    context_size = tool_gate_controller.get_context_size(filtered_tools)
    
    filters_applied = []
    if task_type:
        filters_applied.append("TaskTypeFilter")
    if len(tool_gate_controller.all_tools) > tool_gate_controller.config.max_tools:
        filters_applied.append("ResourceFilter")
    if tool_gate_controller.config.blocklist:
        filters_applied.append("SecurityFilter")
    
    response: dict[str, Any] = {
        "tools": [tool.model_dump() for tool in filtered_tools.values()],
        "filters_applied": filters_applied
    }
    
    from app.core.config import settings
    if settings.DEBUG:
        response["context_size"] = context_size
    
    logger.info(
        f"Tool discovery: {len(filtered_tools)} tools returned",
        extra={
            "request_id": request_id,
            "task_type": task_type,
            "tool_count": len(filtered_tools),
            "context_size": context_size
        }
    )
    
    return response
