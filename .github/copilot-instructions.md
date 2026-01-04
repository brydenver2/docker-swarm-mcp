# GitHub Copilot Instructions for Docker Swarm MCP

## Project Overview
This repository provides a production-ready MCP (Model Context Protocol) server for Docker Swarm. It is designed to offer full Docker Swarm control with minimal context overhead, focusing on services, stacks, configs, and secrets.

## Architecture
- **Core Frameworks**: Python 3.12, FastAPI, Uvicorn, Pydantic
- **Docker Integration**: docker-py SDK for Swarm management
- **Security**: Bearer token authentication, TLS support, and Docker secrets
- **Networking**: Overlay networks for service communication, Traefik integration for reverse proxy and SSL termination
- **Context Filtering**: Tools are dynamically gated based on task requirements

## Critical Workflows
- **Run the MCP Server**:
  ```bash
  docker stack deploy -c docker-swarm-mcp.yml mcp-server
  docker service logs mcp-server_docker-mcp
  ```
- **Set Up Secrets**:
  ```bash
  openssl rand -base64 32 | docker secret create mcp_token -
  ```
- **Test the Server**:
  ```bash
  curl -f http://localhost:8000/mcp/health
  ```
- **Run Tests**:
  ```bash
  pytest
  ```
- **Lint the Codebase**:
  ```bash
  ruff check .
  ```
- **Type Checking** (optional):
  ```bash
  mypy app || true
  ```

## Project Conventions
- **Compose Files**: Use `docker-compose.override.yaml.example` as a template for local overrides.
- **Secrets**: Store sensitive data in Docker secrets (e.g., `MCP_ACCESS_TOKEN_FILE`).
- **Configs**: Use external Docker configs for service-specific configurations.
- **Healthchecks**: Defined in `docker-compose.yaml` to ensure service reliability.
- **Placement Constraints**: Services are constrained to manager nodes for Docker socket access.
- **Traefik Labels**: Used for routing and SSL configuration.

## Key Files
- `docker-compose.yaml`: Main stack configuration
- `Dockerfile`: Base image for the MCP server
- `app/`: Core application logic, including FastAPI endpoints and Docker Swarm integration
  - `app/core/`: Authentication, logging, and configuration utilities
  - `app/routers/`: API endpoints for managing containers, networks, services, stacks, and volumes
  - `app/services/`: Business logic for interacting with Docker Swarm
- `tests/`: Unit tests for core functionality
- `README.md`: Comprehensive setup and usage instructions

## Examples
- **Basic Stack Deployment**:
  ```yaml
  services:
    docker-mcp:
      image: ghcr.io/khaentertainment/docker-swarm-mcp:latest
      environment:
        - MCP_ACCESS_TOKEN=${MCP_ACCESS_TOKEN:-change-me-to-secure-token}
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock:ro
      ports:
        - "8000:8000"
      deploy:
        replicas: 1
        placement:
          constraints:
            - node.role == manager
  ```
- **Traefik Integration**:
  ```yaml
  labels:
    - "traefik.enable=true"
    - "traefik.http.routers.mcp.rule=Host(`mcp.yourdomain.com`)"
    - "traefik.http.routers.mcp.entrypoints=websecure"
    - "traefik.http.routers.mcp.tls=true"
  ```

## Notes
- Avoid committing secrets to the repository. Use environment variables or Docker secrets.
- Follow the Python 3.12 conventions and linting rules defined in the project.
- Refer to `AGENTS.md` for additional context on tool gating and context filtering.