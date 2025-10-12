Overview
The gating layer preserves Model Context Protocol (MCP) context by narrowing the set of exposed tools before each request. A central ToolGateController loads toolsets, tracks active tools, and passes them through a configurable chain of filters whenever getAvailableTools is invoked, ensuring only relevant capabilities remain in context.

Shared Filtering Interface
All filters implement a common ToolFilter interface with an apply(tools, context) contract. The shared FilterContext type carries request metadata (e.g., taskType) that filters can use when deciding which tools to keep, allowing you to add new filters without changing controller logic.

## Intent-Based Classification

The gating system now supports automatic task-type detection from natural language queries, eliminating the need for clients to explicitly specify task types.

### How It Works

1. **Client sends query**: The LLM/client includes a `query` parameter in the `tools/list` request describing what it wants to do
2. **Server analyzes intent**: The `IntentClassifier` analyzes the query using keyword matching to detect relevant task types
3. **Tools filtered automatically**: Only tools matching the detected task types are returned (typically 2-6 tools instead of all 23)
4. **Context optimized**: Dramatically reduces context size without requiring client configuration

### Example Flow

```json
// Client request
{
  "method": "tools/list",
  "params": {
    "query": "I need to check the logs of my running containers"
  }
}

// Server response (only container-ops tools)
{
  "tools": [
    {"name": "list-containers", ...},
    {"name": "get-logs", ...},
    ...
  ],
  "_metadata": {
    "detected_task_types": ["container-ops"],
    "classification_method": "intent",
    "context_size": 1200
  }
}
```

### Keyword Mappings

The classifier uses configurable keyword mappings defined in `filter-config.json`. Each task type has a list of keywords and phrases that trigger its selection. Keywords are matched case-insensitively and support multi-word phrases.

### Backward Compatibility

Explicit `task_type` parameters are still supported but intent classification (`query`) takes precedence when both are provided. This ensures existing clients continue to work while enabling natural language queries.

Filter Implementations
TaskTypeFilter maps task categories to explicit tool allowlists; when a task type is provided, only tools on the corresponding list remain, preserving focus on task-relevant context.

ResourceFilter enforces a configurable maximum tool count, truncating the tool map to keep the context within size or latency budgets.

SecurityFilter removes tools on a blocklist so sensitive or disallowed capabilities never enter the session context.

Because each filter returns a reduced tool dictionary, chaining them sequentially lets you combine policy, safety, and resource constraints while still working with standard MCP tool objects.

Controller Integration and Context Tracking
ToolGateController dynamically loads toolsets, keeps track of which tools belong to each set, and exposes helper methods like listActiveTools and getContextSize. The latter serializes currently loaded tools to measure their footprint, giving you a metric for context preservation strategies.

Configuration Strategy
Filters are toggled and tuned through filter-config.json, letting you enable specific filters, define task-to-tool mappings, set tool count limits, or update security blocklists without code changes. This configuration-driven approach makes it easy to adapt gating behavior per deployment or environment.

The `intent_keywords` section in `filter-config.json` allows customization of keyword mappings for intent classification, enabling deployment-specific tuning without code changes.

Validation
Unit tests cover individual filters and the combined chain, demonstrating how different request contexts yield tailored tool sets. These scenarios can serve as patterns for your MCP project to ensure gating rules are applied as expected.

Intent classification tests verify keyword matching accuracy, multi-task-type detection, and integration with the MCP protocol handlers.