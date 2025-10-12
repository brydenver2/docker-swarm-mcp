"""Volume service functions"""
from typing import Any

from app.docker_client import DockerClient
from app.utils.retry import retry_read, retry_write


@retry_read(operation_name="list_volumes")
async def list_volumes(docker_client: DockerClient, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List Docker volumes"""
    return docker_client.list_volumes()


@retry_write(operation_name="create_volume")
async def create_volume(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Create a Docker volume"""
    return docker_client.create_volume(params)


@retry_write(operation_name="remove_volume")
async def remove_volume(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Remove a Docker volume"""
    volume_name = params.get("name")
    if not volume_name:
        raise ValueError("Missing required parameter: name")
    docker_client.remove_volume(volume_name)
    return {}
