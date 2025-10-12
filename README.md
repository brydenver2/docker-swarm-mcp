# 🐳 Docker Swarm MCP Server

**The missing MCP server for Docker Swarm.** Finally, a production-ready MCP that gives you full Docker Swarm control without drowning your AI in tool descriptions.

![Semgrep](https://img.shields.io/badge/Scanned%20with-Semgrep-brightgreen?logo=semgrep) ![Code Reviewed by CodeRabbit](https://img.shields.io/badge/Code%20Reviewed%20by-CodeRabbit-000000?style=flat-square&logo=appveyor&logoColor=white&color=FF570A) ![Version](https://img.shields.io/badge/version-0.2.0-blue) ![Production Ready](https://img.shields.io/badge/status-production--ready-green)

## 🎯 Why This Exists

**The Gap:** After searching the MCP ecosystem, I found:
- ❌ Regular Docker MCPs with limited functionality (containers only, localhost only)
- ❌ Portainer MCP that only works with CE (not BE/EE)  
- ❌ No proper Swarm support anywhere
- ❌ All existing servers dump 20+ tools into your agents context window

**The Solution:** This server fills that gap with:
- ✅ **Full Docker Swarm support** - Services, stacks, configs, secrets
- ✅ **Smart context preservation** - Only shows tools you need (2-6 instead of 23)
- ✅ **Production security** - Bearer tokens, TLS, remote Docker support, *Tailscale Integration (coming soon)*
- ✅ **No bloat** - Just the tools you need, when you need them, filtered by the task at hand.


Note on secrets and client config:
- Do not commit secrets. Use environment variables (e.g., MCP_ACCESS_TOKEN), Docker secrets, or a secret manager.
- The .kilocode/ directory is gitignored. If you need a local MCP client config, copy mcp.client.json.example to your local tooling and set Authorization to use a runtime value like `Bearer ${MCP_ACCESS_TOKEN}`.

## 🚀 Quick Start (2 Minutes)

### 1️⃣ Deploy to Your Swarm

```bash
# Save this as docker-swarm-mcp.yml (or use one of the examples below)
# Deploy to your swarm
docker stack deploy -c docker-swarm-mcp.yml mcp-server

# Verify it's running
docker service logs mcp-server_docker-mcp
```

<details>
<summary><b>📝 Basic Stack Configuration</b></summary>

```yaml
version: '3.8'

services:
  docker-mcp:
    image: ghcr.io/yourusername/docker-swarm-mcp:latest
    environment:
      - MCP_ACCESS_TOKEN=${MCP_ACCESS_TOKEN:-change-me-to-secure-token}
      - LOG_LEVEL=INFO
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - "8000:8000"
    deploy:
      replicas: 1
      restart_policy:
        condition: any
        delay: 5s
      placement:
        constraints:
          - node.role == manager  # Needs Docker socket access
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: overlay
    attachable: true
```
</details>

<details>
<summary><b>🔒 Production Stack with Secrets</b></summary>

```yaml
version: '3.8'

services:
  docker-mcp:
    image: ghcr.io/yourusername/docker-swarm-mcp:latest
    environment:
      - MCP_ACCESS_TOKEN_FILE=/run/secrets/mcp_token
      - LOG_LEVEL=INFO
      - ALLOWED_ORIGINS=https://claude.ai,http://localhost:*
    secrets:
      - mcp_token
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - "8000:8000"
    deploy:
      replicas: 1
      restart_policy:
        condition: any
        delay: 5s
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/mcp/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    networks:
      - mcp-network

secrets:
  mcp_token:
    external: true  # Create with: echo "your-secure-token" | docker secret create mcp_token -

networks:
  mcp-network:
    driver: overlay
    attachable: true
    encrypted: true
```

**Setup the secret first:**
```bash
# Generate a secure token
openssl rand -base64 32 | docker secret create mcp_token -

# Or use your own token
echo "your-secure-token-here" | docker secret create mcp_token -
```
</details>

<details>
<summary><b>🌐 Stack with Traefik Integration</b></summary>

```yaml
version: '3.8'

services:
  docker-mcp:
    image: ghcr.io/yourusername/docker-swarm-mcp:latest
    environment:
      - MCP_ACCESS_TOKEN_FILE=/run/secrets/mcp_token
      - LOG_LEVEL=INFO
      - ALLOWED_ORIGINS=https://mcp.yourdomain.com
    secrets:
      - mcp_token
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    deploy:
      replicas: 2  # High availability
      restart_policy:
        condition: any
        delay: 5s
      placement:
        constraints:
          - node.role == manager
      update_config:
        parallelism: 1
        delay: 10s
      labels:
        - "traefik.enable=true"
        - "traefik.http.routers.mcp.rule=Host(`mcp.yourdomain.com`)"
        - "traefik.http.routers.mcp.entrypoints=websecure"
        - "traefik.http.routers.mcp.tls=true"
        - "traefik.http.routers.mcp.tls.certresolver=letsencrypt"
        - "traefik.http.services.mcp.loadbalancer.server.port=8000"
        - "traefik.http.middlewares.mcp-headers.headers.customrequestheaders.Authorization=Bearer ${MCP_TOKEN}"
        - "traefik.http.routers.mcp.middlewares=mcp-headers"
    networks:
      - traefik-public
      - mcp-internal

secrets:
  mcp_token:
    external: true

networks:
  traefik-public:
    external: true
  mcp-internal:
    driver: overlay
    encrypted: true
    internal: true
```
</details>

<details>
<summary><b>🔧 Multi-Node Swarm with Constraints</b></summary>

```yaml
version: '3.8'

services:
  docker-mcp:
    image: ghcr.io/yourusername/docker-swarm-mcp:latest
    environment:
      - MCP_ACCESS_TOKEN_FILE=/run/secrets/mcp_token
      - LOG_LEVEL=INFO
    secrets:
      - mcp_token
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    ports:
      - target: 8000
        published: 8000
        protocol: tcp
        mode: host  # Use host mode for better performance
    deploy:
      replicas: 1
      restart_policy:
        condition: any
        delay: 5s
      placement:
        constraints:
          - node.role == manager
          - node.labels.mcp == true  # Only on labeled nodes
        preferences:
          - spread: node.id
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      rollback_config:
        parallelism: 1
        delay: 10s
    networks:
      - mcp-network

configs:
  filter_config:
    file: ./filter-config.json  # Optional: Custom tool filtering

secrets:
  mcp_token:
    external: true

networks:
  mcp-network:
    driver: overlay
    attachable: true
    encrypted: true
```

**Label your node:**
```bash
docker node update --label-add mcp=true <node-name>
```
</details>

### 2️⃣ Configure Your AI Assistant

Add this to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "docker": {
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp/v1/",
        "headers": {
          "Authorization": "Bearer your-secure-token-here"
        }
      }
    }
  }
}
```

### 3️⃣ Start Using It!

Just ask your AI naturally:
- "What containers are running?"
- "Deploy my app stack"
- "Scale the web service to 5 replicas"
- "Show me the swarm nodes"

The server automatically detects what you're trying to do and provides just the right tools!

## 🎯 What Makes This Different

### 🧠 Smart Tool Filtering
Traditional MCP servers dump all their tools into your context. This server is smarter:

| You Say | Tools Returned | Context Saved |
|---------|---------------|--------------|
| "List my containers" | 4 container tools | 19 tools hidden |
| "Deploy a stack" | 3 compose tools | 20 tools hidden |
| "Check swarm status" | 3 swarm tools | 20 tools hidden |
| "Create a network" | 3 network tools | 20 tools hidden |

Your AI focuses on YOUR project, not on reading documentation.

### 🐳 Real Docker Swarm Support
Unlike other Docker MCPs, this one actually understands Swarm:
- **Services** - Create, scale, update, rolling deployments
- **Stacks** - Deploy complete applications
- **Configs & Secrets** - Secure configuration management
- **Networks** - Overlay networks, encryption
- **Nodes** - Manage your swarm cluster

### 🔒 Production Security
Built for real production use:
- Bearer token authentication
- Docker secrets support
- TLS connections to remote Docker
- CORS configuration
- Rate limiting ready

### 📚 Self-Documenting
Your AI can learn the system through meta-tools:
```
Ask: "How do I discover Docker tools?"
Response: Uses `discover-tools` to explain the 6 categories
```

## 💡 Examples

### Container Operations
```bash
# Your AI can now:
- List all containers with detailed status
- Create containers with complex configurations
- Start/stop/restart containers
- View logs and exec into containers
- Remove containers safely
```

### Swarm Service Management
```bash
# Your AI can now:
- Deploy services with replicas
- Scale services up or down
- Update services with rolling updates
- Check service logs across all replicas
- Manage service constraints and preferences
```

### Stack Deployments
```bash
# Your AI can now:
- Deploy complete application stacks
- Update stacks with new configurations
- Remove stacks cleanly
- List all stacks and their services
```

### Network & Volume Management
```bash
# Your AI can now:
- Create overlay networks for swarm
- Manage network encryption
- Create and manage volumes
- Connect/disconnect containers from networks
```

## 🛠️ Advanced Configuration

<details>
<summary><b>Environment Variables</b></summary>

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MCP_ACCESS_TOKEN` | ✅ | - | Bearer token for authentication |
| `DOCKER_HOST` | ❌ | `unix:///var/run/docker.sock` | Docker engine connection |
| `DOCKER_TLS_VERIFY` | ❌ | `0` | Enable TLS verification (1/0) |
| `DOCKER_CERT_PATH` | ❌ | - | Path to TLS certificates |
| `LOG_LEVEL` | ❌ | `INFO` | DEBUG shows context metrics |
| `ALLOWED_ORIGINS` | ❌ | `*` | CORS origins (comma-separated) |
| `MCP_TRANSPORT` | ❌ | `http` | Transport mode (http/sse) |

</details>

<details>
<summary><b>Custom Tool Filtering</b></summary>

Edit `filter-config.json` to customize which tools are available:

```json
{
  "task_type_allowlists": {
    "container-ops": ["list-containers", "create-container", "start-container"],
    "swarm-ops": ["list-services", "create-service", "scale-service"],
    "compose-ops": ["deploy-stack", "list-stacks"]
  },
  "max_tools": 10,
  "blocklist": ["remove-volume", "prune-system"]
}
```

Mount as a config in your stack:
```yaml
configs:
  filter_config:
    file: ./filter-config.json

services:
  docker-mcp:
    configs:
      - source: filter_config
        target: /app/filter-config.json
```
</details>

<details>
<summary><b>Remote Docker Access</b></summary>

**TLS Connection:**
```bash
export DOCKER_HOST="tcp://remote-host:2376"
export DOCKER_TLS_VERIFY="1"
export DOCKER_CERT_PATH="/path/to/certs"
```

**SSH Connection:**
```bash
export DOCKER_HOST="ssh://user@remote-host"
```

**Tailscale/Wireguard:**
```bash
export DOCKER_HOST="tcp://100.x.y.z:2376"  # Tailscale IP
```
</details>

<details>
<summary><b>Building From Source</b></summary>

```bash
# Clone the repository
git clone https://github.com/yourusername/docker-swarm-mcp.git
cd docker-swarm-mcp

# Build with Docker
docker build -t docker-swarm-mcp:latest .

# Or build with Docker Compose
docker-compose build

# For development
poetry install
poetry run uvicorn app.main:app --reload
```
</details>

## 🧪 Testing

```bash
# Quick health check
curl http://localhost:8000/mcp/health

# Test authentication
curl -H "Authorization: Bearer your-token" \
  http://localhost:8000/mcp/tools

# Test with intent detection
curl -X POST http://localhost:8000/mcp/v1 \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"query": "show me running containers"},
    "id": 1
  }'
```

## 📖 Documentation

- [**Client Setup Guide**](docs/MCP-CLIENT-SETUP.md) - Configure Claude Desktop, Cursor, etc.
- [**Quick Reference**](docs/MCP-QUICK-REFERENCE.md) - Common commands
- [**JSON-RPC Protocol**](docs/MCP-JSON-RPC-USAGE.md) - API details
- [**Security**](SECURITY.md) - Best practices
- [**Roadmap**](ROADMAP.md) - Coming features

## 🤝 Contributing

This fills a real gap in the MCP ecosystem! Contributions welcome:

1. **Report bugs** - Open an issue with reproduction steps
2. **Suggest features** - Check the roadmap first
3. **Submit PRs** - Follow existing patterns
4. **Improve docs** - Always appreciated
5. **Share your stacks** - Add examples to help others

**Focus areas:**
- More Swarm-specific tools
- Better Portainer BE/EE integration
- Enhanced security features
- Multi-cluster support

## 🙏 Acknowledgments

- Built on the Model Context Protocol (MCP) by Anthropic with FastAPI MCP.
- Inspired by the need for proper Docker Swarm support in AI workflows
- Thanks to the Docker and Swarm communities

---

**License:** MIT | **Status:** Production Ready | **Gap Filled:** ✅

*Finally, an MCP server that actually understands Docker Swarm.*
See docs/dependencies/tailscale.md for detailed Tailscale setup.
