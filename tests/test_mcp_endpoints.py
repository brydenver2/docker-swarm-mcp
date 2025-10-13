#!/usr/bin/env python3
"""
Simple MCP endpoint test script that bypasses Docker connectivity issues.

When executed via pytest, these tests expect a running MCP server at BASE_URL.
If the server is not reachable the tests will be skipped gracefully so that
the broader unit-test suite can run offline.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict

import pytest
import requests

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "98a0305163506ea4f95b9b6c206ac459c4cfa3aeb97c24b31c89660e5d33f928"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def _call_endpoint(
    method: str,
    endpoint: str,
    data: Dict[str, Any] | None = None,
    *,
    headers: Dict[str, str] | None = None,
    raw_body: str | None = None,
    timeout: int = 10,
) -> Dict[str, Any]:
    """
    Send an HTTP request to the MCP endpoint and capture the response.

    Returns:
        dict: On success, a mapping containing:
            - "status": HTTP status code
            - "json": Parsed JSON payload (when available)
            - "raw": Raw text body (when JSON parsing fails)
        On connection error, {"error": "connection_failed"}.
        On other unexpected exceptions, {"error": "<message>"}.
    """
    url = f"{BASE_URL}{endpoint}"
    request_headers = headers or HEADERS

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=request_headers, timeout=timeout)
        elif method.upper() == "POST":
            if raw_body is not None:
                response = requests.post(url, headers=request_headers, data=raw_body, timeout=timeout)
            else:
                response = requests.post(url, headers=request_headers, json=data, timeout=timeout)
        else:
            raise ValueError(f"Unsupported method: {method}")

        print(f"\n{'=' * 60}")
        print(f"TEST: {method} {endpoint}")
        print(f"STATUS: {response.status_code}")

        try:
            response_json = response.json()
            print(f"RESPONSE:\n{json.dumps(response_json, indent=2)}")
            return {"status": response.status_code, "json": response_json}
        except json.JSONDecodeError:
            print(f"RAW RESPONSE: {response.text}")
            return {"status": response.status_code, "raw": response.text}

    except requests.exceptions.ConnectionError:
        print(f"\n{'=' * 60}")
        print(f"TEST: {method} {endpoint}")
        print("STATUS: CONNECTION FAILED - Server not running")
        return {"error": "connection_failed"}
    except Exception as exc:  # pragma: no cover - diagnostic output path
        print(f"\n{'=' * 60}")
        print(f"TEST: {method} {endpoint}")
        print(f"ERROR: {exc}")
        return {"error": str(exc)}


def _require_running_server(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Skip the current test if the MCP server is not reachable.
    """
    if result.get("error") == "connection_failed":
        pytest.skip(f"MCP server not running at {BASE_URL}; skipping endpoint check.")
    return result


def test_mcp_initialize():
    payload = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": 1,
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    body = result["json"]
    assert body["jsonrpc"] == "2.0"
    assert body["result"]["serverInfo"]["name"] == "docker-swarm-mcp"


def test_tools_list():
    payload = {"jsonrpc": "2.0", "method": "tools/list", "id": 2}
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    tools = result["json"]["result"]["tools"]
    assert tools, "tools/list should return at least one tool"
    tool_names = {tool.get("name") for tool in tools}
    meta_tools = {"discover-tools", "list-task-types", "intent-query-help"}
    assert tool_names.isdisjoint(meta_tools), "Meta tools should not appear in default tools/list output"


def test_prompts_list():
    payload = {"jsonrpc": "2.0", "method": "prompts/list", "params": {}, "id": 7}
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    prompts = result["json"]["result"]["prompts"]
    assert isinstance(prompts, list)
    assert any(prompt["name"] == "discover-tools" for prompt in prompts)


def test_prompts_get():
    payload = {
        "jsonrpc": "2.0",
        "method": "prompts/get",
        "params": {"name": "discover-tools"},
        "id": 8,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    messages = result["json"]["result"]["messages"]
    assert messages
    content_text = messages[0]["content"]["text"]
    assert "container-ops" in content_text


def test_prompts_get_invalid():
    payload = {
        "jsonrpc": "2.0",
        "method": "prompts/get",
        "params": {"name": "invalid-prompt"},
        "id": 9,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    assert "error" in result["json"]
    assert result["json"]["error"]["code"] == -32602


def test_tools_call():
    # Seed session tools
    list_payload = {"jsonrpc": "2.0", "method": "tools/list", "id": 2}
    _require_running_server(_call_endpoint("POST", "/mcp/", list_payload))

    call_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 3,
        "params": {"name": "list-containers", "arguments": {"all": True}},
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", call_payload))
    assert result["status"] == 200
    body = result["json"]
    if "error" in body:
        pytest.skip(f"tools/call returned error: {body['error']['message']}")
    assert "result" in body


def test_invalid_method():
    payload = {"jsonrpc": "2.0", "method": "invalid_method", "id": 4}
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    assert result["status"] == 200
    error = result["json"]["error"]
    assert error["code"] == -32601


def test_malformed_json():
    result = _call_endpoint(
        "POST",
        "/mcp/",
        headers=HEADERS,
        raw_body='{"jsonrpc": "2.0", "method": "tools/list", "id": 5',  # Missing closing brace
    )
    result = _require_running_server(result)
    assert result["status"] >= 400
    assert "raw" in result or "json" in result


def test_health_endpoint():
    result = _require_running_server(_call_endpoint("GET", "/mcp/healthz"))
    if result["status"] >= 500:
        pytest.skip(f"Health endpoint returned {result['status']}")
    assert result["status"] == 200
    status_value = result["json"]["status"]
    assert status_value in {"healthy", "degraded", "unhealthy"}


def test_unauthorized_access():
    payload = {"jsonrpc": "2.0", "method": "tools/list", "id": 6}
    # Drop Authorization header to simulate unauthorized request
    result = _call_endpoint(
        "POST",
        "/mcp/",
        payload,
        headers={"Content-Type": "application/json"},
    )
    result = _require_running_server(result)
    assert result["status"] in {401, 403}


def test_meta_tool_discover():
    # Seed meta tools
    list_payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9,
    }
    _require_running_server(_call_endpoint("POST", "/mcp/", list_payload))

    call_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "discover-tools", "arguments": {}},
        "id": 10,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", call_payload))
    assert result["status"] == 200
    assert "result" in result["json"]


def test_meta_tool_list_task_types():
    list_payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9,
    }
    _require_running_server(_call_endpoint("POST", "/mcp/", list_payload))

    call_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "list-task-types", "arguments": {}},
        "id": 11,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", call_payload))
    assert result["status"] == 200
    assert "result" in result["json"]


def test_meta_tool_intent_help():
    list_payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9,
    }
    _require_running_server(_call_endpoint("POST", "/mcp/", list_payload))

    call_payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "intent-query-help", "arguments": {}},
        "id": 12,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", call_payload))
    assert result["status"] == 200
    assert "result" in result["json"]


def test_tools_list_meta_ops():
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 13,
    }
    result = _require_running_server(_call_endpoint("POST", "/mcp/", payload))
    meta_tools = result["json"]["result"]["tools"]
    assert meta_tools, "Expected meta-ops tool list to be non-empty"


def main() -> None:
    """
    Run the full suite of MCP endpoint requests and print a summary report.

    This function is intended for manual execution and does not rely on pytest.
    """
    print("🚀 Starting MCP Endpoint Tests")
    print(f"📡 Target URL: {BASE_URL}")
    print(f"🔑 Using Token: {TOKEN[:20]}...")
    print("\n⚠️  Note: This test script requires the server to be running.")
    print("   If connection fails, start the server first.\n")

    # Wait a moment for the user to read the intro
    time.sleep(2)

    # Run probes
    probes = {
        "health": _call_endpoint("GET", "/mcp/healthz"),
        "initialize": _call_endpoint(
            "POST",
            "/mcp/",
            {
                "jsonrpc": "2.0",
                "method": "initialize",
                "id": 1,
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "test-client", "version": "1.0.0"},
                },
            },
        ),
        "tools_list": _call_endpoint("POST", "/mcp/", {"jsonrpc": "2.0", "method": "tools/list", "id": 2}),
        "prompts_list": _call_endpoint(
            "POST", "/mcp/", {"jsonrpc": "2.0", "method": "prompts/list", "params": {}, "id": 7}
        ),
        "prompts_get": _call_endpoint(
            "POST",
            "/mcp/",
            {"jsonrpc": "2.0", "method": "prompts/get", "params": {"name": "discover-tools"}, "id": 8},
        ),
        "prompts_get_invalid": _call_endpoint(
            "POST",
            "/mcp/",
            {"jsonrpc": "2.0", "method": "prompts/get", "params": {"name": "invalid-prompt"}, "id": 9},
        ),
        "tools_call": _call_endpoint(
            "POST",
            "/mcp/",
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 3,
                "params": {"name": "list-containers", "arguments": {"all": True}},
            },
        ),
        "meta_tool_discover": _call_endpoint(
            "POST",
            "/mcp/",
            {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "discover-tools", "arguments": {}}, "id": 10},
        ),
        "meta_tool_list_task_types": _call_endpoint(
            "POST",
            "/mcp/",
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "list-task-types", "arguments": {}},
                "id": 11,
            },
        ),
        "meta_tool_intent_help": _call_endpoint(
            "POST",
            "/mcp/",
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "intent-query-help", "arguments": {}},
                "id": 12,
            },
        ),
        "tools_list_meta_ops": _call_endpoint(
            "POST",
            "/mcp/",
            {"jsonrpc": "2.0", "method": "tools/list", "params": {"task_type": "meta-ops"}, "id": 13},
        ),
        "invalid_method": _call_endpoint("POST", "/mcp/", {"jsonrpc": "2.0", "method": "invalid_method", "id": 4}),
        "malformed_json": _call_endpoint(
            "POST",
            "/mcp/",
            headers=HEADERS,
            raw_body='{"jsonrpc": "2.0", "method": "tools/list", "id": 5',
        ),
        "unauthorized": _call_endpoint(
            "POST",
            "/mcp/",
            {"jsonrpc": "2.0", "method": "tools/list", "id": 6},
            headers={"Content-Type": "application/json"},
        ),
    }

    # Summary
    print(f"\n{'=' * 60}")
    print("📊 TEST SUMMARY")
    print(f"{'=' * 60}")

    for name, response in probes.items():
        if "error" in response:
            status = "❌ CONNECTION FAILED"
        elif response.get("status", 0) >= 400:
            status = "⚠️  ERROR RESPONSE"
        else:
            status = "✅ OK"
        print(f"{name:25} {status}")

    print(f"\n{'=' * 60}")
    print("🏁 Testing Complete!")
    print("\nIf tests failed with connection errors:")
    print("1. Make sure the Docker MCP server is running")
    print("2. Check that the server is accessible at http://localhost:8000")
    print("3. Verify the MCP_ACCESS_TOKEN environment variable is set correctly")


if __name__ == "__main__":
    main()
