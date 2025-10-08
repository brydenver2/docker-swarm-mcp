# Docker MCP Server

HTTP-based Model Context Protocol (MCP) server for Docker operations with context-preserving tool gating.

## Features

- **Secure Remote Access**: Access token authentication for MCP clients
- **Context-Efficient Tool Discovery**: Tool gating reduces context from 45K+ to ≤5K tokens
- **Docker Operations**: Containers, Compose stacks, Swarm services, networks, volumes, system info
- **Multi-Transport Support**: HTTP (default) and SSE fallback
- **Remote Docker Engines**: Local socket, TLS, and SSH connections

## Quick Start

### Prerequisites

- Python 3.12+
- Poetry
- Docker Engine 24+

### Installation

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

### Docker Setup

```bash
# Build the container
docker build -t docker-mcp-server .

# Run with Docker Compose
docker-compose up -d
```

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

See `docs/` for complete API documentation.

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

See `docs/dependencies/tls.md`, `docs/dependencies/tailscale.md` for detailed setup.

## Architecture

- **FastAPI**: HTTP framework with async support
- **docker-py**: Docker SDK for Python
- **Pydantic**: Data validation and schema generation
- **Tool Gating**: Pluggable filter chain (TaskType → Resource → Security)

See `specs/001-http-based-docker/plan.md` for complete architecture documentation.

## License

MIT
