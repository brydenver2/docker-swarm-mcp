# MCP Client Setup Guide


This guide shows how to configure MCP clients (Claude Desktop, claude-code, etc.) to connect to your Docker Swarm MCP Server.

## Table of Contents

- [MCP Client Setup Guide](#mcp-client-setup-guide)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
    - [1. Start the Docker Swarm MCP Server](#1-start-the-docker-mcp-server)
    - [2. Configure Your MCP Client](#2-configure-your-mcp-client)
    - [3. Test the Connection](#3-test-the-connection)
  - [Configuration Formats](#configuration-formats)
    - [HTTP Transport](#http-transport)
    - [SSE Transport](#sse-transport)
  - [Client-Specific Examples](#client-specific-examples)
    - [Claude Desktop](#claude-desktop)
    - [claude-code CLI](#claude-code-cli)
    - [Custom MCP Clients](#custom-mcp-clients)
  - [Security Best Practices](#security-best-practices)
    - [1. Token Management](#1-token-management)
    - [2. Network Security](#2-network-security)
    - [3. CORS Configuration](#3-cors-configuration)
    - [4. TLS/HTTPS](#4-tlshttps)
  - [Troubleshooting](#troubleshooting)
    - [Connection Issues](#connection-issues)
    - [Context Size Issues](#context-size-issues)
    - [Performance Issues](#performance-issues)
  - [Intent-Based Tool Discovery (Recommended)](#intent-based-tool-discovery-recommended)
    - [Single Server Configuration](#single-server-configuration)
    - [How It Works](#how-it-works)
    - [Example Workflow](#example-workflow)
    - [Migration from Multi-Server Setup](#migration-from-multi-server-setup)
    - [Kilo Code / Cursor Configuration](#kilo-code--cursor-configuration)
  - [Additional Resources](#additional-resources)

---

## Quick Start

### 1. Start the Docker Swarm MCP Server

```bash
# Set your access token
export MCP_ACCESS_TOKEN="your-secure-token-here"

# Start the server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Configure Your MCP Client

Add the Docker MCP server to your client's configuration file (see [Client-Specific Examples](#client-specific-examples) below).

### 3. Test the Connection

```bash
# Health check (no auth required)
curl http://localhost:8000/mcp/health

# Tool discovery (requires auth) - JSON-RPC
curl -s -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer your-secure-token-here" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}'
```

---

## Configuration Formats

### HTTP Transport

Standard HTTP with JSON-RPC 2.0 over HTTP and Bearer token authentication.

**Standard Configuration (Header-based):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

**Simple Configuration (Custom Header):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      }
    }
  }
}
```

**Alternative Simple Format:**

```json
{
  "mcpServers": {
    "docker": {
      "type": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      }
    }
  }
}
```

**serverUrl Format:**

```json
{
  "mcpServers": {
    "docker": {
      "serverUrl": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      }
    }
  }
}
```

> **Note**: The trailing slash in `/mcp/` is required for proper routing.
> 
> **Authentication Priority**: Authorization header takes precedence over `X-Access-Token` header if both are provided.

**Kilo Code / Cursor Configuration:**

```json
{
  "mcpServers": {
    "docker": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      },
      "disabled": false
    }
  }
}
```

**Kilo Code / Cursor (Simple Format):**

```json
{
  "mcpServers": {
    "docker": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      },
      "disabled": false
    }
  }
}
```

**Remote Server (ngrok/Tailscale):**

```json
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "https://abc123.ngrok.io/mcp/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

**Remote Server (Simple Format):**

```json
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "https://abc123.ngrok.io/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      }
    }
  }
}
```

### SSE Transport

Server-Sent Events for streaming responses (optional, not commonly used).

**Configuration:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "sse",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

> **Note**: Most MCP clients use the standard HTTP transport with JSON-RPC 2.0.

**Server-side setup:**

```bash
export MCP_TRANSPORT="sse"
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### Migration from v0.4.x

If you're upgrading from v0.4.x, you must update your client configuration. Query parameter authentication (`?accessToken=...`) has been removed for security reasons. Replace it with the `X-Access-Token` header:

**Before (v0.4.x):**

```json
{
  "mcpServers": {
    "docker": {
      "url": "http://localhost:8000/mcp/?accessToken=token"
    }
  }
}
```

**After (v0.5.0+):**

```json
{
  "mcpServers": {
    "docker": {
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "token"
      }
    }
  }
}
```

This change keeps tokens out of server logs, browser history, and referrer headers while remaining easy to configure.

---

## Client-Specific Examples

### Claude Desktop

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)  
**Location:** `%APPDATA%\Claude\claude_desktop_config.json` (Windows)  
**Location:** `~/.config/Claude/claude_desktop_config.json` (Linux)

**Example Configuration:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/",
        "headers": {
          "Authorization": "Bearer your-secure-token-here"
        }
      }
    }
  }
}
```

**Claude Desktop (Simple Format):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/",
        "headers": {
          "X-Access-Token": "your-secure-token-here"
        }
      }
    }
  }
}
```

---

### claude-code CLI

**Using `mcp add` Command:**

```bash
# Add Docker MCP server to opencode.json
claude-code mcp add docker \
  --transport http \
  --url http://localhost:8000/mcp/ \
  --header "Authorization: Bearer your-secure-token-here"
```

**Manual Configuration in `opencode.json`:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

**Manual Configuration (Simple Format):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "X-Access-Token": "your-secure-token-here"
      }
    }
  }
}
```

**With Environment Variable for Token:**

```bash
# Set token in environment
export DOCKER_MCP_TOKEN="your-secure-token-here"
```

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    }
  }
}
```

---

### Custom MCP Clients

**Python Example:**

```python
import requests

class DockerMCPClient:
    def __init__(self, url: str, token: str):
        self.url = url
        # Use X-Access-Token header to keep tokens out of URLs
        self.headers = {
            "X-Access-Token": token,
            "Content-Type": "application/json"
        }
        self.request_id = 0

    def _jsonrpc_request(self, method: str, params: dict = None) -> dict:
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self.request_id
        }
        response = requests.post(
            f"{self.url}/mcp/",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise Exception(f"MCP Error: {data['error']}")
        return data["result"]

    def get_tools(self, task_type: str | None = None) -> dict:
        params = {"task_type": task_type} if task_type else {}
        return self._jsonrpc_request("tools/list", params)
    
    def list_containers(self, all: bool = False) -> dict:
        params = {"all": str(all).lower()}
        response = requests.get(
            f"{self.url}/containers",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

# Usage
client = DockerMCPClient("http://localhost:8000", "your-token")
tools = client.get_tools(task_type="container-ops")
containers = client.list_containers(all=True)
```

**JavaScript/TypeScript Example:**

```typescript
interface MCPConfig {
  url: string;
  token: string;
}

class DockerMCPClient {
  private url: string;
  private headers: Record<string, string>;
  private requestId: number = 0;

  constructor(config: MCPConfig) {
    this.url = config.url;
    this.headers = {
      'X-Access-Token': config.token,
      'Content-Type': 'application/json'
    };
  }

  private async jsonrpcRequest(method: string, params: any = {}): Promise<any> {
    this.requestId++;
    const payload = {
      jsonrpc: '2.0',
      method,
      params,
      id: this.requestId
    };

    const response = await fetch(`${this.url}/mcp/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    if (data.error) {
      throw new Error(`MCP Error: ${JSON.stringify(data.error)}`);
    }
    return data.result;
  }

  async getTools(taskType?: string): Promise<any> {
    const params = taskType ? { task_type: taskType } : {};
    return this.jsonrpcRequest('tools/list', params);
  }

  async listContainers(all: boolean = false): Promise<any> {
    const params = `?all=${all}`;
    const response = await fetch(`${this.url}/containers${params}`, {
      headers: this.headers
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
  }
}

// Usage
const client = new DockerMCPClient({
  url: 'http://localhost:8000',
  token: 'your-token'
});

const tools = await client.getTools('container-ops');
const containers = await client.listContainers(true);
```

---

## Security Best Practices

> Tokens are accepted only via HTTP headers (`Authorization: Bearer` or `X-Access-Token`). Query parameter authentication has been removed to prevent tokens from appearing in URLs, logs, and referrer headers.
> 
> Prefer the standard Authorization header when your client supports it. Use the `X-Access-Token` header as a simpler alternative for clients that cannot set Bearer tokens.

### 1. Token Management

**Generate Secure Tokens:**

```bash
# Generate a random token
openssl rand -hex 32

# Or use Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Store Tokens Securely:**

```bash
# Use environment variables (not in config files)
export DOCKER_MCP_TOKEN="$(openssl rand -hex 32)"

# Or use a secrets manager
export DOCKER_MCP_TOKEN="$(aws secretsmanager get-secret-value --secret-id docker-mcp-token --query SecretString --output text)"
```

### 2. Network Security

**Local Development (Safest):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    }
  }
}
```

**Tailscale VPN (Recommended for Remote Access):**

```json
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "http://100.101.102.103:8000",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    }
  }
}
```

**ngrok Tunnel (Development Only):**

```bash
# Start ngrok with basic auth
ngrok http 8000 --basic-auth "user:pass"
```

```json
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "https://abc123.ngrok.io",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}",
        "ngrok-auth": "Basic dXNlcjpwYXNz"
      }
    }
  }
}
```

### 3. CORS Configuration

**Server-side configuration:**

```bash
# Production: specific origins only
export ALLOWED_ORIGINS="https://app.example.com,https://admin.example.com"

# Development: allow all (insecure)
export ALLOWED_ORIGINS="*"
```

### 4. TLS/HTTPS

**For production deployments:**

```bash
# Run behind nginx/Caddy with TLS
# Or use ngrok/Tailscale HTTPS

# Example: Caddy reverse proxy
caddy reverse-proxy --from https://docker-mcp.example.com --to localhost:8000
```

---

## Troubleshooting

### Connection Issues

**Error: "Connection refused"**

```bash
# Check if server is running
curl http://localhost:8000/mcp/health

# Check server logs
docker logs mcp-server
```

**Error: "401 Unauthorized"**

```bash
# Verify token matches
echo $MCP_ACCESS_TOKEN

# Test authentication (JSON-RPC)
curl -s -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}'
```

**Error: "CORS policy"**

```bash
# Update server ALLOWED_ORIGINS
export ALLOWED_ORIGINS="https://your-client-domain.com"

# Restart server
docker restart mcp-server
```

### Context Size Issues

**Error: "Context size exceeds 7600 tokens"**

```bash
# Enable task-type filtering in client config
# This reduces the number of tools returned

# Example: Only container operations (JSON-RPC)
curl -s -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{"task_type":"container-ops"}}'
```

**Check context size (DEBUG mode):**

```bash
# Enable DEBUG logging
export LOG_LEVEL="DEBUG"

# Check response for context_size field (JSON-RPC)
curl -s -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}' | jq '.result._metadata.context_size'
```

### Performance Issues

**Slow responses:**

```bash
# Check server logs for duration_ms
docker logs mcp-server | grep duration_ms

# Verify Docker daemon is responsive
docker ps

# Check network latency (for remote servers)
ping your-server-ip
```

---

## Intent-Based Tool Discovery (Recommended)

The recommended approach is to use a **single MCP server configuration** and let the server automatically filter tools based on your natural language queries.

### Single Server Configuration

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

### How It Works

1. **No task-type configuration needed**: The server analyzes your queries automatically
2. **Dynamic filtering**: Each request returns only relevant tools (2-6 instead of 22)
3. **Natural language**: Describe what you want to do in plain language
4. **Optimal context usage**: Dramatically reduces context size without manual configuration

### Example Workflow

```
User: "Show me all running containers"
→ Server returns: list-containers, get-logs, start-container, stop-container (4 tools)

User: "Deploy my docker-compose stack"
→ Server returns: deploy-compose, list-stacks, remove-compose (3 tools)

User: "Scale the web service to 5 replicas"
→ Server returns: list-services, scale-service, remove-service (3 tools)
```

### Migration from Multi-Server Setup

**Before (Flawed Approach)**:
```json
{
  "docker-containers": {"url": "...", "headers": {"X-Task-Type": "container-ops"}},
  "docker-networks": {"url": "...", "headers": {"X-Task-Type": "network-ops"}},
  "docker-volumes": {"url": "...", "headers": {"X-Task-Type": "volume-ops"}}
}
```
❌ **Problem**: All 23 tools still loaded across multiple connections, no real context reduction

**After (Intent-Based Approach)**:
```json
{
  "docker": {
    "url": "http://localhost:8000/mcp/",
    "headers": {"Authorization": "Bearer your-token"}
  }
}
```
✅ **Solution**: Single connection, automatic filtering, 2-6 tools per request

### Kilo Code / Cursor Configuration

```json
{
  "mcpServers": {
    "docker": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp/",
      "headers": {
        "Authorization": "Bearer your-token-here"
      },
      "disabled": false
    }
  }
}
```

**Note**: Remove the `alwaysAllow` array - it's no longer needed with intent-based discovery.

---

## Meta-Tools for Universal Compatibility

The server provides special meta-tools that work with **all MCP clients**, regardless of prompt support. These tools return instructional content to help you discover and access all available tools.

### Available Meta-Tools

The meta-tools are available in the `meta-ops` task type and include:

1. **`discover-tools`**: Learn about all 23 tools and how they're organized into 7 task types
2. **`list-task-types`**: Get detailed information about each task type category
3. **`intent-query-help`**: Understand how intent-based tool discovery works

### Using Meta-Tools

```bash
# List meta-tools
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"task_type": "meta-ops"},
    "id": 1
  }'

# Call discover-tools to learn about tool organization
curl -X POST http://localhost:8000/mcp/ \
  -H "Authorization: Bearer $TOKEN" \
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

### When to Use Meta-Tools

- **Client Compatibility**: Works with any MCP client (Claude Desktop, claude-code, custom clients)
- **No Prompt Support Required**: Unlike MCP prompts, meta-tools work through the standard tools interface
- **Structured Learning**: Get comprehensive information about tool organization and discovery
- **Universal Access**: Same content available through prompts for clients that support them

### Example Response

The `discover-tools` tool returns structured JSON showing:
- All 7 task types with descriptions
- Intent keywords for automatic discovery
- Tool counts per category
- Best practices for efficient tool usage

This ensures you can access all server capabilities regardless of your MCP client's feature support.

---

## Additional Resources

- **Tool Definitions**: See `tools.yaml` for complete tool specifications
- **Server Configuration**: See `.env.example` for all environment variables
- **Quick Reference**: See `docs/MCP-QUICK-REFERENCE.md` for command cheat sheet
