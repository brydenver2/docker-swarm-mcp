# MCP JSON-RPC Usage Guide

This guide covers the MCP JSON-RPC 2.0 endpoint for programmatic tool access with integrated gating and schema validation.

> **✅ JSON-RPC 2.0 Compliant**: As of the latest version, this server strictly adheres to the JSON-RPC 2.0 specification. Responses include either `result` OR `error`, never both fields simultaneously.

## Overview

The MCP JSON-RPC endpoint provides a standards-compliant interface for:
- Tool discovery with dynamic gating
- Tool execution with schema validation
- Session tracking and observability
- Scope-based authorization

**Endpoint**: `POST /mcp/` (note the trailing slash)

## JSON-RPC Protocol

All requests and responses follow the **JSON-RPC 2.0 specification** ([spec](https://www.jsonrpc.org/specification)):

```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": {},
  "id": 1
}
```

**Important**: 
- ✅ The server strictly follows JSON-RPC 2.0: responses contain either `result` OR `error`, never both
- ✅ The trailing slash in `/mcp/` is required for proper routing
- ⚠️ Notifications (requests without `id` field) are supported but return HTTP 200 with empty body per specification
- ⚠️ Batch requests are not currently supported

### Response Format

**Success Response** (only includes `result`, no `error` field):
```json
{
  "jsonrpc": "2.0",
  "result": {
    "data": "Success data here"
  },
  "id": 1
}
```

**Error Response** (only includes `error`, no `result` field):
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Error description",
    "data": {}
  },
  "id": 1
}
```

> **JSON-RPC 2.0 Compliance**: Per the specification, a response MUST contain either a `result` member OR an `error` member, but NOT both. This server correctly implements this requirement.

## Available Methods

### 1. initialize

Handshake to establish MCP protocol version and capabilities.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    }
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "serverInfo": {
      "name": "docker-swarm-mcp",
      "version": "0.5.0"
    },
    "capabilities": {
      "tools": {
        "gating": true,
        "context_size_enforcement": true,
        "task_type_filtering": true
      },
      "prompts": {
        "listChanged": false
      }
    }
  },
  "id": 1
}
```

### 2. tools/list

Discover available tools with optional task-type filtering.

**Request (all tools):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

**Request (with explicit filtering):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {
    "task_type": "container-ops"
  },
  "id": 2
}
```

**Request (with intent-based filtering):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {
    "query": "Show me all running containers and their logs"
  },
  "id": 2
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "list-containers",
        "description": "List Docker containers",
        "inputSchema": {
          "type": "object",
          "properties": {
            "all": {"type": "boolean"}
          }
        }
      }
    ],
    "_metadata": {
      "context_size": 1200,
      "filters_applied": ["TaskTypeFilter", "SecurityFilter"],
      "query": "Show me all running containers and their logs",
      "detected_task_types": ["container-ops"],
      "classification_method": "intent"
    }
  },
  "id": 2
}
```

**Response Structure Notes:**

- **Standard fields**: `tools` array contains standard MCP tool definitions
- **`_metadata` extension**: Non-standard extension providing observability data
- **Meta-tools discovery**: Use `task_type: "meta-ops"` to see instructional meta-tools like discover-tools
  - `context_size`: Estimated token count for returned tools (helps clients manage context budgets)
  - `filters_applied`: List of filter names that processed the request (TaskTypeFilter, ResourceFilter, SecurityFilter)
  - This field may be omitted in minimal/compliant-only responses
  - Clients should treat `_metadata` as optional and informational only

### 3. tools/call

Execute a tool with parameter validation.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list-containers",
    "arguments": {
      "all": true
    }
  },
  "id": 3
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\":\"abc123\",\"name\":\"web\",\"status\":\"running\"}]"
      }
    ]
  },
  "id": 3
}
```

### 4. prompts/list

Discover available prompt templates that provide guidance on using the server.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "params": {},
  "id": 4
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "prompts": [
      {
        "name": "discover-tools",
        "description": "Learn how to discover tools by task type"
      },
      {
        "name": "list-task-types",
        "description": "View all available task types and their tools"
      },
      {
        "name": "intent-query-help",
        "description": "Learn how to use natural language queries for tool discovery"
      }
    ]
  },
  "id": 4
}
```

### 5. prompts/get

Retrieve a specific prompt template with instructions.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/get",
  "params": {
    "name": "discover-tools"
  },
  "id": 5
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "description": "Guide to discovering Docker tools by task type",
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "This server has 23 Docker tools organized into 7 task types. By default, only 10 tools are shown..."
        }
      }
    ]
  },
  "id": 5
}
```

## Authentication

All requests require tokens to be sent via HTTP headers. Two header formats are supported:

- **Standard (recommended):** `Authorization: Bearer <token>`
- **Simple alternative:** `X-Access-Token: <token>` (for clients that cannot set Bearer headers)

If both headers are present, the Authorization header takes precedence. Query parameter authentication is **not** supported for security reasons (tokens in URLs are logged by servers, proxies, and browsers).

```bash
# Authorization header (recommended)
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'

# X-Access-Token header (simple alternative)
curl -X POST http://localhost:8000/mcp/ \
  -H "X-Access-Token: your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'
```

### Security Considerations

- Tokens are accepted **only** via headers to prevent accidental leakage through URLs, browser history, and referrer headers.
- Web server and reverse-proxy access logs typically include URLs but not headers, making header-based authentication significantly safer.
- Application logging filters redact both `Authorization` and `X-Access-Token` headers to keep credentials out of structured logs.
- See [SECURITY.md](../SECURITY.md) for a deeper dive into authentication hardening and token management best practices.

### Scope-Based Authorization

Configure scopes via `TOKEN_SCOPES` environment variable:

```bash
export TOKEN_SCOPES='{"user-token": ["container-ops", "system-ops"]}'
```

- `admin` scope: Full access to all tools
- Task-type scopes: Access only to specific tool categories

**Scope Semantics:**

Each tool can define explicit `required_scopes` in `tools.yaml`. When `required_scopes` is not defined, the authorization system falls back to the tool's `task_types` field. For example:

```yaml
tools:
  - name: list-containers
    required_scopes: ["container-ops", "read-only"]  # Explicit scopes
    task_types: ["container-ops"]

  - name: remove-container
    # No required_scopes defined - falls back to task_types
    task_types: ["container-ops"]  # Used for authorization
```

**Best Practice:** Define explicit `required_scopes` for all tools, especially destructive operations. Use conservative defaults:
- Non-mutating tools (list, get, info): `["read-only"]` or specific scopes
- Destructive tools (remove, scale, delete): `["admin"]` or specific elevated scopes

## Session Tracking

Include `X-Session-ID` header for session correlation:

```bash
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token" \
  -H "X-Session-ID: session-abc123" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}'
```

Session IDs appear in server logs for tracing and debugging.

## Intent-Based Tool Discovery (Recommended)

Instead of manually specifying task types, you can send a natural language query describing what you want to do. The server automatically detects relevant task types and returns only the necessary tools.

**Benefits**:
- **Automatic filtering**: No need to know task-type taxonomy
- **Reduced context**: Typically returns 2-6 tools instead of all 23
- **Natural interface**: LLMs can describe intent in plain language
- **Single server config**: No need for multiple MCP server configurations

**Example Queries**:
- "List all running containers" → Returns container-ops tools
- "Deploy a docker-compose stack" → Returns compose-ops tools
- "Scale my web service" → Returns service-ops tools
- "Create a new network" → Returns network-ops tools
- "Check Docker status" → Returns system-ops tools

**Fallback Behavior**:
- If no task types detected, returns all tools (configurable via `INTENT_FALLBACK_TO_ALL`)
- Explicit `task_type` parameter still supported for backward compatibility
- `query` takes precedence over `task_type` if both provided

**Python Client Example**:
```python
def list_tools(self, query: str = None, task_type: str = None):
    params = {}
    if query:
        params["query"] = query
    elif task_type:
        params["task_type"] = task_type
    return self._request("tools/list", params)

# Usage
tools = client.list_tools(query="I need to manage containers")
```

**JavaScript Client Example**:
```javascript
async function listTools(query = null, taskType = null) {
    const params = {};
    if (query) params.query = query;
    else if (taskType) params.task_type = taskType;
    
    return await request("tools/list", params);
}

// Usage
const tools = await listTools("I need to manage containers");
```

## Meta-Tools for Discovery

The server provides special meta-tools that return instructional content through the standard tools interface. This approach works with all MCP clients, unlike prompts which require client-side support.

**Available Meta-Tools:**

1. **discover-tools**: Returns guidance on tool discovery and the 6 task type categories
2. **list-task-types**: Provides a complete mapping of task types to their associated tools  
3. **intent-query-help**: Explains how to use natural language queries for automatic filtering

**Example Usage:**

```bash
# Discover meta-tools
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"task_type": "meta-ops"},
    "id": 1
  }'

# Get tool discovery guidance
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "discover-tools",
      "arguments": {}
    },
    "id": 1
  }'
```

Meta-tools are in the "meta-ops" task type and return structured instructional content that helps LLMs understand how to access all Docker tools.

## Prompts for Tool Discovery

**Note**: If your MCP client doesn't support prompts, use the meta-tools instead (see Meta-Tools for Discovery section above).

The server also provides instructional prompts for clients that support the prompts capability. These prompts contain the same information as the meta-tools but through the MCP prompts interface.

**Available Prompts:**

1. **discover-tools**: Explains the 6 task type categories and how to use the `task_type` parameter to filter tools
2. **list-task-types**: Provides a dynamically-generated list of all task types and their associated tools
3. **intent-query-help**: Demonstrates how to use natural language queries for automatic tool filtering

**Example Usage:**

```bash
# List available prompts
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "prompts/list",
    "params": {},
    "id": 1
  }'

# Get specific prompt guidance
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "prompts/get",
    "params": {"name": "discover-tools"},
    "id": 2
  }'
```

**Why Use Prompts?**

- Prompts contain dynamic information about current task types and tool counts
- They help LLMs learn the tool organization without hardcoding assumptions
- Useful for onboarding new clients or when tool organization changes
- Reduce trial-and-error by providing clear, actionable guidance upfront

## Error Codes

| Code | Name | Description |
|------|------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid request | Missing required fields |
| -32601 | Method not found | Unknown method or tool blocked by gating |
| -32602 | Invalid params | Schema validation failure |
| -32603 | Internal error | Server-side error |

## Schema Validation

### Input Validation

Tool parameters are validated against `request_schema` from `tools.yaml`:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create-container",
    "arguments": {
      "name": "web"
    }
  },
  "id": 4
}
```

Submitting the request without the required `image` parameter triggers a `-32602` validation error.

**Error Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid parameters: 'image' is a required property",
    "data": {
      "path": [],
      "schema_path": ["properties", "image"]
    }
  },
  "id": 4
}
```

### Output Validation

Tool responses are validated against `response_schema`. Validation failures are logged but don't fail requests (server-side schema issue).

## Tool Gating Integration

The MCP endpoint integrates with the tool gating system:

1. **TaskTypeFilter**: Filters by `task_type` parameter
2. **ResourceFilter**: Limits tool count based on `max_tools`
3. **SecurityFilter**: Blocks tools in `blocklist`

Gated tools return `-32601` (Method not found) when called.

## Example Client Implementation

### Python

```python
import requests

class MCPClient:
    def __init__(self, url: str, token: str):
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.request_id = 0

    def _request(self, method: str, params: dict = None) -> dict:
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.request_id
        }
        response = requests.post(self.url, json=payload, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise Exception(f"MCP Error: {data['error']}")
        return data["result"]

    def initialize(self):
        return self._request("initialize", {
            "clientInfo": {"name": "python-client", "version": "1.0.0"}
        })

    def list_tools(self, task_type: str = None):
        params = {}
        if task_type:
            params["task_type"] = task_type
        return self._request("tools/list", params)

    def call_tool(self, name: str, arguments: dict):
        return self._request("tools/call", {
            "name": name,
            "arguments": arguments
        })

# Usage
client = MCPClient("http://localhost:8000/mcp/", "your-token")
client.initialize()
tools = client.list_tools(task_type="container-ops")
result = client.call_tool("list-containers", {"all": True})
```

### JavaScript

```javascript
class MCPClient {
  constructor(url, token) {
    this.url = url;
    this.headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    };
    this.requestId = 0;
  }

  async request(method, params = {}) {
    this.requestId++;
    const payload = {
      jsonrpc: '2.0',
      method,
      params,
      id: this.requestId
    };

    const response = await fetch(this.url, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (data.error) {
      throw new Error(`MCP Error: ${JSON.stringify(data.error)}`);
    }
    return data.result;
  }

  initialize() {
    return this.request('initialize', {
      clientInfo: { name: 'js-client', version: '1.0.0' }
    });
  }

  listTools(taskType = null) {
    const params = {};
    if (taskType) params.task_type = taskType;
    return this.request('tools/list', params);
  }

  callTool(name, args) {
    return this.request('tools/call', { name, arguments: args });
  }
}

// Usage
const client = new MCPClient('http://localhost:8000/mcp/', 'your-token');
await client.initialize();
const tools = await client.listTools('container-ops');
const result = await client.callTool('list-containers', { all: true });
```

## Observability

### Structured Logging

All MCP requests generate structured logs:

```json
{
  "timestamp": "2025-10-08T12:34:56Z",
  "level": "INFO",
  "message": "MCP JSON-RPC request: tools/list",
  "request_id": "uuid-1234",
  "session_id": "session-abc",
  "jsonrpc_method": "tools/list",
  "has_params": true
}
```

### Session Tracking

Use `X-Session-ID` header for cross-request correlation. Session IDs appear in all log entries for that session.

## Migration from Deprecated Endpoints

### Before (Deprecated REST-style endpoints - v0.4.x and earlier)

```bash
# These endpoints no longer exist
curl -H "Authorization: Bearer token" \
  http://localhost:8000/mcp/tools?task-type=container-ops
```

### After (JSON-RPC - v0.5.0+)

```bash
curl -s -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"task_type": "container-ops"},
    "id": 1
  }'
```

### Feature Comparison

| Feature | Deprecated REST (removed) | JSON-RPC `/mcp/` |
|---------|-------------------|---------------------|
| Tool discovery | ✅ (removed in v0.5.0) | ✅ |
| Task-type filtering | ✅ (removed in v0.5.0) | ✅ |
| Tool execution | ❌ | ✅ |
| Schema validation | ❌ | ✅ |
| Session tracking | ❌ | ✅ |
| Scope-based auth | ❌ | ✅ |
| Error codes | ❌ | ✅ |

> **Note**: The REST-style `/mcp/tools` and `/mcp/prompts` endpoints were removed in v0.5.0. The optional REST API under `/api/*` (controlled by `ENABLE_REST_API`) remains available for Docker operations.

## Best Practices

1. **Always initialize**: Call `initialize` first to verify protocol compatibility
2. **Handle errors gracefully**: Check for `error` field in responses
3. **Use session IDs**: Include `X-Session-ID` for distributed tracing
4. **Filter tools**: Use `task_type` parameter to reduce context size
5. **Use meta-tools or prompts for discovery**: Call discover-tools tool or prompts/list to learn about tool organization
6. **Access meta-tools on-demand**: Use task_type: 'meta-ops' to see all available meta-tools
7. **Validate inputs client-side**: Use `inputSchema` from tools/list to validate before calling
8. **Log request IDs**: Include request IDs in client logs for troubleshooting
8. **Preserve request IDs**: Echo the exact `id` from request in response tracking
9. **Avoid batch requests**: Use single requests per HTTP call (batch not supported)
10. **Use notifications sparingly**: Only for fire-and-forget operations that don't need responses

## See Also

- [MCP Client Setup](MCP-CLIENT-SETUP.md) - REST API client configuration
- [MCP Quick Reference](MCP-QUICK-REFERENCE.md) - Common operations cheat sheet
- [tools.yaml](../tools.yaml) - Complete tool schema definitions
