
from app.core import constants


def test_root_reports_version_and_name(test_client_with_mock):
    resp = test_client_with_mock.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == constants.APP_VERSION
    assert data["message"] == constants.APP_NAME


def test_health_and_healthz_versions_and_routes(test_client_with_mock):
    # EXPOSE_ENDPOINTS_IN_HEALTHZ is set to true in conftest.py for tests
    
    # Basic health
    r1 = test_client_with_mock.get("/mcp/health")
    assert r1.status_code == 200
    d1 = r1.json()
    assert d1["version"] == constants.APP_VERSION

    # Detailed health exposes route map when feature flag is enabled
    r2 = test_client_with_mock.get("/mcp/healthz")
    assert r2.status_code == 200
    d2 = r2.json()
    assert d2["version"] == constants.APP_VERSION
    assert isinstance(d2.get("endpoints"), dict)
    # Ensure keys match MCP_ROUTES keys
    assert set(d2["endpoints"].keys()) == set(constants.MCP_ROUTES.keys())
    # And the jsonrpc route path matches
    assert d2["endpoints"]["mcp_jsonrpc"] == constants.MCP_ROUTES["mcp_jsonrpc"]


def test_initialize_returns_version_constant(test_client_with_mock):
    # initialize handshake should report APP_VERSION in serverInfo
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {"clientInfo": {"name": "pytest", "version": "0.0.0"}},
        "id": 101,
    }
    # Authorization header provided by fixture via TEST_TOKEN
    from tests.conftest import TEST_TOKEN

    resp = test_client_with_mock.post("/mcp/", json=payload, headers={"Authorization": f"Bearer {TEST_TOKEN}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["jsonrpc"] == "2.0"
    assert body["id"] == 101
    assert "result" in body
    assert body["result"]["serverInfo"]["version"] == constants.APP_VERSION
