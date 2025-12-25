"""Test error handling for HTTPException in MCP protocol"""

import pytest
from fastapi import HTTPException

from tests.conftest import TEST_TOKEN


class TestHTTPExceptionHandling:
    """Test that HTTPException from docker_client is properly handled"""

    def test_get_logs_container_not_found(self, test_client_with_mock, monkeypatch):
        """Test get-logs with container not found returns proper error"""
        
        # Monkeypatch the get_logs to raise HTTPException like docker_client does
        def mock_get_logs_not_found(container_id, tail=100, since=None, follow=False):
            raise HTTPException(status_code=404, detail="Container not found")
        
        # Get the mock docker client and replace get_logs
        from app.main import app as main_app
        docker_client_instance = main_app.state.docker_client
        monkeypatch.setattr(docker_client_instance, "get_logs", mock_get_logs_not_found)
        
        # Make the tools/call request for get-logs (note: schema expects 'id' not 'container_id')
        response = test_client_with_mock.post(
            "/mcp/",
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "get-logs",
                    "arguments": {
                        "id": "nonexistent-container",
                        "tail": 100
                    }
                },
                "id": 99
            },
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        
        # Should return 200 (JSON-RPC) but with an error in the response
        assert response.status_code == 200
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 99
        assert "error" in data
        assert "result" not in data
        
        # Check that the error message is properly extracted from HTTPException
        error = data["error"]
        assert error["code"] == -32603  # INTERNAL_ERROR
        assert "Container not found" in error["message"]
        assert "data" in error
        assert error["data"]["status_code"] == 404
