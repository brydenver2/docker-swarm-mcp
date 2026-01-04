"""Docker Swarm service functions"""
from typing import Any

from app.docker_client import DockerClient
from app.utils.retry import retry_read, retry_write


@retry_read(operation_name="list_services")
async def list_services(docker_client: DockerClient, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List Docker Swarm services"""
    return docker_client.list_services()


@retry_write(operation_name="scale_service")
async def scale_service(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Scale a Docker Swarm service"""
    service_name = params.get("name")
    replicas = params.get("replicas")

    if not service_name or replicas is None:
        raise ValueError("Missing required parameters: name, replicas")

    return docker_client.scale_service(service_name, replicas)


@retry_write(operation_name="remove_service")
async def remove_service(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Remove a Docker Swarm service"""
    service_name = params.get("name")
    if not service_name:
        raise ValueError("Missing required parameter: name")
    docker_client.remove_service(service_name)
    return {}


@retry_read(operation_name="get_service_logs")
async def get_service_logs(docker_client: DockerClient, params: dict[str, Any]) -> str:
    """Retrieve logs for a Docker Swarm service."""
    service_name = params.get("name")
    tail = params.get("tail", 100)
    since = params.get("since")
    follow = params.get("follow", False)

    if not service_name:
        raise ValueError("Missing required parameter: name")

    # Same retry semantics as container logs: only retry when not following
    if follow:
        return docker_client.get_service_logs(service_name, tail=tail, since=since, follow=follow)
    return docker_client.get_service_logs(service_name, tail=tail, since=since, follow=False)
