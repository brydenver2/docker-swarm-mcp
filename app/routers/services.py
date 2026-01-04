from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app.core.auth import verify_token
from app.docker_client import DockerClient, get_docker_client
from app.schemas.services import ServiceResponse, ServiceScaleRequest
from app.services import service_service

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_model=list[ServiceResponse])
async def list_services(
    _: Annotated[bool, Depends(verify_token)],
    docker: Annotated[DockerClient, Depends(get_docker_client)]
):
    services = docker.list_services()
    return services


@router.post("/{name}/scale", response_model=ServiceResponse)
async def scale_service(
    name: str,
    request: ServiceScaleRequest,
    _: Annotated[bool, Depends(verify_token)],
    docker: Annotated[DockerClient, Depends(get_docker_client)]
):
    result = docker.scale_service(name, request.replicas)
    return result


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_service(
    name: str,
    _: Annotated[bool, Depends(verify_token)],
    docker: Annotated[DockerClient, Depends(get_docker_client)]
):
    docker.remove_service(name)


@router.get("/{name}/logs", response_class=Response)
async def get_service_logs(
    name: str,
    _: Annotated[bool, Depends(verify_token)],
    docker: Annotated[DockerClient, Depends(get_docker_client)],
    tail: int = Query(100, ge=1, le=1000, description="Number of lines from end of logs"),
    since: Optional[str] = Query(None, description="RFC3339 timestamp or Unix seconds"),
    follow: bool = Query(False, description="Stream logs (SSE transport only)")
):
    logs = await service_service.get_service_logs(
        docker,
        {"name": name, "tail": tail, "since": since, "follow": follow}
    )
    return Response(content=logs, media_type="text/plain")
