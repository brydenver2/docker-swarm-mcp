"""
Pytest configuration and fixtures for docker-swarm-mcp tests
"""

import pytest
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient
from app.main import app


class MockDockerClient:
    """Lightweight mock Docker client for deterministic testing"""
    
    def __init__(self):
        self.ping_called = False
        self.list_containers_called = False
        self.create_container_called = False
        
    def ping(self):
        """Mock ping that always succeeds"""
        self.ping_called = True
        return True
        
    def list_containers(self, all=False, filters=None):
        """Mock list_containers returning deterministic data"""
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
        """Mock create_container returning deterministic response"""
        self.create_container_called = True
        return {
            "id": "new-container-789",
            "name": config.get("name", "unnamed"),
            "status": "created",
            "image": config.get("image", "scratch"),
            "created": "2025-01-01T02:00:00Z"
        }
        
    def start_container(self, container_id):
        """Mock start_container"""
        return {}
        
    def stop_container(self, container_id, timeout=10):
        """Mock stop_container"""
        return {}
        
    def remove_container(self, container_id, force=False):
        """Mock remove_container"""
        return {}
        
    def get_logs(self, container_id, tail=100, since=None, follow=False):
        """Mock get_logs returning deterministic logs"""
        return "Mock log line 1\nMock log line 2\nMock log line 3"
        
    def list_stacks(self):
        """Mock list_stacks"""
        return [
            {
                "project_name": "test-stack",
                "services": ["web", "db"],
                "service_count": 2
            }
        ]
        
    def deploy_compose(self, project_name, compose_yaml, force_recreate=False):
        """Mock deploy_compose"""
        return {
            "project_name": project_name,
            "services": ["web", "db"],
            "mode": "replicated",
            "created": "2025-01-01T03:00:00Z"
        }
        
    def remove_compose(self, project_name):
        """Mock remove_compose"""
        return {}
        
    def list_services(self):
        """Mock list_services"""
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
        """Mock scale_service"""
        return {
            "id": "service-123",
            "name": service_name,
            "replicas": replicas,
            "image": "nginx:latest",
            "created": "2025-01-01T04:00:00Z",
            "mode": "replicated"
        }
        
    def remove_service(self, service_name):
        """Mock remove_service"""
        return {}
        
    def list_networks(self):
        """Mock list_networks"""
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
        """Mock create_network"""
        return {
            "id": "new-network-456",
            "name": config.get("name", "unnamed"),
            "driver": config.get("driver", "bridge"),
            "scope": "local",
            "created": "2025-01-01T06:00:00Z"
        }
        
    def remove_network(self, network_id):
        """Mock remove_network"""
        return {}
        
    def list_volumes(self):
        """Mock list_volumes"""
        return [
            {
                "name": "test-volume",
                "driver": "local",
                "mountpoint": "/var/lib/docker/volumes/test-volume",
                "created": "2025-01-01T07:00:00Z"
            }
        ]
        
    def create_volume(self, config):
        """Mock create_volume"""
        return {
            "name": config.get("name", "unnamed"),
            "driver": config.get("driver", "local"),
            "mountpoint": f"/var/lib/docker/volumes/{config.get('name', 'unnamed')}",
            "created": "2025-01-01T08:00:00Z"
        }
        
    def remove_volume(self, volume_name):
        """Mock remove_volume"""
        return {}


@pytest.fixture
def mock_docker_client():
    """Fixture providing a mock Docker client"""
    return MockDockerClient()


@pytest.fixture
def test_client_with_mock(mock_docker_client):
    """Fixture providing TestClient with mocked Docker client"""
    # Override the app state with mock client
    app.state.docker_client = mock_docker_client
    
    # Ensure other required state is initialized
    from app.mcp.tool_registry import ToolRegistry
    from app.mcp.tool_gating import FilterConfig, ToolGateController
    from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP
    from app.mcp.intent_classifier import KeywordIntentClassifier
    import json
    import os
    
    tool_registry = ToolRegistry()
    all_tools = tool_registry.get_all_tools()
    
    # Load actual filter config from filter-config.json
    filter_config_data = {}
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "filter-config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
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
            with open(config_path, 'r') as f:
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
    
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Setup test environment variables"""
    monkeypatch.setenv("MCP_ACCESS_TOKEN", "test-token-123")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("MCP_TIMEOUT_READ_OPS", "5")  # Faster tests
    monkeypatch.setenv("MCP_TIMEOUT_WRITE_OPS", "5")
    monkeypatch.setenv("MCP_TIMEOUT_DELETE_OPS", "5")


# Test token for authentication
TEST_TOKEN = "test-token-123"