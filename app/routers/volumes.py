from fastapi import APIRouter, Depends, Response, status

from app.core.auth import verify_token
from app.docker_client import get_docker_client, DockerClient
from app.schemas.volumes import VolumeCreateRequest, VolumeResponse

router = APIRouter()


@router.get("/volumes", response_model=list[VolumeResponse], dependencies=[Depends(verify_token)])
async def list_volumes(
    docker_client: DockerClient = Depends(get_docker_client)
):
    volumes = docker_client.list_volumes()
    return volumes


@router.post("/volumes", response_model=VolumeResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def create_volume(
    request: VolumeCreateRequest,
    docker_client: DockerClient = Depends(get_docker_client)
):
    volume = docker_client.create_volume(request.model_dump())
    return volume


@router.delete("/volumes/{name}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
async def remove_volume(
    name: str,
    docker_client: DockerClient = Depends(get_docker_client)
):
    docker_client.remove_volume(name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
