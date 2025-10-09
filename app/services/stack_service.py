"""Stack service functions"""
from typing import Any

from app.docker_client import DockerClient


async def deploy_compose(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Deploy a Docker Compose stack"""
    project_name = params.get("project_name")
    compose_yaml = params.get("compose_yaml")
    force_recreate = params.get("force_recreate", False)

    if not project_name or not compose_yaml:
        raise ValueError("Missing required parameters: project_name, compose_yaml")

    return docker_client.deploy_compose(project_name, compose_yaml, force_recreate)


async def list_stacks(docker_client: DockerClient, params: dict[str, Any]) -> list[dict[str, Any]]:
    """List Docker Compose stacks"""
    return docker_client.list_stacks()


async def remove_compose(docker_client: DockerClient, params: dict[str, Any]) -> None:
    """Remove a Docker Compose stack"""
    project_name = params.get("project_name")
    if not project_name:
        raise ValueError("Missing required parameter: project_name")
    docker_client.remove_compose(project_name)
    return {}
