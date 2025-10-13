#!/usr/bin/env python3
"""
Minimal MCP server for testing without Docker connectivity
Creates a mock environment to test MCP JSON-RPC endpoints
"""

import json
import logging
import os
import time
import uuid
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Set environment variables
os.environ['MCP_ACCESS_TOKEN'] = '98a0305163506ea4f95b9b6c206ac459c4cfa3aeb97c24b31c89660e5d33f928'
os.environ['LOG_LEVEL'] = 'DEBUG'
os.environ['MCP_TRANSPORT'] = 'http'
os.environ['ALLOWED_ORIGINS'] = 'http://localhost:3000,http://localhost:8080'

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Mock data and tools
MOCK_TOOLS = [
    {
        "name": "list_containers",
        "description": "List all Docker containers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "all": {"type": "boolean", "description": "Show all containers (default false)"},
                "filters": {"type": "object", "description": "Filters to apply"}
            }
        }
    },
    {
        "name": "create_container",
        "description": "Create a new Docker container",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image": {"type": "string", "description": "Docker image name"},
                "name": {"type": "string", "description": "Container name"},
                "command": {"type": "string", "description": "Command to run"}
            },
            "required": ["image"]
        }
    },
    {
        "name": "list_images",
        "description": "List Docker images",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filters": {"type": "object", "description": "Filters to apply"}
            }
        }
    }
]

MOCK_CONTAINERS = [
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

class MockMCPServer:
    """Mock MCP server for testing"""

    def __init__(self):
        """
        Initialize the MockMCPServer instance with predefined mock tools and containers.
        
        Sets the `tools` attribute to the module's MOCK_TOOLS and the `containers` attribute to MOCK_CONTAINERS.
        """
        self.tools = MOCK_TOOLS
        self.containers = MOCK_CONTAINERS

    def handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Responds to an MCP initialize request with the server's protocol version, capabilities, and basic metadata.
        
        Returns:
            dict: A mapping with keys:
                - "protocolVersion" (str): protocol version string.
                - "capabilities" (dict): server capabilities; includes "tools" -> {"listChanged": bool}.
                - "serverInfo" (dict): server metadata with "name" (str) and "version" (str).
        """
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "docker-swarm-mcp-mock",
                "version": "0.1.0"
            }
        }

    def handle_tools_list(self, params: dict[str, Any] = None) -> dict[str, Any]:
        """
        Return the available tool definitions exposed by the mock MCP server.
        
        Parameters:
            params (dict[str, Any] | None): Optional request parameters (ignored by this handler).
        
        Returns:
            dict[str, Any]: A dictionary with a single key `"tools"` whose value is the list of tool definition objects.
        """
        return {"tools": self.tools}

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Dispatch a tools/call request to the corresponding mock tool and return its response content.
        
        Parameters:
            params (dict): Request parameters containing:
                - "name" (str): The tool name to invoke ("list_containers", "create_container", "list_images", ...).
                - "arguments" (dict, optional): Tool-specific arguments (e.g., for "create_container": "image", "name").
        
        Returns:
            dict: A JSON-RPC style result object with a "content" list containing text items describing the result.
        
        Raises:
            ValueError: If `params["name"]` is missing or does not match a known tool.
        """
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "list_containers":
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(self.containers, indent=2)
                    }
                ]
            }
        elif tool_name == "create_container":
            image = arguments.get("image", "scratch")
            name = arguments.get("name", f"container-{uuid.uuid4().hex[:8]}")

            new_container = {
                "id": f"new-{uuid.uuid4().hex[:8]}",
                "name": name,
                "status": "created",
                "image": image,
                "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Created container: {json.dumps(new_container, indent=2)}"
                    }
                ]
            }
        elif tool_name == "list_images":
            mock_images = [
                {"id": "img123", "repoTags": ["nginx:latest"], "size": "133MB"},
                {"id": "img456", "repoTags": ["redis:alpine"], "size": "30MB"}
            ]
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(mock_images, indent=2)
                    }
                ]
            }
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

# Create FastAPI app
app = FastAPI(title="Docker Swarm MCP Server Mock", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock MCP server instance
mock_mcp = MockMCPServer()

# Simple token validation
def validate_token(request: Request) -> bool:
    """
    Check whether the incoming request contains a Bearer token that matches the MCP_ACCESS_TOKEN environment variable.
    
    Parameters:
        request (Request): HTTP request whose `Authorization` header will be inspected; expected format is "Bearer <token>".
    
    Returns:
        bool: `True` if the `Authorization` header contains a Bearer token equal to the `MCP_ACCESS_TOKEN` environment variable, `False` otherwise.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header[7:]  # Remove "Bearer " prefix
    expected_token = os.environ.get('MCP_ACCESS_TOKEN')
    return token == expected_token

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Enforces Bearer-token authentication for MCP HTTP endpoints.
    
    Parameters:
        request (Request): Incoming FastAPI request to authenticate.
        call_next (Callable): ASGI callable to invoke the next middleware or route handler.
    
    Returns:
        Response: The downstream response produced by `call_next`, or a 401 JSON response with keys `"error"` and `"message"` when the token is missing or invalid.
    """
    if request.url.path.startswith("/mcp/") and request.url.path != "/mcp/healthz":
        if not validate_token(request):
            return JSONResponse(
                status_code=401,
                content={"error": "Unauthorized", "message": "Invalid or missing token"}
            )

    response = await call_next(request)
    return response

@app.get("/mcp/healthz")
async def health_check():
    """
    Provide server health status and current timestamp.
    
    Returns:
        dict: A mapping with keys:
            - "status" (str): the health status, set to "healthy".
            - "timestamp" (float): the current Unix time in seconds.
    """
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/mcp/")
async def mcp_endpoint(request: Request):
    """
    Serve the main MCP JSON-RPC 2.0 endpoint and dispatch requests to the mock MCP server.
    
    Processes a JSON-RPC 2.0 request from the provided HTTP request, validates the message, invokes the corresponding MockMCPServer handler for supported methods ("initialize", "tools/list", "tools/call"), and returns a JSON-RPC 2.0 response. On handler errors it returns a JSON-RPC error object with code -32603; on JSON parse errors it returns a JSON-RPC parse error with code -32700 and HTTP 400; on unexpected failures it returns a JSON-RPC internal error with code -32603 and HTTP 500.
    
    Returns:
        A JSON-serializable JSON-RPC 2.0 response (dict) containing either a `result` field for successful calls or an `error` object for failures; in parse or internal error cases a FastAPI JSONResponse is returned with the appropriate HTTP status code.
    """
    try:
        body = await request.json()

        # Validate JSON-RPC format
        if not isinstance(body, dict):
            raise ValueError("Invalid JSON-RPC request: must be object")

        jsonrpc_version = body.get("jsonrpc")
        if jsonrpc_version != "2.0":
            raise ValueError("Invalid JSON-RPC version: must be '2.0'")

        method = body.get("method")
        request_id = body.get("id")
        params = body.get("params", {})

        if not method:
            raise ValueError("Missing 'method' in JSON-RPC request")

        logger.info(f"Processing MCP request: {method} (id: {request_id})")

        # Handle different methods
        try:
            if method == "initialize":
                result = mock_mcp.handle_initialize(params)
            elif method == "tools/list":
                result = mock_mcp.handle_tools_list(params)
            elif method == "tools/call":
                result = mock_mcp.handle_tools_call(params)
            else:
                raise ValueError(f"Method not found: {method}")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            logger.error(f"Error processing {method}: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": str(e),
                    "data": {"method": method}
                }
            }

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error",
                    "data": str(e)
                }
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
        )

@app.get("/")
async def root():
    """
    Return basic server metadata and available endpoints.
    
    Returns:
        dict: A mapping containing:
            - "message" (str): Human-readable server name.
            - "version" (str): Server version string.
            - "endpoints" (dict): Available endpoint paths with keys "mcp" and "health".
    """
    return {
        "message": "Docker Swarm MCP Server Mock",
        "version": "0.1.0",
        "endpoints": {
            "mcp": "/mcp/",
            "health": "/mcp/healthz"
        }
    }

def main():
    """
    Start the mock MCP development server and run it with Uvicorn.
    
    Prints startup information (service URLs and the configured MCP access token) to stdout, then launches the ASGI server bound to 0.0.0.0:8000 serving the application.
    """
    print("🚀 Starting Mock Docker Swarm MCP Server")
    print("📋 This is a development server with mock Docker functionality")
    print("🔗 Server will be available at: http://localhost:8000")
    print("🔑 MCP endpoint: http://localhost:8000/mcp")
    print("💚 Health endpoint: http://localhost:8000/mcp/healthz")
    print("🔑 Access Token:", os.environ.get('MCP_ACCESS_TOKEN'))
    print("")

    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug"
    )

if __name__ == "__main__":
    main()