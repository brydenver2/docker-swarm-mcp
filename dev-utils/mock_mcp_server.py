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
        self.tools = MOCK_TOOLS
        self.containers = MOCK_CONTAINERS

    def handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle initialize request"""
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
        """Handle tools/list request"""
        return {"tools": self.tools}

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        """Handle tools/call request"""
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
    """Validate authorization token"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header[7:]  # Remove "Bearer " prefix
    expected_token = os.environ.get('MCP_ACCESS_TOKEN')
    return token == expected_token

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Authentication middleware"""
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
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/mcp/")
async def mcp_endpoint(request: Request):
    """Main MCP JSON-RPC endpoint"""
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
    """Root endpoint"""
    return {
        "message": "Docker Swarm MCP Server Mock",
        "version": "0.1.0",
        "endpoints": {
            "mcp": "/mcp/",
            "health": "/mcp/healthz"
        }
    }

def main():
    """Run the mock MCP server"""
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
