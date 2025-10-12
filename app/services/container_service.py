"""Container service functions"""
from typing import Any

from app.docker_client import DockerClient
from app.utils.retry import retry_read, retry_write, retry_none


@retry_read(operation_name="list_containers")
async def list_containers(docker_client: DockerClient, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List Docker containers"""
    all_containers = params.get("all", False)
    filters = params.get("filters")
    return docker_client.list_containers(all=all_containers, filters=filters)


@retry_write(operation_name="create_container")
async def create_container(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Create a Docker container"""
    return docker_client.create_container(params)


@retry_write(operation_name="start_container")
async def start_container(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Start a Docker container"""
    container_id = params.get("id")
    if not container_id:
        raise ValueError("Missing required parameter: id")
    docker_client.start_container(container_id)
    return {}


@retry_write(operation_name="stop_container")
async def stop_container(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Stop a Docker container"""
    container_id = params.get("id")
    timeout = params.get("timeout", 10)
    if not container_id:
        raise ValueError("Missing required parameter: id")
    docker_client.stop_container(container_id, timeout=timeout)
    return {}


@retry_write(operation_name="remove_container")
async def remove_container(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Remove a Docker container"""
    container_id = params.get("id")
    force = params.get("force", False)
    if not container_id:
        raise ValueError("Missing required parameter: id")
    docker_client.remove_container(container_id, force=force)
    return {}


@retry_read(operation_name="get_logs")
async def get_logs(docker_client: DockerClient, params: dict[str, Any]) -> str:
    """Get Docker container logs"""
    container_id = params.get("id")
    tail = params.get("tail", 100)
    since = params.get("since")
    follow = params.get("follow", False)
    if not container_id:
        raise ValueError("Missing required parameter: id")
    
    # Only retry if not following (following is not idempotent)
    if follow:
        return docker_client.get_logs(container_id, tail=tail, since=since, follow=follow)
    else:
        return docker_client.get_logs(container_id, tail=tail, since=since, follow=False)
