import json
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app.core.auth import verify_token
from app.docker_client import DockerClient, get_docker_client
from app.schemas.containers import ContainerCreateRequest, ContainerResponse, ContainerSummary
from app.services import container_service

router = APIRouter()


@router.get("/containers", response_model=list[ContainerSummary], dependencies=[Depends(verify_token)])
async def list_containers(
    all: bool = Query(False, description="Include stopped containers"),
    filters: Optional[str] = Query(None, description="JSON-encoded filters"),
    docker_client: DockerClient = Depends(get_docker_client)
):
    """List containers using service layer"""
    filters_dict = json.loads(filters) if filters else None
    params = {"all": all}
    if filters_dict:
        params["filters"] = filters_dict

    containers = await container_service.list_containers(docker_client, params)
    return containers


@router.post("/containers", response_model=ContainerResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def create_container(
    request: ContainerCreateRequest,
    docker_client: DockerClient = Depends(get_docker_client)
):
    """Create container using service layer"""
    container = await container_service.create_container(docker_client, request.model_dump())
    return container


@router.post("/containers/{id}/start", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
async def start_container(
    id: str,
    docker_client: DockerClient = Depends(get_docker_client)
):
    """Start container using service layer"""
    await container_service.start_container(docker_client, {"id": id})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/containers/{id}/stop", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
async def stop_container(
    id: str,
    timeout: int = Query(10, description="Seconds to wait before killing"),
    docker_client: DockerClient = Depends(get_docker_client)
):
    """Stop container using service layer"""
    await container_service.stop_container(docker_client, {"id": id, "timeout": timeout})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/containers/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
async def remove_container(
    id: str,
    force: bool = Query(False, description="Force removal of running container"),
    docker_client: DockerClient = Depends(get_docker_client)
):
    """Remove container using service layer"""
    await container_service.remove_container(docker_client, {"id": id, "force": force})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/containers/{id}/logs", response_class=Response, dependencies=[Depends(verify_token)])
async def get_container_logs(
    id: str,
    tail: int = Query(100, description="Number of lines from end of logs"),
    since: Optional[str] = Query(None, description="RFC3339 timestamp to filter logs"),
    follow: bool = Query(False, description="Stream logs (SSE transport only)"),
    docker_client: DockerClient = Depends(get_docker_client)
):
    """Get container logs using service layer"""
    logs = await container_service.get_logs(
        docker_client,
        {"id": id, "tail": tail, "since": since, "follow": follow}
    )
    return Response(content=logs, media_type="text/plain")
