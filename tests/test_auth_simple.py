"""
Simple authentication tests that work with FastAPI TestClient
"""

import logging

# Test token from .env file
TEST_TOKEN = "test-token-123"
INVALID_TOKEN = "invalid_token_12345"





def test_tools_endpoint_requires_auth(test_client_with_mock):
    """Test JSON-RPC tools/list requires authentication"""
    response = test_client_with_mock.post(
        "/mcp/",
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 403
    data = response.json()
    assert "Not authenticated" in data["detail"]


def test_tools_endpoint_with_valid_bearer_token(test_client_with_mock):
    """Test JSON-RPC tools/list with valid Authorization header"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "tools" in data["result"]


def test_tools_endpoint_with_valid_x_access_token(test_client_with_mock):
    """Test JSON-RPC tools/list with valid X-Access-Token header"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"X-Access-Token": TEST_TOKEN},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "tools" in data["result"]


def test_tools_endpoint_with_invalid_token(test_client_with_mock):
    """Test JSON-RPC tools/list with invalid token"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"Authorization": f"Bearer {INVALID_TOKEN}"},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 401
    data = response.json()
    assert "Invalid or missing access token" in data["detail"]


def test_authorization_header_takes_precedence(test_client_with_mock):
    """Test that Authorization header takes precedence over X-Access-Token"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={
            "Authorization": f"Bearer {TEST_TOKEN}",
            "X-Access-Token": INVALID_TOKEN
        },
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    # Should succeed because Authorization header is valid
    assert response.status_code == 200


def test_legacy_query_param_warning(test_client_with_mock, caplog):
    """Test warning is logged when accessToken query parameter is detected"""
    with caplog.at_level(logging.WARNING):
        response = test_client_with_mock.post(
            "/mcp/?accesstoken=sometoken",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )

        # Request should succeed with valid header auth
        assert response.status_code == 200

        # Check warning was logged
        assert any(
            "Query parameter authentication is unsupported" in record.message
            for record in caplog.records
        )


def test_no_warning_without_query_param(test_client_with_mock, caplog):
    """Test no warning is logged when no accessToken query parameter"""
    with caplog.at_level(logging.WARNING):
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )

        assert response.status_code == 200

        # Check no warning about query param auth
        assert not any(
            "Query parameter authentication is unsupported" in record.message
            for record in caplog.records
        )


def test_no_sensitive_data_in_warning_logs(test_client_with_mock, caplog):
    """Test that warning does not expose sensitive token values"""
    with caplog.at_level(logging.WARNING):
        sensitive_token = "secret_token_value_12345"
        response = test_client_with_mock.post(
            f"/mcp/?accesstoken={sensitive_token}",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )

        assert response.status_code == 200

        # Check that sensitive token is NOT in any log messages
        for record in caplog.records:
            assert sensitive_token not in record.message
            assert sensitive_token not in str(record.__dict__)


def test_case_insensitive_bearer_scheme(test_client_with_mock):
    """Test that Bearer scheme is case-insensitive"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"Authorization": f"bearer {TEST_TOKEN}"},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 200


def test_empty_authorization_header(test_client_with_mock):
    """Test empty Authorization header"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"Authorization": ""},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    assert response.status_code == 403


def test_empty_x_access_token_header(test_client_with_mock):
    """Test empty X-Access-Token header"""
    response = test_client_with_mock.post(
        "/mcp/",
        headers={"X-Access-Token": ""},
        json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
    )
    # Empty header is treated as no credentials (403), not invalid credentials (401)
    assert response.status_code == 403
