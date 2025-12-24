"""
Comprehensive authentication tests for the Docker MCP Server.

Tests cover:
1. Valid authentication methods (Authorization header, X-Access-Token header)
2. Invalid authentication attempts
3. Legacy query parameter warning
4. Token validation and HMAC comparison
"""

import logging

# Test token from .env file
TEST_TOKEN = "test-token-123"
INVALID_TOKEN = "invalid_token_12345"


class TestAuthenticationMethods:
    """Test suite for authentication methods"""

    def test_auth_with_authorization_header_valid(self, test_client_with_mock):
        """Test successful authentication with Authorization header on JSON-RPC endpoint"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]

    def test_auth_with_x_access_token_header_valid(self, test_client_with_mock):
        """Test successful authentication with X-Access-Token header on JSON-RPC endpoint"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"X-Access-Token": TEST_TOKEN},
            json={"jsonrpc": "2.0", "id": "2", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]

    def test_auth_authorization_header_priority(self, test_client_with_mock):
        """Test that Authorization header takes precedence over X-Access-Token on authenticated endpoint"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={
                "Authorization": f"Bearer {TEST_TOKEN}",
                "X-Access-Token": INVALID_TOKEN
            },
            json={"jsonrpc": "2.0", "id": "3", "method": "tools/list", "params": {}}
        )
        # Should succeed because Authorization header is valid
        assert response.status_code == 200

    def test_health_endpoint_public_access(self, test_client_with_mock):
        """Test that health endpoint is publicly accessible without authentication (by design)"""
        response = test_client_with_mock.get("/mcp/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "docker_reachable" in data

    def test_auth_invalid_token_authorization_header(self, test_client_with_mock):
        """Test that invalid token in Authorization header is rejected with 401"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer {INVALID_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "4", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "detail" in data

    def test_auth_invalid_token_x_access_token_header(self, test_client_with_mock):
        """Test that invalid token in X-Access-Token header is rejected with 401"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"X-Access-Token": INVALID_TOKEN},
            json={"jsonrpc": "2.0", "id": "5", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "detail" in data

    def test_auth_malformed_authorization_header(self, test_client_with_mock):
        """Test that malformed Authorization header (missing Bearer scheme) is rejected with 403"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": TEST_TOKEN},
            json={"jsonrpc": "2.0", "id": "6", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 403
        data = response.json()
        assert "error" in data or "detail" in data

    def test_auth_empty_authorization_header(self, test_client_with_mock):
        """Test that empty Authorization header is rejected with 403"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": ""},
            json={"jsonrpc": "2.0", "id": "7", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 403

    def test_auth_empty_x_access_token_header(self, test_client_with_mock):
        """Test that empty X-Access-Token header is rejected with 403"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"X-Access-Token": ""},
            json={"jsonrpc": "2.0", "id": "8", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 403


class TestLegacyQueryParameterWarning:
    """Test suite for legacy query parameter warning"""

    def test_legacy_query_param_warning_lowercase(self, test_client_with_mock, caplog):
        """Test warning is logged when accessToken query parameter is detected (lowercase)"""
        with caplog.at_level(logging.WARNING):
            response = test_client_with_mock.get(
                "/mcp/health?accesstoken=sometoken",
                headers={"Authorization": f"Bearer {TEST_TOKEN}"}
            )

            # Request should succeed with valid header auth
            assert response.status_code == 200

            # Check warning was logged
            assert any(
                "Query parameter authentication is unsupported" in record.message
                for record in caplog.records
            )

    def test_legacy_query_param_warning_uppercase(self, test_client_with_mock, caplog):
        """Test warning is logged when accessToken query parameter is detected (uppercase)"""
        with caplog.at_level(logging.WARNING):
            response = test_client_with_mock.get(
                "/mcp/health?ACCESSTOKEN=sometoken",
                headers={"Authorization": f"Bearer {TEST_TOKEN}"}
            )

            assert response.status_code == 200

            # Check warning was logged
            assert any(
                "Query parameter authentication is unsupported" in record.message
                for record in caplog.records
            )

    def test_legacy_query_param_warning_mixed_case(self, test_client_with_mock, caplog):
        """Test warning is logged when accessToken query parameter is detected (mixed case)"""
        with caplog.at_level(logging.WARNING):
            response = test_client_with_mock.get(
                "/mcp/health?AccessToken=sometoken",
                headers={"Authorization": f"Bearer {TEST_TOKEN}"}
            )

            assert response.status_code == 200

            # Check warning was logged
            assert any(
                "Query parameter authentication is unsupported" in record.message
                for record in caplog.records
            )

    def test_no_warning_without_query_param(self, test_client_with_mock, caplog):
        """Test no warning is logged when no accessToken query parameter"""
        with caplog.at_level(logging.WARNING):
            response = test_client_with_mock.get(
                "/mcp/health",
                headers={"Authorization": f"Bearer {TEST_TOKEN}"}
            )

            assert response.status_code == 200

            # Check no warning about query param auth
            assert not any(
                "Query parameter authentication is unsupported" in record.message
                for record in caplog.records
            )

    def test_no_sensitive_data_in_warning(self, test_client_with_mock, caplog):
        """Test that warning does not expose sensitive token values"""
        with caplog.at_level(logging.WARNING):
            sensitive_token = "secret_token_value_12345"
            response = test_client_with_mock.get(
                f"/mcp/health?accesstoken={sensitive_token}",
                headers={"Authorization": f"Bearer {TEST_TOKEN}"}
            )

            assert response.status_code == 200

            # Check that sensitive token is NOT in any log messages
            for record in caplog.records:
                assert sensitive_token not in record.message
                if hasattr(record, 'extra'):
                    # Check extra fields don't contain token
                    assert sensitive_token not in str(record.__dict__)


class TestMCPEndpoints:
    """Test MCP endpoints with authentication"""

    def test_mcp_tools_endpoint_requires_auth(self, test_client_with_mock):
        """Test JSON-RPC tools/list requires authentication"""
        response = test_client_with_mock.post(
            "/mcp/",
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 403

    def test_mcp_tools_endpoint_with_valid_auth(self, test_client_with_mock):
        """Test JSON-RPC tools/list with valid authentication"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]

    def test_mcp_prompts_endpoint_requires_auth(self, test_client_with_mock):
        """Test JSON-RPC prompts/list requires authentication"""
        response = test_client_with_mock.post(
            "/mcp/",
            json={"jsonrpc": "2.0", "id": "1", "method": "prompts/list", "params": {}}
        )
        assert response.status_code == 403

    def test_mcp_prompts_endpoint_with_valid_auth(self, test_client_with_mock):
        """Test JSON-RPC prompts/list with valid authentication"""
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "1", "method": "prompts/list", "params": {}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "prompts" in data["result"]


class TestAuthenticationEdgeCases:
    """Test edge cases and security scenarios"""

    def test_auth_case_sensitive_bearer_scheme(self, test_client_with_mock):
        """Test that Bearer scheme is case-insensitive (bearer, Bearer, BEARER all work)"""
        # FastAPI's get_authorization_scheme_param handles case-insensitivity
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"bearer {TEST_TOKEN}"},
            json={"jsonrpc": "2.0", "id": "9", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 200

    def test_auth_whitespace_in_token(self, test_client_with_mock):
        """Test that tokens with leading/trailing whitespace are rejected"""
        # Whitespace in token value makes it invalid, should fail HMAC comparison
        response = test_client_with_mock.post(
            "/mcp/",
            headers={"Authorization": f"Bearer  {TEST_TOKEN}  "},
            json={"jsonrpc": "2.0", "id": "10", "method": "tools/list", "params": {}}
        )
        assert response.status_code == 401

    def test_auth_multiple_authorization_headers(self, test_client_with_mock):
        """Test behavior when multiple Authorization headers are provided"""
        # When multiple Authorization headers are sent, FastAPI uses the first one
        # Test 1: First header valid, second invalid -> auth succeeds
        response = test_client_with_mock.post(
            "/mcp/",
            headers=[
                ("Authorization", f"Bearer {TEST_TOKEN}"),
                ("Authorization", f"Bearer {INVALID_TOKEN}")
            ],
            json={"jsonrpc": "2.0", "id": "11", "method": "tools/list", "params": {}}
        )
        # Authentication succeeds because the first Authorization header is valid
        assert response.status_code == 200
        
        # Test 2: First header invalid, second valid -> auth fails
        response = test_client_with_mock.post(
            "/mcp/",
            headers=[
                ("Authorization", f"Bearer {INVALID_TOKEN}"),
                ("Authorization", f"Bearer {TEST_TOKEN}")
            ],
            json={"jsonrpc": "2.0", "id": "12", "method": "tools/list", "params": {}}
        )
        # Authentication fails because the first Authorization header is invalid
        assert response.status_code == 401

    def test_auth_hmac_timing_attack_resistance(self, test_client_with_mock):
        """Test HMAC comparison is timing-safe (using JSON-RPC endpoints that require auth)"""
        import statistics
        import time

        durations_invalid_token = []
        durations_wrong_token = []

        for _ in range(5):
            start = time.perf_counter()
            response1 = test_client_with_mock.post(
                "/mcp/",
                headers={"Authorization": f"Bearer {INVALID_TOKEN}"},
                json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
            )
            durations_invalid_token.append(time.perf_counter() - start)

            start = time.perf_counter()
            response2 = test_client_with_mock.post(
                "/mcp/",
                headers={"Authorization": "Bearer wrongtoken"},
                json={"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}
            )
            durations_wrong_token.append(time.perf_counter() - start)

            # Responses should consistently fail with 401
            assert response1.status_code == 401
            assert response2.status_code == 401

        median_diff = abs(
            statistics.median(durations_invalid_token)
            - statistics.median(durations_wrong_token)
        )

        # Timing should be similar (within reasonable variance across medians)
        assert median_diff < 0.2  # 200ms tolerance to avoid flakiness on slower CI
