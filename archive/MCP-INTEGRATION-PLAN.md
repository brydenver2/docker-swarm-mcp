# MCP Protocol Integration Plan

**Objective**: Add proper MCP JSON-RPC protocol support to the Docker Swarm MCP Server using fastapi-mcp library while preserving 100% of existing tool gating and context optimization functionality.

**Status**: 🟡 In Progress  
**Started**: 2025-10-08  
**Estimated Completion**: 3-4 hours

---

## Executive Summary

### Problem Statement
The Docker Swarm MCP Server was built as a REST API instead of implementing the MCP JSON-RPC protocol specification. While all Docker operations and tool gating logic are correctly implemented, MCP clients (like kilocode/opencode) cannot use the server because it doesn't speak the MCP protocol.

### Solution Approach
Integrate the `fastapi-mcp` library to add MCP JSON-RPC protocol support. Create a custom `DynamicToolGatingMCP` class that extends `FastApiMCP` to preserve our dynamic per-request tool filtering using the existing `ToolGateController`.

### What Will Be Preserved (100%)
- ✅ All tool gating logic (TaskTypeFilter, ResourceFilter, SecurityFilter)
- ✅ Context size enforcement (7600 token hard limit, 5000 warning)
- ✅ Dynamic filtering based on task-type
- ✅ Configuration files (filter-config.json, tools.yaml)
- ✅ All logging and observability
- ✅ All Docker operation implementations

### What Will Change
- ❌ REST API endpoints replaced with MCP JSON-RPC protocol
- ✅ Single `/mcp` endpoint accepting JSON-RPC requests
- ✅ Proper MCP methods: `initialize`, `tools/list`, `tools/call`
- ✅ MCP-compliant message format

---

## Phase 1: Dependency & Setup
**Status**: ⬜ Not Started  
**Estimated Time**: 15 minutes

### Tasks
- [√] **T151**: Add `fastapi-mcp` to pyproject.toml dependencies
- [√]  **T152**: Run `poetry install` to install fastapi-mcp
- [√] **T153**: Verify installation and version compatibility
- [√] **T154**: Review fastapi-mcp documentation for OpenAPI conversion

### Success Criteria
- fastapi-mcp installed successfully
- No dependency conflicts
- Import `from fastapi_mcp import FastApiMCP` works

---

## Phase 2: Core Integration Class
**Status**: ⬜ Not Started  
**Estimated Time**: 2 hours

### Tasks
- [ ] **T155**: Create `app/mcp/fastapi_mcp_integration.py`
- [ ] **T156**: Implement `DynamicToolGatingMCP` class extending `FastApiMCP`
- [ ] **T157**: Override `handle_list_tools()` method for dynamic filtering
- [ ] **T158**: Implement `_extract_task_type()` from MCP request params
- [ ] **T159**: Implement `_convert_to_mcp_tools()` for tool format conversion
- [ ] **T160**: Add integration with existing `ToolGateController`
- [ ] **T161**: Preserve context size checking and enforcement

### Technical Details

#### Class Structure
```python
class DynamicToolGatingMCP(FastApiMCP):
    def __init__(self, app, tool_gate_controller: ToolGateController, **kwargs)
    async def handle_list_tools(self, request)
    def _extract_task_type(self, request)
    def _convert_to_mcp_tools(self, tools: dict)
```

#### Key Integration Points
1. **Tool Filtering Flow**:
   - Extract task_type from MCP request params
   - Create FilterContext with task_type and request_id
   - Call `tool_gate_controller.get_available_tools(context)`
   - Check context size with `tool_gate_controller.get_context_size()`
   - Convert filtered tools to MCP format

2. **Context Size Enforcement**:
   - Maintain 7600 token hard limit
   - Maintain 5000 token warning threshold
   - Use existing tiktoken/char-based calculation

### Success Criteria
- `DynamicToolGatingMCP` class implemented
- All existing tool gating logic integrated
- Context size limits enforced
- Tool filtering works per-request

---

## Phase 3: Application Integration
**Status**: ⬜ Not Started  
**Estimated Time**: 30 minutes

### Tasks
- [ ] **T162**: Update `app/main.py` to initialize `DynamicToolGatingMCP`
- [ ] **T163**: Mount MCP endpoint at `/mcp` or `/` (TBD)
- [ ] **T164**: Configure authentication for MCP endpoints
- [ ] **T165**: Update startup logging to reflect MCP protocol
- [ ] **T166**: Add MCP-specific health check endpoint (if needed)

### Code Changes in main.py
```python
from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP

# After existing ToolGateController initialization
mcp = DynamicToolGatingMCP(
    app=app,
    tool_gate_controller=tool_gate_controller,
    auth_config=...  # TBD based on fastapi-mcp docs
)

# Mount MCP endpoint
mcp.mount_http(path="/mcp")
```

### Success Criteria
- MCP endpoint mounted successfully
- Server starts without errors
- Health check confirms MCP protocol available

---

## Phase 4: Protocol Compliance Testing
**Status**: ⬜ Not Started  
**Estimated Time**: 1 hour

### Tasks
- [ ] **T167**: Test MCP `initialize` handshake
- [ ] **T168**: Test `tools/list` without task_type filter
- [ ] **T169**: Test `tools/list` with task_type=container-ops (expect 6 tools)
- [ ] **T170**: Test `tools/list` with task_type=network-ops (expect 3 tools)
- [ ] **T171**: Test `tools/call` for container operations
- [ ] **T172**: Test context size limits (verify 7600 hard cap)
- [ ] **T173**: Test authentication/authorization
- [ ] **T174**: Test with actual MCP client (kilocode/opencode)

### Test Scenarios

#### 1. Tool List Without Filter
```json
POST /mcp
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```
Expected: All tools up to max_tools (10) returned

#### 2. Tool List With Container Filter
```json
POST /mcp
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {
    "task_type": "container-ops"
  }
}
```
Expected: 6 container-related tools only

#### 3. Tool Call
```json
POST /mcp
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "ping",
    "arguments": {}
  }
}
```
Expected: Docker ping response

### Success Criteria
- All MCP protocol methods work correctly
- Tool filtering works as expected
- Context size limits enforced
- MCP clients can connect and use tools

---

## Phase 5: MCP Client Configuration
**Status**: ⬜ Not Started  
**Estimated Time**: 30 minutes

### Tasks
- [ ] **T175**: Update `.kilocode/mcp.json` with proper MCP server config
- [ ] **T176**: Test with kilocode MCP client
- [ ] **T177**: Create test containers for kilocode testing
- [ ] **T178**: Update documentation with MCP client examples

### MCP Client Config
```json
{
  "mcpServers": {
    "docker-swarm-mcp": {
      "type": "streamable-http",
      "url": "http://localhost:8000/mcp",
      "headers": {
        "Authorization": "Bearer test-token-12345"
      },
      "alwaysAllow": [
        "ping",
        "info",
        "version",
        "list-containers",
        "inspect-container"
      ]
    }
  }
}
```

### Success Criteria
- kilocode successfully connects to MCP server
- Tool discovery works from kilocode
- Tool execution works from kilocode
- Dynamic filtering works with MCP clients

---

## Phase 6: Docker Deployment Update
**Status**: ⬜ Not Started  
**Estimated Time**: 30 minutes

### Tasks
- [ ] **T179**: Rebuild Docker image with fastapi-mcp dependency
- [ ] **T180**: Update docker-compose.yaml if needed
- [ ] **T181**: Test containerized deployment
- [ ] **T182**: Verify MCP protocol works in container

### Success Criteria
- Docker image builds successfully
- Container runs with MCP protocol
- Health checks pass
- MCP clients can connect to containerized server

---

## Phase 7: Documentation & Cleanup
**Status**: ⬜ Not Started  
**Estimated Time**: 30 minutes

### Tasks
- [ ] **T183**: Update README.md with MCP protocol information
- [ ] **T184**: Update MCP-CLIENT-SETUP.md with working examples
- [ ] **T185**: Remove or deprecate REST endpoint documentation
- [ ] **T186**: Update architecture diagrams
- [ ] **T187**: Create migration guide for existing users (if any)
- [ ] **T188**: Update CHANGELOG

### Documentation Updates
- Architecture section: Add MCP JSON-RPC protocol flow
- Client setup: Update with tested configurations
- Tool gating: Document how it works with MCP protocol
- Examples: Add working curl/client examples

### Success Criteria
- Documentation accurately reflects MCP implementation
- Examples are tested and working
- Migration path clear for any existing users

---

## Risk Mitigation

### Risk 1: fastapi-mcp Alpha Status
**Mitigation**: 
- Vendor the code if stability issues arise
- Fork and maintain if needed
- Contribute fixes upstream

### Risk 2: Dynamic Filtering Not Supported
**Status**: ✅ Solved via custom class extension
**Mitigation**: 
- Override `handle_list_tools()` method
- Implement custom filtering logic

### Risk 3: Breaking Existing Tool Gating
**Mitigation**:
- Preserve all existing classes unchanged
- Create integration layer only
- Extensive testing of filtering logic

### Risk 4: MCP Client Compatibility
**Mitigation**:
- Test with multiple MCP clients
- Follow MCP spec strictly
- Document any client-specific quirks

---

## Success Metrics

### Functional
- ✅ MCP JSON-RPC protocol fully implemented
- ✅ All 6 tool types working (container, network, volume, service, stack, system)
- ✅ Dynamic tool filtering preserved
- ✅ Context size limits enforced
- ✅ Authentication working

### Performance
- ✅ Tool list response < 100ms
- ✅ Tool call response < 500ms (depends on Docker op)
- ✅ Context size reduction: 20+ tools → 5-10 tools
- ✅ Token usage: < 5000 tokens typical, < 7600 hard limit

### Quality
- ✅ Zero regression in existing tool gating
- ✅ MCP spec compliance verified
- ✅ Works with kilocode/opencode clients
- ✅ Production-ready deployment

---

## Rollback Plan

If integration fails or causes issues:

1. **Immediate**: Remove fastapi-mcp dependency
2. **Quick Fix**: Revert to REST API endpoints
3. **Alternative**: Implement minimal JSON-RPC layer manually
4. **Fallback**: Keep REST API alongside MCP for transition period

---

## Progress Tracking

**Overall Progress**: 0/38 tasks complete (0%)

### Phase Status
- Phase 1 (Dependency): ⬜ 0/4 tasks
- Phase 2 (Integration): ⬜ 0/7 tasks
- Phase 3 (Application): ⬜ 0/5 tasks
- Phase 4 (Testing): ⬜ 0/8 tasks
- Phase 5 (Client Config): ⬜ 0/4 tasks
- Phase 6 (Deployment): ⬜ 0/4 tasks
- Phase 7 (Documentation): ⬜ 0/6 tasks

---

## Next Steps

**Immediate Action**: Begin Phase 1 - Add fastapi-mcp dependency

**Command**:
```bash
cd ~/Documents/Scripting\ Projects/docker-mcp-server
# Add to pyproject.toml and run poetry install
```

---

*Last Updated: 2025-10-08 16:50 PST*
