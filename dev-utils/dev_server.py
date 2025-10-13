#!/usr/bin/env python3
"""
Development server for docker-swarm-mcp with mock Docker client
Run this to test MCP endpoints without requiring Docker connectivity
"""

import os
import sys

import uvicorn

# Set environment variables BEFORE importing app modules
os.environ['MCP_ACCESS_TOKEN'] = '98a0305163506ea4f95b9b6c206ac459c4cfa3aeb97c24b31c89660e5d33f928'
os.environ['LOG_LEVEL'] = 'DEBUG'
os.environ['MCP_TRANSPORT'] = 'http'
os.environ['ALLOWED_ORIGINS'] = 'http://localhost:3000,http://localhost:8080'

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app
from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP
from app.mcp.tool_gating import FilterConfig, ToolGateController
from app.mcp.tool_registry import ToolRegistry


class MockDockerClient:
    """Lightweight mock Docker client for development testing"""

    def __init__(self):
        """
        Initialize the mock client state with boolean flags tracking which API methods have been invoked.
        
        Attributes:
            ping_called (bool): True if `ping()` has been called.
            list_containers_called (bool): True if `list_containers()` has been called.
            create_container_called (bool): True if `create_container()` has been called.
        """
        self.ping_called = False
        self.list_containers_called = False
        self.create_container_called = False

    def ping(self):
        """
        Mark the mock client as pinged and report availability.
        
        Sets the instance attribute `ping_called` to True.
        
        Returns:
            True if the mock ping is successful.
        """
        self.ping_called = True
        return True

    def list_containers(self, all=False, filters=None):
        """
        Return a deterministic list of mock container records and mark that listing was invoked.
        
        Parameters:
            all (bool): If True, include non-running containers; otherwise include default set.
            filters (dict | None): Optional dictionary of filter criteria (ignored by mock).
        
        Returns:
            list[dict]: A list of container dictionaries with keys `id`, `name`, `status`, `image`, and `created`.
        """
        self.list_containers_called = True
        return [
            {
                "id": "abc123",
                "name": "test-container-1",
                "status": "running",
                "image": "nginx:latest",
                "created": "2025-01-01T00:00:00Z"
            },
            {
                "id": "def456",
                "name": "test-container-2",
                "status": "stopped",
                "image": "redis:alpine",
                "created": "2025-01-01T01:00:00Z"
            }
        ]

    def create_container(self, config):
        """
        Create a mock container record using values from the provided configuration.
        
        Parameters:
            config (dict): Container configuration; may include 'name' and 'image' to populate the returned record.
        
        Returns:
            dict: Container representation with keys 'id', 'name', 'status', 'image', and 'created'. 'name' and 'image' reflect values from `config` when present.
        """
        self.create_container_called = True
        return {
            "id": "new-container-789",
            "name": config.get("name", "unnamed"),
            "status": "created",
            "image": config.get("image", "scratch"),
            "created": "2025-01-01T02:00:00Z"
        }

    def start_container(self, container_id):
        """
        Start a mock container with the given container identifier.
        
        Parameters:
            container_id (str): Identifier of the container to start.
        
        Returns:
            dict: An empty dictionary representing a mocked start response.
        """
        return {}

    def stop_container(self, container_id, timeout=10):
        """
        Stop a container in the mock Docker client.
        
        Parameters:
            container_id (str): Identifier of the container to stop.
            timeout (int): Seconds to wait before forcefully stopping the container.
        
        Returns:
            dict: Mocked response object (empty dictionary).
        """
        return {}

    def remove_container(self, container_id, force=False):
        """
        Remove a container from the mock Docker client's state.
        
        Parameters:
        	container_id (str): Identifier or name of the container to remove.
        	force (bool): If True, force removal even if the container is running.
        
        Returns:
        	dict: An empty dictionary representing the mocked removal result.
        """
        return {}

    def get_logs(self, container_id, tail=100, since=None, follow=False):
        """
        Provide mock container logs as a single newline-delimited string.
        
        Parameters:
            container_id (str): Identifier of the container to retrieve logs for.
            tail (int): Maximum number of most recent log lines to include.
            since (int | float | None): Unix timestamp (seconds) to include logs from, or None to include all.
            follow (bool): Whether to indicate streaming (continuous) logs.
        
        Returns:
            str: Newline-delimited mock log lines.
        """
        return "Mock log line 1\nMock log line 2\nMock log line 3"

    def list_stacks(self):
        """
        Return a deterministic list of mock stack summaries.
        
        Returns:
            list[dict]: List of stacks where each dict contains:
                - project_name (str): stack name
                - services (list[str]): names of services in the stack
                - service_count (int): number of services in the stack
        """
        return [
            {
                "project_name": "test-stack",
                "services": ["web", "db"],
                "service_count": 2
            }
        ]

    def deploy_compose(self, project_name, compose_yaml, force_recreate=False):
        """
        Deploy a Docker Compose project into the mock environment.
        
        Parameters:
            project_name (str): Name of the compose project.
            compose_yaml (str): Docker Compose YAML content used for deployment.
            force_recreate (bool): If True, indicate services should be force-recreated (mocked behavior).
        
        Returns:
            dict: Deployment summary with keys:
                - `project_name` (str): The deployed project's name.
                - `services` (list[str]): Names of services included in the deployment.
                - `mode` (str): Deployment mode (e.g., "replicated").
                - `created` (str): ISO 8601 timestamp when the mock deployment was created.
        """
        return {
            "project_name": project_name,
            "services": ["web", "db"],
            "mode": "replicated",
            "created": "2025-01-01T03:00:00Z"
        }

    def remove_compose(self, project_name):
        """
        Remove a deployed Compose project from the mock Docker client state.
        
        Parameters:
            project_name (str): Name of the Compose project to remove.
        
        Returns:
            dict: An empty dictionary indicating the mock removal result.
        """
        return {}

    def list_services(self):
        """
        Return a deterministic list of mock service metadata for development testing.
        
        Returns:
            list[dict]: A list of service objects where each object contains:
                - id (str): Unique service identifier.
                - name (str): Service name.
                - replicas (int): Number of desired replicas.
                - image (str): Container image reference.
                - created (str): ISO 8601 UTC timestamp of creation.
                - mode (str): Service mode (e.g., "replicated").
        """
        return [
            {
                "id": "service-123",
                "name": "test-service",
                "replicas": 3,
                "image": "nginx:latest",
                "created": "2025-01-01T04:00:00Z",
                "mode": "replicated"
            }
        ]

    def scale_service(self, service_name, replicas):
        """
        Return a dictionary representing a service scaled to the requested replica count.
        
        Parameters:
            service_name (str): Name of the service to scale.
            replicas (int): Desired number of replicas for the service.
        
        Returns:
            dict: Service representation with keys:
                - id (str): Service identifier.
                - name (str): Service name (matches `service_name`).
                - replicas (int): Number of replicas (matches `replicas`).
                - image (str): Service image.
                - created (str): ISO-8601 creation timestamp.
                - mode (str): Service mode (e.g., "replicated").
        """
        return {
            "id": "service-123",
            "name": service_name,
            "replicas": replicas,
            "image": "nginx:latest",
            "created": "2025-01-01T04:00:00Z",
            "mode": "replicated"
        }

    def remove_service(self, service_name):
        """
        Remove a mocked service from the in-memory Docker state.
        
        Parameters:
            service_name (str): Name of the service to remove.
        
        Returns:
            dict: An empty dictionary indicating the mock removal succeeded.
        """
        return {}

    def list_networks(self):
        """
        Return a deterministic list of mock network metadata.
        
        Returns:
            list: A list of dictionaries, each representing a network with the following keys:
                - id (str): Unique network identifier.
                - name (str): Network name.
                - driver (str): Network driver (e.g., "bridge").
                - scope (str): Network scope (e.g., "local").
                - created (str): Creation timestamp in ISO 8601 format.
        """
        return [
            {
                "id": "network-123",
                "name": "test-network",
                "driver": "bridge",
                "scope": "local",
                "created": "2025-01-01T05:00:00Z"
            }
        ]

    def create_network(self, config):
        """
        Create a mock network record using values from the provided configuration.
        
        Parameters:
            config (dict): Configuration for the network; may include `name` and `driver`. Missing keys default to `"unnamed"` for `name` and `"bridge"` for `driver`.
        
        Returns:
            dict: A network representation with keys `id`, `name`, `driver`, `scope`, and `created`.
        """
        return {
            "id": "new-network-456",
            "name": config.get("name", "unnamed"),
            "driver": config.get("driver", "bridge"),
            "scope": "local",
            "created": "2025-01-01T06:00:00Z"
        }

    def remove_network(self, network_id):
        """
        Simulate removal of a network identified by `network_id` from the mock Docker client.
        
        Parameters:
            network_id (str): The identifier or name of the network to remove.
        
        Returns:
            dict: An empty dictionary (mocked response).
        """
        return {}

    def list_volumes(self):
        """
        Return a deterministic mock list of Docker volumes for development/testing.
        
        The returned list contains one volume dictionary describing its name, storage driver,
        mountpoint path, and creation time.
        
        Returns:
            list[dict]: A list of volume objects. Each object has the following keys:
                - name (str): Volume name.
                - driver (str): Storage driver (e.g., "local").
                - mountpoint (str): Filesystem path where the volume is mounted.
                - created (str): Creation timestamp as an ISO 8601 UTC string.
        """
        return [
            {
                "name": "test-volume",
                "driver": "local",
                "mountpoint": "/var/lib/docker/volumes/test-volume",
                "created": "2025-01-01T07:00:00Z"
            }
        ]

    def create_volume(self, config):
        """
        Create a deterministic mock volume record from the provided configuration.
        
        Parameters:
            config (dict): Volume configuration. Recognized keys:
                - "name": desired volume name (defaults to "unnamed").
                - "driver": storage driver name (defaults to "local").
        
        Returns:
            dict: A volume representation with the following keys:
                - "name": the volume name.
                - "driver": the volume driver.
                - "mountpoint": filesystem path for the volume, based on the name.
                - "created": ISO 8601 timestamp when the mock volume was created.
        """
        return {
            "name": config.get("name", "unnamed"),
            "driver": config.get("driver", "local"),
            "mountpoint": f"/var/lib/docker/volumes/{config.get('name', 'unnamed')}",
            "created": "2025-01-01T08:00:00Z"
        }

    def remove_volume(self, volume_name):
        """
        Remove a mocked volume by name.
        
        Parameters:
            volume_name (str): Name of the volume to remove.
        
        Returns:
            dict: Empty dictionary representing a successful mock removal response.
        """
        return {}


def setup_mock_app_state():
    """
    Initialize the FastAPI application state with a mock Docker client and MCP components.
    
    Sets the following app.state attributes:
    - docker_client: MockDockerClient used for development/testing
    - tool_registry: ToolRegistry instance
    - tool_gate_controller: ToolGateController configured with an empty task-type allowlist, a max tools limit of 10, and an empty blocklist
    - mcp_server: DynamicToolGatingMCP constructed from the tool registry and tool gate controller
    """

    # Create mock Docker client
    mock_docker_client = MockDockerClient()

    # Initialize MCP components
    tool_registry = ToolRegistry()
    all_tools = tool_registry.get_all_tools()

    filter_config = FilterConfig(
        task_type_allowlists={},
        max_tools=10,
        blocklist=[]
    )

    tool_gate_controller = ToolGateController(
        all_tools=all_tools,
        config=filter_config
    )

    mcp_server = DynamicToolGatingMCP(tool_registry, tool_gate_controller)

    # Set app state
    app.state.docker_client = mock_docker_client
    app.state.tool_registry = tool_registry
    app.state.tool_gate_controller = tool_gate_controller
    app.state.mcp_server = mcp_server


def main():
    """
    Start the development Uvicorn server configured to use a mock Docker client.
    
    Sets up application state with mock components for testing (mock Docker client, tool registry, tool gate controller, and MCP server), prints development startup information and URLs, and runs the ASGI server on 0.0.0.0:8000.
    """

    print("🚀 Starting Docker Swarm MCP Server in development mode with mock Docker client")
    print("📋 Mock Docker client - no real Docker connectivity required")
    print("🔗 Server will be available at: http://localhost:8000")
    print("🔑 MCP endpoint: http://localhost:8000/mcp/ (note trailing slash)")
    print("💚 Health endpoint: http://localhost:8000/mcp/health")
    print("")

    # Setup mock app state
    setup_mock_app_state()

    # Run the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="debug"
    )


if __name__ == "__main__":
    main()