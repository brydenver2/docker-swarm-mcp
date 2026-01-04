import logging
from datetime import datetime, timezone
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
        Create and configure the Docker client using application settings and verify connectivity.
        
        Configures the client from settings:
        - DOCKER_HOST controls the daemon endpoint (e.g., unix://, tcp://, ssh://). If not explicitly set, falls back to environment/default Unix socket.
        - DOCKER_TLS_VERIFY and DOCKER_CERT_PATH enable and configure TLS with client and CA certificates when provided.
        
        Verifies the Docker daemon is reachable by issuing a ping during initialization.
        
        Raises:
            RuntimeError: If the Docker engine is unreachable or an unexpected error occurs during client setup.
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
        except Exception as e:
            logger.exception("Unexpected error initializing Docker client")
            raise RuntimeError("Docker engine unreachable") from e

        self._is_swarm_cache: bool | None = None
        self._service_name_cache: dict[str, bool] = {}

    @staticmethod
    def _normalize_since(since: Any) -> int | None:
        """Convert incoming since values (ISO string or seconds) to epoch seconds."""
        if since in (None, ""):
            return None

        if isinstance(since, (int, float)):
            return int(since)

        if isinstance(since, str):
            trimmed = since.strip()
            if trimmed == "":
                return None
            # Accept numeric strings directly
            try:
                return int(float(trimmed))
            except ValueError:
                pass

            iso_candidate = trimmed.replace("Z", "+00:00") if trimmed.endswith("Z") else trimmed
            try:
                parsed = datetime.fromisoformat(iso_candidate)
            except ValueError as exc:  # pragma: no cover - defensive
                raise HTTPException(status_code=400, detail=f"Invalid since value: {since}") from exc

            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)

            return int(parsed.timestamp())

        raise HTTPException(status_code=400, detail=f"Unsupported since value type: {type(since).__name__}")

    def _is_swarm(self) -> bool:
        """
        Determine whether the connected Docker daemon is an active swarm manager.
        
        Caches the detected swarm state on first check to avoid repeated queries.
        
        Returns:
            bool: `True` if the daemon's Swarm.LocalNodeState equals "active", `False` otherwise.
        """
        if self._is_swarm_cache is None:
            info = self.client.info()
            swarm_info = info.get("Swarm", {})
            self._is_swarm_cache = swarm_info.get("LocalNodeState") == "active"
        return self._is_swarm_cache

    def ping(self) -> bool:
        """
        Check connectivity to the Docker daemon.
        
        Returns:
            True if the Docker daemon responded to a ping, False otherwise.
        """
        return self.client.ping()

    def get_info(self) -> dict[str, Any]:
        """
        Retrieve Docker daemon information.
        
        Returns:
            info (dict[str, Any]): Dictionary of daemon attributes reported by the Docker engine (for example: 'ID', 'Containers', 'Images', 'Swarm', and other engine-provided metadata).
        """
        return self.client.info()

    def list_containers(self, all: bool = False, filters: Optional[dict] = None) -> list[dict[str, Any]]:
        """
        Return a list of containers with key metadata suitable for JSON responses.
        
        Returns:
            list[dict[str, Any]]: Each item contains:
                - `id`: full container id
                - `name`: container name
                - `status`: container status string
                - `image`: preferred image tag or image short id
                - `created`: ISO 8601 creation timestamp (UTC offset preserved)
                - `ports`: list of port mappings where each mapping has
                    - `private_port` (int): container port
                    - `public_port` (int | None): host port if published, otherwise `None`
                    - `type` (str): protocol, e.g. "tcp" or "udp"
        """
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
                    "id": container.id,
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
        """
        Remove a Compose project (standalone) or stack (Swarm) identified by its project name from the Docker host.
        
        Parameters:
            project_name (str): The Compose project or stack name to remove. The operation removes all services/containers belonging to that project/stack.
        """
        if self._is_swarm():
            self._remove_compose_swarm(project_name)
        else:
            self._remove_compose_standalone(project_name)

    def _remove_compose_swarm(self, project_name: str) -> None:
        """
        Remove all Docker Swarm services that belong to the specified Compose stack.
        
        Locates services labeled `com.docker.stack.namespace=<project_name>` and removes each matching service. Raises an HTTPException with status 404 if no services for the given stack are found; raises 424 on Docker API errors and 500 on other Docker-related errors.
        
        Parameters:
            project_name (str): Name of the Compose stack (value of the `com.docker.stack.namespace` label).
        
        Raises:
            HTTPException: 404 if the stack is not found.
            HTTPException: 424 if a Docker API error occurs.
            HTTPException: 500 if a general Docker error occurs.
        """
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
        """
        Remove all standalone containers belonging to a Compose project identified by its project name.
        
        Looks up containers labeled `com.docker.compose.project=<project_name>` and removes each one with force=True.
        
        Parameters:
            project_name (str): Compose project name used in the `com.docker.compose.project` label.
        
        Raises:
            HTTPException: 404 if no containers for the project are found.
            HTTPException: 424 if the Docker API returns an error while removing containers.
            HTTPException: 500 if a generic Docker error occurs.
        """
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
        """
        Create a new container from the provided configuration and return its basic metadata.
        
        Parameters:
            config (dict): Container creation configuration. Expected keys:
                - image (str): Required. Image reference to create the container from.
                - name (str, optional): Container name.
                - environment (dict|list[str], optional): Environment variables as a dict or list of `KEY=VALUE` strings.
                - ports (dict|list, optional): Port mappings accepted by the Docker SDK.
                - volumes (dict|list, optional): Volume bindings accepted by the Docker SDK.
                - restart_policy (str, optional): Restart policy name (defaults to `"no"`).
        
        Returns:
            dict: Metadata about the created container with keys:
                - id (str): Container full ID.
                - name (str): Container name.
                - status (str): Container status immediately after creation.
                - image (str): Image reference used to create the container.
                - created (str): ISO-formatted timestamp when the record was created.
        
        Raises:
            HTTPException: 404 if the image is not found.
            HTTPException: 409 if there is a container name conflict.
            HTTPException: 400 for other Docker API errors during creation.
            HTTPException: 500 for generic Docker client errors.
        """
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
                "id": container.id,
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
        """
        Start a container by its ID or name.
        
        Parameters:
            container_id (str): The container identifier or name to start.
        
        Raises:
            HTTPException: 404 if the container does not exist.
            HTTPException: 424 if the Docker API returns an error while starting.
            HTTPException: 500 for other Docker-related errors.
        """
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
        """
        Stop the container identified by `container_id`, waiting up to `timeout` seconds for it to stop.
        
        Parameters:
            container_id (str): Container identifier or name.
            timeout (int): Seconds to wait for the container to stop before killing it.
        
        Raises:
            HTTPException: 404 if the container does not exist.
            HTTPException: 424 if the Docker Engine returns an API error while stopping the container.
            HTTPException: 500 for other Docker-related errors.
        """
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
        """
        Remove a container identified by `container_id`, optionally forcing removal of running containers.
        
        Parameters:
            container_id (str): ID or name of the container to remove.
            force (bool): If `True`, force removal even if the container is running.
        
        Raises:
            HTTPException: 404 if the container does not exist.
            HTTPException: 424 for Docker API errors.
            HTTPException: 500 for other Docker-related errors.
        """
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
        """
        Retrieve the logs of a container as a UTF-8 string.
        
        Parameters:
            container_id (str): ID or name of the container to fetch logs from.
            tail (int): Number of lines from the end of the logs to return (default 100).
            since (Optional[str]): Return logs since this timestamp (RFC3339 or seconds) or None to ignore.
            follow (bool): If True, stream logs; otherwise return a snapshot (streaming is controlled by the Docker client).
        
        Returns:
            str: Container logs decoded as a UTF-8 string.
        
        Raises:
            HTTPException: 404 if the container does not exist; 424 for Docker API errors; 500 for other Docker client errors.
        """
        try:
            container = self.client.containers.get(container_id)
            normalized_since = self._normalize_since(since)
            logs = container.logs(tail=tail, since=normalized_since, follow=follow, stream=False)
            return logs.decode("utf-8") if isinstance(logs, bytes) else logs
        except NotFound:
            if self._looks_like_service(container_id):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Resource appears to be a Swarm service. Use /services/{name}/logs or the service-logs tool "
                        "to retrieve Swarm service logs."
                    )
                )
            raise HTTPException(status_code=404, detail="Container not found")
        except APIError as e:
            logger.error(f"Docker API error getting logs: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error getting logs: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def get_service_logs(self, service_name: str, tail: int = 100, since: Optional[str] = None, follow: bool = False) -> str:
        """Retrieve the logs for a Docker Swarm service."""
        try:
            service = self.client.services.get(service_name)
            normalized_since = self._normalize_since(since)
            logs = service.logs(
                stdout=True,
                stderr=True,
                tail=tail,
                since=normalized_since,
                follow=follow,
                timestamps=True,
            )
            return logs.decode("utf-8") if isinstance(logs, bytes) else logs
        except NotFound:
            raise HTTPException(status_code=404, detail="Service not found")
        except APIError as e:
            logger.error(f"Docker API error getting service logs: {e}")
            raise HTTPException(status_code=424, detail=f"Docker API error: {str(e)}")
        except DockerException as e:
            logger.error(f"Docker error getting service logs: {e}")
            raise HTTPException(status_code=500, detail=f"Docker error: {str(e)}")

    def _looks_like_service(self, identifier: str) -> bool:
        """Heuristically determine if the identifier matches an existing swarm service."""
        cached = self._service_name_cache.get(identifier)
        if cached is not None:
            return cached

        try:
            services = self.client.services.list(filters={"name": identifier})
            is_service = bool(services)
        except DockerException:
            is_service = False

        self._service_name_cache[identifier] = is_service
        return is_service

    def deploy_compose(self, project_name: str, compose_yaml: str, force_recreate: bool = False) -> dict[str, Any]:
        """
        Deploy a Docker Compose project to the connected Docker daemon, using swarm mode when available.
        
        Parses the provided Compose YAML, validates it targets Compose specification version 3.x, ensures services are defined, and dispatches to the swarm or standalone deployment path. If swarm mode is active, services are deployed as Swarm services; otherwise containers are created and started.
        
        Parameters:
            project_name (str): Logical name used as the Compose project/stack namespace for created services or containers.
            compose_yaml (str): Compose file contents in YAML format describing services and their configuration.
            force_recreate (bool): If true, existing services/containers with the same project+service names will be removed and recreated; otherwise existing resources are left in place.
        
        Returns:
            dict[str, Any]: Deployment summary including at least `project_name`, `services` (created or existing service/container names), `mode` ("swarm" or "standalone"), and `created` (ISO timestamp).
        
        Raises:
            HTTPException: If the YAML cannot be parsed (400), if the Compose version is not 3.x (400), or if no services are defined (400).
        """
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
        """
        Deploys a compose-style project as Docker Swarm services under a stack namespace.
        
        Parameters:
        	project_name (str): Stack/compose project name used as the service namespace prefix.
        	services (dict[str, Any]): Mapping of service keys to service definitions; each definition must include an `image` and may include `environment` (dict or list of "KEY=VAL" strings) and `replicas` (int).
        	force_recreate (bool): If true, remove any existing services with the same names before creating new ones.
        
        Returns:
        	result (dict[str, Any]): Deployment summary with keys:
        		- `project_name` (str): the provided project_name,
        		- `services` (list[str]): list of created or existing full service names (formatted as "{project_name}_{service_name}"),
        		- `mode` (str): `"swarm"`,
        		- `created` (str): ISO-8601 timestamp of the deployment.
        
        Raises:
        	HTTPException: 400 if a service definition is missing `image`; 424 for Docker API errors; 500 for other Docker errors.
        """
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

                labels = service_config.get("labels") or {}
                if isinstance(labels, list):
                    label_dict = {}
                    for item in labels:
                        if "=" in item:
                            k, v = item.split("=", 1)
                            label_dict[k.strip()] = v.strip()
                    labels = label_dict
                elif not isinstance(labels, dict):
                    labels = {}

                stack_labels = {
                    "com.docker.stack.namespace": project_name,
                    "com.docker.stack.service.name": service_name,
                    "com.docker.stack.image": image,
                }
                labels.update(stack_labels)

                service = self.client.services.create(
                    image=image,
                    name=full_service_name,
                    env=env,
                    labels=labels,
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
        """
        Deploy a compose-style set of services as standalone Docker containers under a project namespace.
        
        Parameters:
            project_name (str): Project/stack name used as a prefix for container names and as the `com.docker.compose.project` label.
            services (dict[str, Any]): Mapping of service name to Compose-like service configuration. Supported keys:
                - image (str): Required image reference for the service.
                - environment (dict | list): Environment variables as a dict or a list of "KEY=VAL" strings.
                - ports (list): List of port bindings as strings in the form "host_port:container_port".
            force_recreate (bool): If true, existing containers with the same project-prefixed name will be removed before creation.
        
        Returns:
            dict[str, Any]: Result object containing:
                - project_name: the provided project_name,
                - services: list of created (or preserved) container names,
                - mode: the string "standalone",
                - created: ISO-8601 timestamp for when the deployment was recorded.
        
        Raises:
            HTTPException: Raised with status 400 for invalid service configuration (e.g., missing image);
                424 for Docker API errors; 500 for other Docker errors.
        """
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
        """
        List deployed stacks (compose projects) on the connected Docker daemon.
        
        Each returned item describes a stack/project and includes:
        - `project_name` (str): stack or compose project name.
        - `services` (list[str]): names of services/containers belonging to the stack.
        - `service_count` (int): number of services in the stack.
        
        The method detects whether the daemon is a Swarm manager and returns stacks accordingly (Swarm services grouped by `com.docker.stack.namespace`, or standalone containers grouped by `com.docker.compose.project`).
        
        Returns:
            list[dict[str, Any]]: List of stack descriptors as described above.
        """
        if self._is_swarm():
            return self._list_stacks_swarm()
        else:
            return self._list_stacks_standalone()

    def _list_stacks_swarm(self) -> list[dict[str, Any]]:
        """
        Collects Docker stack (compose project) names from Swarm services and summarizes their services.
        
        Returns:
            list[dict[str, Any]]: A list of dictionaries, each containing:
                - "project_name": stack namespace (str)
                - "services": list of service names belonging to the stack (list[str])
                - "service_count": number of services in the stack (int)
        
        Raises:
            fastapi.HTTPException: with status 424 if a Docker API error occurs, or 500 for other Docker errors.
        """
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
        """
        Collect standalone Docker Compose projects by grouping containers that have the `com.docker.compose.project` label.
        
        Returns:
            list[dict[str, Any]]: Each dict contains:
                - "project_name": the compose project name (str).
                - "services": list of container names (list[str]).
                - "service_count": number of services in the project (int).
        
        Raises:
            HTTPException: with status 424 if a Docker API error occurs.
            HTTPException: with status 500 if a general Docker error occurs.
        """
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
        """
        List Docker services and return a simplified overview for each service.
        
        Each item in the returned list represents a service and contains the following keys:
        - `id`: full service identifier.
        - `name`: service name.
        - `replicas`: integer number of replicas (0 if the service is in global mode or replicas not specified).
        - `image`: container image string from the service specification (empty string if not present).
        - `created`: `CreatedAt` timestamp string from the service attributes.
        - `mode`: service mode, either `"replicated"` or `"global"`.
        
        Returns:
            list[dict[str, Any]]: A list of service summary dictionaries as described above.
        """
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
                    "id": service.id,
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
        """
        Scale a swarm service to the requested number of replicas and return its updated metadata.
        
        Parameters:
            service_name (str): Name or ID of the service to scale.
            replicas (int): Desired number of replicas for the service.
        
        Returns:
            dict: Metadata for the service after scaling with keys:
                - id (str): Full service ID.
                - name (str): Service name.
                - replicas (int): Current number of replicas.
                - image (str): Container image used by the service.
                - created (str): Service creation timestamp from the Docker API.
                - mode (str): Service mode (will be "replicated" on success).
        
        Raises:
            HTTPException: 400 if the service is in global mode and cannot be scaled.
            HTTPException: 404 if the service is not found.
            HTTPException: 424 for Docker API errors.
            HTTPException: 500 for other Docker-related errors.
        """
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
                "id": service.id,
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
        """
        Remove a Docker Swarm service identified by name or ID.
        
        Parameters:
            service_name (str): The service name or ID to remove.
        
        Raises:
            HTTPException: 404 if the service is not found.
            HTTPException: 424 if the Docker API returns an error.
            HTTPException: 500 for other Docker-related errors.
        """
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
        """
        List Docker networks available to the configured Docker daemon.
        
        Returns:
            networks (list[dict[str, Any]]): A list of network descriptors. Each descriptor contains:
                - id: full network ID (str)
                - name: network name (str)
                - driver: network driver (str)
                - scope: network scope, e.g. "local" (str)
                - created: creation timestamp in ISO 8601 format (str)
        
        Raises:
            HTTPException: Raises an HTTPException with status 424 for Docker API errors or 500 for other Docker errors.
        """
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
                    "id": network.id,
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
        """
        Create a Docker network from the provided configuration.
        
        Parameters:
            config (dict[str, Any]): Network configuration. Expected keys:
                - name (str): Required network name.
                - driver (str, optional): Network driver (default "bridge").
                - ipam (dict, optional): IP Address Management configuration.
                - options (dict, optional): Driver-specific options.
        
        Returns:
            dict[str, Any]: Network summary containing:
                - id: Full network ID.
                - name: Network name.
                - driver: Network driver.
                - scope: Network scope (e.g., "local").
                - created: ISO 8601 creation timestamp.
        
        Raises:
            HTTPException: 409 if a network name conflict occurs;
                           400 for other Docker API errors;
                           500 for generic Docker errors.
        """
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
                "id": network.id,
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
        """
        Remove a Docker network by its ID or name.
        
        Parameters:
            network_id (str): The Docker network ID or name to remove.
        
        Raises:
            HTTPException: 404 if the network does not exist.
            HTTPException: 424 if the Docker API returns an error while removing the network.
            HTTPException: 500 if a general Docker error occurs.
        """
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
        """
        Return a list of Docker volumes with normalized metadata.
        
        Returns:
            list[dict[str, Any]]: A list of volume records, each containing:
                - name: volume name
                - driver: volume driver (defaults to "local" if absent)
                - mountpoint: volume mountpoint (empty string if absent)
                - created: ISO 8601 creation timestamp (falls back to current time if parsing fails)
        
        Raises:
            HTTPException: 424 if the Docker API returns an error.
            HTTPException: 500 if a general Docker client error occurs.
        """
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
        """
        Create a Docker volume from the provided configuration and return its metadata.
        
        Parameters:
            config (dict): Volume configuration. Expected keys:
                - name (str): Required volume name.
                - driver (str, optional): Volume driver to use (default "local").
                - options (dict, optional): Driver-specific options passed as driver_opts.
                - labels (dict, optional): Labels to apply to the volume.
        
        Returns:
            dict: Metadata for the created volume with keys:
                - name (str): Volume name.
                - driver (str): Driver used for the volume.
                - mountpoint (str): Host path where the volume is mounted.
                - created (str): Creation time as an ISO 8601 timestamp.
        
        Raises:
            HTTPException: If the Docker API reports an error (409 for name conflict, 400 for other API errors),
                           or if a lower-level Docker error occurs (500).
        """
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
        """
        Remove a Docker volume by name.
        
        Parameters:
            volume_name (str): Name or ID of the volume to remove.
        
        Raises:
            HTTPException: 404 if the volume does not exist.
            HTTPException: 409 if the volume is in use and cannot be removed.
            HTTPException: 424 if the Docker API returns an error.
            HTTPException: 500 for other Docker-related errors.
        """
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
    """
    Return the singleton DockerClient instance, creating and caching it on first call.
    
    Returns:
        DockerClient: The cached global DockerClient instance.
    """
    global _docker_client_instance
    if _docker_client_instance is None:
        _docker_client_instance = DockerClient()
    return _docker_client_instance