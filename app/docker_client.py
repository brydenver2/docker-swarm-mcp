import logging
from typing import Any, Optional
from datetime import datetime

import docker
from docker.errors import DockerException, NotFound, APIError
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)


class DockerClient:
    def __init__(self) -> None:
        try:
            self.client = docker.from_env()
            self.client.ping()
            logger.info("Docker client initialized successfully", extra={"docker_host": settings.DOCKER_HOST})
        except DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise RuntimeError(f"Docker engine unreachable: {e}")
        
        self._is_swarm_cache: bool | None = None
    
    def _is_swarm(self) -> bool:
        if self._is_swarm_cache is None:
            info = self.client.info()
            swarm_info = info.get("Swarm", {})
            self._is_swarm_cache = swarm_info.get("LocalNodeState") == "active"
        return self._is_swarm_cache
    
    def ping(self) -> bool:
        return self.client.ping()
    
    def get_info(self) -> dict[str, Any]:
        return self.client.info()
    
    def list_containers(self, all: bool = False, filters: Optional[dict] = None) -> list[dict[str, Any]]:
        try:
            containers = self.client.containers.list(all=all, filters=filters)
            result = []
            for container in containers:
                ports = []
                for private_port, bindings in (container.attrs.get("NetworkSettings", {}).get("Ports") or {}).items():
                    port_num = int(private_port.split("/")[0])
                    port_type = private_port.split("/")[1] if "/" in private_port else "tcp"
                    if bindings:
                        for binding in bindings:
                            ports.append({
                                "private_port": port_num,
                                "public_port": int(binding["HostPort"]) if binding.get("HostPort") else None,
                                "type": port_type
                            })
                    else:
                        ports.append({
                            "private_port": port_num,
                            "public_port": None,
                            "type": port_type
                        })
                
                result.append({
                    "id": container.short_id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else container.image.short_id,
                    "created": datetime.fromisoformat(container.attrs["Created"].replace("Z", "+00:00")),
                    "ports": ports
                })
            return result
        except APIError as e:
            logger.error(f"Docker API error listing containers: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing containers: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    
    def create_container(self, config: dict[str, Any]) -> dict[str, Any]:
        try:
            container = self.client.containers.create(
                image=config["image"],
                name=config.get("name"),
                environment=config.get("environment"),
                ports=config.get("ports"),
                volumes=config.get("volumes"),
                restart_policy={"Name": config.get("restart_policy", "no")}
            )
            return {
                "id": container.short_id,
                "name": container.name,
                "status": container.status,
                "image": config["image"],
                "created": datetime.now()
            }
        except NotFound as e:
            logger.error(f"Image not found: {e}")
            raise HTTPException(status_code=404, detail=f"Image not found: {str(e)}")
        except APIError as e:
            if e.status_code == 409:
                raise HTTPException(status_code=409, detail=f"Container name conflict: {str(e)}")
            logger.error(f"Docker API error creating container: {e}")
            raise HTTPException(status_code=400, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error creating container: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    
    def start_container(self, container_id: str) -> None:
        try:
            container = self.client.containers.get(container_id)
            container.start()
        except NotFound:
            raise HTTPException(status_code=404, detail="Container not found")
        except APIError as e:
            logger.error(f"Docker API error starting container: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error starting container: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    
    def stop_container(self, container_id: str, timeout: int = 10) -> None:
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=timeout)
        except NotFound:
            raise HTTPException(status_code=404, detail="Container not found")
        except APIError as e:
            logger.error(f"Docker API error stopping container: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error stopping container: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    
    def remove_container(self, container_id: str, force: bool = False) -> None:
        try:
            container = self.client.containers.get(container_id)
            container.remove(force=force)
        except NotFound:
            raise HTTPException(status_code=404, detail="Container not found")
        except APIError as e:
            logger.error(f"Docker API error removing container: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing container: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")
    
    def get_logs(self, container_id: str, tail: int = 100, since: Optional[str] = None, follow: bool = False) -> str:
        try:
            container = self.client.containers.get(container_id)
            logs = container.logs(tail=tail, since=since, follow=follow, stream=False)
            return logs.decode("utf-8") if isinstance(logs, bytes) else logs
        except NotFound:
            raise HTTPException(status_code=404, detail="Container not found")
        except APIError as e:
            logger.error(f"Docker API error getting logs: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error getting logs: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")


_docker_client_instance: DockerClient | None = None


def get_docker_client() -> DockerClient:
    global _docker_client_instance
    if _docker_client_instance is None:
        _docker_client_instance = DockerClient()
    return _docker_client_instance
