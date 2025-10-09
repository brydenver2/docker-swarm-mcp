# MCP Client Setup Guide

This guide shows how to configure MCP clients (Claude Desktop, claude-code, etc.) to connect to your Docker MCP Server.

## Table of Contents

- [Quick Start](#quick-start)
- [Configuration Formats](#configuration-formats)
  - [HTTP Transport](#http-transport)
  - [SSE Transport](#sse-transport)
- [Client-Specific Examples](#client-specific-examples)
  - [Claude Desktop](#claude-desktop)
  - [claude-code CLI](#claude-code-cli)
  - [Custom MCP Clients](#custom-mcp-clients)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Start the Docker MCP Server

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

# Tool discovery (requires auth)
curl -H "Authorization: Bearer your-secure-token-here" \
  http://localhost:8000/mcp/tools
```

---

## Configuration Formats

### HTTP Transport

Standard HTTP REST API with Bearer token authentication.

**Minimal Configuration:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

**Full Configuration with Task-Type Filtering:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      },
      "endpoints": {
        "tools": "/mcp/tools",
        "health": "/mcp/health"
      },
      "queryParams": {
        "task-type": "container-ops"
      }
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
      "url": "https://abc123.ngrok.io",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

### SSE Transport

Server-Sent Events for streaming responses (optional).

**Configuration:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "sse",
      "url": "http://localhost:8000",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

**Server-side setup:**

```bash
export MCP_TRANSPORT="sse"
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

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
      "command": "curl",
      "args": [
        "-H", "Authorization: Bearer your-secure-token-here",
        "http://localhost:8000/mcp/tools"
      ],
      "env": {}
    }
  }
}
```

**Alternative: Using HTTP Transport (Recommended):**

```json
{
  "mcpServers": {
    "docker": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000",
        "headers": {
          "Authorization": "Bearer your-secure-token-here"
        }
      }
    }
  }
}
```

**With Task-Type Filtering:**

```json
{
  "mcpServers": {
    "docker-containers": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/tools?task-type=container-ops",
        "headers": {
          "Authorization": "Bearer your-secure-token-here"
        }
      }
    },
    "docker-stacks": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/tools?task-type=compose-ops",
        "headers": {
          "Authorization": "Bearer your-secure-token-here"
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
  --url http://localhost:8000 \
  --header "Authorization: Bearer your-secure-token-here"
```

**Add with Task-Type Filtering:**

```bash
# Container operations only
claude-code mcp add docker-containers \
  --transport http \
  --url "http://localhost:8000/mcp/tools?task-type=container-ops" \
  --header "Authorization: Bearer your-secure-token-here"

# Compose stack operations only
claude-code mcp add docker-stacks \
  --transport http \
  --url "http://localhost:8000/mcp/tools?task-type=compose-ops" \
  --header "Authorization: Bearer your-secure-token-here"
```

**Manual Configuration in `opencode.json`:**

```json
{
  "mcpServers": {
    "docker": {
      "transport": "http",
      "url": "http://localhost:8000",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
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
      "url": "http://localhost:8000",
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
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def get_tools(self, task_type: str | None = None) -> dict:
        params = {"task-type": task_type} if task_type else {}
        response = requests.get(
            f"{self.url}/mcp/tools",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
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

  constructor(config: MCPConfig) {
    this.url = config.url;
    this.headers = {
      'Authorization': `Bearer ${config.token}`,
      'Content-Type': 'application/json'
    };
  }

  async getTools(taskType?: string): Promise<any> {
    const params = taskType ? `?task-type=${taskType}` : '';
    const response = await fetch(`${this.url}/mcp/tools${params}`, {
      headers: this.headers
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return response.json();
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

# Test authentication
curl -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  http://localhost:8000/mcp/tools
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

# Example: Only container operations
curl -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  "http://localhost:8000/mcp/tools?task-type=container-ops"
```

**Check context size (DEBUG mode):**

```bash
# Enable DEBUG logging
export LOG_LEVEL="DEBUG"

# Check response for context_size field
curl -H "Authorization: Bearer $MCP_ACCESS_TOKEN" \
  http://localhost:8000/mcp/tools | jq '.context_size'
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

## Task-Type Reference

Available task types for filtering:

- `container-ops` - Container lifecycle operations (6 tools)
- `compose-ops` - Compose stack deployment (3 tools)
- `service-ops` - Swarm service management (3 tools)
- `network-ops` - Network management (3 tools)
- `volume-ops` - Volume management (3 tools)
- `system-ops` - System info and health checks (2 tools)

**Example: Multi-context setup for different workflows**

```json
{
  "mcpServers": {
    "docker-dev": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/tools?task-type=container-ops",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    },
    "docker-deploy": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/tools?task-type=compose-ops",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    },
    "docker-ops": {
      "transport": "http",
      "url": "http://localhost:8000/mcp/tools?task-type=system-ops",
      "headers": {
        "Authorization": "Bearer ${DOCKER_MCP_TOKEN}"
      }
    }
  }
}
```

---

## Additional Resources

- **Tool Definitions**: See `tools.yaml` for complete tool specifications
- **Server Configuration**: See `.env.example` for all environment variables
- **Quick Reference**: See `docs/MCP-QUICK-REFERENCE.md` for command cheat sheet

