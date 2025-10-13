import logging
from datetime import datetime
from typing import Any, Optional

import docker
import docker.tls
import yaml
from docker.errors import APIError, DockerException, NotFound
from docker.types import ServiceMode
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger(__name__)


class DockerClient:
    def __init__(self) -> None:
        """
        Initialize Docker client with explicit DOCKER_HOST/TLS/SSH semantics

        Honors environment variables:
        - DOCKER_HOST: Docker daemon socket (unix://, tcp://, ssh://)
        - DOCKER_TLS_VERIFY: Enable TLS verification
        - DOCKER_CERT_PATH: Path to TLS certificates (ca.pem, cert.pem, key.pem)
        """
        try:
            # Construct client based on explicit configuration
            if settings.DOCKER_HOST and settings.DOCKER_HOST != "unix:///var/run/docker.sock":
                # Explicit DOCKER_HOST configuration
                client_kwargs: dict[str, Any] = {"base_url": settings.DOCKER_HOST}

                # Handle TLS configuration
                if settings.DOCKER_TLS_VERIFY and settings.DOCKER_CERT_PATH:
                    tls_config = docker.tls.TLSConfig(
                        client_cert=(
                            f"{settings.DOCKER_CERT_PATH}/cert.pem",
                            f"{settings.DOCKER_CERT_PATH}/key.pem"
                        ),
                        ca_cert=f"{settings.DOCKER_CERT_PATH}/ca.pem",
                        verify=True
                    )
                    client_kwargs["tls"] = tls_config
                    logger.info(
                        "Docker client initialized with TLS",
                        extra={
                            "docker_host": settings.DOCKER_HOST,
                            "tls_verify": True,
                            "cert_path": settings.DOCKER_CERT_PATH
                        }
                    )
                elif settings.DOCKER_HOST.startswith("tcp://") and settings.DOCKER_TLS_VERIFY:
                    logger.warning(
                        "DOCKER_TLS_VERIFY=1 but DOCKER_CERT_PATH not set, "
                        "falling back to unverified TLS"
                    )

                self.client = docker.DockerClient(**client_kwargs)
                logger.info(
                    "Docker client initialized with explicit configuration",
                    extra={
                        "docker_host": settings.DOCKER_HOST,
                        "mode": "tcp+TLS" if settings.DOCKER_TLS_VERIFY else (
                            "ssh" if settings.DOCKER_HOST.startswith("ssh://") else "tcp"
                        )
                    }
                )
            else:
                # Fallback to from_env() for default Unix socket
                self.client = docker.from_env()
                logger.info(
                    "Docker client initialized from environment",
                    extra={"docker_host": settings.DOCKER_HOST, "mode": "unix"}
                )

            # Verify connection
            self.client.ping()

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

                # Convert datetime to ISO string for JSON serialization
                created_dt = datetime.fromisoformat(container.attrs["Created"].replace("Z", "+00:00"))

                result.append({
                    "id": container.short_id,
                    "name": container.name,
                    "status": container.status,
                    "image": container.image.tags[0] if container.image.tags else container.image.short_id,
                    "created": created_dt.isoformat(),
                    "ports": ports
                })
            return result
        except APIError as e:
            logger.error(f"Docker API error listing stacks: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing stacks: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def remove_compose(self, project_name: str) -> None:
        if self._is_swarm():
            self._remove_compose_swarm(project_name)
        else:
            self._remove_compose_standalone(project_name)

    def _remove_compose_swarm(self, project_name: str) -> None:
        try:
            services = self.client.services.list(filters={"label": f"com.docker.stack.namespace={project_name}"})

            if not services:
                raise HTTPException(status_code=404, detail=f"Stack {project_name} not found")

            for service in services:
                service.remove()
        except HTTPException:
            raise
        except APIError as e:
            logger.error(f"Docker API error removing compose stack: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing compose stack: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def _remove_compose_standalone(self, project_name: str) -> None:
        try:
            containers = self.client.containers.list(all=True, filters={"label": f"com.docker.compose.project={project_name}"})

            if not containers:
                raise HTTPException(status_code=404, detail=f"Stack {project_name} not found")

            for container in containers:
                container.remove(force=True)
        except HTTPException:
            raise
        except APIError as e:
            logger.error(f"Docker API error removing compose stack: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing compose stack: {e}")
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
                "created": datetime.now().isoformat()
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

    def deploy_compose(self, project_name: str, compose_yaml: str, force_recreate: bool = False) -> dict[str, Any]:
        try:
            compose_dict = yaml.safe_load(compose_yaml)
        except yaml.YAMLError as e:
            raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")

        version = compose_dict.get("version", "")
        if not version.startswith("3"):
            raise HTTPException(status_code=400, detail="Compose version must be 3 or higher")

        services = compose_dict.get("services", {})
        if not services:
            raise HTTPException(status_code=400, detail="No services defined in Compose YAML")

        if self._is_swarm():
            return self._deploy_compose_swarm(project_name, services, force_recreate)
        else:
            return self._deploy_compose_standalone(project_name, services, force_recreate)

    def _deploy_compose_swarm(self, project_name: str, services: dict[str, Any], force_recreate: bool) -> dict[str, Any]:
        try:
            created_services = []

            for service_name, service_config in services.items():
                full_service_name = f"{project_name}_{service_name}"

                existing_services = self.client.services.list(filters={"name": full_service_name})
                if existing_services and force_recreate:
                    for svc in existing_services:
                        svc.remove()
                elif existing_services:
                    created_services.append(full_service_name)
                    continue

                image = service_config.get("image")
                if not image:
                    raise HTTPException(status_code=400, detail=f"Service {service_name} missing image")

                env = service_config.get("environment", {})
                if isinstance(env, list):
                    env_dict = {}
                    for item in env:
                        if "=" in item:
                            k, v = item.split("=", 1)
                            env_dict[k] = v
                    env = env_dict

                service = self.client.services.create(
                    image=image,
                    name=full_service_name,
                    env=env,
                    labels={"com.docker.stack.namespace": project_name},
                    mode=ServiceMode("replicated", replicas=service_config.get("replicas", 1))
                )
                created_services.append(full_service_name)

            return {
                "project_name": project_name,
                "services": created_services,
                "mode": "swarm",
                "created": datetime.now().isoformat()
            }
        except APIError as e:
            logger.error(f"Docker API error deploying compose stack: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error deploying compose stack: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def _deploy_compose_standalone(self, project_name: str, services: dict[str, Any], force_recreate: bool) -> dict[str, Any]:
        try:
            created_containers = []

            for service_name, service_config in services.items():
                container_name = f"{project_name}_{service_name}"

                try:
                    existing = self.client.containers.get(container_name)
                    if force_recreate:
                        existing.remove(force=True)
                    else:
                        created_containers.append(container_name)
                        continue
                except NotFound:
                    pass

                image = service_config.get("image")
                if not image:
                    raise HTTPException(status_code=400, detail=f"Service {service_name} missing image")

                env = service_config.get("environment", {})
                if isinstance(env, list):
                    env_dict = {}
                    for item in env:
                        if "=" in item:
                            k, v = item.split("=", 1)
                            env_dict[k] = v
                    env = env_dict

                ports = service_config.get("ports", [])
                port_bindings = {}
                if isinstance(ports, list):
                    for port in ports:
                        if isinstance(port, str):
                            if ":" in port:
                                host_port, container_port = port.split(":", 1)
                                port_bindings[container_port] = host_port

                container = self.client.containers.create(
                    image=image,
                    name=container_name,
                    environment=env,
                    ports=port_bindings,
                    labels={"com.docker.compose.project": project_name},
                    detach=True
                )
                container.start()
                created_containers.append(container_name)

            return {
                "project_name": project_name,
                "services": created_containers,
                "mode": "standalone",
                "created": datetime.now().isoformat()
            }
        except APIError as e:
            logger.error(f"Docker API error deploying compose stack: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error deploying compose stack: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def list_stacks(self) -> list[dict[str, Any]]:
        if self._is_swarm():
            return self._list_stacks_swarm()
        else:
            return self._list_stacks_standalone()

    def _list_stacks_swarm(self) -> list[dict[str, Any]]:
        try:
            services = self.client.services.list()
            stacks = {}

            for service in services:
                labels = service.attrs.get("Spec", {}).get("Labels", {})
                stack_name = labels.get("com.docker.stack.namespace")

                if stack_name:
                    if stack_name not in stacks:
                        stacks[stack_name] = []
                    stacks[stack_name].append(service.name)

            result = []
            for stack_name, services_list in stacks.items():
                result.append({
                    "project_name": stack_name,
                    "services": services_list,
                    "service_count": len(services_list)
                })

            return result
        except APIError as e:
            logger.error(f"Docker API error listing stacks: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing stacks: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def _list_stacks_standalone(self) -> list[dict[str, Any]]:
        try:
            containers = self.client.containers.list(all=True)
            stacks = {}

            for container in containers:
                labels = container.labels
                project_name = labels.get("com.docker.compose.project")

                if project_name:
                    if project_name not in stacks:
                        stacks[project_name] = []
                    stacks[project_name].append(container.name)

            result = []
            for project_name, services_list in stacks.items():
                result.append({
                    "project_name": project_name,
                    "services": services_list,
                    "service_count": len(services_list)
                })

            return result
        except APIError as e:
            logger.error(f"Docker API error listing stacks: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing stacks: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def list_services(self) -> list[dict[str, Any]]:
        try:
            services = self.client.services.list()
            result = []

            for service in services:
                spec = service.attrs.get("Spec", {})
                task_template = spec.get("TaskTemplate", {})
                container_spec = task_template.get("ContainerSpec", {})
                mode = spec.get("Mode", {})

                replicas = 0
                service_mode = "replicated"
                if "Replicated" in mode:
                    replicas = mode["Replicated"].get("Replicas", 0)
                    service_mode = "replicated"
                elif "Global" in mode:
                    service_mode = "global"

                created_at = service.attrs.get("CreatedAt", "")

                result.append({
                    "id": service.short_id,
                    "name": service.name,
                    "replicas": replicas,
                    "image": container_spec.get("Image", ""),
                    "created": created_at,
                    "mode": service_mode
                })

            return result
        except APIError as e:
            logger.error(f"Docker API error listing services: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing services: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def scale_service(self, service_name: str, replicas: int) -> dict[str, Any]:
        try:
            service = self.client.services.get(service_name)

            spec = service.attrs.get("Spec", {})
            mode = spec.get("Mode", {})

            if "Global" in mode:
                raise HTTPException(status_code=400, detail="Cannot scale global services")

            service.update(mode=ServiceMode("replicated", replicas=replicas))

            service.reload()

            spec = service.attrs.get("Spec", {})
            task_template = spec.get("TaskTemplate", {})
            container_spec = task_template.get("ContainerSpec", {})
            mode = spec.get("Mode", {})

            current_replicas = mode.get("Replicated", {}).get("Replicas", 0)
            created_at = service.attrs.get("CreatedAt", "")

            return {
                "id": service.short_id,
                "name": service.name,
                "replicas": current_replicas,
                "image": container_spec.get("Image", ""),
                "created": created_at,
                "mode": "replicated"
            }
        except NotFound:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        except APIError as e:
            logger.error(f"Docker API error scaling service: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error scaling service: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def remove_service(self, service_name: str) -> None:
        try:
            service = self.client.services.get(service_name)
            service.remove()
        except NotFound:
            raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
        except APIError as e:
            logger.error(f"Docker API error removing service: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing service: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def list_networks(self) -> list[dict[str, Any]]:
        try:
            networks = self.client.networks.list()
            result = []

            for network in networks:
                created_time = network.attrs.get("Created", "")
                if created_time:
                    try:
                        created = datetime.fromisoformat(created_time.replace("Z", "+00:00")).isoformat()
                    except (ValueError, AttributeError):
                        created = datetime.now().isoformat()
                else:
                    created = datetime.now().isoformat()

                result.append({
                    "id": network.short_id,
                    "name": network.name,
                    "driver": network.attrs.get("Driver", ""),
                    "scope": network.attrs.get("Scope", "local"),
                    "created": created
                })

            return result
        except APIError as e:
            logger.error(f"Docker API error listing networks: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing networks: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def create_network(self, config: dict[str, Any]) -> dict[str, Any]:
        try:
            network = self.client.networks.create(
                name=config["name"],
                driver=config.get("driver", "bridge"),
                ipam=config.get("ipam"),
                options=config.get("options")
            )

            created_time = network.attrs.get("Created", "")
            if created_time:
                try:
                    created = datetime.fromisoformat(created_time.replace("Z", "+00:00")).isoformat()
                except (ValueError, AttributeError):
                    created = datetime.now().isoformat()
            else:
                created = datetime.now().isoformat()

            return {
                "id": network.short_id,
                "name": network.name,
                "driver": network.attrs.get("Driver", config.get("driver", "bridge")),
                "scope": network.attrs.get("Scope", "local"),
                "created": created
            }
        except APIError as e:
            if e.status_code == 409:
                raise HTTPException(status_code=409, detail=f"Network name conflict: {str(e)}")
            logger.error(f"Docker API error creating network: {e}")
            raise HTTPException(status_code=400, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error creating network: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def remove_network(self, network_id: str) -> None:
        try:
            network = self.client.networks.get(network_id)
            network.remove()
        except NotFound:
            raise HTTPException(status_code=404, detail="Network not found")
        except APIError as e:
            logger.error(f"Docker API error removing network: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing network: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def list_volumes(self) -> list[dict[str, Any]]:
        try:
            volumes = self.client.volumes.list()
            result = []

            for volume in volumes:
                created_time = volume.attrs.get("CreatedAt", "")
                if created_time:
                    try:
                        created = datetime.fromisoformat(created_time.replace("Z", "+00:00")).isoformat()
                    except (ValueError, AttributeError):
                        created = datetime.now().isoformat()
                else:
                    created = datetime.now().isoformat()

                result.append({
                    "name": volume.name,
                    "driver": volume.attrs.get("Driver", "local"),
                    "mountpoint": volume.attrs.get("Mountpoint", ""),
                    "created": created
                })

            return result
        except APIError as e:
            logger.error(f"Docker API error listing volumes: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error listing volumes: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def create_volume(self, config: dict[str, Any]) -> dict[str, Any]:
        try:
            volume = self.client.volumes.create(
                name=config["name"],
                driver=config.get("driver", "local"),
                driver_opts=config.get("options"),
                labels=config.get("labels")
            )

            created_time = volume.attrs.get("CreatedAt", "")
            if created_time:
                try:
                    created = datetime.fromisoformat(created_time.replace("Z", "+00:00")).isoformat()
                except (ValueError, AttributeError):
                    created = datetime.now().isoformat()
            else:
                created = datetime.now().isoformat()

            return {
                "name": volume.name,
                "driver": volume.attrs.get("Driver", config.get("driver", "local")),
                "mountpoint": volume.attrs.get("Mountpoint", ""),
                "created": created
            }
        except APIError as e:
            if e.status_code == 409:
                raise HTTPException(status_code=409, detail=f"Volume name conflict: {str(e)}")
            logger.error(f"Docker API error creating volume: {e}")
            raise HTTPException(status_code=400, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error creating volume: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def remove_volume(self, volume_name: str) -> None:
        try:
            volume = self.client.volumes.get(volume_name)
            volume.remove()
        except NotFound:
            raise HTTPException(status_code=404, detail="Volume not found")
        except APIError as e:
            if e.status_code == 409:
                raise HTTPException(status_code=409, detail=f"Volume in use, cannot remove: {str(e)}")
            logger.error(f"Docker API error removing volume: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error removing volume: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")


_docker_client_instance: DockerClient | None = None


def get_docker_client() -> DockerClient:
    global _docker_client_instance
    if _docker_client_instance is None:
        _docker_client_instance = DockerClient()
    return _docker_client_instance
