#!/usr/bin/env python3
"""
Simple MCP endpoint test script that bypasses Docker connectivity issues
Tests the MCP JSON-RPC endpoints directly using mock data
"""

import json
import time
from typing import Any

import requests

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "98a0305163506ea4f95b9b6c206ac459c4cfa3aeb97c24b31c89660e5d33f928"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_endpoint(method: str, endpoint: str, data: dict[str, Any] = None) -> dict[str, Any]:
    """Test an endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=HEADERS, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")

        print(f"\n{'='*60}")
        print(f"TEST: {method} {endpoint}")
        print(f"STATUS: {response.status_code}")

        try:
            response_json = response.json()
            print(f"RESPONSE:\n{json.dumps(response_json, indent=2)}")
            return response_json
        except json.JSONDecodeError:
            print(f"RAW RESPONSE: {response.text}")
            return {"raw_response": response.text}

    except requests.exceptions.ConnectionError:
        print(f"\n{'='*60}")
        print(f"TEST: {method} {endpoint}")
        print("STATUS: CONNECTION FAILED - Server not running")
        return {"error": "connection_failed"}
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"TEST: {method} {endpoint}")
        print(f"ERROR: {e}")
        return {"error": str(e)}

def test_mcp_initialize():
    """Test MCP initialize endpoint"""
    print("\n🔧 Testing MCP Initialize Endpoint")

    data = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "id": 1,
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }

    return test_endpoint("POST", "/mcp/", data)

def test_tools_list():
    """Test tools/list endpoint"""
    print("\n🔧 Testing Tools List Endpoint")

    data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 2
    }

    result = test_endpoint("POST", "/mcp/", data)

    # Verify that meta-tools are not in the default list
    if result.get("status") == 200 and "result" in result:
        tools_data = result["result"]
        if "tools" in tools_data:
            tool_names = [tool.get("name") for tool in tools_data["tools"]]
            meta_tools = ["discover-tools", "list-task-types", "intent-query-help"]
            found_meta_tools = [name for name in meta_tools if name in tool_names]

            if found_meta_tools:
                print(f"⚠️  Warning: Found meta-tools in default list: {found_meta_tools}")
            else:
                print("✅ Verified: No meta-tools in default tools/list")

    return result

def test_prompts_list():
    """Test prompts/list endpoint"""
    print("\n🔧 Testing Prompts List Endpoint")

    data = {
        "jsonrpc": "2.0",
        "method": "prompts/list",
        "params": {},
        "id": 7
    }

    return test_endpoint("POST", "/mcp/", data)

def test_prompts_get():
    """Test prompts/get endpoint"""
    print("\n🔧 Testing Prompts Get Endpoint")

    data = {
        "jsonrpc": "2.0",
        "method": "prompts/get",
        "params": {
            "name": "discover-tools"
        },
        "id": 8
    }

    result = test_endpoint("POST", "/mcp/", data)

    # Optional assertion to ensure dynamic content includes known task type
    if isinstance(result, dict) and "result" in result and "messages" in result["result"]:
        messages = result["result"]["messages"]
        if messages and "content" in messages[0] and "text" in messages[0]["content"]:
            content_text = messages[0]["content"]["text"]
            assert "container-ops" in content_text, "discover-tools prompt should include container-ops task type"
            print("✅ Assertion passed: discover-tools prompt includes dynamic content")

    return result

def test_prompts_get_invalid():
    """Test prompts/get endpoint with invalid prompt name"""
    print("\n🔧 Testing Invalid Prompt Name")

    data = {
        "jsonrpc": "2.0",
        "method": "prompts/get",
        "params": {
            "name": "invalid-prompt"
        },
        "id": 9
    }

    return test_endpoint("POST", "/mcp/", data)

def test_tools_call():
    """Test tools/call endpoint"""
    print("\n🔧 Testing Tools Call Endpoint")

    # First call tools/list to seed session_tools
    print("First calling tools/list to seed session tools...")
    list_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 2
    }
    test_endpoint("POST", "/mcp/", list_data)

    # Then call tools/call
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 3,
        "params": {
            "name": "list-containers",
            "arguments": {
                "all": True
            }
        }
    }

    return test_endpoint("POST", "/mcp/", data)

def test_invalid_method():
    """Test invalid MCP method"""
    print("\n🔧 Testing Invalid Method")

    data = {
        "jsonrpc": "2.0",
        "method": "invalid_method",
        "id": 4
    }

    return test_endpoint("POST", "/mcp/", data)

def test_malformed_json():
    """Test malformed JSON"""
    print("\n🔧 Testing Malformed JSON")

    url = f"{BASE_URL}/mcp/"

    try:
        response = requests.post(
            url,
            headers=HEADERS,
            data='{"jsonrpc": "2.0", "method": "tools/list", "id": 5',  # Missing closing brace
            timeout=10
        )

        print(f"\n{'='*60}")
        print("TEST: POST /mcp (malformed JSON)")
        print(f"STATUS: {response.status_code}")
        print(f"RESPONSE: {response.text}")

        return {"status": response.status_code, "response": response.text}

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def test_health_endpoint():
    """Test health endpoint"""
    print("\n🔧 Testing Health Endpoint")
    return test_endpoint("GET", "/mcp/healthz")

def test_unauthorized_access():
    """Test unauthorized access"""
    print("\n🔧 Testing Unauthorized Access")

    url = f"{BASE_URL}/mcp/"
    data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 6
    }

    try:
        # Send request without authorization header
        response = requests.post(url, json=data, timeout=10)

        print(f"\n{'='*60}")
        print("TEST: POST /mcp (unauthorized)")
        print(f"STATUS: {response.status_code}")
        print(f"RESPONSE: {response.text}")

        return {"status": response.status_code, "response": response.text}

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def test_meta_tool_discover():
    """Test discover-tools meta-tool"""
    print("\n🔧 Testing Meta-Tool: discover-tools")

    # First call tools/list with meta-ops to seed session tools
    print("First calling tools/list with meta-ops to seed session tools...")
    list_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9
    }
    test_endpoint("POST", "/mcp/", list_data)

    # Then call the meta-tool
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "discover-tools",
            "arguments": {}
        },
        "id": 10
    }

    return test_endpoint("POST", "/mcp/", data)

def test_meta_tool_list_task_types():
    """Test list-task-types meta-tool"""
    print("\n🔧 Testing Meta-Tool: list-task-types")

    # First call tools/list with meta-ops to seed session tools
    print("First calling tools/list with meta-ops to seed session tools...")
    list_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9
    }
    test_endpoint("POST", "/mcp/", list_data)

    # Then call the meta-tool
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "list-task-types",
            "arguments": {}
        },
        "id": 11
    }

    return test_endpoint("POST", "/mcp/", data)

def test_meta_tool_intent_help():
    """Test intent-query-help meta-tool"""
    print("\n🔧 Testing Meta-Tool: intent-query-help")

    # First call tools/list with meta-ops to seed session tools
    print("First calling tools/list with meta-ops to seed session tools...")
    list_data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {"task_type": "meta-ops"},
        "id": 9
    }
    test_endpoint("POST", "/mcp/", list_data)

    # Then call the meta-tool
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "intent-query-help",
            "arguments": {}
        },
        "id": 12
    }

    return test_endpoint("POST", "/mcp/", data)

def test_tools_list_meta_ops():
    """Test tools/list with meta-ops task type"""
    print("\n🔧 Testing Tools List with meta-ops Task Type")

    data = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {
            "task_type": "meta-ops"
        },
        "id": 13
    }

    return test_endpoint("POST", "/mcp/", data)

def main():
    """Run all MCP endpoint tests"""
    print("🚀 Starting MCP Endpoint Tests")
    print(f"📡 Target URL: {BASE_URL}")
    print(f"🔑 Using Token: {TOKEN[:20]}...")
    print("\n⚠️  Note: This test script requires the server to be running.")
    print("   If connection fails, start the server first.\n")

    # Wait a moment for user to read the intro
    time.sleep(2)

    # Run tests
    results = {}

    results['health'] = test_health_endpoint()
    results['initialize'] = test_mcp_initialize()
    results['tools_list'] = test_tools_list()
    results['prompts_list'] = test_prompts_list()
    results['prompts_get'] = test_prompts_get()
    results['prompts_get_invalid'] = test_prompts_get_invalid()
    results['tools_call'] = test_tools_call()
    results['meta_tool_discover'] = test_meta_tool_discover()
    results['meta_tool_list_task_types'] = test_meta_tool_list_task_types()
    results['meta_tool_intent_help'] = test_meta_tool_intent_help()
    results['tools_list_meta_ops'] = test_tools_list_meta_ops()
    results['invalid_method'] = test_invalid_method()
    results['malformed_json'] = test_malformed_json()
    results['unauthorized'] = test_unauthorized_access()

    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")

    for test_name, result in results.items():
        if 'error' in result:
            status = "❌ FAILED"
        elif isinstance(result.get('status'), int) and result.get('status') == 200:
            status = "✅ PASSED"
        elif isinstance(result.get('status'), int) and result.get('status') >= 400:
            status = "⚠️  ERROR RESPONSE"
        else:
            status = "❓ UNKNOWN"

        print(f"{test_name:20} {status}")

    print(f"\n{'='*60}")
    print("🏁 Testing Complete!")
    print("\nIf tests failed with connection errors:")
    print("1. Make sure the Docker MCP server is running")
    print("2. Check that the server is accessible at http://localhost:8000")
    print("3. Verify the MCP_ACCESS_TOKEN environment variable is set correctly")

if __name__ == "__main__":
    main()
