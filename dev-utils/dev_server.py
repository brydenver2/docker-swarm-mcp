#!/usr/bin/env python3
"""
Development server for docker-swarm-mcp with mock Docker client
Run this to test MCP endpoints without requiring Docker connectivity
"""

import os
import sys
import uvicorn
from unittest.mock import Mock

# Set environment variables BEFORE importing app modules
os.environ['MCP_ACCESS_TOKEN'] = '98a0305163506ea4f95b9b6c206ac459c4cfa3aeb97c24b31c89660e5d33f928'
os.environ['LOG_LEVEL'] = 'DEBUG'
os.environ['MCP_TRANSPORT'] = 'http'
os.environ['ALLOWED_ORIGINS'] = 'http://localhost:3000,http://localhost:8080'

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app
from app.mcp.tool_registry import ToolRegistry
from app.mcp.tool_gating import FilterConfig, ToolGateController
from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP


class MockDockerClient:
    """Lightweight mock Docker client for development testing"""
    
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


def setup_mock_app_state():
    """Setup app state with mock Docker client and MCP components"""
    
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
    """Run the development server with mock Docker client"""
    
    print("🚀 Starting Docker Swarm MCP Server in development mode with mock Docker client")
    print("📋 Mock Docker client - no real Docker connectivity required")
    print("🔗 Server will be available at: http://localhost:8000")
    print("🔑 MCP endpoint: http://localhost:8000/mcp/v1/ (note trailing slash)")
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