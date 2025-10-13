"""System service functions"""
from typing import Any

from app.core.constants import APP_VERSION
from app.docker_client import DockerClient
from app.utils.retry import retry_read


@retry_read(operation_name="ping")
async def ping(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """
    Check connectivity to the Docker engine.
    
    Parameters:
        params (dict[str, Any]): Optional parameters (reserved for future use).
    
    Returns:
        dict[str, Any]: A status object with keys `status` and `message` describing the ping result.
    
    Raises:
        RuntimeError: If the Docker engine ping fails.
    """
    is_alive = docker_client.ping()

    if is_alive:
        return {"status": "ok", "message": "Docker engine is reachable"}
    else:
        raise RuntimeError("Docker engine ping failed")


@retry_read(operation_name="info")
async def info(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """
    Return a summary of Docker system information.
    
    Parameters:
        docker_client (DockerClient): Client used to query the Docker engine for system information.
        params (dict[str, Any]): Additional parameters (currently unused).
    
    Returns:
        dict[str, Any]: A mapping with the following keys:
            - version: Application version.
            - os: Operating system reported by Docker or "unknown".
            - architecture: Architecture reported by Docker or "unknown".
            - docker_version: Docker server version or "unknown".
            - swarm_status: Swarm local node state or "inactive".
            - containers: Number of containers (integer, 0 if missing).
            - images: Number of images (integer, 0 if missing).
    """
    docker_info = docker_client.get_info()

    return {
        "version": APP_VERSION,
        "os": docker_info.get("OperatingSystem", "unknown"),
        "architecture": docker_info.get("Architecture", "unknown"),
        "docker_version": docker_info.get("ServerVersion", "unknown"),
        "swarm_status": docker_info.get("Swarm", {}).get("LocalNodeState", "inactive"),
        "containers": docker_info.get("Containers", 0),
        "images": docker_info.get("Images", 0)
    }
