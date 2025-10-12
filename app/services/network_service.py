"""Network service functions"""
from typing import Any

from app.docker_client import DockerClient
from app.utils.retry import retry_read, retry_write


@retry_read(operation_name="list_networks")
async def list_networks(docker_client: DockerClient, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List Docker networks"""
    return docker_client.list_networks()


@retry_write(operation_name="create_network")
async def create_network(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Create a Docker network"""
    return docker_client.create_network(params)


@retry_write(operation_name="remove_network")
async def remove_network(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Remove a Docker network"""
    network_id = params.get("id")
    if not network_id:
        raise ValueError("Missing required parameter: id")
    docker_client.remove_network(network_id)
    return {}
