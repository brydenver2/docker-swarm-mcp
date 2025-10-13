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
    required_scopes: list[str] | None = None  # Explicit required scopes per tool


class FilterContext(BaseModel):
    task_type: str | None = None
    client_id: str | None = None
    session_id: str | None = None
    request_id: str
    # Intent-based filtering fields
    query: str | None = None
    detected_task_types: list[str] | None = None
    intent_confidence: dict[str, float] | None = None


class ToolFilter(ABC):
    @abstractmethod
    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        pass


class TaskTypeFilter(ToolFilter):
    def __init__(self, task_type_allowlists: dict[str, list[str]]):
        self.task_type_allowlists = task_type_allowlists

    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        # Check for strict no-match behavior before processing
        if (context.query is not None and
            context.detected_task_types == [] and
            (settings.STRICT_CONTEXT_LIMIT or not settings.INTENT_FALLBACK_TO_ALL)):
            logger.warning(
                "Strict no-match mode: returning empty tool set",
                extra={
                    "request_id": context.request_id,
                    "query": context.query[:100] + "..." if len(context.query) > 100 else context.query,
                    "strict_mode": True,
                    "fallback_disabled": not settings.INTENT_FALLBACK_TO_ALL
                }
            )
            return {}

        # Determine which task types to use based on INTENT_PRECEDENCE setting
        task_types_to_use = []
        classification_source = "none"

        if settings.INTENT_PRECEDENCE == "intent":
            # Intent takes precedence (default behavior)
            if context.detected_task_types:
                task_types_to_use = context.detected_task_types
                classification_source = "intent"
            elif context.task_type:
                task_types_to_use = [context.task_type]
                classification_source = "explicit"
        else:
            # Explicit takes precedence (legacy behavior)
            if context.task_type:
                task_types_to_use = [context.task_type]
                classification_source = "explicit"
            elif context.detected_task_types:
                task_types_to_use = context.detected_task_types
                classification_source = "intent"

        if not task_types_to_use:
            # When no task type is specified, exclude meta-ops tools by default
            # to keep the default tool list focused on Docker operations
            filtered_tools = {
                name: tool
                for name, tool in tools.items()
                if "meta-ops" not in tool.task_types
            }
            logger.debug(
                f"TaskTypeFilter: Excluding meta-ops tools from default list - {len(tools)} → {len(filtered_tools)} tools",
                extra={"request_id": context.request_id, "excluded_category": "meta-ops"}
            )
            return filtered_tools

        # Merge allowlists for all detected task types
        merged_allowlist = self._merge_allowlists(task_types_to_use)

        if not merged_allowlist:
            # Check fallback behavior based on settings
            if settings.STRICT_CONTEXT_LIMIT or not settings.INTENT_FALLBACK_TO_ALL:
                logger.warning(
                    f"Unknown task_types '{task_types_to_use}' - returning empty set (strict/fallback disabled)",
                    extra={"request_id": context.request_id, "classification_source": classification_source}
                )
                return {}
            else:
                logger.warning(
                    f"Unknown task_types '{task_types_to_use}' - returning all tools (fallback enabled)",
                    extra={"request_id": context.request_id, "classification_source": classification_source}
                )
                return tools

        # Filter by merged allowlist first (if exists), then by task_types
        filtered = {
            name: tool
            for name, tool in tools.items()
            if (name in merged_allowlist) and any(task_type in tool.task_types for task_type in task_types_to_use)
        }

        logger.debug(
            f"TaskTypeFilter: {len(tools)} → {len(filtered)} tools",
            extra={
                "request_id": context.request_id,
                "task_types": task_types_to_use,
                "allowlist": merged_allowlist,
                "classification_source": classification_source
            }
        )

        return filtered

    def _merge_allowlists(self, task_types: list[str]) -> list[str]:
        """
        Merge allowlists for multiple task types.

        Args:
            task_types: List of task types to merge

        Returns:
            Combined allowlist with unique tool names
        """
        merged = set()
        for task_type in task_types:
            allowlist = self.task_type_allowlists.get(task_type, [])
            merged.update(allowlist)
        return list(merged)


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

        # Precompute tool sizes for caching
        self._tool_sizes: dict[str, int] = {}
        self._total_all_tools_size = 0
        self._estimator_type = "unknown"

        self._precompute_tool_sizes()

    def get_available_tools(self, context: FilterContext) -> tuple[dict[str, Tool], list[str]]:
        tools = self.all_tools.copy()
        filters_applied = []

        for filter_instance in self.filters:
            tools_before = tools.copy()
            tools = filter_instance.apply(tools, context)

            # Check if this filter actually changed the tool set
            if tools != tools_before:
                filter_name = filter_instance.__class__.__name__
                filters_applied.append(filter_name)

        return tools, filters_applied

    def list_active_tools(self) -> list[str]:
        return list(self.all_tools.keys())

    def get_context_size(self, tools: dict[str, Tool], enforce_hard_limit: bool | None = None) -> int:
        # Use STRICT_CONTEXT_LIMIT config if enforce_hard_limit not explicitly provided
        if enforce_hard_limit is None:
            enforce_hard_limit = settings.STRICT_CONTEXT_LIMIT

        # Use cached sizes if available
        if self._tool_sizes and self._estimator_type != "fallback":
            token_count = sum(self._tool_sizes.get(name, 0) for name in tools.keys())
        else:
            # Fallback to original method
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
            error_msg = (
                f"Context size {token_count} tokens exceeds hard limit of 7600 tokens. "
                f"Reduce tool count or enable task-type filtering."
            )
            logger.error(
                error_msg,
                extra={
                    "token_count": token_count,
                    "tool_count": len(tools),
                    "estimator": self._estimator_type
                }
            )

            # Graceful degradation: truncate to max_tools instead of raising
            if not enforce_hard_limit:
                logger.warning(
                    "Graceful degradation: truncating tool list to fit context window",
                    extra={"estimator": self._estimator_type}
                )
                # Already handled by ResourceFilter, just log
            else:
                raise ValueError(error_msg)

        if token_count > 5000:
            logger.warning(
                f"Context size {token_count} tokens exceeds recommended threshold of 5000 tokens",
                extra={
                    "token_count": token_count,
                    "tool_count": len(tools),
                    "estimator": self._estimator_type
                }
            )

        return token_count

    def _precompute_tool_sizes(self) -> None:
        """Precompute serialized sizes for all tools to avoid repeated serialization"""
        try:
            if settings.DEBUG:
                try:
                    import tiktoken
                    enc = tiktoken.get_encoding("cl100k_base")
                    self._estimator_type = "tiktoken"

                    for name, tool in self.all_tools.items():
                        serialized = json.dumps(tool.model_dump())
                        self._tool_sizes[name] = len(enc.encode(serialized))

                except ImportError:
                    self._estimator_type = "approx"
                    logger.warning("tiktoken not available, using char-based estimation")

                    for name, tool in self.all_tools.items():
                        serialized = json.dumps(tool.model_dump())
                        self._tool_sizes[name] = len(serialized) // 4
            else:
                self._estimator_type = "approx"

                for name, tool in self.all_tools.items():
                    serialized = json.dumps(tool.model_dump())
                    self._tool_sizes[name] = len(serialized) // 4

            self._total_all_tools_size = sum(self._tool_sizes.values())

            logger.info(
                f"Precomputed sizes for {len(self._tool_sizes)} tools using {self._estimator_type} estimator",
                extra={
                    "estimator": self._estimator_type,
                    "tool_count": len(self._tool_sizes),
                    "total_tokens": self._total_all_tools_size
                }
            )

        except Exception as e:
            logger.error(f"Failed to precompute tool sizes: {e}")
            self._estimator_type = "fallback"
            self._tool_sizes = {}
            self._total_all_tools_size = 0
