import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.auth import verify_token
from app.core.constants import APP_VERSION
from app.schemas.system import PingResponse, SystemInfo

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/ping", response_model=PingResponse, dependencies=[Depends(verify_token)])
async def ping_docker(request: Request) -> PingResponse:
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
