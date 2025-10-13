from fastapi import APIRouter, Depends, Response, status

from app.core.auth import verify_token
from app.docker_client import DockerClient, get_docker_client
from app.schemas.networks import NetworkCreateRequest, NetworkResponse

router = APIRouter()


@router.get("/networks", response_model=list[NetworkResponse], dependencies=[Depends(verify_token)])
async def list_networks(
    docker_client: DockerClient = Depends(get_docker_client)
):
    networks = docker_client.list_networks()
    return networks


@router.post("/networks", response_model=NetworkResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
async def create_network(
    request: NetworkCreateRequest,
    docker_client: DockerClient = Depends(get_docker_client)
):
    network = docker_client.create_network(request.model_dump())
    return network


@router.delete("/networks/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
async def remove_network(
    id: str,
    docker_client: DockerClient = Depends(get_docker_client)
):
    docker_client.remove_network(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
