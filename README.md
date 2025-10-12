# Docker Swarm MCP Server

![Semgrep](https://img.shields.io/badge/Scanned%20with-Semgrep-brightgreen?logo=semgrep) ![Code Reviewed by CodeRabbit](https://img.shields.io/badge/Code%20Reviewed%20by-CodeRabbit-000000?style=flat-square&logo=appveyor&logoColor=white&color=FF570A)


Streamable-HTTP-based Model Context Protocol (MCP) server for Docker operations with context-preserving tool gating. Let your agents focus their context on your project not tool description! 

## Features

- **Intent-Based Tool Discovery**: Automatic task-type detection from natural language queries to avoid context overload from bulk tool descriptions
- **📚 Instructional Content**: Built-in guidance through meta-tools and prompts for discovering and accessing all tools
- **Dynamic Context Optimization**: Returns only 2-6 relevant tools per request instead of all 23, keeping context size under control.
- **Secure Remote Access**: Access token authentication for MCP clients
- **Docker Operations**: Containers, Compose stacks, Swarm services, networks, volumes, system info
- **Multi-Transport Support**: HTTP (default) and SSE fallback
- **Remote Docker Engines**: Local socket, TLS, and SSH connections

### Intent-Based Tool Discovery

The server automatically filters tools based on your queries:

```bash
# The server automatically filters tools based on your queries
curl -X POST http://localhost:8000/mcp/v1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {"query": "show me running containers"},
    "id": 1
  }'

# Returns only container-ops tools (4-6 tools instead of 23)
```


## Quick Start

### Prerequisites

- Python 3.12+
- Poetry
- Docker Engine 24+

### Docker Installation (Recommended)

```bash
# Build the **container**
docker build -t docker-swarm-mcp .

# Run with Docker Compose
docker-compose up -d
```

### Developer Installation

```bash
# Install dependencies
poetry install

# Set required environment variables
export MCP_ACCESS_TOKEN="your-secure-token-here"
export DOCKER_HOST="unix:///var/run/docker.sock"  # or tcp://host:2376 with TLS

# Optional: Configure transport mode
export MCP_TRANSPORT="http"  # or "sse"
export LOG_LEVEL="INFO"  # DEBUG for context size metrics

# Run the server
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## MCP Client Setup

Once the server is running, configure your MCP client to connect:

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Kilo Code / Cursor

Add to `.kilocode/mcp.json` in your project:

```json
{
  "mcpServers": {
    "docker": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp/v1/",
      "headers": {
        "Authorization": "Bearer your-secure-token-here"
      }
    }
  }
}
```

### claude-code CLI

```bash
claude mcp add docker \
  --transport http \
  --url http://localhost:8000/mcp/v1/ \
  --header "Authorization: Bearer your-secure-token-here"
```

**See [`docs/MCP-CLIENT-SETUP.md`](docs/MCP-CLIENT-SETUP.md) for complete configuration examples.**

## **Protocol**

This server implements the **Model Context Protocol (MCP) JSON-RPC 2.0** specification:

- **Endpoint**: `POST /mcp/v1/` (note the trailing slash)
- **Protocol**: JSON-RPC 2.0 over HTTP
- **Methods**: `initialize`, `tools/list`, `tools/call`, `prompts/list`, `prompts/get`
- **Authentication**: Bearer token in `Authorization` header
- **Response Format**: Compliant with JSON-RPC 2.0 (result OR error, never both)

The server also provides meta-tools (discover-tools, list-task-types, intent-query-help) that return instructional content through the standard tools interface, ensuring compatibility with all MCP clients.

**Prompts Capability**: Prompts provide instructional templates to help LLMs understand tool organization and discovery mechanisms.

**See [`docs/MCP-JSON-RPC-USAGE.md`](docs/MCP-JSON-RPC-USAGE.md) for detailed protocol documentation.**

## Configuration

### Environment Variables

- `MCP_ACCESS_TOKEN` (required): Bearer token for client authentication
- `DOCKER_HOST` (optional): Docker engine connection (default: unix:///var/run/docker.sock)
- `DOCKER_TLS_VERIFY` (optional): Enable TLS verification (1/0)
- `DOCKER_CERT_PATH` (optional): Path to TLS certificates
- `MCP_TRANSPORT` (optional): Transport mode (http/sse, default: http)
- `LOG_LEVEL` (optional): Logging level (DEBUG/INFO/WARNING/ERROR, default: INFO)
- `ALLOWED_ORIGINS` (optional): CORS allowed origins (comma-separated)

### Filter Configuration

Edit `filter-config.json` to customize tool gating:

```json
{
  "task_type_allowlists": {
    "container-ops": ["list-containers", "create-container", "start-container"],
    "network-ops": ["list-networks", "create-network"]
  },
  "max_tools": 10,
  "blocklist": ["remove-volume"]
}
```

Server restart required for configuration changes.

## Intent-Based Tool Discovery

The server automatically detects which Docker operations you need based on natural language queries, dramatically reducing context size:

- **"List running containers"** → Returns container management tools (6 tools)
- **"Deploy docker-compose stack"** → Returns compose tools (3 tools)  
- **"Scale web service"** → Returns swarm service tools (3 tools)
- **"Create network"** → Returns network tools (3 tools)

**No client configuration needed** - just describe what you want to do.

### Learning About Tool Organization

The server includes special meta-tools that provide guidance on tool organization and filtering. Call the discover-tools tool to learn about the 6 task type categories and how to access specific tools.

**Example**: Use `tools/list` with `task_type: "meta-ops"` to see all available meta-tools, then call `discover-tools` to get guidance on tool discovery. This approach works with any MCP client, unlike prompts which require client-side support.

## API Usage

### Authentication

All endpoints (except `/mcp/health`) require Bearer token authentication:

```bash
curl -H "Authorization: Bearer your-token" http://localhost:8000/mcp/tools
```

### Tool Discovery

```bash
# Get all available tools
curl -H "Authorization: Bearer your-token" \
  http://localhost:8000/mcp/tools

# Filter by task type
curl -H "Authorization: Bearer your-token" \
  "http://localhost:8000/mcp/tools?task-type=container-ops"
```

### Container Operations

```bash
# List containers
curl -H "Authorization: Bearer your-token" \
  http://localhost:8000/containers

# Create container
curl -X POST -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{"image": "nginx:alpine", "name": "web"}' \
  http://localhost:8000/containers
```

See `specs/001-http-based-docker/contracts/` for complete API documentation and OpenAPI schemas.

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/unit/test_docker_client.py
```

### Code Quality

```bash
# Lint and format
poetry run ruff check .
poetry run ruff format .

# Type checking
poetry run mypy app/

# Security scanning
poetry run bandit -r app/
```

## Remote Docker Access

### TLS Connection

```bash
export DOCKER_HOST="tcp://remote-host:2376"
export DOCKER_TLS_VERIFY="1"
export DOCKER_CERT_PATH="/path/to/certs"
```

### SSH Connection

```bash
export DOCKER_HOST="ssh://user@remote-host"
```

### Tunnel with Tailscale

```bash
# Connect via Tailscale private network
export DOCKER_HOST="tcp://100.x.y.z:2376"
```

See `docs/dependencies/tls.md`, `docs/dependencies/tailscale.md`, `docs/dependencies/ngrok.md` for detailed setup.

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for planned features and improvements.

**Coming in v0.3.0:**
- 🔒 Integrated Tailscale/ngrok support for secure remote access
- 🔄 Automatic token rotation
- 📊 Authentication monitoring and alerting
- 📈 Prometheus metrics

## Documentation

- **Security**: `SECURITY.md` - Security policy, best practices, and vulnerability reporting
- **Security Audit**: `SECURITY-AUDIT-REPORT.md` - Comprehensive security scan results (Semgrep validated)
- **Roadmap**: `ROADMAP.md` - Planned features and release timeline
- **Changelog**: `CHANGELOG.md` - Version history and changes
- **MCP Client Setup**: `docs/MCP-CLIENT-SETUP.md` - Complete guide for configuring MCP clients (Claude Desktop, claude-code, etc.)
- **Quick Reference**: `docs/MCP-QUICK-REFERENCE.md` - Command cheat sheet and common workflows
- **JSON-RPC Protocol**: `docs/MCP-JSON-RPC-USAGE.md` - Detailed protocol documentation
- **Client Config Schema**: `docs/mcp-client-config.schema.json` - JSON schema for validation
- **Dependencies**: `docs/dependencies/` - Reference stubs for Docker SDK, FastAPI, Pydantic, Uvicorn, Compose, Swarm, TLS, tunneling
- **Architecture**: `specs/001-http-based-docker/plan.md` - Complete architecture and design decisions
- **API Contracts**: `specs/001-http-based-docker/contracts/` - OpenAPI schemas for all endpoints
- **Quickstart**: `specs/001-http-based-docker/quickstart.md` - Detailed server setup and testing guide

## Architecture

- **FastAPI**: HTTP framework with async support
- **docker-py**: Docker SDK for Python
- **Pydantic**: Data validation and schema generation
- **Tool Gating**: Pluggable filter chain (TaskType → Resource → Security)
- **Intent Classification**: Keyword-based automatic task-type detection

See `specs/001-http-based-docker/plan.md` for complete architecture documentation.

## Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Open an issue with reproduction steps
2. **Suggest Features**: Have an idea? Check `ROADMAP.md` or propose new features
3. **Improve Documentation**: Clarify setup steps, add examples, fix typos
4. **Submit Pull Requests**: Fix bugs, add features from the roadmap
5. **Security**: Report vulnerabilities privately (see `SECURITY.md`)

**Current Focus Areas** (see `ROADMAP.md`):
- Tailscale/ngrok integration for secure remote access
- Token rotation mechanisms
- Authentication monitoring and alerting
- Prometheus metrics

## License

MIT

---

**Status**: ✅ Production-ready | Semgrep validated | Security audited  
**Version**: 0.2.0 | **Next**: v0.3.0 with advanced features
