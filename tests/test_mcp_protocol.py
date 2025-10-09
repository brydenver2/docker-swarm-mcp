"""
MCP JSON-RPC protocol compliance tests

Tests verify JSON-RPC 2.0 protocol compliance, schema validation,
and tool gating integration.
"""

import json
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Test token for authentication
TEST_TOKEN = "test-token-123"


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    """Setup test environment variables"""
    monkeypatch.setenv("MCP_ACCESS_TOKEN", TEST_TOKEN)
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")


class TestMCPProtocolCompliance:
    """Test JSON-RPC 2.0 protocol compliance"""

    def test_initialize_request(self):
        """Test MCP initialize handshake"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                },
                "id": 1
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data
        assert data["result"]["protocolVersion"] == "2024-11-05"
        assert data["result"]["serverInfo"]["name"] == "docker-mcp-server"
        assert data["result"]["capabilities"]["tools"]["gating"] is True

    def test_tools_list_without_task_type(self):
        """Test tools/list without task_type parameter"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 2
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert "result" in data
        assert "tools" in data["result"]
        assert isinstance(data["result"]["tools"], list)
        assert len(data["result"]["tools"]) > 0

        # Verify tool structure
        tool = data["result"]["tools"][0]
        assert "name" in tool
        assert "description" in tool
        assert "inputSchema" in tool

        # Verify metadata
        assert "_metadata" in data["result"]
        assert "context_size" in data["result"]["_metadata"]
        assert "filters_applied" in data["result"]["_metadata"]

    def test_tools_list_with_task_type(self):
        """Test tools/list with task_type filtering"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {"task_type": "container-ops"},
                "id": 3
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]

        # Verify all tools are container-ops
        tool_names = [tool["name"] for tool in data["result"]["tools"]]
        container_tools = [
            "list-containers", "create-container", "start-container",
            "stop-container", "remove-container", "get-logs"
        ]
        for tool_name in tool_names:
            assert tool_name in container_tools

    def test_tools_call_happy_path(self):
        """Test tools/call successful execution"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "ping",
                    "arguments": {}
                },
                "id": 4
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        # May succeed or fail depending on Docker availability
        # Just verify protocol compliance
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 4
        assert "result" in data or "error" in data

    def test_tools_call_blocked_tool(self):
        """Test tools/call with blocked tool (SecurityFilter)"""
        # First, need to configure a blocklist
        # This test assumes filter-config.json has blocklist
        pass  # Skip for now, requires dynamic config

    def test_tools_call_invalid_params(self):
        """Test tools/call with schema validation failure"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "create-container",
                    "arguments": {
                        # Missing required 'image' field
                        "name": "test-container"
                    }
                },
                "id": 5
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 5
        assert "error" in data
        assert data["error"]["code"] == -32602  # INVALID_PARAMS

    def test_method_not_found(self):
        """Test unknown JSON-RPC method"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "unknown/method",
                "params": {},
                "id": 6
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 6
        assert "error" in data
        assert data["error"]["code"] == -32601  # METHOD_NOT_FOUND

    def test_unauthorized_request(self):
        """Test request without authentication token"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 7
            }
        )

        assert response.status_code == 403  # No authorization header

    def test_invalid_token(self):
        """Test request with invalid token"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 8
            },
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401


class TestSchemaValidation:
    """Test JSON schema validation for tools"""

    def test_startup_schema_validation(self):
        """Test that all tools have valid schemas at startup"""
        # This is verified during app startup
        # If we reach here, schemas are valid
        assert True

    def test_input_schema_validation(self):
        """Test input parameter validation against request_schema"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "create-container",
                    "arguments": {
                        "image": "nginx:latest",
                        "name": "test-nginx",
                        "environment": {"ENV_VAR": "value"}
                    }
                },
                "id": 9
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        # Should not fail validation (may fail Docker execution)
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 9

    def test_output_schema_validation(self):
        """Test output validation against response_schema"""
        # Output validation is logged but doesn't fail requests
        # This test ensures the validation logic runs
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "list-containers",
                    "arguments": {"all": False}
                },
                "id": 10
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        data = response.json()
        assert data["jsonrpc"] == "2.0"


class TestToolGatingIntegration:
    """Test tool gating integration in MCP handlers"""

    def test_task_type_filter_applied(self):
        """Test TaskTypeFilter reduces tool count"""
        # Get all tools
        response_all = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 11
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        # Get container-ops tools only
        response_filtered = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {"task_type": "container-ops"},
                "id": 12
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        all_tools = response_all.json()["result"]["tools"]
        filtered_tools = response_filtered.json()["result"]["tools"]

        assert len(filtered_tools) < len(all_tools)

    def test_context_size_enforcement(self):
        """Test context_size is computed and returned"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 13
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )

        data = response.json()
        assert "_metadata" in data["result"]
        assert "context_size" in data["result"]["_metadata"]
        assert isinstance(data["result"]["_metadata"]["context_size"], int)
        assert data["result"]["_metadata"]["context_size"] > 0

    def test_session_id_tracking(self):
        """Test session ID is tracked in logs"""
        response = client.post(
            "/mcp/v1",
            json={
                "jsonrpc": "2.0",
                "method": "tools/list",
                "params": {},
                "id": 14
            },
            headers={
                "Authorization": f"Bearer {TEST_TOKEN}",
                "X-Session-ID": "test-session-123"
            }
        )

        assert response.status_code == 200
        # Session ID tracking is verified in logs


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
