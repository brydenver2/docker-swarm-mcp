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
        """
        Filter the provided tools according to the request context's task type signals and configured allowlists.
        
        Determines which task types to honor based on the INTENT_PRECEDENCE setting (preferring either detected intent or explicit task_type), merges per-task-type allowlists, and returns only tools that are both in the merged allowlist and declare one of the selected task types. If no task types are available, tools categorized as "meta-ops" are excluded from the default set. Behavior when allowlists are empty is controlled by strict and fallback settings: the method will either return an empty set or fall back to returning all tools.
        
        Parameters:
            tools (dict[str, Tool]): Mapping of tool name to Tool instances to be filtered.
            context (FilterContext): Context containing request metadata and task type signals (e.g., `task_type`, `detected_task_types`, `query`, `request_id`).
        
        Returns:
            dict[str, Tool]: Subset of the input `tools` that pass the task-type and allowlist filters (possibly empty).
        """
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
        Merge tool allowlists for the given task types into a unique list.
        
        Parameters:
            task_types (list[str]): Task types whose configured allowlists will be combined.
        
        Returns:
            merged_allowlist (list[str]): Unique tool names present in any of the specified allowlists.
        """
        merged = set()
        for task_type in task_types:
            allowlist = self.task_type_allowlists.get(task_type, [])
            merged.update(allowlist)
        return list(merged)


class ResourceFilter(ToolFilter):
    def __init__(self, max_tools: int):
        """
        Initialize the resource filter with a maximum allowed number of tools.
        
        Parameters:
            max_tools (int): Maximum number of tools to retain when filtering; if the current tool count
                is less than or equal to this value, no reduction will be performed.
        """
        self.max_tools = max_tools

    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        """
        Limit the provided tools to the top-ranked entries according to priority and name until reaching the configured maximum.
        
        Returns:
            dict[str, Tool]: A dictionary containing up to `max_tools` tools, selected by descending `priority` and then by ascending tool name as a tiebreaker.
        """
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
        """
        Initialize the SecurityFilter with a set of blocked tool names.
        
        Parameters:
            blocklist (list[str]): Iterable of tool names to block; duplicates will be removed and names are stored as a set for membership checks.
        """
        self.blocklist = set(blocklist)

    def apply(self, tools: dict[str, Tool], context: FilterContext) -> dict[str, Tool]:
        """
        Exclude tools whose names are present in this filter's blocklist.
        
        Parameters:
        	tools (dict[str, Tool]): Mapping of tool names to Tool objects to be filtered.
        	context (FilterContext): Request-specific context (used for logging request_id).
        
        Returns:
        	filtered (dict[str, Tool]): Mapping of tool names to Tool objects after removing blocked tools.
        
        Notes:
        	If any tools are removed, their names are logged along with the request_id from the context.
        """
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
        """
        Initialize the ToolGateController with a set of tools and filter configuration, build the filter pipeline, and precompute per-tool size estimates for context budgeting.
        
        Parameters:
            all_tools (dict[str, Tool]): Mapping of tool name to Tool model representing the available tools.
            config (FilterConfig): Filtering configuration controlling task-type allowlists, resource limits, and security blocklist.
        
        Notes:
            This constructor populates `self.filters` in the fixed pipeline order (task-type, resource, security), initializes internal size-caching fields (`_tool_sizes`, `_total_all_tools_size`, `_estimator_type`), and calls `_precompute_tool_sizes()` to compute serialized size estimates used by context-size calculations.
        """
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
        """
        Selects the subset of configured tools that remain after applying the filter pipeline for the given context.
        
        Applies each configured filter in order to the full tool set and records which filters actually changed the available tools.
        
        Parameters:
            context (FilterContext): Contextual information used by filters to decide which tools to keep.
        
        Returns:
            tuple[dict[str, Tool], list[str]]: A tuple where the first element is a mapping of tool names to Tool instances remaining after filtering, and the second element is an ordered list of filter class names that modified the tool set.
        """
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
        """
        List all tool names registered with the controller.
        
        Returns:
            list[str]: The names of all tools known to the controller.
        """
        return list(self.all_tools.keys())

    def get_context_size(self, tools: dict[str, Tool], enforce_hard_limit: bool | None = None) -> int:
        # Use STRICT_CONTEXT_LIMIT config if enforce_hard_limit not explicitly provided
        """
        Determine the estimated token size of the provided tool set and validate it against configured context limits.
        
        Parameters:
            tools (dict[str, Tool]): Mapping of tool names to Tool instances to be measured.
            enforce_hard_limit (bool | None): If True, raise an error when the hard token limit is exceeded;
                if False, allow graceful degradation; if None, use the global STRICT_CONTEXT_LIMIT setting.
        
        Returns:
            int: Estimated number of tokens required to include the given tools in context.
        
        Raises:
            ValueError: If the estimated token count exceeds the hard limit (7600 tokens) and `enforce_hard_limit` is True.
        """
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
        """
        Precompute and cache token-size estimates for every tool to avoid repeated serialization.
        
        This populates the instance attributes `_tool_sizes` (mapping of tool name to estimated token count),
        `_total_all_tools_size` (sum of all per-tool estimates), and `_estimator_type` (one of `"tiktoken"`, `"approx"`, or `"fallback"`).
        When DEBUG is enabled and the `tiktoken` package is available, sizes are measured using the `cl100k_base` encoding; otherwise sizes are approximated by character length divided by four.
        On any unexpected error the method sets `_estimator_type` to `"fallback"`, clears `_tool_sizes`, and sets `_total_all_tools_size` to 0.
        """
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