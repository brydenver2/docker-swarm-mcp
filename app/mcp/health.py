from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.constants import APP_VERSION, MCP_ROUTES

router = APIRouter()


@router.get("/health")
async def health_check(request: Request) -> dict[str, str | bool | int]:
    """Basic health check endpoint"""
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
async def detailed_health_check(request: Request) -> dict[str, str | bool | int]:
    """
    Detailed health check endpoint that reflects MCP readiness

    Returns comprehensive health status including:
    - MCP server readiness
    - Tool availability
    - Authentication configuration
    - Protocol version
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

    return {
        "status": status,
        "mcp_ready": mcp_ready,
        "docker_reachable": docker_reachable,
        "auth_configured": auth_configured,
        "tool_count": tool_count,
        "protocol_version": settings.MCP_PROTOCOL_VERSION,
        "version": APP_VERSION,
        "endpoints": MCP_ROUTES
    }
