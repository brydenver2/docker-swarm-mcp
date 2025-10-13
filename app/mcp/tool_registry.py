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
        """
        Initialize the ToolRegistry and load tool configurations from the specified YAML file.
        
        Parameters:
            tools_yaml_path (str): Path to the YAML file containing tool definitions. Defaults to "tools.yaml".
        
        Raises:
            FileNotFoundError: If the YAML file does not exist at the provided path.
            ValueError: If the YAML file cannot be parsed, does not contain a valid tools list, or no valid tools are loaded after validation.
        """
        self.tools_yaml_path = tools_yaml_path
        self.tools: dict[str, Tool] = {}
        self._load_tools()

    def _load_tools(self) -> None:
        """
        Load and validate tool definitions from the configured YAML file and populate self.tools.
        
        Reads the YAML at self.tools_yaml_path, validates its structure (top-level dict with a 'tools' list), constructs Tool instances for each entry, and stores them keyed by tool.name in self.tools. If any tool entries fail to construct, or if the file is missing, contains invalid YAML, has an unexpected structure, or results in no valid tools, an exception is raised.
        
        Raises:
            FileNotFoundError: If the configured tools YAML file does not exist.
            ValueError: If the YAML is invalid, the top-level structure is not a dict, the 'tools' key is not a list, one or more tools fail to load, or no valid tools are found.
        """
        tools_file = Path(self.tools_yaml_path)

        if not tools_file.exists():
            logger.error(f"Tools file not found: {self.tools_yaml_path}")
            raise FileNotFoundError(f"Required file not found: {self.tools_yaml_path}")

        try:
            with tools_file.open() as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {self.tools_yaml_path}: {e}")
            raise ValueError(f"Invalid YAML in {self.tools_yaml_path}: {e}")

        if not isinstance(data, dict):
            logger.error(f"tools.yaml must contain a dict, got {type(data)}")
            raise ValueError("tools.yaml must contain a dict with 'tools' key")

        tools_list = data.get("tools", [])

        if not isinstance(tools_list, list):
            logger.error(f"'tools' key must be a list, got {type(tools_list)}")
            raise ValueError("'tools' key in tools.yaml must be a list")

        failed_tools = []
        for tool_data in tools_list:
            try:
                tool = Tool(**tool_data)
                self.tools[tool.name] = tool
            except Exception as e:
                failed_tools.append((tool_data.get('name', 'unknown'), str(e)))
                logger.error(f"Failed to load tool {tool_data.get('name')}: {e}")

        if failed_tools:
            error_msg = f"Failed to load {len(failed_tools)} tools: {failed_tools}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not self.tools:
            logger.error("No valid tools loaded from tools.yaml")
            raise ValueError("No valid tools found in tools.yaml")

        logger.info(f"Successfully validated and loaded {len(self.tools)} tools from {self.tools_yaml_path}")

    def get_all_tools(self) -> dict[str, Tool]:
        """
        Provide a mapping of loaded tools keyed by tool name.
        
        Returns:
            dict[str, Tool]: A shallow copy of the internal mapping from tool name to `Tool` instances.
        """
        return self.tools.copy()

    def get_tool(self, name: str) -> Tool | None:
        """
        Retrieve a loaded Tool by its name.
        
        Returns:
            The Tool with the given name, or None if no matching tool is loaded.
        """
        return self.tools.get(name)


@router.get("/tools", dependencies=[Depends(verify_token)])
async def get_available_tools(
    request: Request,
    task_type: str | None = Query(None, description="Task category to filter tools")
) -> dict[str, Any]:
    """
    Retrieve available tools filtered by the provided task type and request context.
    
    Parameters:
        task_type (str | None): Optional task category used to filter tools.
    
    Returns:
        dict[str, Any]: A dictionary with two keys:
            - "tools": a list of serialized tool objects (each produced by `Tool.model_dump()`).
            - "_metadata": an object containing "filters_applied" (details of filters used) and "context_size" (calculated context size).
    """
    request_id = str(uuid.uuid4())

    tool_gate_controller = request.app.state.tool_gate_controller

    context = FilterContext(
        task_type=task_type,
        request_id=request_id
    )

    filtered_tools, filters_applied = tool_gate_controller.get_available_tools(context)

    context_size = tool_gate_controller.get_context_size(filtered_tools)

    response: dict[str, Any] = {
        "tools": [tool.model_dump() for tool in filtered_tools.values()],
        "_metadata": {
            "filters_applied": filters_applied,
            "context_size": context_size,
        },
    }

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