"""System service functions"""
from typing import Any

from app.core.constants import APP_VERSION
from app.docker_client import DockerClient
from app.utils.retry import retry_read


@retry_read(operation_name="ping")
async def ping(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Ping Docker engine to verify connectivity"""
    is_alive = docker_client.ping()

    if is_alive:
        return {"status": "ok", "message": "Docker engine is reachable"}
    else:
        raise RuntimeError("Docker engine ping failed")


@retry_read(operation_name="info")
async def info(docker_client: DockerClient, params: dict[str, Any]) -> dict[str, Any]:
    """Get Docker system information"""
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

