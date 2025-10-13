from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.auth import verify_token
from app.docker_client import DockerClient, get_docker_client
from app.schemas.services import ServiceResponse, ServiceScaleRequest

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
