"""Meta operations service for providing instructional content to LLMs."""

import json
from typing import Any

from app.core.config import settings


async def discover_tools(docker_client: Any, params: dict[str, Any], config: Any = None) -> dict[str, Any]:
    """Return guidance on tool discovery and task type filtering."""
    # Use provided config or get from ToolGateController
    if config is None:
        # This should not happen in normal operation, but provide fallback
        raise ValueError("Config must be provided to meta_service functions")
    
    task_type_allowlists = config.task_type_allowlists
    max_tools = config.max_tools
    
    # Build task types info with example tools (first 3-5)
    task_types_info = []
    for task_type, tools in task_type_allowlists.items():
        example_tools = tools[:3] if len(tools) > 3 else tools
        task_types_info.append({
            "name": task_type,
            "tool_count": len(tools),
            "example_tools": example_tools
        })
    
    # Sort by name for consistent ordering
    task_types_info.sort(key=lambda x: x["name"])
    
    guidance = (
        f"This Docker MCP server provides {sum(len(tools) for tools in task_type_allowlists.values())} tools organized into "
        f"{len(task_type_allowlists)} task type categories. By default, tools/list returns up to {max_tools} tools. "
        f"Use the task_type parameter to filter tools by category: "
        f"{{\"task_type\": \"container-ops\"}} for container operations, "
        f"{{\"task_type\": \"meta-ops\"}} for discovery and guidance tools."
    )
    
    example_request = json.dumps({"task_type": "container-ops"})
    
    return {
        "guidance": guidance,
        "task_types": task_types_info,
        "example_request": example_request
    }


async def list_task_types(docker_client: Any, params: dict[str, Any], config: Any = None) -> dict[str, Any]:
    """Return complete mapping of task types to tools."""
    # Use provided config or get from ToolGateController
    if config is None:
        # This should not happen in normal operation, but provide fallback
        raise ValueError("Config must be provided to meta_service functions")
    
    task_type_allowlists = config.task_type_allowlists
    max_tools = config.max_tools
    
    # Count total unique tools
    all_tools = set()
    for tools in task_type_allowlists.values():
        all_tools.update(tools)
    
    usage_hint = (
        f"Use task_type parameter in tools/list to filter: "
        f"{{\"task_type\": \"container-ops\"}} returns container tools only. "
        f"Available task types: {', '.join(sorted(task_type_allowlists.keys()))}."
    )
    
    return {
        "task_types": task_type_allowlists,
        "total_tools": len(all_tools),
        "max_tools_per_request": max_tools,
        "usage_hint": usage_hint
    }


async def intent_query_help(docker_client: Any, params: dict[str, Any]) -> dict[str, Any]:
    """Return guidance on natural language query usage."""
    enabled = settings.INTENT_CLASSIFICATION_ENABLED
    
    guidance = (
        "Use natural language queries with the 'query' parameter in tools/list for automatic tool discovery. "
        "The system analyzes your query to detect the intended task type and returns relevant tools. "
        f"Intent classification is currently {'enabled' if enabled else 'disabled'}."
    )
    
    examples = [
        {
            "query": "Show me running containers",
            "detected_task_type": "container-ops",
            "description": "Returns container management tools"
        },
        {
            "query": "Deploy a compose stack",
            "detected_task_type": "compose-ops", 
            "description": "Returns Docker Compose tools"
        },
        {
            "query": "Create a network",
            "detected_task_type": "network-ops",
            "description": "Returns network management tools"
        },
        {
            "query": "Check Docker system info",
            "detected_task_type": "system-ops",
            "description": "Returns system information tools"
        },
        {
            "query": "How do I discover tools?",
            "detected_task_type": "meta-ops",
            "description": "Returns meta-tools for guidance and discovery"
        }
    ]
    
    example_request = json.dumps({"query": "Show me running containers"})
    
    result = {
        "guidance": guidance,
        "examples": examples,
        "enabled": enabled,
        "example_request": example_request
    }
    
    if not enabled:
        result["note"] = "Intent classification is currently disabled. Use explicit task_type parameter instead."
    
    return result