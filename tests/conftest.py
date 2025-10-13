"""
Pytest configuration and fixtures for docker-swarm-mcp tests
"""

import os

import pytest
from fastapi.testclient import TestClient

# Set environment variables before importing app
os.environ.setdefault("MCP_ACCESS_TOKEN", "test-token-123")
os.environ.setdefault("LOG_LEVEL", "DEBUG")
os.environ.setdefault("EXPOSE_ENDPOINTS_IN_HEALTHZ", "true")

from app.main import app


class MockDockerClient:
    """Lightweight mock Docker client for deterministic testing"""

    def __init__(self):
        """
        Initialize the mock client with boolean flags that track whether key Docker operations were invoked.
        
        Each of ping_called, list_containers_called, and create_container_called is initialized to False and should be set to True by the corresponding method when that operation is performed.
        """
        self.ping_called = False
        self.list_containers_called = False
        self.create_container_called = False

    def ping(self):
        """
        Record that the mock client was pinged.
        
        Returns:
            True indicating the mock client is reachable.
        """
        self.ping_called = True
        return True

    def list_containers(self, all=False, filters=None):
        """
        Return a deterministic list of mock container descriptors for testing.
        
        Returns:
            list[dict]: Two container dictionaries with keys "id", "name", "status", "image", and "created".
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
        Create a deterministic mock container record from the provided config and mark the create call.
        
        Parameters:
            config (dict): Container configuration; may include "name" and "image" keys used to populate the returned record.
        
        Returns:
            dict: A container dictionary with keys:
                - id: deterministic container id
                - name: container name (from config "name" or "unnamed")
                - status: "created"
                - image: image name (from config "image" or "scratch")
                - created: ISO-8601 timestamp of creation
        
        Side effects:
            Sets self.create_container_called = True.
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
        Start a container in the mock Docker client.
        
        Parameters:
            container_id (str): Identifier of the container to start.
        
        Returns:
            dict: An empty dictionary representing a successful no-op start operation.
        """
        return {}

    def stop_container(self, container_id, timeout=10):
        """
        Stop a container in the mock Docker client.
        
        Parameters:
            container_id (str): Identifier of the container to stop.
            timeout (int): Seconds to wait for graceful shutdown before forcing stop (default 10).
        
        Returns:
            dict: Empty dictionary representing the mock operation result.
        """
        return {}

    def remove_container(self, container_id, force=False):
        """
        Remove a container from the mock Docker client.
        
        Parameters:
            container_id (str): Identifier of the container to remove.
            force (bool): If True, request a forced removal (ignored by the mock).
        
        Returns:
            dict: Empty dictionary representing a successful no-op removal.
        """
        return {}

    def get_logs(self, container_id, tail=100, since=None, follow=False):
        """
        Return a deterministic multiline mock log string for a container.
        
        Parameters:
            container_id (str): Identifier of the container whose logs are being requested.
            tail (int): Number of most recent log lines to include.
            since (Optional[Union[int, str]]): Start time for logs (timestamp or string).
            follow (bool): If true, indicates logs should be streamed.
        
        Returns:
            str: Multiline string of mock log lines separated by newline characters.
        """
        return "Mock log line 1\nMock log line 2\nMock log line 3"

    def list_stacks(self):
        """
        Return a deterministic list of mock stack summaries for testing.
        
        Each stack entry is a dictionary with the stack's project name, the service names, and the total service count.
        
        Returns:
            list[dict]: List of stack summaries. Each dictionary contains:
                - project_name (str): Name of the stack/project.
                - services (list[str]): Names of services in the stack.
                - service_count (int): Number of services in the stack.
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
        Simulate deploying a Docker Compose project and return a deterministic deployment summary.
        
        Parameters:
            project_name (str): Name of the compose project.
            compose_yaml (str): Docker Compose YAML content used for the deployment.
            force_recreate (bool): If True, indicates services should be force-recreated (no effect in mock).
        
        Returns:
            dict: Deployment summary containing:
                - project_name (str): The provided project name.
                - services (list[str]): List of service names in the deployment.
                - mode (str): Deployment mode (e.g., "replicated").
                - created (str): ISO-8601 timestamp of the mock creation time.
        """
        return {
            "project_name": project_name,
            "services": ["web", "db"],
            "mode": "replicated",
            "created": "2025-01-01T03:00:00Z"
        }

    def remove_compose(self, project_name):
        """
        Remove a compose project from the mock Docker client (no-op for tests).
        
        Parameters:
            project_name (str): Name of the compose project to remove.
        
        Returns:
            dict: An empty dictionary.
        """
        return {}

    def list_services(self):
        """
        Return a deterministic list of mock service dictionaries for tests.
        
        Returns:
            list[dict]: A list containing a single mock service entry with fixed fields:
                - id: "service-123"
                - name: "test-service"
                - replicas: 3
                - image: "nginx:latest"
                - created: "2025-01-01T04:00:00Z"
                - mode: "replicated"
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
        Provide a deterministic mock representation of a service scaled to the requested replica count.
        
        Parameters:
        	service_name (str): Name of the service to scale.
        	replicas (int): Desired number of replicas for the service.
        
        Returns:
        	dict: Mocked service dictionary with keys `id`, `name`, `replicas`, `image`, `created`, and `mode`.
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
        Remove a service in the mock Docker client and record that the operation was invoked.
        
        Parameters:
            service_name (str): Name or identifier of the service to remove.
        
        Returns:
            dict: An empty dictionary representing a no-op removal result.
        """
        return {}

    def list_networks(self):
        """
        Return a deterministic list of mock Docker network metadata for tests.
        
        Returns:
            list: A list of network dictionaries. Each dictionary contains the keys
                `id` (str), `name` (str), `driver` (str), `scope` (str), and
                `created` (ISO 8601 timestamp string).
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
        Create a deterministic mock network object using values from the provided config.
        
        Parameters:
            config (dict): Network creation options. Recognized keys:
                - "name": desired network name (defaults to "unnamed").
                - "driver": network driver (defaults to "bridge").
        
        Returns:
            dict: A network representation with keys:
                - "id": fixed identifier for the created network.
                - "name": network name from `config` or the default.
                - "driver": network driver from `config` or the default.
                - "scope": network scope ("local").
                - "created": ISO-8601 timestamp string representing creation time.
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
        Remove a network from the mock Docker client state.
        
        Parameters:
        	network_id (str): Identifier of the network to remove.
        
        Returns:
        	result (dict): An empty dictionary representing a no-op removal result.
        """
        return {}

    def list_volumes(self):
        """
        Return a deterministic list of mock Docker volumes.
        
        Each item is a dict with the following keys:
        - "name": volume name.
        - "driver": volume driver.
        - "mountpoint": filesystem path where the volume is mounted.
        - "created": ISO 8601 UTC creation timestamp.
        
        Returns:
            list[dict]: A list containing one mock volume dictionary.
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
        Create a deterministic mock volume representation using the provided configuration.
        
        Parameters:
            config (dict): Volume configuration; recognized keys:
                - "name": volume name (defaults to "unnamed")
                - "driver": volume driver (defaults to "local")
        
        Returns:
            dict: Volume record with keys:
                - "name": the volume name
                - "driver": the volume driver
                - "mountpoint": constructed mount path based on the name
                - "created": ISO 8601 creation timestamp
        """
        return {
            "name": config.get("name", "unnamed"),
            "driver": config.get("driver", "local"),
            "mountpoint": f"/var/lib/docker/volumes/{config.get('name', 'unnamed')}",
            "created": "2025-01-01T08:00:00Z"
        }

    def remove_volume(self, volume_name):
        """
        Simulate removing a Docker volume from the mock client.
        
        Parameters:
            volume_name (str): Name of the volume to remove.
        
        Returns:
            dict: An empty dictionary.
        """
        return {}


@pytest.fixture
def mock_docker_client():
    """Fixture providing a mock Docker client"""
    return MockDockerClient()


@pytest.fixture
def test_client_with_mock(mock_docker_client, monkeypatch):
    """
    Provide a TestClient for the FastAPI app wired with a mocked Docker client and initialized MCP components.
    
    This fixture patches app.docker_client.get_docker_client to return the provided mock, injects the mock into app.state.docker_client, and initializes tool_registry, tool_gate_controller, intent_classifier, and mcp_server in app.state using any available filter-config.json values (with safe fallbacks).
    
    Returns:
        TestClient: A TestClient wrapping the FastAPI app configured to use the mocked Docker client and initialized MCP components.
    """
    # Stub get_docker_client before constructing TestClient
    monkeypatch.setattr('app.docker_client.get_docker_client', lambda: mock_docker_client)

    # Override the app state with mock client
    app.state.docker_client = mock_docker_client

    # Ensure other required state is initialized
    import json
    import os

    from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP
    from app.mcp.intent_classifier import KeywordIntentClassifier
    from app.mcp.tool_gating import FilterConfig, ToolGateController
    from app.mcp.tool_registry import ToolRegistry

    tool_registry = ToolRegistry()
    all_tools = tool_registry.get_all_tools()

    # Load actual filter config from filter-config.json
    filter_config_data = {}
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "filter-config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                filter_config_data = json.load(f)
    except Exception:
        # Fallback to empty config if file read fails
        pass

    filter_config = FilterConfig(
        task_type_allowlists=filter_config_data.get("task_type_allowlists", {}),
        max_tools=filter_config_data.get("max_tools", 10),
        blocklist=filter_config_data.get("blocklist", [])
    )

    tool_gate_controller = ToolGateController(
        all_tools=all_tools,
        config=filter_config
    )

    # Initialize intent classifier with keyword mappings
    keyword_mappings = None
    try:
        # Try to read filter-config.json for intent keywords
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "filter-config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config_data = json.load(f)
                keyword_mappings = config_data.get("intent_keywords")
    except Exception:
        # Fallback to default mappings if file read fails
        pass

    intent_classifier = KeywordIntentClassifier(keyword_mappings)

    mcp_server = DynamicToolGatingMCP(tool_registry, tool_gate_controller, intent_classifier)

    app.state.tool_registry = tool_registry
    app.state.tool_gate_controller = tool_gate_controller
    app.state.mcp_server = mcp_server
    app.state.intent_classifier = intent_classifier

    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """
    Configure deterministic environment variables used by tests.
    
    This fixture sets the following environment variables to stable, test-friendly values:
    - MCP_ACCESS_TOKEN="test-token-123"
    - LOG_LEVEL="DEBUG"
    - MCP_TIMEOUT_READ_OPS="5"
    - MCP_TIMEOUT_WRITE_OPS="5"
    - MCP_TIMEOUT_DELETE_OPS="5"
    """
    monkeypatch.setenv("MCP_ACCESS_TOKEN", "test-token-123")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("MCP_TIMEOUT_READ_OPS", "5")  # Faster tests
    monkeypatch.setenv("MCP_TIMEOUT_WRITE_OPS", "5")
    monkeypatch.setenv("MCP_TIMEOUT_DELETE_OPS", "5")


# Test token for authentication (matches setup_test_env fixture)
TEST_TOKEN = "test-token-123"