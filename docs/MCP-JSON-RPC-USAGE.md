# MCP JSON-RPC Usage Guide

This guide covers the new MCP JSON-RPC 2.0 endpoint for programmatic tool access with integrated gating and schema validation.

## Overview

The MCP JSON-RPC endpoint provides a standards-compliant interface for:
- Tool discovery with dynamic gating
- Tool execution with schema validation
- Session tracking and observability
- Scope-based authorization

**Endpoint**: `POST /mcp/v1`

## JSON-RPC Protocol

All requests and responses follow JSON-RPC 2.0 specification:

```json
{
  "jsonrpc": "2.0",
  "method": "method_name",
  "params": {},
  "id": 1
}
```

### Response Format

**Success:**
```json
{
  "jsonrpc": "2.0",
  "result": {},
  "id": 1
}
```

**Error:**
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
      "name": "docker-mcp-server",
      "version": "0.1.0"
    },
    "capabilities": {
      "tools": {
        "gating": true,
        "context_size_enforcement": true,
        "task_type_filtering": true
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

**Request (with filtering):**
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
      "context_size": 2450,
      "filters_applied": ["TaskTypeFilter", "SecurityFilter"]
    }
  },
  "id": 2
}
```

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

## Authentication

All requests require Bearer token authentication:

```bash
curl -X POST http://localhost:8000/mcp/v1 \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'
```

### Scope-Based Authorization

Configure scopes via `TOKEN_SCOPES` environment variable:

```bash
export TOKEN_SCOPES='{"user-token": ["container-ops", "system-ops"]}'
```

- `admin` scope: Full access to all tools
- Task-type scopes: Access only to specific tool categories

## Session Tracking

Include `X-Session-ID` header for session correlation:

```bash
curl -X POST http://localhost:8000/mcp/v1 \
  -H "Authorization: Bearer your-token" \
  -H "X-Session-ID: session-abc123" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}'
```

Session IDs appear in server logs for tracing and debugging.

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
      "image": "nginx:latest"  // Missing 'image' causes -32602 error
    }
  },
  "id": 4
}
```

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
client = MCPClient("http://localhost:8000/mcp/v1", "your-token")
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
const client = new MCPClient('http://localhost:8000/mcp/v1', 'your-token');
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

## Migration from REST API

### Before (REST)

```bash
curl -H "Authorization: Bearer token" \
  http://localhost:8000/mcp/tools?task-type=container-ops
```

### After (JSON-RPC)

```bash
curl -X POST http://localhost:8000/mcp/v1 \
  -H "Authorization: Bearer token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"task_type": "container-ops"},
    "id": 1
  }'
```

### Feature Parity

| Feature | REST `/mcp/tools` | JSON-RPC `/mcp/v1` |
|---------|-------------------|---------------------|
| Tool discovery | ✅ | ✅ |
| Task-type filtering | ✅ | ✅ |
| Tool execution | ❌ | ✅ |
| Schema validation | ❌ | ✅ |
| Session tracking | ❌ | ✅ |
| Scope-based auth | ❌ | ✅ |
| Error codes | ❌ | ✅ |

## Best Practices

1. **Always initialize**: Call `initialize` first to verify protocol compatibility
2. **Handle errors gracefully**: Check for `error` field in responses
3. **Use session IDs**: Include `X-Session-ID` for distributed tracing
4. **Filter tools**: Use `task_type` parameter to reduce context size
5. **Validate inputs client-side**: Use `inputSchema` from tools/list to validate before calling
6. **Log request IDs**: Include request IDs in client logs for troubleshooting

## See Also

- [MCP Client Setup](MCP-CLIENT-SETUP.md) - REST API client configuration
- [MCP Quick Reference](MCP-QUICK-REFERENCE.md) - Common operations cheat sheet
- [tools.yaml](../tools.yaml) - Complete tool schema definitions
