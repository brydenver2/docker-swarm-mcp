from typing import Any
from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.constants import APP_VERSION, MCP_ROUTES

router = APIRouter()


@router.get("/health")
async def health_check(request: Request) -> dict[str, Any]:
    """
    Perform a basic health check that verifies Docker reachability and reports service status.
    
    Parameters:
        request (Request): FastAPI request used to access application state (expects `request.app.state.docker_client`).
    
    Returns:
        dict: A mapping with:
            - status (str): "healthy" if Docker is reachable, "degraded" otherwise.
            - docker_reachable (bool): Whether the Docker client responded to a ping.
            - version (str): Application version (APP_VERSION).
    """
    try:
        docker_client = request.app.state.docker_client
        docker_reachable = docker_client.ping()
    except Exception:
        docker_reachable = False

    return {
        "status": "healthy" if docker_reachable else "degraded",
        "docker_reachable": docker_reachable,
        "version": APP_VERSION
    }


@router.get("/healthz")
async def detailed_health_check(request: Request) -> dict[str, Any]:
    """
    Provide a detailed health status for the service, reflecting MCP readiness, Docker reachability, authentication setup, and available tools.
    
    Returns:
        dict: Health report with keys:
            - status (str): One of "healthy", "degraded", or "unhealthy".
            - mcp_ready (bool): Whether the MCP server and its tool registry appear ready.
            - docker_reachable (bool): Whether the configured Docker client responded to a ping.
            - auth_configured (bool): Whether MCP authentication settings are configured.
            - tool_count (int): Number of tools discovered in the MCP tool registry.
            - protocol_version (str): MCP protocol version from configuration.
            - version (str): Application version.
            - endpoints (dict, optional): Exposed MCP route metadata (only when EXPOSE_ENDPOINTS_IN_HEALTHZ=true).
    """
    try:
        docker_client = request.app.state.docker_client
        docker_reachable = docker_client.ping()
    except Exception:
        docker_reachable = False

    # Check MCP server components
    mcp_ready = True
    tool_count = 0
    auth_configured = False

    try:
        # Check if MCP server is initialized
        if hasattr(request.app.state, 'mcp_server'):
            mcp_server = request.app.state.mcp_server
            if hasattr(mcp_server, 'tool_registry'):
                tool_count = len(mcp_server.tool_registry.get_all_tools())
            else:
                mcp_ready = False
        else:
            mcp_ready = False

        # Check authentication configuration
        if settings.MCP_ACCESS_TOKEN or settings.TOKEN_SCOPES:
            auth_configured = True

    except Exception:
        mcp_ready = False

    # Overall status determination
    if docker_reachable and mcp_ready and auth_configured and tool_count > 0:
        status = "healthy"
    elif docker_reachable and mcp_ready:
        status = "degraded"  # Missing auth or tools
    else:
        status = "unhealthy"

    response_data = {
        "status": status,
        "mcp_ready": mcp_ready,
        "docker_reachable": docker_reachable,
        "auth_configured": auth_configured,
        "tool_count": tool_count,
        "protocol_version": settings.MCP_PROTOCOL_VERSION,
        "version": APP_VERSION
    }
    
    # Only include endpoints when explicitly enabled via feature flag
    if settings.EXPOSE_ENDPOINTS_IN_HEALTHZ:
        response_data["endpoints"] = MCP_ROUTES
    
    return response_data