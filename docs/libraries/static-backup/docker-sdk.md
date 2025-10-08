================
CODE SNIPPETS
================
TITLE: Install Docker SDK for Python
DESCRIPTION: Instructions for installing the Docker SDK for Python using pip. This command installs the library and its dependencies, enabling programmatic interaction with Docker.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Shell
CODE:
```
pip install docker
```

--------------------------------

TITLE: Initialize Docker Client in Python
DESCRIPTION: Demonstrates how to import the Docker SDK and initialize a client connection to the Docker Engine. This setup uses environment variables or the default socket for connection.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
import docker
client = docker.from_env()
```

--------------------------------

TITLE: Install Docker SDK for Python
DESCRIPTION: Instructions for installing the Docker SDK for Python using pip, the Python package installer. This command adds the 'docker' package to your Python environment.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: bash
CODE:
```
pip install docker
```

--------------------------------

TITLE: Manage Docker Containers
DESCRIPTION: Provides examples of common container management operations: listing all running containers, getting a specific container by ID, accessing container attributes like image name, retrieving all logs, and stopping a container.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
client.containers.list()
container = client.containers.get('45e6d2de7c54')
container.attrs['Config']['Image']
container.logs()
container.stop()
```

--------------------------------

TITLE: Docker-py Client Container Configuration and Management API
DESCRIPTION: This section details updates to `docker-py`'s `Client` methods for creating and starting containers, including new parameters for host configuration, resource limits, and device mapping. It also covers a utility method for constructing host configuration dictionaries.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_container(..., host_config, cpuset, mem_limit, environment, volumes)
  - Adds support for detailed host configuration when creating containers.
  - Parameters:
    - host_config: A dictionary representing the HostConfig, can be built with `docker.utils.create_host_config`.
    - cpuset: CPU set constraints for the container.
    - mem_limit: Memory limit for the container, now supports string values.
    - environment: Environment variables, fixed bug with unicode characters.
    - volumes: Improved validation for the volumes parameter.

Client.start(..., dns, volumes_from, extra_hosts, devices)
  - Enhances container startup options.
  - Parameters:
    - dns: DNS server configuration (raises exception for API < 1.10).
    - volumes_from: Mount volumes from other containers (raises exception for API < 1.10).
    - extra_hosts: Additional host entries to be added to /etc/hosts.
    - devices: Host devices to be mapped into the container, supports proper delimiter.

docker.utils.create_host_config(binds, port_bindings, lxc_conf, publish_all_ports, links, privileged, dns, dns_search, volumes_from, cap_add, cap_drop, extra_hosts, restart_policy, network_mode, devices, ulimits, log_config, security_opt, cgroup_parent, mem_limit, memswap_limit, cpu_shares, cpuset_cpus, cpuset_mems, cpu_quota, cpu_period, blkio_weight, blkio_weight_device, blkio_device_read_bps, blkio_device_write_bps, blkio_device_read_iops, blkio_device_write_iops, pids_limit, ipc_mode, uts_mode, sysctls, runtime, auto_remove, oom_kill_disable, init, group_add, userns_mode, shm_size, stdin_open, tty, attach_stdin, attach_stdout, attach_stderr, stream, detach, entrypoint, command, working_dir, user, hostname, domainname, mac_address, labels, stop_signal, stop_timeout, healthcheck, isolation, mounts, nano_cpus, cpu_rt_period, cpu_rt_runtime, device_requests, kernel_memory, memory_reservation, memory_swap, memory_swappiness, oom_score_adj, pids_limit, tmpfs, ulimits, userns_mode, uts_mode, pid_mode, network_mode, ip_address, ip_prefix_len, ipv6_address, ipv6_prefix_len, links, log_config, group_add, cgroup_parent, security_opt, sysctls, runtime, auto_remove, oom_kill_disable, init, group_add, userns_mode, shm_size, stdin_open, tty, attach_stdin, attach_stdout, attach_stderr, stream, detach, entrypoint, command, working_dir, user, hostname, domainname, mac_address, labels, stop_signal, stop_timeout, healthcheck, isolation, mounts, nano_cpus, cpu_rt_period, cpu_rt_runtime, device_requests, kernel_memory, memory_reservation, memory_swap, memory_swappiness, oom_score_adj, pids_limit, tmpfs, ulimits, userns_mode, uts_mode, pid_mode, network_mode, ip_address, ip_prefix_len, ipv6_address, ipv6_prefix_len, links, log_config, group_add, cgroup_parent, security_opt, sysctls, runtime, auto_remove, oom_kill_disable, init, group_add, userns_mode, shm_size, stdin_open, tty, attach_stdin, attach_stdout, attach_stderr, stream, detach, entrypoint, command, working_dir, user, hostname, domainname, mac_address, labels, stop_signal, stop_timeout, healthcheck, isolation, mounts, nano_cpus, cpu_rt_period, cpu_rt_runtime, device_requests, kernel_memory, memory_reservation, memory_swap, memory_swappiness, oom_score_adj, pids_limit, tmpfs, ulimits, userns_mode, uts_mode, pid_mode, network_mode, ip_address, ip_prefix_len, ipv6_address, ipv6_prefix_len)
  - A utility method to help build a proper `HostConfig` dictionary for `create_container`.
```

--------------------------------

TITLE: Manage Docker Containers with Python
DESCRIPTION: Provides examples for common Docker container management operations using the Python SDK, including listing all containers, retrieving a specific container by ID, accessing its attributes, fetching logs, and stopping it.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
client.containers.list()
container = client.containers.get('45e6d2de7c54')
container.attrs['Config']['Image']
container.logs()
container.stop()
```

--------------------------------

TITLE: Initialize Docker Client, Run Container, and Define Test Command in Python
DESCRIPTION: This snippet initializes a Docker client, runs a detached container, and defines a shell command that outputs distinct messages to both stdout and stderr. This setup is a prerequisite for demonstrating stream handling with `exec_run`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/multiplex.rst

LANGUAGE: python
CODE:
```
client = docker.from_env()
container = client.containers.run(
    'bfirsh/reticulate-splines', detach=True)
cmd = '/bin/sh -c "echo hello stdout ; echo hello stderr >&2"'
```

--------------------------------

TITLE: Docker Client Container Management Methods
DESCRIPTION: Documentation for methods managing Docker containers, including creation, starting, stopping, removing, attaching, and logging, detailing various parameter additions and behavioral changes.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_container(image, command=None, hostname=None, user=None, detach=False, stdin_open=False, tty=False, ports=None, environment=None, volumes=None, network_disabled=False, cpu_shares=None, working_dir=None, entrypoint=None, memswap_limit=None, domainname=None, volumes_from=None)
  - Creates a new container.
  - Parameters:
    - image: The image to use for the container.
    - command: The command to run in the container (now optional).
    - ports: Port bindings (changed format for simplicity).
    - volumes: Volume bindings (changed format for simplicity).
    - network_disabled: Disable networking for the container.
    - cpu_shares: CPU shares (relative weight).
    - working_dir: Working directory inside the container.
    - entrypoint: The entrypoint for the container.
    - memswap_limit: Memory swap limit (e.g., '1g').
    - domainname: Container's domain name.
    - volumes_from: List or iterable of container names/IDs to mount volumes from.
  - Returns: A dictionary containing 'Id' and 'Warnings'.

Client.start(container_id, binds=None, port_bindings=None, lxc_conf=None, publish_all_ports=False, links=None, dns=None, dns_search=None, network_mode=None, volumes_from=None)
  - Starts a created container.
  - Parameters:
    - container_id: The ID of the container.
    - publish_all_ports: Publish all exposed ports to random ports.
    - links: Container links (can now be specified as tuples).
    - dns: List of DNS servers.
    - dns_search: List of DNS search domains.
    - network_mode: Network mode for the container (e.g., 'bridge', 'host').
    - volumes_from: List of container names/IDs to mount volumes from (moved from create_container for API >= 1.10).
    - ports: Port bindings (changed format for simplicity).
    - volumes: Volume bindings (changed format for simplicity).
  - Returns: None.

Client.remove_container(container_id, v=False, link=False, force=False)
  - Removes a container.
  - Parameters:
    - container_id: The ID of the container.
    - force: Force removal of a running container.
  - Returns: None.

Client.kill(container_id, signal=None)
  - Kills a running container.
  - Parameters:
    - container_id: The ID of the container.
    - signal: The signal to send to the container (e.g., 'SIGKILL').
  - Returns: None.

Client.attach(container_id, stream=False, stdout=True, stderr=True, logs=False, websockets=False)
  - Attaches to a container's stdout/stderr.
  - Parameters:
    - container_id: The ID of the container.
    - stream: If True, stream the output as a generator.
    - logs: If True, include historical logs (reworked to be similar to Client.logs, but without historical data by default).
    - websockets: If True, use websockets for attachment.
  - Returns: A generator yielding output lines or a websocket client.

Client.logs(container_id, stream=False, timestamps=False)
  - Retrieves logs from a container.
  - Parameters:
    - container_id: The ID of the container.
    - stream: If True, stream the logs as a generator.
    - timestamps: If True, include timestamps in the log output.
  - Returns: Log string or a generator if stream=True.

Client.containers(all=False, size=False)
  - Lists containers.
  - Parameters:
    - all: Show all containers (default shows only running).
    - size: If True, include the size of the containers.
  - Returns: A list of container dictionaries.

Client.build(path=None, fileobj=None, tag=None, rm=False, custom_context=False, timeout=None, auth_config=None, stream=False)
  - Builds an image from a Dockerfile.
  - Parameters:
    - path: Path to the build context.
    - fileobj: A file-like object containing the Dockerfile.
    - rm: Remove intermediate containers after a successful build.
    - custom_context: If True, `path` is treated as a custom context (e.g., a tarball).
    - timeout: Custom timeout for the build process.
    - auth_config: Authentication configuration for registries (new in API 1.9).
    - stream: If True, stream the build output as a generator.
  - Returns: Image ID or a generator if stream=True.

Client.copy(container_id, resource, dst_path)
  - Copies a file or folder from a container.
  - Parameters:
    - container_id: The ID of the container.
    - resource: Path to the file/folder in the container.
    - dst_path: Destination path on the host.
  - Returns: None.
  - Note: Now accepts a dictionary as an argument for resource/dst_path (implied by bugfix).
```

--------------------------------

TITLE: Docker-py PluginCollection API
DESCRIPTION: Provides methods to interact with and manage Docker plugins at a collection level. These methods allow for retrieving specific plugins, installing new ones, and listing all currently installed plugins on the Docker daemon.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/plugins.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.plugins.PluginCollection:
  get(plugin_id_or_name: str)
    - Retrieve a plugin by its ID or name.
    - Parameters:
      - plugin_id_or_name: The ID or name of the plugin to retrieve.
    - Returns: A Plugin object if found.
  install(remote: str, **kwargs)
    - Install a new plugin from a specified remote source.
    - Parameters:
      - remote: The remote source of the plugin (e.g., 'plugin/name:tag').
      - **kwargs: Additional parameters for installation (e.g., 'enabled', 'grant_all_permissions').
    - Returns: The newly installed Plugin object.
  list(**kwargs)
    - List all installed plugins on the Docker daemon.
    - Parameters:
      - **kwargs: Optional filters to narrow down the list (e.g., 'filters').
    - Returns: A list of Plugin objects.
```

--------------------------------

TITLE: Run Docker Container in Background with Python
DESCRIPTION: Illustrates how to start a Docker container in detached mode, allowing it to run in the background without blocking the current process. The method returns a Container object for further management.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
client.containers.run("bfirsh/reticulate-splines", detach=True)
```

--------------------------------

TITLE: Docker Client Image Management Methods
DESCRIPTION: Documentation for methods related to managing Docker images, including getting, loading, removing, importing, pulling, and pushing images, with details on new parameters and streaming capabilities.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.get_image(image_id)
  - Retrieves an image (similar to `docker save`).
  - Parameters:
    - image_id: The ID or name of the image.
  - Returns: A tar archive of the image.

Client.load_image(data)
  - Loads an image from a tar archive (similar to `docker load`).
  - Parameters:
    - data: A file-like object containing the image tar archive.
  - Returns: None.

Client.remove_image(image_id, force=False, noprune=False)
  - Removes an image.
  - Parameters:
    - image_id: The ID or name of the image.
    - force: Force removal of the image (even if in use).
    - noprune: Do not remove untagged parent images.
  - Returns: A list of dictionaries detailing removed images and untagged images.

Client.import_image(src=None, repository=None, tag=None, changes=None, data=None)
  - Imports an image from a tarball or URL.
  - Parameters:
    - src: URL or path to the source (e.g., tarball).
    - repository: The repository name for the imported image.
    - tag: The tag for the imported image.
    - changes: List of Dockerfile instructions to apply.
    - data: A file-like object containing the tarball data (for tarball imports).
  - Returns: The imported image ID.

Client.pull(repository, tag=None, stream=False)
  - Pulls an image from a registry.
  - Parameters:
    - repository: The image repository name.
    - tag: The image tag (defaults to 'latest').
    - stream: If True, stream the response as a generator.
  - Returns: Image object or a generator if stream=True.

Client.push(repository, tag=None, stream=False)
  - Pushes an image to a registry.
  - Parameters:
    - repository: The image repository name.
    - tag: The image tag (defaults to 'latest').
    - stream: If True, stream the response as a generator.
  - Returns: Response object or a generator if stream=True.
```

--------------------------------

TITLE: Docker Client Exec API Operations
DESCRIPTION: Documents the introduction of new `exec` related methods in the Docker Client API, mirroring the Docker Engine's Exec API, and the deprecation of the older `Client.execute` method. These methods allow for creating, starting, inspecting, and resizing execution commands within containers.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.exec_create(container, cmd, detach=False, tty=False, stdin=False, privileged=False, user=None, environment=None, workdir=None)
  - Creates a new exec instance to run a command inside a container.
  - Parameters:
    - container: The container ID or name.
    - cmd: The command to execute.
    - detach: Boolean, detach from the command.
    - tty: Boolean, allocate a TTY.
    - stdin: Boolean, enable stdin.
    - privileged: Boolean, run in privileged mode.
    - user: String, user to run the command as.
    - environment: List of strings, environment variables.
    - workdir: String, working directory for the command.
  - Returns: An exec ID.

Client.exec_start(exec_id, detach=False, tty=False, stream=False)
  - Starts a previously created exec instance.
  - Parameters:
    - exec_id: The ID of the exec instance.
    - detach: Boolean, detach from the command.
    - tty: Boolean, allocate a TTY.
    - stream: Boolean, stream the output.
  - Returns: The output stream of the command.

Client.exec_inspect(exec_id)
  - Returns low-level information about an exec instance.
  - Parameters:
    - exec_id: The ID of the exec instance.
  - Returns: A dictionary containing exec instance details.

Client.exec_resize(exec_id, height, width)
  - Resizes the TTY of an exec instance.
  - Parameters:
    - exec_id: The ID of the exec instance.
    - height: New height of the TTY.
    - width: New width of the TTY.
  - Returns: True on success.

DEPRECATED: Client.execute
  - This method is deprecated and will be removed in version 1.3.0.
  - Use Client.exec_start and Client.exec_create instead for more granular control.
```

--------------------------------

TITLE: Python: General Library Enhancements and Bugfixes
DESCRIPTION: Details general improvements and bug fixes not directly tied to specific API methods, including Python version support, testing infrastructure, and package installation issues.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: Python
CODE:
```
Python 3 Support:
  - Fixed Python 3 support.
  - Added Python 3 support (initial).

Testing & CI:
  - docker-py is now unit-tested.
  - Travis-CI has been enabled on the source repository.
  - Improvements to the `tox.ini` file.

Package Installation:
  - Fixed a bug where the package would fail with an `ImportError` if requests was installed using `apt-get`.

Codebase:
  - Added license header to python files.
  - Several `README.md` updates.
```

--------------------------------

TITLE: Build and View Project Documentation Locally
DESCRIPTION: These commands allow developers to build the project's documentation locally using `make docs` and then open the generated `index.html` file in the default web browser. This is essential for reviewing and verifying documentation changes before submission.

SOURCE: https://github.com/docker/docker-py/blob/main/CONTRIBUTING.md

LANGUAGE: bash
CODE:
```
make docs
open _build/index.html
```

--------------------------------

TITLE: Clone Repository and Run Project Tests
DESCRIPTION: These commands facilitate setting up the development environment by cloning the Docker SDK for Python repository and then executing the `make test` command. Running tests is a critical step to ensure code changes do not introduce regressions before submitting a pull request.

SOURCE: https://github.com/docker/docker-py/blob/main/CONTRIBUTING.md

LANGUAGE: bash
CODE:
```
git clone git://github.com/docker/docker-py.git
cd docker-py
make test
```

--------------------------------

TITLE: Initialize Docker Client from Environment
DESCRIPTION: Demonstrates how to instantiate a Docker client in Python by connecting to the Docker daemon using default socket or environment configuration. This is the first step to interact with Docker via the SDK.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
import docker
client = docker.from_env()
```

--------------------------------

TITLE: Instantiate Docker Client from Environment Variables
DESCRIPTION: Provides a convenient way to create a Docker client instance by automatically configuring it from environment variables (e.g., DOCKER_HOST, DOCKER_TLS_VERIFY, DOCKER_CERT_PATH). This is the easiest recommended method for client creation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/client.rst

LANGUAGE: APIDOC
CODE:
```
docker.client.from_env()
  - Creates a Docker client instance using environment variables.
  - Parameters: None explicitly shown, but implicitly uses DOCKER_HOST, DOCKER_TLS_VERIFY, DOCKER_CERT_PATH.
  - Returns: A configured DockerClient instance.
```

--------------------------------

TITLE: Docker Client Initialization and Environment Configuration
DESCRIPTION: Documents enhancements to the `docker-py` Client constructor and utility functions for client instantiation, including support for IPv6 host addresses, Windows named pipes, custom User-Agent headers, and flexible environment variable parsing.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client(base_url: str = None, version: str = 'auto', user_agent: str = None, ...)
  - base_url: The URL to the Docker daemon socket.
    - Supports IPv6 addresses (e.g., 'tcp://[::1]:2375').
    - Supports Windows named pipes (e.g., 'npipe://./pipe/docker_engine').
  - user_agent: A custom string to be sent in the User-Agent header.

docker.from_env(version: str = 'auto', ...)
  - Shortcut function to instantiate a Client using environment variables.
  - version: The API version to use.

docker.utils.kwargs_from_env(environment: dict = None, ...)
  - Generates keyword arguments for Client instantiation from environment variables.
  - environment: An optional dictionary to fetch environment values from, instead of os.environ.
```

--------------------------------

TITLE: Execution Management (Client.exec_create, Client.exec_start, Client.execute)
DESCRIPTION: Covers the deprecation of `Client.execute` in favor of `Client.exec_create` and `Client.exec_start`, along with new features for `Client.exec_create` such as privileged execution and container ID handling.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.execute(...)
  - Removed in favor of Client.exec_create and Client.exec_start.
  - Bugfix: Fixed a bug in this deprecated method.

Client.exec_create(
  container: Union[str, dict],
  ...,
  privileged: bool = False,
  ...
)
  - container: Can now retrieve the 'Id' key from a dictionary for its container parameter.
  - privileged: Added support for privileged execution (only available in API >= 1.19).

Client.exec_start(...)
  - Use in conjunction with Client.exec_create for executing commands.
```

--------------------------------

TITLE: Host Configuration Utilities and Deprecations
DESCRIPTION: Documents the deprecation of `docker.utils.create_host_config` in favor of `Client.create_host_config` and the deprecation of passing host configuration directly to `Client.start`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
docker.utils.create_host_config
  - Deprecated in favor of Client.create_host_config.

Client.create_host_config(...)
  - Recommended method for creating host configurations.

Client.start(container, host_config=...)
  - Deprecated: Passing host config directly to this method is deprecated.
  - Use Client.create_container(..., host_config=...) instead.
```

--------------------------------

TITLE: Container Creation and Configuration (Client.create_container)
DESCRIPTION: Details various parameters supported by `Client.create_container` and related host configuration options, including `volume_driver`, `extra_hosts`, `memory_limit`, `memswap_limit`, and advanced volume bind modes.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_container(
  ...,
  volume_driver: str = None,
  user: Union[str, int] = None,
  host_config: dict = None,
  ...
)
  - volume_driver: Added support for specifying a volume driver.
  - user: Can now accept an integer as the user parameter.
  - host_config:
    - extra_hosts: Can now be provided as a list.
    - memory_limit: Added support for memory limits.
    - memswap_limit: Added support for memory swap limits.
    - volume binds: Supports advanced modes using the 'mode' key.
    - read_only: Fixed handling of this parameter.
    - cpuset: Passed as CpusetCpus (Cpuset deprecated in recent API versions).
```

--------------------------------

TITLE: Manage Docker Images
DESCRIPTION: Shows how to pull a Docker image from a registry (e.g., Docker Hub) and list all available images on the local Docker daemon using the Python SDK. This is essential for preparing images for container deployment.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
client.images.pull('nginx')
client.images.list()
```

--------------------------------

TITLE: Run a Docker Container in Foreground
DESCRIPTION: Shows how to run a Docker container using the Python SDK, executing a command inside the container and capturing its output directly. The command blocks until the container finishes.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
client.containers.run("ubuntu", "echo hello world")
```

--------------------------------

TITLE: Docker Swarm Initialization Parameters
DESCRIPTION: This section outlines new parameters for initializing a Docker Swarm, including options for external CAs, labels, signing certificates, and manager autolocking, enhancing security and management capabilities.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Swarm Initialization Specification
create_swarm_spec( # Function used by APIClient.init_swarm
    ...,
    external_cas: list[dict] = None, # Added support
    labels: dict = None, # Added support
    signing_ca_cert: str = None, # Added support
    signing_ca_key: str = None, # Added support
    ca_force_rotate: bool = False, # Added support
    autolock_managers: bool = False, # Added support
    log_driver: dict = None, # Added support
    # ... other swarm spec parameters
)

# DockerClient Swarm Initialization
DockerClient.swarm.init(
    ..., # All parameters from create_swarm_spec apply
)
```

--------------------------------

TITLE: API: Docker Client Image Build Methods (`Client.build`)
DESCRIPTION: Provides a comprehensive overview of changes and new features for the `Client.build` method, detailing improvements in build context handling, caching, logging, and the transition to a server-side build system.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.build(path, tag=None, nocache=False, quiet=False, custom_logger=None, ...)
  - Behavior Change: Now uses tempfiles to store build context instead of storing it in memory.
  - New Option: `nocache` option added.
  - New Option: `quiet` parameter added (mirrors `q` parameter in API).
  - New Option: Supports custom loggers.
  - System Change: Switched to server-side build system.
  - Removal: `BuilderClient` removed.
  - New Feature: Added support for contextual builds.
  - New Feature: Added support for remote URL builds.
  - Bugfix: Fixed a bug where the `tag` parameter would not be taken into account.
  - Bugfix: Fixed a bug where the build command would list tar contents before sending the request.
  - Bugfix: Fixed a bug where `Client.build` would fail if given a `path` parameter.
  - Bugfix: Fixed a bug where generated images would be removed after a successful build.
```

--------------------------------

TITLE: Docker Client Core Utility Methods
DESCRIPTION: Documentation for general utility methods added or modified in the `docker-py` client, including ping, resize, event monitoring, and deprecated functionalities.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.ping()
  - Checks the Docker daemon's availability.
  - Returns: True if successful, raises DockerException otherwise.

Client.resize(container_id, height, width)
  - Resizes the TTY of a container.
  - Parameters:
    - container_id: The ID of the container.
    - height: New height for the TTY.
    - width: New width for the TTY.
  - Returns: None.

Client.events()
  - Accesses the Docker daemon's /events endpoint to stream real-time events.
  - Returns: A generator yielding event dictionaries.

Client.insert(image_id, url, path) (Deprecated)
  - Deprecated in API version > 1.11.
  - Inserts a file from a URL into an image.
  - Parameters:
    - image_id: The ID of the image.
    - url: URL of the file to insert.
    - path: Destination path in the image.
  - Returns: The updated image ID.
```

--------------------------------

TITLE: Docker Client Configuration and Creation Parameters
DESCRIPTION: Details various new parameters added to Docker Client methods and host configuration utilities, enhancing control over container creation, building, and pulling operations, including authentication, resource limits, and network settings.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.pull(repository, tag=None, auth_config=None)
  - Pulls an image from a registry.
  - Parameters:
    - auth_config: Dictionary containing one-off credentials for this pull request.

Client.build(path=None, dockerfile=None, rm=True, tag=None, container_resource_limits=None, ...)
  - Builds an image from a Dockerfile.
  - Parameters:
    - dockerfile: Path to the Dockerfile within the build context (mirrors `docker build -f`).
    - container_resource_limits: Dictionary for setting resource limits (e.g., memory, CPU) during the build process.

Client.create_container(image, command=None, mac_address=None, memswap_limit=None, ...)
  - Creates a new container.
  - Parameters:
    - mac_address: The MAC address to assign to the container.
    - memswap_limit: Accepts string type values (e.g., '6g', '120000k') similar to `mem_limit`.

utils.create_host_config(read_only=False, pid_mode=None, ipc_mode=None, log_config=None, ulimit=None, ...)
  - Creates a host configuration dictionary for container creation.
  - Parameters:
    - read_only: Boolean, enables read-only root filesystem for the container.
    - pid_mode: String, sets the PID namespace mode (e.g., 'host').
    - ipc_mode: String, sets the IPC namespace mode.
    - log_config: Dictionary, specifies logging driver and options.
    - ulimit: List of Ulimit objects, sets resource limits for the container.

Client.start(container, read_only=False, pid_mode=None, ...)
  - Starts a container.
  - Parameters:
    - read_only: Boolean, enables read-only root filesystem for the container.
    - pid_mode: String, sets the PID namespace mode.
```

--------------------------------

TITLE: Manage Docker Images with Python
DESCRIPTION: Shows how to perform essential Docker image management tasks using the Python SDK, including pulling new images from a registry and listing all locally available images.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
client.images.pull('nginx')
client.images.list()
```

--------------------------------

TITLE: Container Lifecycle Management (Client.stop, Client.insert)
DESCRIPTION: Addresses bug fixes for `Client.stop` regarding `timeout=None` and a general fix for `Client.insert`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.stop(
  container,
  timeout: Optional[int] = None,
  ...
)
  - Bugfix: Providing timeout=None no longer results in an exception.

Client.insert(...)
  - Bugfix: Fixed an issue with this method.
```

--------------------------------

TITLE: Check Docker SDK and Python Versions for Debugging
DESCRIPTION: This command combines `pip freeze`, `python --version`, and `docker version` to quickly gather essential version information for debugging and reporting issues related to the Docker SDK for Python. It helps in providing a comprehensive environment snapshot for troubleshooting.

SOURCE: https://github.com/docker/docker-py/blob/main/CONTRIBUTING.md

LANGUAGE: bash
CODE:
```
pip freeze | grep docker && python --version && docker version
```

--------------------------------

TITLE: Image Build and Registry Operations (Client.build, Client.push, Client.pull)
DESCRIPTION: Details enhancements for image building and registry interactions, including decoding JSON streams during build, default pull behavior, and improved error handling for push/pull operations.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.build(
  ...,
  decode: bool = False,
  pull: bool = False,
  ...
)
  - decode: Added support for decoding JSON stream on the fly.
  - pull: Now defaults to False.
  - Bugfix: Fixed auth headers issue with Docker 1.7.x for private images.
  - Remote build paths: Added 'git@' to the list of valid prefixes.

Client.push(...)
  - Will now raise exceptions if the HTTP status indicates an error.

Client.pull(...)
  - Will now raise exceptions if the HTTP status indicates an error.
```

--------------------------------

TITLE: List Docker Swarm services using docker-py
DESCRIPTION: Illustrates how to list existing Docker Swarm services using the `APIClient.services` method. This method supports optional filters to narrow down the results, such as filtering by service name.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/swarm_services.md

LANGUAGE: python
CODE:
```
client.services(filters={'name': 'mysql'})
```

--------------------------------

TITLE: Docker Container and Image Build/Run Configuration Parameters
DESCRIPTION: Adds new configuration options for building images and running containers, including `cache_from` for builds, and `auto_remove`, `storage_opt`, `stop_timeout` for container lifecycle management.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Image Build Parameters:
  cache_from
    - Supported in APIClient.build and DockerClient.images.build.
    - Specifies images to use as a cache source during the build process.

Container Configuration Parameters:
  auto_remove
    - Supported in APIClient.create_host_config and DockerClient.containers.run.
    - Automatically removes the container when it exits.
  storage_opt
    - Supported in APIClient.create_host_config and DockerClient.containers.run.
    - Specifies storage options for the container, such as size limits.
  stop_timeout
    - Supported in APIClient.create_container and DockerClient.containers.run.
    - Timeout (in seconds) to wait for a container to stop before killing it.
```

--------------------------------

TITLE: Docker Host Configuration and Container Specification Enhancements
DESCRIPTION: This section details new parameters for host configuration, container execution, and the `Mount` object, enabling more granular control over volume consistency, temporary file systems, and named pipes. It also lists new configuration classes for advanced Docker Swarm and container settings.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Host Configuration and Container Run
APIClient.create_host_config(
    ...,
    mounts: list[docker.types.Mount] = None,
    # ... other host config parameters
)
DockerClient.containers.run(
    ...,
    mounts: list[docker.types.Mount] = None,
    # ... other container run parameters
)

# Mount Object Enhancements
docker.types.Mount(
    source: str,
    target: str,
    type: str = 'bind' | 'volume' | 'tmpfs' | 'npipe', # 'tmpfs' and 'npipe' types added
    consistency: str = None, # Added support
    tmpfs_size: int = None, # Added support
    tmpfs_mode: int = None, # Added support
    # ... other mount parameters
)

# Container Specification Enhancements
docker.types.ContainerSpec(
    ...,
    groups: list[str] = None, # Added support
    open_stdin: bool = False, # Added support
    read_only: bool = False, # Added support
    stop_signal: str = None, # Added support
    healthcheck: dict = None, # Added support (assuming dict for healthcheck config)
    hosts: dict = None, # Added support
    ns_config: dict = None, # Added support (assuming dict for namespace config)
    configs: list[docker.types.ConfigReference] = None, # Added support
    privileges: docker.types.Privileges = None, # Added support
    # ... other container spec parameters
)

# New Configuration Classes
docker.types.ConfigReference # New class
docker.types.DNSConfig # New class
docker.types.Privileges # New class
docker.types.SwarmExternalCA # New class
```

--------------------------------

TITLE: Docker-py Core Low-level API Client
DESCRIPTION: Documents the `APIClient` class, which serves as the foundation for the low-level API in `docker-py`. Each method on this client directly maps to a Docker Engine REST API endpoint, providing granular control over Docker operations. While powerful, basic operations might require multiple API calls.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/api.rst

LANGUAGE: APIDOC
CODE:
```
docker.api.client.APIClient
  - Core low-level client for Docker Engine REST API.
  - Each method maps one-to-one with a REST API endpoint.
  - Provides direct access and flexibility for Docker interactions.
```

--------------------------------

TITLE: CPU Real-time Scheduling Parameters for Containers
DESCRIPTION: Introduces parameters for configuring CPU real-time runtime and period, allowing fine-grained control over CPU scheduling for latency-sensitive container workloads.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.create_host_config(..., cpu_rt_runtime: int, cpu_rt_period: int, ...)
DockerClient.containers.run(..., cpu_rt_runtime: int, cpu_rt_period: int, ...)
  - Description: Configures CPU real-time scheduling for containers.
  - Parameters:
    - cpu_rt_runtime: The CPU real-time runtime in microseconds.
    - cpu_rt_period: The CPU real-time period in microseconds.
```

--------------------------------

TITLE: HostConfig Parameter Additions and Fixes
DESCRIPTION: Documents new parameters supported by `HostConfig` for container configuration, including resource allocation and initialization settings, and fixes related to existing parameters.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
HostConfig.nano_cpus
  - Fixed a bug where values exceeding 2^32 would raise a type error.

HostConfig parameters
  - Added support for `volume_driver`, `cpu_count`, `cpu_percent`, `nano_cpus`, `cpuset_mems`.
  - Added support for `init` and `init_path` parameters.
```

--------------------------------

TITLE: Image and Volume Management API Additions
DESCRIPTION: Covers new parameters for image-related operations like building, importing, committing, pushing, and pulling, as well as label support for volume creation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.build(
  path: str = None,
  gzip: bool = False,
  ...
)
  - gzip: Set to True to indicate that the context is gzipped.

Client.import_image(
  src: str,
  changes: str = None,
  ...
)
  - changes: A Dockerfile instruction (e.g., 'CMD ["/bin/bash"]') to apply to the image.

Client.commit(
  container: str,
  changes: str = None,
  ...
)
  - changes: A Dockerfile instruction to apply when committing the container.

Client.push(
  repository: str,
  auth_config: dict = None,
  decode: bool = False,
  ...
)
  - auth_config: A dictionary containing authentication credentials.
  - decode: Decode the streaming response into a dictionary.

Client.pull(
  repository: str,
  decode: bool = False,
  ...
)
  - decode: Decode the streaming response into a dictionary.

Client.create_volume(
  name: str = None,
  labels: dict = None,
  ...
)
  - labels: A dictionary of labels to apply to the volume.
```

--------------------------------

TITLE: Run Docker Container in Foreground with Python
DESCRIPTION: Shows how to execute a command within a new Docker container and capture its output directly. This runs the container in the foreground, blocking until the command completes.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
client.containers.run("ubuntu:latest", "echo hello world")
```

--------------------------------

TITLE: Create a Docker Swarm service using docker-py
DESCRIPTION: Demonstrates how to create a new Docker Swarm service using the `APIClient.create_service` method. This operation requires a `TaskTemplate` object, which is typically constructed from a `ContainerSpec` defining the container's image and command.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/swarm_services.md

LANGUAGE: python
CODE:
```
container_spec = docker.types.ContainerSpec(
    image='busybox', command=['echo', 'hello']
)
task_tmpl = docker.types.TaskTemplate(container_spec)
service_id = client.create_service(task_tmpl, name=name)
```

--------------------------------

TITLE: Docker Client Build and Execution API Updates
DESCRIPTION: Documents updates to container build and execution methods. This includes support for build arguments in `Client.build` and input support for `Client.exec_create`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.build
  - buildargs: Supports passing build arguments to the Docker build process.
Client.exec_create
  - Added input support for executing commands inside a container.
```

--------------------------------

TITLE: Service Scaling with Docker Python SDK
DESCRIPTION: Introduces a convenient shorthand method to scale Docker services by specifying the desired number of replicas. This simplifies service management by abstracting the underlying update service call.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Service.scale(replicas: int)
  - Description: Shorthand method to update a service with the required number of replicas.
  - Parameters:
    - replicas: The desired number of replicas for the service (integer).
```

--------------------------------

TITLE: Stream Docker Container Logs
DESCRIPTION: Demonstrates how to stream logs from a Docker container in real-time using `stream=True`. This allows iterating over each log line as it becomes available, useful for long-running processes.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
for line in container.logs(stream=True):
  print(line.strip())
```

--------------------------------

TITLE: Docker Image Build and Management Enhancements
DESCRIPTION: This section details new parameters for building Docker images, including `squash`, `target`, and `network_mode`. It also describes changes to `load_image` for progress streaming and `remove_image` for response content.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Image Build Enhancements
APIClient.build(
    ...,
    squash: bool = False, # Added support
    target: str = None, # Added support
    network_mode: str = None, # Added support
    # ... other build parameters
)
DockerClient.images.build(
    ..., # All parameters from APIClient.build apply
)

# Image Load Progress Streaming
load_image(
    ...,
    # When using API version 1.23 or above, returns a generator of progress as JSON dicts.
) -> Generator[dict, None, None]

# Image Removal Response Content
remove_image(
    image: str,
    # ... other parameters
) -> dict # Now returns the content of the API's response.
```

--------------------------------

TITLE: Docker-py Client Connection, Login, and Lifecycle API
DESCRIPTION: This section covers updates to `Client` methods related to waiting for container status, user login, and stopping containers. It includes support for custom timeouts and `.dockercfg` paths, and addresses issues with registry URL expansion.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.wait(..., timeout)
  - Adds support for a custom timeout when waiting for a container to stop.
  - Parameters:
    - timeout: Integer, the maximum time to wait in seconds.

Client.login(..., dockercfg_path, registry)
  - Enhances the login functionality for Docker registries.
  - Parameters:
    - dockercfg_path: String, path to a custom `.dockercfg` file.
    - registry: String, the registry URL; now properly expands if provided.

Client.stop(...)
  - Fixed timeout behavior for stopping containers.
```

--------------------------------

TITLE: Stream Docker Container Logs with Python
DESCRIPTION: Demonstrates how to stream logs from a running Docker container in real-time. This is useful for monitoring long-running processes or debugging applications within containers.

SOURCE: https://github.com/docker/docker-py/blob/main/README.md

LANGUAGE: Python
CODE:
```
for line in container.logs(stream=True):
  print(line.strip())
```

--------------------------------

TITLE: Container Host Configuration Enhancements
DESCRIPTION: Documents new parameters added to `Client.create_host_config` for fine-grained control over container resource limits, kernel parameters, and temporary file systems (tmpfs).

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_host_config(
  pids_limit: int = None,
  sysctls: dict = None,
  userns_mode: str = None,
  cpuset_cpus: str = None,
  cpu_shares: int = None,
  mem_reservation: int = None,
  kernel_memory: int = None,
  blkio_weight: int = None,
  blkio_weight_device: list = None,
  device_read_bps: list = None,
  device_write_bps: list = None,
  device_read_iops: list = None,
  device_write_iops: list = None,
  tmpfs: dict = None,
  ...
)
  - pids_limit: Maximum number of PIDs allowed in the container.
  - sysctls: Dictionary of sysctls to set in the container.
  - userns_mode: User namespace mode (e.g., 'host').
  - cpuset_cpus: CPUs in which to allow execution (e.g., '0-3', '0,1').
  - cpu_shares: CPU shares (relative weight).
  - mem_reservation: Memory soft limit (in bytes).
  - kernel_memory: Kernel memory limit (in bytes).
  - blkio_weight: Block IO weight (relative weight).
  - blkio_weight_device: List of block IO weight per device.
  - device_read_bps: List of device read BPS limits.
  - device_write_bps: List of device write BPS limits.
  - device_read_iops: List of device read IOPS limits.
  - device_write_iops: List of device write IOPS limits.
  - tmpfs: Dictionary of tmpfs mounts (e.g., {'/mnt/tmp': 'size=64m'}).
```

--------------------------------

TITLE: Docker-py Client Resource Listing and Filtering API
DESCRIPTION: This section describes enhancements to `Client` methods for retrieving container logs and listing images or containers. It includes support for tailing logs and applying filters to resource listings.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.logs(..., tail)
  - Adds support for tailing container logs.
  - Parameters:
    - tail: Integer, the number of last log lines to retrieve.

Client.images(..., filters)
Client.containers(..., filters)
  - Adds support for filtering results when listing images or containers.
  - Parameters:
    - filters: Dictionary, a set of filters to apply.
```

--------------------------------

TITLE: Docker-py API Mixins for Component Management
DESCRIPTION: This section documents various API mixin classes within `docker-py`, each dedicated to managing specific Docker Engine components. These mixins extend the functionality of the core client, providing methods for configurations, containers, images, networks, volumes, execution, swarms, services, plugins, secrets, and daemon-related operations.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/api.rst

LANGUAGE: APIDOC
CODE:
```
docker.api.config.ConfigApiMixin
docker.api.container.ContainerApiMixin
docker.api.image.ImageApiMixin
docker.api.build.BuildApiMixin
docker.api.network.NetworkApiMixin
docker.api.volume.VolumeApiMixin
docker.api.exec_api.ExecApiMixin
docker.api.swarm.SwarmApiMixin
docker.api.service.ServiceApiMixin
docker.api.plugin.PluginApiMixin
docker.api.secret.SecretApiMixin
docker.api.daemon.DaemonApiMixin
  - Each mixin provides a set of methods for managing specific Docker resources.
  - All public and undocumented members of these classes are exposed as part of the API.
```

--------------------------------

TITLE: Docker Config Collection API
DESCRIPTION: This section outlines the methods available on the `client.configs` collection for managing Docker configurations. It includes functionalities for creating new configs, retrieving existing ones by ID, and listing all available configurations on the Docker daemon.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/configs.rst

LANGUAGE: APIDOC
CODE:
```
ConfigCollection:
  create(...)
    - Creates a new Docker config on the server.
  get(config_id: str)
    - Retrieves a specific Docker config by its ID.
    - Parameters:
      - config_id: The ID of the config to retrieve.
  list(...)
    - Lists all Docker configs available on the server.
```

--------------------------------

TITLE: API Error Handling and Exceptions
DESCRIPTION: Documents the introduction of `docker.errors.NotFound` for 404 API status codes, which inherits from `APIError` for consistent error handling.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
docker.errors.NotFound
  - Raised when a 404 API status is encountered.
  - Inherits from docker.errors.APIError.
```

--------------------------------

TITLE: Other Docker Client and Utility Enhancements
DESCRIPTION: Covers various other new client methods, utility functions, and package attributes introduced to improve Docker interaction, including container renaming, version auto-detection, and error handling.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.rename(container, name)
  - Renames a container.
  - Parameters:
    - container: The container ID or name.
    - name: The new name for the container.
  - Returns: True on success.

Client.__init__(version='auto', ...)
  - Initializes the Docker Client.
  - Parameters:
    - version: String, can be 'auto' to autodetect the daemon's API version.

docker.errors.NullResource
  - Exception raised when a None value is passed as a resource identifier (image or container ID) to a Client method.

docker.utils.ports
  - Package providing tools to parse port ranges.

docker.version_info
  - Attribute of the `docker` package providing version information.

Client.timeout
  - Public attribute for changing request timeouts at runtime.

Client.api_version
  - Read-only property indicating the API version used by the client.
```

--------------------------------

TITLE: Docker Client Archive and Top API Support
DESCRIPTION: Introduces support for the Docker archive API endpoints, enabling retrieval and pushing of archive content. Also notes the addition of `ps_args` parameter for `Client.top`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.get_archive: Retrieves an archive from a container.
Client.put_archive: Puts an archive into a container.
Client.top
  - ps_args: Supports passing arguments to the 'ps' command executed inside the container.
```

--------------------------------

TITLE: Network Creation and Connection API Updates
DESCRIPTION: Describes new parameters for `Client.create_network` and `create_endpoint_config`, enabling more control over network properties like labels, IPv6, internal-only networks, and IP address assignment for connected containers.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_network(
  name: str,
  labels: dict = None,
  enable_ipv6: bool = False,
  internal: bool = False,
  check_duplicate: bool = False,
  ...
)
  - labels: A dictionary of labels to apply to the network.
  - enable_ipv6: Enable IPv6 networking for the network.
  - internal: Restrict external access to the network.
  - check_duplicate: Prevent creating a network with a duplicate name.

create_endpoint_config(
  link_local_ips: list = None,
  ipv4_address: str = None,
  ipv6_address: str = None,
  ...
)
  - link_local_ips: List of link-local IP addresses for the endpoint.
  - ipv4_address: Static IPv4 address for the container on this network.
  - ipv6_address: Static IPv6 address for the container on this network.

Client.connect_container_to_network(
  container: str,
  network: str,
  ipv4_address: str = None,
  ipv6_address: str = None,
  ...
)
  - Allows specifying a static IP address when connecting a container to a network.

Client.disconnect_container_from_network(
  container: str,
  network: str,
  force: bool = False,
  ...
)
  - force: Force the disconnection of the container from the network.
```

--------------------------------

TITLE: Docker Plugin API Methods
DESCRIPTION: Adds comprehensive support for managing Docker plugins, including creation, inspection, enabling/disabling, pulling, pushing, and listing, accessible through `APIClient` and `DockerClient`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient Plugin Methods:
  configure_plugin()
    - Configures an existing plugin.
  create_plugin()
    - Creates a new plugin.
  disable_plugin()
    - Disables a plugin.
  enable_plugin()
    - Enables a plugin.
  inspect_plugin()
    - Inspects details of a plugin.
  pull_plugin()
    - Pulls a plugin from a registry.
  plugins()
    - Lists all plugins.
  plugin_privileges()
    - Retrieves privileges for a plugin.
  push_plugin()
    - Pushes a plugin to a registry.
  remove_plugin()
    - Removes a plugin.

DockerClient Plugin Methods:
  plugins.create()
    - Creates a new plugin.
  plugins.get(plugin_id_or_name)
    - Retrieves a specific plugin by ID or name.
  plugins.install()
    - Installs a plugin.
  plugins.list()
    - Lists all plugins.
  Plugin model
    - Represents a Docker plugin object for programmatic interaction.
```

--------------------------------

TITLE: Docker-py Client Build Process API Enhancements
DESCRIPTION: This section details new parameters for the `Client.build` method, allowing greater control over image pulling and intermediate container removal during the build process. It also highlights support for `.dockerignore` files.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.build(..., pull, forcerm)
  - Adds support for controlling the image build process.
  - Parameters:
    - pull: Boolean, whether to pull the base image.
    - forcerm: Boolean, whether to force removal of intermediate containers.

.dockerignore file support
  - The `Client.build` method now supports processing `.dockerignore` files, ensuring only relevant files are included in the build context.
```

--------------------------------

TITLE: Docker Client Exception Handling and API Versioning
DESCRIPTION: Details on changes to exception handling, API version defaults, and general library behavior.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
DockerException (and subclasses)
  - The client now raises `DockerException`s (from `docker.errors` module) for API errors and other issues.
  - `docker.APIError` has been moved to `docker.errors`.

Default API Version
  - Default API version is now 1.12 (supporting Docker 1.0) as of 0.3.2.
  - Previously 1.9 (as of 0.3.1).
  - Previously 1.8 (as of 0.3.0).
  - Previously 1.6 (as of 0.2.3).

Streaming Responses
  - Streaming responses (e.g., from `logs`, `pull`) no longer yield blank lines.

Requests Library Compatibility
  - The client has been updated to support Requests 2.x (`requests==2.2.1` recommended).
```

--------------------------------

TITLE: Docker Client Host Configuration API Updates
DESCRIPTION: Documents various parameters added to the `Client.create_host_config` method across different docker-py versions. These parameters allow for fine-grained control over container resource limits and settings, such as shared memory size, stop signals, memory swappiness, OOM kill disable, device mappings, group additions, and CPU CFS parameters.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_host_config
  - shm_size: Configures the size of /dev/shm for the container.
  - stop_signal: Sets the signal to stop the container.
  - mem_swappiness: Adjusts the container's memory swappiness.
  - oom_kill_disable: Disables OOM (Out Of Memory) killer for the container.
  - devices: Specifies device mappings for the container.
  - group_add: Adds supplementary group IDs to the container.
  - cpu_quota: Sets the CPU CFS (Completely Fair Scheduler) quota.
  - cpu_period: Sets the CPU CFS period.
```

--------------------------------

TITLE: Greedy Network Listing for Detailed Information
DESCRIPTION: Adds an option to retrieve more comprehensive details when listing Docker networks, providing richer data for network inspection and management.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
DockerClient.networks.list(..., greedy: bool, ...)
  - Description: Lists Docker networks with additional details.
  - Parameters:
    - greedy: If True, includes additional details about the listed networks.
```

--------------------------------

TITLE: Docker-py Configuration and Type Definitions
DESCRIPTION: Documents various data structure classes defined in `docker.types` that are used for configuring Docker objects and operations. These types represent the schema for parameters and return values in the low-level API, covering aspects like container specifications, network attachments, resource limits, and swarm configurations.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/api.rst

LANGUAGE: APIDOC
CODE:
```
docker.types.ConfigReference
docker.types.ContainerSpec
docker.types.DNSConfig
docker.types.DriverConfig
docker.types.EndpointSpec
docker.types.Healthcheck
docker.types.IPAMConfig
docker.types.IPAMPool
docker.types.LogConfig
docker.types.Mount
docker.types.NetworkAttachmentConfig
docker.types.Placement
docker.types.PlacementPreference
docker.types.Privileges
docker.types.Resources
docker.types.RestartPolicy
docker.types.RollbackConfig
docker.types.SecretReference
docker.types.ServiceMode
docker.types.SwarmExternalCA
docker.types.SwarmSpec(*args, **kwargs)
docker.types.TaskTemplate
docker.types.Ulimit
docker.types.UpdateConfig
  - These classes define the structure for various Docker configuration objects and data types.
  - They are used as parameters or return values in the low-level API methods.
```

--------------------------------

TITLE: DockerClient Class Reference
DESCRIPTION: Represents a client for interacting with the Docker daemon, providing programmatic access to various Docker resources and operations. This class can be instantiated directly for manual configuration.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/client.rst

LANGUAGE: APIDOC
CODE:
```
docker.client.DockerClient()
  - Represents a client for interacting with the Docker daemon.
  - Attributes:
    - configs: Access to Docker configs.
    - containers: Access to Docker containers.
    - images: Access to Docker images.
    - networks: Access to Docker networks.
    - nodes: Access to Docker Swarm nodes.
    - plugins: Access to Docker plugins.
    - secrets: Access to Docker secrets.
    - services: Access to Docker Swarm services.
    - swarm: Access to Docker Swarm management.
    - volumes: Access to Docker volumes.
  - Methods:
    - close(): Closes the client connection.
    - df(): Get data usage information from the Docker daemon.
    - events(): Get events from the Docker daemon.
    - info(): Get system information from the Docker daemon.
    - login(): Log in to a Docker registry.
    - ping(): Ping the Docker daemon to check connectivity.
    - version(): Get the Docker version information.
```

--------------------------------

TITLE: Docker Client Volumes API Support
DESCRIPTION: Describes the added support for the Docker Volumes API, introduced in Docker 1.9.0. This set of methods allows for the management of Docker volumes, including listing, creating, inspecting, and removing them.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.volumes: Lists available volumes.
Client.create_volume: Creates a new volume.
Client.inspect_volume: Inspects details of a specific volume.
Client.remove_volume: Removes an existing volume.
```

--------------------------------

TITLE: Docker-py client.services Collection API
DESCRIPTION: Documents the core methods available on the `client.services` object in `docker-py`, which are used to manage Docker Swarm services at a collection level. These methods allow for creating new services, retrieving existing ones by ID, and listing all services.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/services.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.services.ServiceCollection:
  create(image: str, command: list = null, name: str = null, **kwargs)
    - Creates a new service on the Docker Swarm.
    - Parameters:
      - image (str): The image to use for the service.
      - command (list, optional): The command to run in the service containers.
      - name (str, optional): The name of the service.
      - **kwargs: Additional parameters for service creation (e.g., replicas, networks, mounts).
    - Returns: Service object
  get(service_id_or_name: str)
    - Retrieves a specific service by its ID or name.
    - Parameters:
      - service_id_or_name (str): The ID or name of the service to retrieve.
    - Returns: Service object
  list(filters: dict = null)
    - Lists all services currently running on the Docker Swarm, optionally filtered.
    - Parameters:
      - filters (dict, optional): A dictionary of filters to apply.
    - Returns: List of Service objects
```

--------------------------------

TITLE: API: Docker Client Image Pull, Push, and Login Methods
DESCRIPTION: Summarizes updates and fixes related to image pulling, pushing, and user authentication methods within the docker-py Client, including parameter removals, authentication support, and bug fixes for private registries and login persistence.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.pull(repository, tag=None, registry=None, ...)
  - Parameter Removal: Removed unused `registry` parameter.
  - New Feature: Added support for authentication (API version >=1.5).
  - Bugfix: Fixed a bug where private registry images wouldn't be parsed properly if they contained port information.

Client.push(repository, tag=None, ...)
  - Bugfix: Fixed a bug where `Client.push` would break when pushing to private registries.
  - Bugfix: Fixed a bug where it would raise an exception if the auth config wasn't loaded.
  - Bugfix: Fixed a bug where anonymous push/pull would break when no authconfig is present.

Client.login(username, password=None, email=None, ...)
  - Bugfix: Fixed several bugs in `Client.login`. It should now work with API versions 1.4, 1.5.
  - Limitation: `Client.login` currently doesn't write auth to the `.dockercfg` file, thus authentication is not persistent when using this method.
```

--------------------------------

TITLE: Event Monitoring and Utility Functions (Client.events, utils.parse_env_file)
DESCRIPTION: Describes updates to `Client.events` for handling `datetime` arguments and the addition of `utils.parse_env_file` to support environment variable files.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.events(
  ...,
  since: datetime = None,
  until: datetime = None,
  ...
)
  - since: datetime arguments are now always considered UTC.
  - until: datetime arguments are now always considered UTC.

docker.utils.parse_env_file(path: str)
  - Added to support env-files.
```

--------------------------------

TITLE: General API Version and Port Mapping Enhancements
DESCRIPTION: Covers the bumped default API version and new flexibility in port mapping configurations, along with a related bug fix.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Default API Version
  - Has been bumped to `1.26` (Engine 1.13.1+).

Port Mappings
  - Added support for port range to single port (e.g., `8000-8010:80`).
  - Fixed a bug where a missing container port in a port mapping would raise an unexpected `TypeError`.
```

--------------------------------

TITLE: Docker-py Container and Image Management Commands
DESCRIPTION: This section outlines new commands for container lifecycle management, including `execute`, `pause`, and `unpause`. It also details an update to the `remove_image` method for improved ID parameter handling.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
execute command
  - A new command added to the API, likely for executing commands inside a running container.

pause command
  - A new command to pause all processes within a container.

unpause command
  - A new command to unpause all processes within a container.

remove_image(id)
  - Supports a dictionary containing an `Id` key as its `id` parameter, similar to other resource ID methods.
```

--------------------------------

TITLE: Docker-py Client TLS and Registry Security Configuration
DESCRIPTION: This section details updates to TLS configuration, including an option to disable hostname verification, and changes to `Client.push` and `Client.pull` for handling insecure registries. It also covers improvements to the `Client` constructor for base URL parsing and version enforcement, and a utility for environment-based connection parameters.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
TLSConfig(..., assert_hostname)
  - Adds an option to control hostname verification for TLS connections.
  - Parameters:
    - assert_hostname: Boolean, if set to False, disables verification of hostnames.

Client.push(..., insecure_registry)
Client.pull(..., insecure_registry)
  - Adds support for interacting with insecure registries.
  - Parameters:
    - insecure_registry: Boolean, defaults to False. Set to True to allow pushing/pulling from non-HTTPS private registries.

Client(..., version, base_url)
  - Constructor updates for connection parameters.
  - Parameters:
    - version: String, now enforced to be passed as a string.
    - base_url: String, now allows most `DOCKER_HOST` environment values (except fd:// protocol); URLs without a port are now invalid.

docker.utils.kwargs_from_env()
  - A utility method available in `docker.utils` to simplify connecting to the Docker daemon for boot2docker users by extracting connection parameters from environment variables.
```

--------------------------------

TITLE: Configure Docker TLS with CA certificate verification
DESCRIPTION: This snippet demonstrates how to configure a `TLSConfig` object to verify the Docker daemon's server certificate against a specific CA certificate. It then uses this configuration to initialize a `DockerClient` instance, equivalent to `docker --tlsverify --tlscacert ...`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/tls.rst

LANGUAGE: python
CODE:
```
tls_config = docker.tls.TLSConfig(ca_cert='/path/to/ca.pem', verify=True)
client = docker.DockerClient(base_url='<https_url>', tls=tls_config)
```

--------------------------------

TITLE: Docker Swarm Management API (docker.models.swarm)
DESCRIPTION: API reference for managing Docker Engine's swarm mode through the `docker.models.swarm.Swarm` class. This includes methods for swarm initialization, joining, leaving, updating, and retrieving swarm-related information, along with attributes for raw data access.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/swarm.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.swarm.Swarm Class API:

Methods:
  get_unlock_key()
    - Retrieves the unlock key for the swarm.
  init()
    - Initializes a new Docker swarm.
  join()
    - Joins an existing Docker swarm.
  leave()
    - Leaves the current Docker swarm.
  unlock()
    - Unlocks the swarm.
  update()
    - Updates the swarm configuration.
  reload()
    - Reloads the swarm object's data from the server.

Attributes:
  version
    - Represents the version of the swarm object.
  attrs
    - The raw representation of this object from the server.
```

--------------------------------

TITLE: Docker Client Container Creation and Filtering Bugfixes
DESCRIPTION: Details bug fixes related to container creation and filtering. This includes handling of unicode characters in commands and volume binds, and corrections for filter application and memory limit parsing.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.create_container
  - Fixed bug where commands containing unicode characters were incorrectly handled.
Client.volumes
  - Fixed bug where the `filters` parameter would not be applied properly.
Client.create_host_config
  - Fixed bug where the `devices` parameter would sometimes be misinterpreted.
  - Fixed bug where memory limits would parse to incorrect values.
  - Fixed bug where specifying volume binds with unicode characters would fail.
```

--------------------------------

TITLE: Configure Docker TLS with client certificate authentication
DESCRIPTION: This snippet shows how to set up a `TLSConfig` object for client authentication using a client certificate and key pair. The configured `TLSConfig` is then passed to a `DockerClient` instance for secure communication, mirroring `docker --tls --tlscert ... --tlskey ...`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/tls.rst

LANGUAGE: python
CODE:
```
tls_config = docker.tls.TLSConfig(
  client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem')
)
client = docker.DockerClient(base_url='<https_url>', tls=tls_config)
```

--------------------------------

TITLE: Docker Swarm Unlock and Key Retrieval Methods
DESCRIPTION: Introduces API methods for unlocking a Docker Swarm and retrieving the unlock key, crucial for disaster recovery and managing encrypted swarm data.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.unlock_swarm(key: str)
  - Description: Unlocks a Docker Swarm.
  - Parameters:
    - key: The swarm unlock key.

APIClient.get_unlock_key()
  - Description: Retrieves the Docker Swarm unlock key.
  - Returns: The swarm unlock key.

DockerClient.swarm.unlock(key: str)
  - Description: Unlocks a Docker Swarm.
  - Parameters:
    - key: The swarm unlock key.

DockerClient.swarm.get_unlock_key()
  - Description: Retrieves the Docker Swarm unlock key.
  - Returns: The swarm unlock key.
```

--------------------------------

TITLE: Docker ImageCollection Management Methods
DESCRIPTION: Provides methods to manage Docker images on the server, including building, retrieving, listing, loading, pruning, pulling, pushing, searching, and removing images via the `client.images` interface.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/images.rst

LANGUAGE: APIDOC
CODE:
```
ImageCollection:
  build()
  get()
  get_registry_data()
  list(**kwargs)
  load()
  prune()
  pull()
  push()
  remove()
  search()
```

--------------------------------

TITLE: Docker Volume Management Parameters
DESCRIPTION: Enhances volume management with a `force` option for removal and makes the `name` parameter optional during volume creation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Volume Removal Parameters:
  force
    - Supported in APIClient.remove_volume and Volume.remove.
    - Forces the removal of a volume, even if it is in use.

Volume Creation Parameters:
  name
    - Made optional in APIClient.create_volume and DockerClient.volumes.create.
    - Specifies the name of the volume; if omitted, a random name will be generated.
```

--------------------------------

TITLE: Plugin Class Method Additions
DESCRIPTION: Introduces a new method for the `Plugin` class to support upgrade functionality.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Plugin.upgrade()
  - Added new method.
```

--------------------------------

TITLE: API: Miscellaneous Docker Client Methods and General Improvements
DESCRIPTION: Covers various other method updates, bug fixes, and general API improvements across the docker-py library, including support for new API features like UNIX sockets, privileged containers, and enhanced error management.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.port(container_id, private_port)
  - Bugfix: Fixed a bug where `Client.port` would fail if provided with a port of type number.

Client._post_json(url, data)
  - Bugfix: Fixed a bug where `Client._post_json` wouldn't set the Content-Type header to `application/json`.

Client.attach(container_id, ...)
  - New Command: Added `Client.attach` command.

Client.logs(container_id, ...)
  - Bugfix: Improved handling of logs.

Client.images(..., quiet=False)
  - Bugfix: Fixed the `quiet` option.

Client.tag(image_id, repository, tag=None)
  - Bugfix: Fixed a bug in `Client.tag`.

General API Improvements:
  - Added support for API connection through UNIX socket (default for docker 0.5.2+).
  - The client now tries to load the auth config from `~/.dockercfg` (necessary for push command if API version >1.0).
  - Error management overhaul: The new version should be more consistent.
  - Added support for privileged containers.
  - Added API version support.
  - Added bind mounts support.
  - Added support for `ADD` command in builder.
  - Use `shlex` to parse plain string commands when creating a container.
  - Improved error reporting.
```

--------------------------------

TITLE: APIClient Method Enhancements and Fixes
DESCRIPTION: Covers updates to the `APIClient` class, including new method additions, parameter support, and bug fixes for logging, network inspection, and error handling.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient instances
  - Can now be pickled.

APIClient.logs(since: Union[str, datetime])
  - Now raises an exception if the `since` argument uses an unsupported type instead of ignoring the value.

APIClient.inspect_network(verbose: bool)
  - Added support for the `verbose` parameter.

APIClient.exec_create(environment: dict)
  - Added support for the `environment` parameter.

APIClient.reload_config()
  - Added new method that lets the user reload the `config.json` data from disk.

APIClient.create_service(mounts: list)
  - Fixed a bug where a list of `mounts` would sometimes be parsed incorrectly.

APIClient.create_host_config(cpuset_cpus: str)
  - Fixed a bug where the `cpuset_cpus` parameter would not be properly set.

APIClient.upgrade_plugin()
  - Added new method.

APIClient.service_logs()
  - Added new method.

APIClient.df()
  - Added new method.

APIClient.events()
  - Fixed a bug where it would not respect custom headers set in `config.json`.

APIError exceptions
  - Fixed a bug where the `status_code` attribute would not reflect the expected value.

events method (general)
  - Fixed an issue where it would time out unexpectedly if no data was sent by the engine for a given amount of time.
```

--------------------------------

TITLE: Docker Client Monitoring and Event Methods
DESCRIPTION: Introduces enhanced capabilities for monitoring container statistics and events, including new parameters for filtering and decoding output streams.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.stats(container, decode=False, stream=True)
  - Returns a live stream of container's resource usage statistics.
  - Parameters:
    - decode: Boolean, if True, JSON objects are decoded on the fly.

Client.events(since=None, until=None, filters=None, decode=False, stream=True)
  - Returns a live stream of events from the Docker daemon.
  - Parameters:
    - since: Timestamp, only events since this time.
    - until: Timestamp, only events until this time.
    - filters: Dictionary, filters to apply to the event stream.
    - decode: Boolean, if True, JSON objects are decoded on the fly.
```

--------------------------------

TITLE: docker.tls.TLSConfig Class Reference
DESCRIPTION: Documentation for the `TLSConfig` class in `docker-py`, used to configure TLS settings for connecting to the Docker daemon. It allows specifying CA certificates for server verification and client certificates for authentication.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/tls.rst

LANGUAGE: APIDOC
CODE:
```
docker.tls.TLSConfig(ca_cert=None, verify=False, client_cert=None)
  - Description: Configures TLS settings for Docker daemon connections.
  - Parameters:
    - ca_cert (str, optional): Path to the CA certificate file used to verify the Docker daemon's server certificate.
    - verify (bool, optional): If True, the Docker daemon's server certificate will be verified against the provided CA certificate. Defaults to False.
    - client_cert (tuple[str, str], optional): A tuple containing the path to the client certificate file and the path to the client key file, used for client authentication.
  - Usage Examples:
    - Server verification:
      tls_config = docker.tls.TLSConfig(ca_cert='/path/to/ca.pem', verify=True)
    - Client authentication:
      tls_config = docker.tls.TLSConfig(client_cert=('/path/to/client-cert.pem', '/path/to/client-key.pem'))
```

--------------------------------

TITLE: Docker Configs API Operations
DESCRIPTION: This section covers the new API endpoints and client methods for managing Docker configs, including creation, inspection, listing, and removal. It highlights how configs can be referenced within container specifications.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# APIClient Config Methods
APIClient.create_config(
    name: str,
    data: bytes,
    labels: dict = None,
    # ... other parameters
)
APIClient.inspect_config(
    config_id: str,
    # ... other parameters
)
APIClient.remove_config(
    config_id: str,
    # ... other parameters
)
APIClient.configs(
    filters: dict = None,
    # ... other parameters
)

# DockerClient Config Methods and Model
DockerClient.configs.create(
    name: str,
    data: bytes,
    labels: dict = None,
    # ... other parameters
)
DockerClient.configs.get(
    config_id: str,
    # ... other parameters
)
DockerClient.configs.list(
    filters: dict = None,
    # ... other parameters
)
docker.models.configs.Config # New Config model
```

--------------------------------

TITLE: Working Directory Specification for Container Exec Commands
DESCRIPTION: Allows users to define the working directory for commands executed inside a running container, providing flexibility for script execution and file operations within the container's environment.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.exec_create(..., workdir: str, ...)
Container.exec_run(..., workdir: str, ...)
  - Description: Specifies the working directory for the executed command inside the container.
  - Parameters:
    - workdir: The path to the working directory within the container.
```

--------------------------------

TITLE: Docker-py Plugin Object API
DESCRIPTION: Represents a single Docker plugin, providing access to its properties and methods for configuration, state management, and lifecycle operations. This includes enabling, disabling, removing, and upgrading the plugin, as well as accessing its raw server representation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/plugins.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.plugins.Plugin:
  Attributes:
    id: The unique identifier of the plugin.
    short_id: A truncated version of the plugin's ID.
    name: The full name of the plugin.
    enabled: A boolean indicating whether the plugin is currently enabled.
    settings: A dictionary containing the plugin's configuration settings.
    attrs: The raw representation of this plugin object as returned by the Docker daemon API.

  Methods:
    configure(**kwargs)
      - Configure the plugin with new settings.
      - Parameters:
        - **kwargs: Key-value pairs of settings to apply.
    disable(**kwargs)
      - Disable the plugin.
      - Parameters:
        - **kwargs: Optional parameters for disabling.
    enable(**kwargs)
      - Enable the plugin.
      - Parameters:
        - **kwargs: Optional parameters for enabling.
    reload()
      - Reload the plugin's configuration.
    push()
      - Push the plugin to a registry.
    remove(**kwargs)
      - Remove the plugin from the Docker daemon.
      - Parameters:
        - **kwargs: Optional parameters for removal (e.g., 'force').
    upgrade(remote: str, **kwargs)
      - Upgrade the plugin to a new version from a specified remote source.
      - Parameters:
        - remote: The remote source of the new plugin version.
        - **kwargs: Additional parameters for upgrading.
```

--------------------------------

TITLE: Update Configuration Order Argument
DESCRIPTION: Adds an `order` argument to `UpdateConfig`, providing control over the update strategy for services, such as 'stop-first' or 'start-first', ensuring desired deployment behavior.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
UpdateConfig(..., order: str, ...)
  - Description: Specifies the order of operations during a service update.
  - Parameters:
    - order: The update order (e.g., 'stop-first', 'start-first').
```

--------------------------------

TITLE: Docker Network API Scope Enhancements
DESCRIPTION: This section describes the addition of `scope` parameter support for inspecting and creating Docker networks, providing more control over network visibility and reachability.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Network Inspection with Scope
APIClient.inspect_network(
    network_id: str,
    scope: str = None, # Added support
    # ... other parameters
)

# Network Creation with Scope and Ingress
APIClient.create_network(
    name: str,
    driver: str = None,
    scope: str = None, # Added support
    ingress: bool = False, # Added support
    # ... other parameters
)

# DockerClient equivalents also support these parameters.
```

--------------------------------

TITLE: Docker-py Container Collection Management
DESCRIPTION: Methods available on the `client.containers` object for managing Docker containers at a collection level, including running, creating, retrieving, listing, and pruning containers.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/containers.rst

LANGUAGE: APIDOC
CODE:
```
client.containers.run(image, command=None, **kwargs)
  - Runs a new container.
  - Parameters:
    - image: The image to run.
    - command: The command to execute in the container.
    - **kwargs: Additional arguments for container creation.

client.containers.create(image, command=None, **kwargs)
  - Creates a container without starting it.
  - Parameters:
    - image: The image to use.
    - command: The command to execute in the container.
    - **kwargs: Additional arguments for container creation.

client.containers.get(id_or_name)
  - Retrieves a container by its ID or name.
  - Parameters:
    - id_or_name: The ID or name of the container.

client.containers.list(**kwargs)
  - Lists all containers.
  - Parameters:
    - **kwargs: Filters or options for listing containers.

client.containers.prune()
  - Removes all stopped containers.
```

--------------------------------

TITLE: Docker Client Networking API Support
DESCRIPTION: Details the introduction of comprehensive networking API support in docker-py, aligning with Docker 1.9.0. This includes methods for managing networks (creation, removal, inspection) and connecting/disconnecting containers from specific networks.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.networks: Lists available networks.
Client.create_network: Creates a new network.
Client.remove_network: Removes an existing network.
Client.inspect_network: Inspects details of a specific network.
Client.connect_container_to_network: Connects a container to a network.
Client.disconnect_container_from_network: Disconnects a container from a network.
  - Added support for custom IPAM configuration in Client.create_network.
```

--------------------------------

TITLE: Inspect Docker Swarm service configuration using docker-py
DESCRIPTION: Shows how to retrieve detailed information and configuration for a specific Docker Swarm service using the `APIClient.inspect_service` method. The service can be identified by its ID or name.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/swarm_services.md

LANGUAGE: python
CODE:
```
client.inspect_service(service='my_service_name')
```

--------------------------------

TITLE: Container Update and Logging API
DESCRIPTION: Introduces the `Client.update_container` method for modifying container resource configurations and adds a `follow` parameter to `Client.logs` for real-time log streaming.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.update_container(
  container: str,
  blkio_weight: int = None,
  cpu_shares: int = None,
  ...
)
  - container: The ID or name of the container to update.
  - blkio_weight: Block IO weight (relative weight).
  - cpu_shares: CPU shares (relative weight).
  - (Note: This method supports updating various resource configs, similar to create_host_config parameters).

Client.logs(
  container: str,
  follow: bool = False,
  ...
)
  - container: The ID or name of the container.
  - follow: Set to True to stream logs as they are generated.
```

--------------------------------

TITLE: Docker Swarm and Service Update Configuration Parameters
DESCRIPTION: Introduces new parameters for fine-tuning service update behavior in Docker Swarm, including `max_failure_ratio`, `monitor` in `UpdateConfig`, and `force_update` in `TaskTemplate`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Service Update Configuration (UpdateConfig):
  max_failure_ratio
    - Maximum percentage of failed tasks during an update before it's rolled back.
  monitor
    - Duration (in seconds) to monitor a task for failures after it starts before considering the update successful.

Task Template Configuration (TaskTemplate):
  force_update
    - Forces a service update even if no changes are detected, triggering a rolling update.
```

--------------------------------

TITLE: docker-py 3.1.0 API New Features
DESCRIPTION: Details new features and API enhancements introduced in docker-py version 3.1.0, including support for new host configuration options, resource management, and service update mechanisms.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Host Configuration:
  - Added support for device_cgroup_rules in host config.

Resource Management:
  - Added support for generic_resources when creating a Resources object.

Data Transfer:
  - Added support for a configurable chunk_size parameter in export, get_archive, and get_image (Image.save).

Service Management:
  - Added a force_update method to the Service class.
  - In Service.update, when the force_update parameter is set to True, the current force_update counter is incremented by one in the update request.
```

--------------------------------

TITLE: Container Class Method and Property Updates
DESCRIPTION: Summarizes updates to the `Container` class, including logging behavior, execution environment support, and new property additions.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Container.logs(since: Union[str, datetime])
  - Now raises an exception if the `since` argument uses an unsupported type instead of ignoring the value.

Container.exec_run(environment: dict)
  - Added support for the `environment` parameter.

Container.labels
  - Added new property.

Container.image
  - Added new property.
```

--------------------------------

TITLE: DockerClient API Updates and Bug Fixes
DESCRIPTION: This section details various enhancements and bug fixes related to the `DockerClient` class, including property accessibility, method parameter support, and corrected behaviors across different versions.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
docker.from_env
  - Fixed a bug where instantiating `DockerClient` wouldn't correctly set the default timeout value.

DockerClient.secrets
  - Now accessible as a property.

DockerClient.build
  - Fixed a bug where it would sometimes return the wrong image.

DockerClient.networks.get(verbose: bool)
  - Added support for the `verbose` parameter.

DockerClient.images.build
  - Fixed reporting a failure after a successful build if a `tag` was set.

DockerClient.images.pull
  - Fixed failure to return the corresponding image object if a `tag` was set.

DockerClient.containers.run(init: bool, init_path: str)
  - Added support for `init` and `init_path` parameters.

DockerClient.containers.run(network: str)
  - The invalid `networks` argument has been replaced with a working singular `network` argument.

DockerClient.df()
  - Added new method.

DockerClient.service.create(hostname: str)
  - Added support for `hostname` parameter in `ContainerSpec`.

DockerClient.events()
  - Fixed a bug where it would not respect custom headers set in `config.json`.
```

--------------------------------

TITLE: Docker RegistryData Object Attributes and Methods
DESCRIPTION: Describes the RegistryData object, which provides access to raw server representation, identifiers, and methods for checking platform compatibility, pulling, and reloading registry data.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/images.rst

LANGUAGE: APIDOC
CODE:
```
RegistryData:
  Attributes:
    attrs: The raw representation of this object from the server.
    id
    short_id
  Methods:
    has_platform()
    pull()
    reload()
```

--------------------------------

TITLE: Docker Type Definitions and Healthcheck Configuration
DESCRIPTION: This section details new configuration options for `TaskTemplate`, `ContainerSpec`, and `Healthcheck` types, providing more granular control over swarm service tasks, container properties, and health monitoring.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Task Template Configuration
docker.types.TaskTemplate(
    ...,
    placement: dict = None, # Added support for placement configuration
    # ... other task template parameters
)

# Container Specification Configuration
docker.types.ContainerSpec(
    ...,
    tty: bool = False, # Added support for tty configuration
    # ... other container spec parameters
)

# Healthcheck Configuration
docker.types.Healthcheck(
    ...,
    start_period: int = None, # Added support for start_period configuration
    # ... other healthcheck parameters
)
```

--------------------------------

TITLE: API: Docker Client Container Lifecycle & Management Methods
DESCRIPTION: Documents breaking changes and new behaviors for various container lifecycle management methods within the docker-py Client, including parameter changes and new commands. It also notes a general update for container ID arguments.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.kill(container_id, ...)
  - Breaking Change: No longer supports varargs.
  - Note: This change also applies to Client.remove_container, Client.remove_image, Client.restart, Client.start, Client.stop, and Client.wait.

Client.remove_container(container_id, ...)
  - Behavior Change: Now raises an exception when attempting to remove a running container.

Client.start(container_id, ..., lxc_conf=None)
  - New Parameter: `lxc_conf` (configuration for LXC).

Client.create_container(..., environment=None)
  - Parameter Update: The `environment` parameter now accepts dictionary objects.
  - Bugfix: Fixed parsing of unicode commands on Python 2.6.
  - Bugfix: Removed obsolete custom error message.

Client.top(container_id)
  - New Command: Retrieves top processes of a container.

Client.copy(container_id, resource)
  - New Command: Copies files/folders from a container.

Client.containers(..., quiet=False)
  - Bugfix: Fixed a bug where the `quiet` parameter wouldn't be taken into account.

General API Update:
  - All methods that expected a container ID as argument now also support a dictionary containing an `Id` key.
```

--------------------------------

TITLE: Platform Specification for Docker Image Operations
DESCRIPTION: Adds support for specifying the target platform (e.g., linux/amd64, windows/arm64) during Docker image build and pull operations, enhancing cross-platform compatibility and enabling multi-architecture image management.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.build(..., platform: str, ...)
DockerClient.images.build(..., platform: str, ...)
APIClient.pull(..., platform: str, ...)
DockerClient.images.pull(..., platform: str, ...)
  - Description: Specifies the target platform for the image build or pull operation.
  - Parameters:
    - platform: A string representing the target platform (e.g., "linux/amd64").
```

--------------------------------

TITLE: Service Class Method and Parameter Updates
DESCRIPTION: Details updates to the `Service` class, including validation for replicas and new logging capabilities.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
ServiceMode.replicas
  - Fixed a bug where setting `replicas` to zero would not register as a valid entry.

Service.logs()
  - Added new method.
```

--------------------------------

TITLE: Custom Detach Keys for Attach and Exec Operations
DESCRIPTION: Allows users to override the default detach key sequence for interactive attach and exec sessions, providing a customizable exit mechanism. If unspecified, the value from the `config.json` file will be used.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.attach_socket(..., detach_keys: str, ...)
APIClient.exec_create(..., detach_keys: str, ...)
  - Description: Specifies the key sequence to detach from the container.
  - Parameters:
    - detach_keys: A string representing the key sequence (e.g., "ctrl-p,ctrl-q"). If unspecified, uses value from config.json.
```

--------------------------------

TITLE: Service Update with Current Specification Fetch
DESCRIPTION: Enhances service update functionality by allowing the API to fetch the service's current configuration and merge it with provided parameters, simplifying partial updates and ensuring consistency.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.update_service(..., fetch_current_spec: bool, ...)
Service.update(..., fetch_current_spec: bool, ...)
  - Description: Retrieves the current service configuration and merges it with provided parameters for the update.
  - Parameters:
    - fetch_current_spec: If True, the current service spec is fetched and merged before applying updates.
```

--------------------------------

TITLE: Image Class Property and Method Updates
DESCRIPTION: Details changes to the `Image` class, including the addition of new properties and corrections to method return values.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Image.tag()
  - Now properly returns `True` when the operation is successful.

Image.labels
  - Added new property.
```

--------------------------------

TITLE: Docker Service Inspection Defaults
DESCRIPTION: This section highlights the new `insert_defaults` parameter for service inspection, allowing users to retrieve service configurations with default values populated.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Service Inspection with Default Insertion
APIClient.inspect_service(
    service_id: str,
    insert_defaults: bool = False, # Added support
    # ... other parameters
)
DockerClient.services.get(
    service_id: str,
    insert_defaults: bool = False, # Added support
    # ... other parameters
)
```

--------------------------------

TITLE: Docker Pruning API Methods
DESCRIPTION: Introduces new methods for pruning unused Docker resources (containers, images, networks, volumes) via both `APIClient` and `DockerClient` interfaces.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient Pruning Methods:
  prune_containers()
    - Removes stopped containers.
  prune_images()
    - Removes unused images.
  prune_networks()
    - Removes unused networks.
  prune_volumes()
    - Removes unused volumes.

DockerClient Pruning Methods:
  containers.prune()
    - Removes stopped containers.
  images.prune()
    - Removes unused images.
  networks.prune()
    - Removes unused networks.
  volumes.prune()
    - Removes unused volumes.
```

--------------------------------

TITLE: Docker Container Runtime and Lifecycle Fixes
DESCRIPTION: This section addresses bug fixes related to container runtime behavior, including the `auto_remove` parameter, and improved handling of TTY-enabled containers during `attach` and `exec_run` operations. It also notes a fix for service creation with dictionary task templates.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Container Runtime Parameter Fix
DockerClient.containers.run(
    ...,
    auto_remove: bool = False, # Fixed: now correctly taken into account.
    runtime: str = None, # Added support
    # ... other parameters
)
APIClient.create_container(
    ...,
    runtime: str = None, # Added support
    # ... other parameters
)

# TTY Handling Fixes
attach(
    ...,
    # Fixed: improved handling of TTY-enabled containers.
)
exec_run(
    ...,
    # Fixed: improved handling of TTY-enabled containers.
)

# Service Creation/Update Task Template Fix
create_service(
    ...,
    task_template: dict, # Fixed: no longer raises exception when dict is used.
)
update_service(
    ...,
    task_template: dict, # Fixed: no longer raises exception when dict is used.
)
```

--------------------------------

TITLE: Docker-py Container Object Reference
DESCRIPTION: Attributes and methods available on individual `Container` objects, providing detailed information and control over a specific Docker container.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/containers.rst

LANGUAGE: APIDOC
CODE:
```
Container Attributes:
  attrs: The raw representation of this object from the server.
  id: The ID of the container.
  image: The image used by the container.
  labels: Labels associated with the container.
  name: The name of the container.
  short_id: The short ID of the container.
  status: The current status of the container.

Container Methods:
  attach()
    - Attaches to the container's stdout and stderr.
  attach_socket()
    - Attaches to the container's socket.
  commit(repository=None, tag=None, message=None, author=None, changes=None, conf=None)
    - Commits the container as a new image.
  diff()
    - Returns a diff of the changes to the container's filesystem.
  exec_run(cmd, stdout=True, stderr=True, stdin=False, tty=False, privileged=False, user='', detach=False, stream=False, socket=False, environment=None, workdir=None, demux=False)
    - Runs a command inside the container.
  export()
    - Exports the container's filesystem as a tar archive.
  get_archive(path)
    - Retrieves an archive of a path in the container.
  kill(signal=None)
    - Kills the container.
  logs(stdout=True, stderr=True, stream=False, follow=False, since=None, until=None, timestamps=False, tail='all')
    - Retrieves logs from the container.
  pause()
    - Pauses the container.
  put_archive(path, data)
    - Puts an archive of data into the container at a given path.
  reload()
    - Reloads the container's attributes from the server.
  remove(v=False, link=False, force=False)
    - Removes the container.
  rename(name)
    - Renames the container.
  resize(height, width)
    - Resizes the TTY of the container.
  restart(timeout=10)
    - Restarts the container.
  start()
    - Starts the container.
  stats(stream=False, decode=False)
    - Retrieves statistics for the container.
  stop(timeout=10)
    - Stops the container.
  top(ps_args=None)
    - Displays the running processes in the container.
  unpause()
    - Unpauses the container.
  update(blkio_weight=None, cpu_period=None, cpu_quota=None, cpu_shares=None, cpuset_cpus=None, cpuset_mems=None, mem_limit=None, mem_reservation=None, memswap_limit=None, kernel_memory=None, restart_policy=None)
    - Updates the container's resource limits.
  wait(timeout=None, condition=None)
    - Waits for the container to stop, or for a given condition.
```

--------------------------------

TITLE: Docker Client Logging and Statistics API Enhancements
DESCRIPTION: Covers enhancements to the `Client.logs` and `Client.stats` methods. These updates provide more control over retrieving container logs (e.g., 'since' parameter) and statistics (e.g., single snapshot vs. stream).

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.logs
  - since: Filters logs to those generated since a specific timestamp (API version 1.19+).
  - tail=0: No longer shows past logs when set to 0.
Client.stats
  - stream: When set to `False`, allows retrieving a single snapshot of stats instead of a constant data stream.
```

--------------------------------

TITLE: Docker Swarm Node Object Reference (docker-py)
DESCRIPTION: The `Node` object in `docker-py` encapsulates the properties and actions associated with a single Docker Swarm node. It exposes attributes like `id`, `short_id`, `attrs`, and `version`, along with methods to `reload` its state from the server and `update` its configuration.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/nodes.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.nodes.Node():
  id (str): The unique ID of the node.
  short_id (str): A truncated version of the node's ID.
  attrs (dict): The raw representation of this object from the server.
  version (dict): The version information of the node.
  reload():
    - Reloads the attributes of the node from the Docker daemon.
  update():
    - Updates the node's properties on the Docker daemon.
```

--------------------------------

TITLE: Network Class Method Fixes
DESCRIPTION: Addresses bug fixes related to the `Network` class, specifically concerning container association and parameter acceptance for connection methods.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Network.containers()
  - Fixed a bug where it would crash when no containers were associated with the network.

Network.connect()
  - Fixed an issue where it would not accept some of the documented parameters.

Network.disconnect()
  - Fixed an issue where it would not accept some of the documented parameters.
```

--------------------------------

TITLE: Run a Docker Container in Background
DESCRIPTION: Illustrates how to run a Docker container in detached mode using the `detach=True` argument. This allows the container to run in the background without blocking the current Python process, returning a Container object.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/index.rst

LANGUAGE: python
CODE:
```
client.containers.run("bfirsh/reticulate-splines", detach=True)
```

--------------------------------

TITLE: Docker Client Image Pull/Push and Port Mapping Updates
DESCRIPTION: Addresses bug fixes related to image pull/push operations and port mapping. This includes handling of unicode characters in credentials and image names, and corrections for port protocol priority.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Client.pull
  - Fixed bug where image names containing a dot caused failures.
Client.push
  - Fixed bug where image names containing a dot caused failures.
  - Fixed bug where auth config credentials containing unicode characters caused failures.
Client.port
  - Fixed bug where explicit protocol failed to yield expected result.
  - Fixed bug where priority protocol returned was UDP instead of TCP.
```

--------------------------------

TITLE: Time-Bound Log Retrieval for Docker Containers
DESCRIPTION: Enables fetching container logs up to a specific timestamp, providing more granular control over log retrieval for debugging, analysis, and historical data collection.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.logs(..., until: datetime, ...)
Container.logs(..., until: datetime, ...)
  - Description: Retrieves logs up to the specified timestamp.
  - Parameters:
    - until: A datetime object or timestamp string indicating the end time for log retrieval.
```

--------------------------------

TITLE: Docker Config Object API
DESCRIPTION: This section describes the attributes and methods of a single `Config` object within the `docker-py` library. It covers properties like `id`, `name`, and `attrs` (raw server representation), as well as methods to `reload` its state from the server and `remove` the config.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/configs.rst

LANGUAGE: APIDOC
CODE:
```
Config():
  id: str
    - The unique identifier of the config object.
  name: str
    - The name of the config object.
  attrs: dict
    - The raw representation of this object from the server, containing all its properties.
  reload()
    - Reloads the config object's attributes from the server to update its state.
  remove()
    - Removes the config object from the Docker server.
```

--------------------------------

TITLE: Conditional Waiting for Docker Container States
DESCRIPTION: Introduces the ability to wait for a container to reach a specific condition (e.g., 'not-running', 'removed'), improving orchestration and automation workflows by allowing precise state-based synchronization.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient.wait(..., condition: str, ...)
Container.wait(..., condition: str, ...)
  - Description: Waits for the container to reach a specified condition.
  - Parameters:
    - condition: The condition to wait for (e.g., 'not-running', 'removed').
```

--------------------------------

TITLE: Docker Volume Collection Management (docker-py)
DESCRIPTION: Provides methods on `client.volumes` to manage collections of Docker volumes, including creating new volumes, retrieving existing ones by ID, listing all volumes with optional filters, and pruning unused volumes.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/volumes.rst

LANGUAGE: APIDOC
CODE:
```
VolumeCollection:
  create(...)
    - Creates a new Docker volume.
  get(volume_id: str)
    - Retrieves a specific Docker volume by its ID.
  list(**kwargs)
    - Lists all Docker volumes, optionally filtered by various criteria.
  prune(**kwargs)
    - Removes unused Docker volumes based on specified filters.
```

--------------------------------

TITLE: Execute Docker Command with Demultiplexed Tuple Output (stream=False, demux=True) in Python
DESCRIPTION: Demonstrates `container.exec_run` with `stream=False` and `demux=True`. The output is a single tuple `(stdout_string, stderr_string)`, providing the complete stdout and stderr as separate elements.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/multiplex.rst

LANGUAGE: python
CODE:
```
res = container.exec_run(cmd, stream=False, demux=True)
res.output
```

--------------------------------

TITLE: Flexible Port Publishing Modes in EndpointSpec
DESCRIPTION: Enhances port mapping capabilities by allowing users to specify a publish mode (e.g., 'ingress', 'host') for ports within the `EndpointSpec` for services, offering more control over network exposure.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
EndpointSpec Port Mapping Syntax:
{published_port: (target_port, protocol, publish_mode)}
  - Description: Defines how a service port is published.
  - Parameters:
    - published_port: The port on the host or ingress network.
    - target_port: The port inside the container.
    - protocol: The network protocol (e.g., 'tcp', 'udp').
    - publish_mode: The mode of publishing ('ingress' or 'host').
```

--------------------------------

TITLE: Docker Image Object Attributes and Methods
DESCRIPTION: Defines the structure and available operations for a Docker Image object, including access to its raw server representation, identifiers, labels, tags, and methods for retrieving history, reloading, saving, and tagging.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/images.rst

LANGUAGE: APIDOC
CODE:
```
Image:
  Attributes:
    attrs: The raw representation of this object from the server.
    id
    labels
    short_id
    tags
  Methods:
    history()
    reload()
    save()
    tag()
```

--------------------------------

TITLE: Container Isolation Parameter for Services
DESCRIPTION: Adds support for defining the isolation technology (e.g., 'process', 'hyperv' on Windows) for containers created as part of a service, providing more control over security and resource separation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
ContainerSpec(..., isolation: str, ...)
DockerClient.services.create(..., isolation: str, ...)
Service.update(..., isolation: str, ...)
  - Description: Specifies the isolation technology for the container.
  - Parameters:
    - isolation: The isolation mode (e.g., 'process', 'hyperv').
```

--------------------------------

TITLE: Docker Secrets API Enhancements
DESCRIPTION: This section details the added support for specifying a `driver` when creating Docker secrets, allowing for custom secret storage backends.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
# Secret Creation with Driver Support
APIClient.create_secret(
    name: str,
    data: bytes,
    labels: dict = None,
    driver: dict = None, # Added support for driver
    # ... other parameters
)
DockerClient.secrets.create(
    name: str,
    data: bytes,
    labels: dict = None,
    driver: dict = None, # Added support for driver
    # ... other parameters
)
```

--------------------------------

TITLE: Execute Docker Command with Combined Output (stream=False, demux=False) in Python
DESCRIPTION: Demonstrates `container.exec_run` when both `stream` and `demux` are set to `False`. The output is returned as a single string containing both stdout and stderr, with no stream separation.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/multiplex.rst

LANGUAGE: python
CODE:
```
res = container.exec_run(cmd, stream=False, demux=False)
res.output
```

--------------------------------

TITLE: Docker Volume Object Reference (docker-py)
DESCRIPTION: Defines the attributes and methods available on a `Volume` object, allowing access to its properties like ID and name, and performing actions such as reloading its state from the server or removing the volume.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/volumes.rst

LANGUAGE: APIDOC
CODE:
```
Volume():
  id: str
    - The full ID of the volume.
  short_id: str
    - The short ID of the volume.
  name: str
    - The name of the volume.
  attrs: dict
    - The raw representation of this object from the server.
  reload()
    - Reloads the volume's attributes from the Docker daemon.
  remove(**kwargs)
    - Removes the volume from the Docker daemon.
```

--------------------------------

TITLE: Docker API Breaking Changes (Version 2.0.0)
DESCRIPTION: Details significant breaking changes introduced in docker-py 2.0.0, including class renames, method behavior changes, package structure adjustments, and minimum API version requirements.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
Class Renames:
  docker.Client renamed to docker.APIClient

Client Instantiation:
  docker.from_env now creates a DockerClient instance (was APIClient).

Removed Parameters:
  HostConfig parameters removed from APIClient.start.

Minimum API Version:
  Minimum supported API version is now 1.21 (Engine version 1.9.0+).

Package Naming:
  pip package name is now 'docker' (was 'docker-py').
  New versions will only be published as 'docker'.

Module Path Changes:
  docker.ssladapter moved to docker.transport.ssladapter.
  Package structure flattened, affecting imports for docker.auth and docker.utils.ports.
  docker.utils.types moved to docker.types.

Removed Utility Functions (Replaced by Types):
  create_host_config removed from docker.utils. Replaced by docker.types.HostConfig.
  create_ipam_pool removed from docker.utils. Replaced by docker.types.IPAMPool.
  create_ipam_config removed from docker.utils. Replaced by docker.types.IPAMConfig.
```

--------------------------------

TITLE: Docker-py Service Object API
DESCRIPTION: Details the attributes and methods of the `Service` object in `docker-py`, providing programmatic access to individual Docker Swarm service properties and actions. This includes retrieving service metadata, forcing updates, managing logs, scaling, and removal.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/services.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.services.Service:
  Attributes:
    id (str): The unique ID of the service.
    short_id (str): A short version of the service ID.
    name (str): The name of the service.
    version (str): The version of the service.
    attrs (dict): The raw representation of this object from the server, containing all service details.

  Methods:
    force_update()
      - Forces an update of the service, typically used to redeploy tasks.
    logs(stdout: bool = true, stderr: bool = true, stream: bool = false, follow: bool = false, since: int = 0, tail: str = 'all', **kwargs)
      - Retrieves logs for the service.
      - Parameters:
        - stdout (bool, optional): Get stdout logs.
        - stderr (bool, optional): Get stderr logs.
        - stream (bool, optional): Stream logs.
        - follow (bool, optional): Follow log output.
        - since (int, optional): Only logs since this timestamp (Unix epoch).
        - tail (str, optional): Number of lines to show from the end of the logs ('all' or integer).
        - **kwargs: Additional parameters for log retrieval (e.g., timestamps).
    reload()
      - Reloads the service object's data from the Docker daemon, refreshing its attributes.
    remove()
      - Removes the service from the Docker Swarm.
    scale(replicas: int)
      - Scales the service to a specified number of replicas.
      - Parameters:
        - replicas (int): The desired number of replicas for the service.
    tasks(filters: dict = null)
      - Retrieves the tasks associated with the service, optionally filtered.
      - Parameters:
        - filters (dict, optional): A dictionary of filters to apply.
    update(**kwargs)
      - Updates the service configuration.
      - Parameters:
        - **kwargs: Parameters to update (e.g., image, command, replicas, networks, mounts).
```

--------------------------------

TITLE: docker-py 3.0.0 API Breaking Changes and Deprecations
DESCRIPTION: Documents significant API changes introduced in docker-py version 3.0.0, including removed methods and parameters, renamed parameters, and modifications to method return values. Users should review these changes for migration.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
API Version Support:
  - Support for API version < 1.21 has been removed.

Removed Methods:
  - APIClient.copy: Use APIClient.get_archive instead.
  - APIClient.insert: Use APIClient.put_archive combined with APIClient.commit.
  - utils.ping_registry
  - utils.ping

Removed Parameters:
  - stream: In APIClient.build
  - cpu_shares, cpuset, dns, mem_limit, memswap_limit, volume_driver, volumes_from: In APIClient.create_container (replaced by create_host_config)
  - insecure_registry: In APIClient.login, APIClient.pull, APIClient.push, DockerClient.images.push, DockerClient.images.pull
  - viz: In APIClient.images

Renamed Parameters:
  - endpoint_config: In APIClient.create_service and APIClient.update_service, renamed to endpoint_spec.
  - name: In DockerClient.images.pull, renamed to repository.

Changed Return Values:
  - APIClient.wait, Container.wait: Now return a dict representing the API's response (previously status code).
  - DockerClient.images.load: Now returns a list of Image objects for loaded images (previously log stream).
  - Container.exec_run: Now returns a tuple of (exit_code, output) (previously just output).
  - DockerClient.images.build: Now returns a tuple of (image, build_logs) (previously just image object).
  - APIClient.export, APIClient.get_archive, APIClient.get_image: Now return generators streaming raw binary data.
  - DockerClient.images.pull (no tag provided): Now returns a list of Image objects associated with the pulled repository (previously just the 'latest' image).
```

--------------------------------

TITLE: Execute Docker Command with Streaming Combined Output (stream=True, demux=False) in Python
DESCRIPTION: Illustrates `container.exec_run` with `stream=True` and `demux=False`. The output is a generator that yields strings, where each string contains a chunk of the combined stdout and stderr.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/multiplex.rst

LANGUAGE: python
CODE:
```
res = container.exec_run(cmd, stream=True, demux=False)
next(res.output)
next(res.output)
```

--------------------------------

TITLE: Execute Docker Command with Streaming Demultiplexed Output (stream=True, demux=True) in Python
DESCRIPTION: Shows `container.exec_run` with `stream=True` and `demux=True`. The output is a generator that yields tuples `(stdout_chunk, stderr_chunk)`, allowing separate processing of stdout and stderr streams.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/multiplex.rst

LANGUAGE: python
CODE:
```
res = container.exec_run(cmd, stream=True, demux=True)
next(res.output)
next(res.output)
```

--------------------------------

TITLE: Update Docker Swarm service configuration using docker-py
DESCRIPTION: Explains how to update an existing Docker Swarm service's configuration using the `APIClient.update_service` method. A mandatory `version` argument, obtained from `APIClient.inspect_service`, is required to prevent concurrent writes and ensure data consistency.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/swarm_services.md

LANGUAGE: python
CODE:
```
container_spec = docker.types.ContainerSpec(
    image='busybox', command=['echo', 'hello world']
)
task_tmpl = docker.types.TaskTemplate(container_spec)

svc_version = client.inspect_service(svc_id)['Version']['Index']

client.update_service(
    svc_id, svc_version, name='new_name', task_template=task_tmpl
)
```

--------------------------------

TITLE: Manage Docker Swarm Nodes with NodeCollection (docker-py)
DESCRIPTION: This section details the `NodeCollection` class within `docker-py`, which provides functionalities to retrieve a specific Docker Swarm node by its identifier or to list all available nodes in the swarm. It serves as the primary interface for querying node information.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/nodes.rst

LANGUAGE: APIDOC
CODE:
```
docker.models.nodes.NodeCollection:
  get(id_or_name):
    - Retrieves a single Docker Swarm node by its ID or name.
    - Parameters:
      - id_or_name (str): The ID or name of the node to retrieve.
    - Returns: Node object
  list(**kwargs):
    - Lists all Docker Swarm nodes.
    - Parameters:
      - **kwargs: Additional keyword arguments for filtering nodes (e.g., filters).
    - Returns: list of Node objects
```

--------------------------------

TITLE: Docker Secret API Methods
DESCRIPTION: Introduces API support for managing Docker secrets, allowing creation, inspection, and removal of secrets, along with integration into container specifications.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
APIClient Secret Methods:
  create_secret()
    - Creates a new secret.
  inspect_secret(secret_id_or_name)
    - Inspects details of a secret.
  remove_secret(secret_id_or_name)
    - Removes a secret.
  secrets()
    - Lists all secrets.

DockerClient Secret Methods:
  secret.create()
    - Creates a new secret.
  secret.get(secret_id_or_name)
    - Retrieves a specific secret by ID or name.
  secret.list()
    - Lists all secrets.
  Secret model
    - Represents a Docker secret object for programmatic interaction.

ContainerSpec Integration:
  secrets parameter in ContainerSpec
    - A list of docker.types.SecretReference instances to attach secrets to a container.
```

--------------------------------

TITLE: TLS Protocol Default for Docker Connections
DESCRIPTION: Updates the default TLS protocol used for Docker connections to TLSv1.2 when available, enhancing security for communications with the Docker daemon.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/change-log.md

LANGUAGE: APIDOC
CODE:
```
TLS Connection Protocol:
  - Default: TLSv1.2 (when available)
  - Description: Enhances security for Docker API communications by defaulting to TLSv1.2.
```

--------------------------------

TITLE: Docker SecretCollection API Methods
DESCRIPTION: Provides methods to interact with Docker secrets at a collection level, allowing creation, retrieval, and listing of secrets managed by the Docker daemon. These methods are typically accessed via `client.secrets`.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/secrets.rst

LANGUAGE: APIDOC
CODE:
```
SecretCollection:
  create(name: str, data: bytes, labels: dict = None, driver: dict = None)
    - Description: Creates a new secret on the Docker daemon.
    - Parameters:
      - name (str): The name of the secret.
      - data (bytes): The secret data.
      - labels (dict, optional): User-defined key/value labels for the secret.
      - driver (dict, optional): Driver options for the secret.
    - Returns: Secret object
  get(secret_id: str)
    - Description: Retrieves a specific secret by its ID.
    - Parameters:
      - secret_id (str): The ID of the secret to retrieve.
    - Returns: Secret object
  list(filters: dict = None)
    - Description: Lists all secrets managed by the Docker daemon.
    - Parameters:
      - filters (dict, optional): A dictionary of filters to apply (e.g., {'name': 'my_secret'}).
    - Returns: List of Secret objects
```

--------------------------------

TITLE: Remove a Docker Swarm service using docker-py
DESCRIPTION: Demonstrates how to remove a Docker Swarm service using the `APIClient.remove_service` method. The service to be removed can be specified by either its name or its ID.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/user_guides/swarm_services.md

LANGUAGE: python
CODE:
```
client.remove_service('my_service_name')
```

--------------------------------

TITLE: Docker Secret Object API
DESCRIPTION: Represents an individual Docker secret object, providing access to its attributes and methods for reloading its state or removing it from the Docker daemon. Instances of this class are returned by `SecretCollection` methods.

SOURCE: https://github.com/docker/docker-py/blob/main/docs/secrets.rst

LANGUAGE: APIDOC
CODE:
```
Secret():
  id: string
    - Description: The unique ID of the secret.
  name: string
    - Description: The name of the secret.
  attrs: dict
    - Description: The raw representation of this object from the server, containing all secret attributes and metadata.
  reload()
    - Description: Reloads the secret's attributes from the Docker daemon, updating the object's state with the latest information.
    - Returns: None
  remove()
    - Description: Removes the secret from the Docker daemon. This action is irreversible.
    - Returns: None
```