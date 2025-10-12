# FastAPI-MCP Integration Research Summary

## Architecture Overview

### How FastAPI-MCP Works

1. **OpenAPI → MCP Tool Conversion**:
   - Reads FastAPI's OpenAPI schema via `get_openapi()`
   - Converts each endpoint to an MCP tool using `convert_openapi_to_mcp_tools()`
   - Each tool gets `name` (operation_id), `description`, and `inputSchema` (JSON schema)

2. **MCP Protocol Implementation**:
   - Creates an MCP `Server` instance from `mcp.server.lowlevel.server`
   - Registers two handlers:
     - `@mcp_server.list_tools()` → Returns list of available tools
     - `@mcp_server.call_tool()` → Executes a tool by calling the FastAPI endpoint

3. **Static Filtering** (Current Limitation):
   - Filtering happens once during `setup_server()` at line 142
   - Uses `_filter_tools()` method with static filters:
     - `include_operations` / `exclude_operations` (by operation_id)
     - `include_tags` / `exclude_tags` (by OpenAPI tags)
   - Filtered tools stored in `self.tools` attribute
   - `handle_list_tools()` decorator at line 146-148 simply returns `self.tools`

## Key Extension Points

### 1. Override `handle_list_tools()` for Dynamic Filtering

**Current Implementation** (line 146-148):
```python
@mcp_server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    return self.tools
```

**Problem**: This always returns the same static list.

**Solution**: Override in subclass to return different tools per request:

```python
class DynamicToolGatingMCP(FastApiMCP):
    def setup_server(self) -> None:
        # Call parent to set up tools and operation_map
        super().setup_server()
        
        # Store reference to all tools BEFORE filtering
        self.all_tools = self.tools.copy()
        
        # Override the list_tools handler
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            # Extract task_type from MCP request context
            task_type = self._extract_task_type_from_context()
            
            # Use existing ToolGateController for filtering
            filtered_tools = self.tool_gate_controller.filter_tools(
                tools=self.all_tools,
                task_type=task_type,
                # ... other params
            )
            
            return filtered_tools
```

### 2. Access MCP Request Context

**Pattern Used in `handle_call_tool()`** (line 158-176):
```python
async def handle_call_tool(name: str, arguments: Dict[str, Any]):
    # Extract HTTP request info from MCP context
    request_context = mcp_server.request_context
    
    if request_context and hasattr(request_context, "request"):
        http_request = request_context.request
        
        if http_request and hasattr(http_request, "method"):
            http_request_info = HTTPRequestInfo(
                method=http_request.method,
                path=http_request.url.path,
                headers=dict(http_request.headers),
                cookies=http_request.cookies,
                query_params=dict(http_request.query_params),
                body=None,
            )
```

**We can use the same pattern to extract `task_type`** from:
- Request headers: `X-Task-Type` header
- Query parameters: `?task_type=container_management`
- Body parameters (if POST): `{"task_type": "container_management"}`

### 3. Preserve Existing Tool Gating Logic

**Integration Strategy**:
```python
from app.mcp.tool_gating import ToolGateController
from app.mcp.tool_registry import ToolRegistry

class DynamicToolGatingMCP(FastApiMCP):
    def __init__(self, fastapi, **kwargs):
        # Initialize tool gating components BEFORE parent init
        self.tool_registry = ToolRegistry(...)
        self.tool_gate_controller = ToolGateController(
            tool_registry=self.tool_registry,
            filter_config_path="filter-config.json"
        )
        
        # Parent init will call setup_server()
        super().__init__(fastapi, **kwargs)
    
    def _extract_task_type_from_context(self) -> str:
        try:
            context = self.server.request_context
            if context and hasattr(context, "request"):
                request = context.request
                
                # Check header (preferred)
                task_type = request.headers.get("X-Task-Type")
                if task_type:
                    return task_type
                
                # Check query param
                task_type = request.query_params.get("task_type")
                if task_type:
                    return task_type
                
                # Default fallback
                return "general"
        except:
            return "general"
```

## Implementation Plan

### Phase 2: Create DynamicToolGatingMCP Class

**File**: `app/mcp/fastapi_mcp_integration.py`

**Structure**:
```python
from typing import List
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import mcp.types as types

from app.mcp.tool_gating import ToolGateController
from app.mcp.tool_registry import ToolRegistry

class DynamicToolGatingMCP(FastApiMCP):
    """
    Extended FastApiMCP with dynamic per-request tool filtering.
    
    Integrates with existing ToolGateController to apply:
    - Task type filtering (container_management, monitoring, etc.)
    - Resource filters (available vs. hidden)
    - Security filters (read-only vs. write operations)
    - Context limits (7600 token hard cap)
    """
    
    def __init__(
        self,
        fastapi: FastAPI,
        tool_registry: ToolRegistry,
        tool_gate_controller: ToolGateController,
        **kwargs
    ):
        self.tool_registry = tool_registry
        self.tool_gate_controller = tool_gate_controller
        self.all_tools: List[types.Tool] = []
        
        # Parent __init__ will call setup_server()
        super().__init__(fastapi, **kwargs)
    
    def setup_server(self) -> None:
        # Call parent to convert OpenAPI → MCP tools
        super().setup_server()
        
        # Store ALL tools before any filtering
        self.all_tools = self.tools.copy()
        
        # Override list_tools handler for dynamic filtering
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            return await self._handle_dynamic_list_tools()
    
    async def _handle_dynamic_list_tools(self) -> List[types.Tool]:
        """
        Dynamically filter tools based on current request context.
        """
        # Extract task_type from MCP request
        task_type = self._extract_task_type_from_context()
        
        # Use existing ToolGateController for filtering
        filtered_tools = self.tool_gate_controller.filter_tools(
            tools=self.all_tools,
            task_type=task_type,
            operation_map=self.operation_map
        )
        
        return filtered_tools
    
    def _extract_task_type_from_context(self) -> str:
        """
        Extract task_type from MCP request context.
        Priority: Header > Query Param > Default
        """
        try:
            context = self.server.request_context
            if context and hasattr(context, "request"):
                request = context.request
                
                # Check X-Task-Type header (preferred)
                task_type = request.headers.get("X-Task-Type")
                if task_type:
                    return task_type
                
                # Check query parameter
                task_type = request.query_params.get("task_type")
                if task_type:
                    return task_type
        except (LookupError, AttributeError):
            pass
        
        # Default to general task type
        return "general"
```

### Phase 3: Update main.py

**Changes Required**:
```python
from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP
from app.mcp.tool_registry import ToolRegistry
from app.mcp.tool_gating import ToolGateController

# Initialize tool gating components
tool_registry = ToolRegistry(tools_yaml_path="tools.yaml")
tool_gate_controller = ToolGateController(
    tool_registry=tool_registry,
    filter_config_path="filter-config.json"
)

# Create MCP server with dynamic filtering
mcp = DynamicToolGatingMCP(
    fastapi=app,
    tool_registry=tool_registry,
    tool_gate_controller=tool_gate_controller,
    name="Docker Swarm MCP Server",
    description="Intelligent Docker management with dynamic tool filtering"
)

# Mount at /mcp endpoint
mcp.mount_http()
```

## Expected Tool Flow

### Before (Static Filtering):
1. Client connects → `list_tools` → Returns ALL 20+ tools
2. Client calls tool → Tool executes
3. Result: Context bloat, no task-specific filtering

### After (Dynamic Filtering):
1. Client sends request with `X-Task-Type: container_management`
2. MCP server extracts task_type from context
3. ToolGateController applies filters:
   - TaskTypeFilter: Only container-related tools (5-7 tools)
   - ResourceFilter: Exclude tools for unavailable resources
   - SecurityFilter: Exclude write ops if read-only mode
   - ContextLimitFilter: Enforce 7600 token cap
4. `list_tools` returns filtered subset (5-10 tools)
5. Client sees only relevant tools
6. Result: Clean context, task-focused operations

## Context Extraction Patterns

### MCP JSON-RPC Request Structure
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {
    "task_type": "container_management"  // ❌ NOT STANDARD MCP
  }
}
```

**Problem**: MCP spec doesn't define custom params in `tools/list`.

**Solution**: Use HTTP layer (headers/query params):

### HTTP Request to MCP Endpoint
```http
POST /mcp HTTP/1.1
X-Task-Type: container_management
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

OR

```http
GET /mcp?task_type=container_management HTTP/1.1
```

## Files Modified Summary

### New Files:
- ✅ `app/mcp/fastapi_mcp_integration.py` - DynamicToolGatingMCP class

### Modified Files:
- `app/main.py` - Switch from REST routes to MCP integration
- `.kilocode/mcp.json` - Configure task_type headers/params

### Preserved Files (No Changes):
- ✅ `app/mcp/tool_gating.py` - All filtering logic intact
- ✅ `app/mcp/tool_registry.py` - Tool discovery intact
- ✅ `filter-config.json` - Task configurations intact
- ✅ `tools.yaml` - Tool definitions intact

## Success Criteria

1. **MCP Protocol Compliance**: 
   - `/mcp` endpoint responds to JSON-RPC `tools/list` and `tools/call`
   - Not REST endpoints like `/containers` or `/networks`

2. **Dynamic Filtering**:
   - Different task_type → Different tools returned
   - 20+ total tools → 5-10 tools per task

3. **Context Management**:
   - Hard cap at 7600 tokens enforced
   - Warning at 5000 tokens

4. **Integration Test**:
   - MCP Inspector can connect
   - kilocode/opencode clients can use tools
   - Tool filtering works per request

## Next Steps

1. ✅ Review fastapi-mcp documentation (COMPLETE)
2. ✅ Understand class extension pattern (COMPLETE)
3. Create `app/mcp/fastapi_mcp_integration.py` with DynamicToolGatingMCP
4. Update `app/main.py` to use new MCP integration
5. Test with MCP Inspector
6. Configure `.kilocode/mcp.json` with task_type headers
7. Test with kilocode client
