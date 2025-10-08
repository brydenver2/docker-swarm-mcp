import json
import logging
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)


class Tool(BaseModel):
    name: str
    description: str
    method: str
    path: str
    request_schema: dict[str, Any] | None = None
    response_schema: dict[str, Any]
    task_types: list[str]
    priority: int = 0


class FilterContext(BaseModel):
    task_type: str | None = None
    client_id: str | None = None
    session_id: str | None = None
    request_id: str


class ToolFilter(ABC):
    @abstractmethod
    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        pass


class TaskTypeFilter(ToolFilter):
    def __init__(self, task_type_allowlists: dict[str, list[str]]):
        self.task_type_allowlists = task_type_allowlists
    
    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        if not context.task_type:
            return tools
        
        allowlist = self.task_type_allowlists.get(context.task_type, [])
        if not allowlist:
            logger.warning(f"Unknown task_type: {context.task_type}", extra={"request_id": context.request_id})
            return tools
        
        filtered = {
            name: tool
            for name, tool in tools.items()
            if context.task_type in tool.task_types
        }
        
        logger.debug(
            f"TaskTypeFilter: {len(tools)} → {len(filtered)} tools",
            extra={"request_id": context.request_id, "task_type": context.task_type}
        )
        
        return filtered


class ResourceFilter(ToolFilter):
    def __init__(self, max_tools: int):
        self.max_tools = max_tools
    
    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        if len(tools) <= self.max_tools:
            return tools
        
        sorted_tools = sorted(tools.items(), key=lambda x: (-x[1].priority, x[0]))
        filtered = dict(sorted_tools[:self.max_tools])
        
        logger.debug(
            f"ResourceFilter: {len(tools)} → {len(filtered)} tools",
            extra={"request_id": context.request_id, "max_tools": self.max_tools}
        )
        
        return filtered


class SecurityFilter(ToolFilter):
    def __init__(self, blocklist: list[str]):
        self.blocklist = set(blocklist)
    
    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        filtered = {
            name: tool
            for name, tool in tools.items()
            if name not in self.blocklist
        }
        
        if len(filtered) < len(tools):
            blocked = set(tools.keys()) - set(filtered.keys())
            logger.debug(
                f"SecurityFilter: blocked {blocked}",
                extra={"request_id": context.request_id}
            )
        
        return filtered


class FilterConfig(BaseModel):
    task_type_allowlists: dict[str, list[str]]
    max_tools: int
    blocklist: list[str]


class ToolGateController:
    def __init__(self, all_tools: dict[str, Tool], config: FilterConfig):
        self.all_tools = all_tools
        self.config = config
        self.filters: list[ToolFilter] = [
            TaskTypeFilter(config.task_type_allowlists),
            ResourceFilter(config.max_tools),
            SecurityFilter(config.blocklist)
        ]
    
    def get_available_tools(self, context: FilterContext) -> dict[str, Tool]:
        tools = self.all_tools.copy()
        
        for filter_instance in self.filters:
            tools = filter_instance.apply(tools, context)
        
        return tools
    
    def list_active_tools(self) -> list[str]:
        return list(self.all_tools.keys())
    
    def get_context_size(self, tools: dict[str, Tool]) -> int:
        serialized = json.dumps([tool.model_dump() for tool in tools.values()])
        
        if settings.DEBUG:
            try:
                import tiktoken
                enc = tiktoken.get_encoding("cl100k_base")
                token_count = len(enc.encode(serialized))
            except ImportError:
                logger.warning("tiktoken not available, using char-based estimation")
                token_count = len(serialized) // 4
        else:
            token_count = len(serialized) // 4
        
        if token_count > 7600:
            raise ValueError(
                f"Context size {token_count} tokens exceeds hard limit of 7600 tokens. "
                f"Reduce tool count or enable task-type filtering."
            )
        
        if token_count > 5000:
            logger.warning(
                f"Context size {token_count} tokens exceeds recommended threshold of 5000 tokens",
                extra={"token_count": token_count, "tool_count": len(tools)}
            )
        
        return token_count
