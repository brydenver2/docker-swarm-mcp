import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.auth import verify_token
from app.core.constants import APP_VERSION
from app.schemas.system import PingResponse, SystemInfo

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ping", response_model=PingResponse, dependencies=[Depends(verify_token)])
async def ping_docker(request: Request) -> PingResponse:
    """
    Check whether the Docker engine is reachable.
    
    Parameters:
        request (Request): FastAPI request whose `app.state.docker_client` is used to perform the ping.
    
    Returns:
        PingResponse: `PingResponse(status="ok", message="Docker engine is reachable")` when the Docker engine responds.
    
    Raises:
        HTTPException: 500 with detail "Docker engine ping failed" if ping returns falsy, or 500 with detail "Docker engine is unreachable" on unexpected errors.
    """
    try:
        docker_client = request.app.state.docker_client
        is_alive = docker_client.ping()

        if is_alive:
            return PingResponse(status="ok", message="Docker engine is reachable")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Docker engine ping failed"
            )
    except Exception as e:
        logger.error(f"Docker ping failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Docker engine is unreachable"
        )


@router.get("/info", response_model=SystemInfo, dependencies=[Depends(verify_token)])
async def get_system_info(request: Request) -> SystemInfo:
    """
    Return system information about the running Docker environment.
    
    Reads the Docker client from `request.app.state.docker_client`, queries the Docker engine for runtime info, and returns a SystemInfo populated with the application version, operating system, CPU architecture, and Docker server version.
    
    Parameters:
        request (Request): FastAPI request whose `app.state.docker_client` provides the Docker client.
    
    Returns:
        SystemInfo: Object with fields:
            - version: application version (APP_VERSION)
            - os: operating system string or "unknown" if unavailable
            - architecture: CPU architecture string or "unknown" if unavailable
            - docker_version: Docker server version string or "unknown" if unavailable
    
    Raises:
        HTTPException: with status 500 if system information cannot be retrieved.
    """
    try:
        docker_client = request.app.state.docker_client
        info = docker_client.get_info()

        return SystemInfo(
            version=APP_VERSION,
            os=info.get("OperatingSystem", "unknown"),
            architecture=info.get("Architecture", "unknown"),
            docker_version=info.get("ServerVersion", "unknown")
        )
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system information"
        )