# Docker Swarm MCP Server - Quick Reference

## Server Setup

```bash
# 1. Generate access token
export MCP_ACCESS_TOKEN="$(openssl rand -hex 32)"

# 2. Start server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. Test health check
curl http://localhost:8000/mcp/health
```

## Client Configuration

### Claude Desktop

**File:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "docker": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/v1/",
        "headers": {
          "Authorization": "Bearer your-token-here"
        }
      }
    }
  }
}
```

### claude-code CLI

```bash
# Add server
claude-code mcp add docker \
  --transport http \
  --url http://localhost:8000/mcp/v1/ \
  --header "Authorization: Bearer your-token-here"
```

### Kilo Code / Cursor

**File:** `.kilocode/mcp.json` (project-specific)

```json
{
  "mcpServers": {
    "docker": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp/v1/",
      "headers": {
        "Authorization": "Bearer your-token-here"
      },
      "alwaysAllow": [
        "ping", "info", "list-containers", "create-container",
        "start-container", "stop-container", "remove-container",
        "get-logs", "deploy-compose", "list-stacks", "remove-compose",
        "list-services", "scale-service", "remove-service",
        "list-networks", "create-network", "remove-network",
        "list-volumes", "create-volume", "remove-volume"
      ],
      "disabled": false
    }
  }
}
```

## Task Types

| Task Type | Tools | Description |
|-----------|-------|-------------|
| `container-ops` | 6 | List, create, start, stop, remove, logs |
| `compose-ops` | 3 | Deploy, list, remove stacks |
| `service-ops` | 3 | List, scale, remove services (Swarm) |
| `network-ops` | 3 | List, create, remove networks |
| `volume-ops` | 3 | List, create, remove volumes |
| `system-ops` | 2 | Info, ping |

## API Endpoints

### Discovery & Health

```bash
# Health check (no auth)
GET /mcp/health

# Tool discovery
GET /mcp/tools
GET /mcp/tools?task-type=container-ops
```

### Containers

```bash
GET    /containers                    # List containers
POST   /containers                    # Create container
POST   /containers/{id}/start         # Start container
POST   /containers/{id}/stop          # Stop container
DELETE /containers/{id}               # Remove container
GET    /containers/{id}/logs          # Get logs
```

### Stacks (Compose)

```bash
POST   /stacks/deploy                 # Deploy stack
GET    /stacks                        # List stacks
DELETE /stacks/{project_name}         # Remove stack
```

### Services (Swarm)

```bash
GET    /services                      # List services
POST   /services/{name}/scale         # Scale service
DELETE /services/{name}               # Remove service
```

### Networks

```bash
GET    /networks                      # List networks
POST   /networks                      # Create network
DELETE /networks/{id}                 # Remove network
```

### Volumes

```bash
GET    /volumes                       # List volumes
POST   /volumes                       # Create volume
DELETE /volumes/{name}                # Remove volume
```

### System

```bash
GET    /system/ping                   # Ping Docker
GET    /system/info                   # System info
```

## cURL Examples

```bash
# Set token
TOKEN="your-token-here"

# Tool discovery
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/mcp/tools

# List containers
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/containers?all=true"

# Create container
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"image":"nginx:alpine","name":"web","ports":{"80/tcp":8080}}' \
  http://localhost:8000/containers

# Deploy stack
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_name":"demo","compose_yaml":"version: \"3.8\"\nservices:\n  web:\n    image: nginx:alpine\n"}' \
  http://localhost:8000/stacks/deploy
```

## Remote Access

### Tailscale (Recommended)

```bash
# Server: Install Tailscale
tailscale up

# Server: Get IP
tailscale ip -4  # e.g., 100.101.102.103

# Client config
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "http://100.101.102.103:8000/mcp/v1/",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

### ngrok (Development)

```bash
# Server: Start ngrok
ngrok http 8000

# Use provided URL in client config
{
  "mcpServers": {
    "docker-remote": {
      "transport": "http",
      "url": "https://abc123.ngrok.io/mcp/v1/",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

### TLS/SSH (Production)

```bash
# TLS
export DOCKER_HOST="tcp://remote:2376"
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH="/path/to/certs"

# SSH
export DOCKER_HOST="ssh://user@remote"
```

## Environment Variables

```bash
# Required
MCP_ACCESS_TOKEN="your-token"

# Docker connection
DOCKER_HOST="unix:///var/run/docker.sock"
DOCKER_TLS_VERIFY="0"
DOCKER_CERT_PATH=""

# Server config
MCP_TRANSPORT="http"
LOG_LEVEL="INFO"
ALLOWED_ORIGINS="*"
```

## Troubleshooting

```bash
# Check server health
curl http://localhost:8000/mcp/health

# Test authentication
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/mcp/tools

# Check context size (requires LOG_LEVEL=DEBUG)
export LOG_LEVEL="DEBUG"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/mcp/tools | jq '.context_size'

# View server logs
docker logs mcp-server

# Check Docker connectivity
docker ps
```

## Security Checklist

- [ ] Generate strong random token: `openssl rand -hex 32`
- [ ] Store token in environment variable, not config file
- [ ] Use HTTPS for remote access (Tailscale/ngrok)
- [ ] Set `ALLOWED_ORIGINS` to specific domains in production
- [ ] Enable pre-commit hooks: `pre-commit install`
- [ ] Run security scan: `poetry run bandit -r app/`
- [ ] Review logs for exposed secrets
- [ ] Rotate access tokens regularly
- [ ] Use Tailscale ACLs to restrict access
- [ ] Monitor failed authentication attempts

## Files & Paths

```
# Configuration
.env                           # Environment variables (DO NOT COMMIT)
.env.example                   # Template for environment variables
filter-config.json             # Tool gating configuration
tools.yaml                     # MCP tool definitions

# Documentation
docs/MCP-CLIENT-SETUP.md       # Detailed client setup guide
docs/mcp-client-config.schema.json  # JSON schema for validation
docs/MCP-QUICK-REFERENCE.md    # This file
docs/dependencies/             # Dependency reference stubs

# Client configs
~/Library/Application Support/Claude/claude_desktop_config.json  # Claude Desktop
~/.config/opencode/opencode.json  # claude-code CLI
```

## Common Workflows

### Workflow 1: Container Development

```bash
# 1. Configure client with container-ops only
# 2. Ask Claude to list running containers
# 3. Ask Claude to create a test container
# 4. Ask Claude to view logs
# 5. Ask Claude to stop and remove container
```

### Workflow 2: Stack Deployment

```bash
# 1. Configure client with compose-ops only
# 2. Ask Claude to deploy a compose file
# 3. Ask Claude to list stacks
# 4. Ask Claude to remove the stack
```

### Workflow 3: System Monitoring

```bash
# 1. Configure client with system-ops only
# 2. Ask Claude to check Docker connectivity
# 3. Ask Claude to get system information
# 4. Ask Claude to report on resource usage
```

## Version Info

- **Server Version**: 0.2.0
- **Python**: 3.12+
- **Docker Engine**: 24+
- **MCP Protocol**: HTTP/SSE transport
- **Tool Count**: 23 tools across 7 task types

## Resources

- GitHub: [docker-swarm-mcp](https://github.com/yourusername/docker-swarm-mcp)
- Issues: [Report a bug](https://github.com/yourusername/docker-swarm-mcp/issues)
- Documentation: See `docs/` directory for detailed guides
- Tool Definitions: See `tools.yaml` for API specifications
