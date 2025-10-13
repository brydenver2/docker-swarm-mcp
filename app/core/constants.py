APP_NAME: str = "Docker Swarm MCP Server"
APP_VERSION: str = "0.5.0"

# Centralized MCP route paths for reference in responses/documentation
# Note: tools_list is deprecated (removed in v0.5.0), use mcp_jsonrpc with method "tools/list" instead
MCP_ROUTES: dict[str, str] = {
    "mcp_jsonrpc": "/mcp/",
    "tools_list": "/mcp/tools",  # DEPRECATED: Removed in v0.5.0, use JSON-RPC instead
    "health": "/mcp/health",
    "detailed_health": "/mcp/healthz",
}
