# Changelog

All notable changes to the Docker Swarm MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-10-12

This release adds optional Tailscale VPN integration for secure remote access to Docker Swarm environments. The integration provides encrypted networking while maintaining backward compatibility and comprehensive security controls.

### Added

- **Tailscale VPN Integration**: Optional secure networking feature
  - Built-in Tailscale client installation in Docker image
  - Conditional activation via `TAILSCALE_ENABLED` environment variable
  - Automatic IP address logging in container startup logs
  - Comprehensive status monitoring and logging in application
  - State persistence for node identity across container restarts

- **Tailscale Configuration Options**: Full control over VPN settings
  - `TAILSCALE_ENABLED`: Master toggle (default: `false` for backward compatibility)
  - `TAILSCALE_AUTH_KEY` / `TAILSCALE_AUTH_KEY_FILE`: Authentication methods
  - `TAILSCALE_HOSTNAME`: Custom hostname in Tailscale network
  - `TAILSCALE_TAGS`: Node tags for ACL policy control
  - `TAILSCALE_EXTRA_ARGS`: Additional Tailscale command-line arguments
  - `TAILSCALE_STATE_DIR`: Persistent state directory
  - `TAILSCALE_TIMEOUT`: Operation timeout configuration

- **Enhanced Entrypoint Script**: Robust Tailscale lifecycle management
  - Conditional Tailscale activation based on environment configuration
  - Secure authentication with file-based key support
  - Graceful shutdown handling with proper cleanup
  - Comprehensive error handling and validation
  - Automatic IP address discovery and logging

- **Docker Compose Integration**: Production-ready Tailscale configuration
  - NET_ADMIN capability for network operations
  - TUN device access for VPN functionality
  - Persistent volume support for state directory
  - Docker secrets integration for auth keys

### Security

- **Tailscale Security Documentation**: Comprehensive security considerations
  - NET_ADMIN capability requirements and implications documented
  - TUN device access security considerations
  - Tailscale auth key management best practices
  - Production security checklist for Tailscale deployments
  - File-based authentication recommended over environment variables

- **Security Audit Enhancement**: Updated security documentation
  - Added Tailscale-specific security considerations to SECURITY.md
  - Enhanced security checklist with Tailscale deployment requirements
  - Documented security benefits of Tailscale VPN integration

### Changed

- **Dockerfile**: Added Tailscale installation and configuration
  - Tailscale client installation during build process
  - Tailscale state directory creation and permissions
  - Non-root user access to Tailscale directories

- **docker-compose.yaml**: Added Tailscale configuration options
  - Environment variables for Tailscale integration
  - Conditional capability and device requirements
  - Optional volume mounting for state persistence

- **env.example**: Enhanced with Tailscale configuration examples
  - Comprehensive Tailscale environment variable documentation
  - Production security recommendations
  - Configuration examples for different deployment scenarios

- **Documentation**: Updated all documentation with Tailscale integration
  - README.md: Added Tailscale features, configuration, and examples
  - SECURITY.md: Enhanced with Tailscale security considerations
  - CHANGELOG.md: This release documentation

### Fixed

- **Backward Compatibility**: Tailscale integration disabled by default
  - Existing deployments unaffected by default configuration
  - No breaking changes to current functionality
  - Optional feature requires explicit enablement

## [0.2.0] - 2025-10-11

This release adds multiple mechanisms for tool discovery to ensure compatibility with all MCP clients. Instructional content is now available through both MCP prompts (for supporting clients) and callable meta-tools (for universal access).

### Added

- **MCP Prompts Capability**: Added instructional prompts for tool discovery guidance
  - Three instructional prompts: `discover-tools`, `list-task-types`, and `intent-query-help`
  - `prompts/list` JSON-RPC method to discover available prompts
  - `prompts/get` JSON-RPC method to retrieve specific prompt content
  - Dynamic prompt content based on current filter configuration from `filter-config.json`
  - Helps LLMs understand how to discover all 23 tools beyond the initial 10 shown by default

- **Meta-Tools for Universal Compatibility**: Added callable meta-tools that work with all MCP clients
  - Three meta-tools: `discover-tools`, `list-task-types`, and `intent-query-help`
  - Available through standard `tools/call` interface in the "meta-ops" task type
  - Returns structured instructional content for tool discovery and filtering
  - Ensures compatibility with MCP clients that don't support prompts capability

- **New "meta-ops" Task Type**: Added dedicated task type for organizing meta-tools
  - Contains discover-tools, list-task-types, and intent-query-help meta-tools
  - Intent keywords include "help", "guide", "discover", "available tools", etc.
  - Enables automatic discovery when users ask help-related questions

### Changed

- Enhanced tool discovery with dual approach: prompts for clients that support them, meta-tools for universal compatibility
- Updated `initialize` response to advertise `prompts` capability with `listChanged: false`
- Enhanced MCP endpoint routing to handle `prompts/list` and `prompts/get` methods
- Updated documentation to include both prompts and meta-tools usage examples and best practices

### Security

- **Container Security Hardening**: Removed root user override in `docker-compose.yaml`
  - Removed `user: "0:0"` that was bypassing Dockerfile's non-root user
  - Docker socket now mounted read-only (`:ro`) for additional security
  - Container runs as user `mcp` (UID 1000) with docker group access
  
- **Health Check Fix**: Corrected health check endpoint path
  - Fixed `Dockerfile` and `docker-compose.yaml` to use `/mcp/health` instead of `/mcp/healthz`
  - Health checks now function correctly
  
- **JWT Decode Documentation**: Added comprehensive security notes
  - Documented why `verify_signature=False` is safe in `app/core/auth.py`
  - Token verified with HMAC before JWT decode (used only for scope extraction)
  - Addresses Semgrep security warning with clear explanation

- **Security Policy**: Created `SECURITY.md` with:
  - Security features and best practices
  - Production deployment checklist
  - Vulnerability reporting process
  - Security audit history
  - Comprehensive security considerations documentation

- **Security Audit Report**: Created `SECURITY-AUDIT-REPORT.md`
  - Semgrep OSS scan results (0 critical issues)
  - Manual code review findings
  - All vulnerabilities addressed and documented
  - Approved for public release

- **Roadmap**: Created `ROADMAP.md` with feature planning
  - v0.2.0: Tailscale/ngrok integration, token rotation, monitoring
  - v0.3.0: Advanced Docker features, multi-cluster support
  - v1.0.0: Stable release milestone
  - Open-ended for community contributions

### Added

- **Intent-Based Tool Discovery**: Automatic task-type detection from natural language queries
  - Added `IntentClassifier` with keyword-based pattern matching
  - Server analyzes queries like "list containers" or "deploy stack" to determine relevant tools
  - Returns only 2-6 relevant tools per request instead of all 23 tools
  - Dramatically reduces context size without requiring client configuration
  - Supports `query` parameter in `tools/list` JSON-RPC method
  - Configurable keyword mappings in `filter-config.json`
  - Backward compatible with explicit `task_type` parameter
  - New configuration options: `INTENT_CLASSIFICATION_ENABLED`, `INTENT_FALLBACK_TO_ALL`

### Changed

- **Tool Gating**: Enhanced `FilterContext` to support intent-based filtering
  - Added `query`, `detected_task_types`, and `intent_confidence` fields
  - `TaskTypeFilter` now supports multiple detected task types
  - Response `_metadata` includes classification method and detected types

- **Client Configuration**: Simplified MCP client setup
  - Removed need for multiple server configurations with different task types
  - Single server connection with automatic tool filtering
  - Updated `.kilocode/mcp.json` to remove `alwaysAllow` list
  - Updated documentation to show intent-based approach as recommended pattern

### Deprecated

- **Multi-Server Task-Type Configuration**: The pattern of creating multiple MCP server configurations with different `X-Task-Type` headers is deprecated
  - This approach didn't actually reduce context size (all tools still loaded)
  - Use intent-based discovery with a single server configuration instead
  - Explicit `task_type` parameter still supported for backward compatibility

### Fixed - Critical

- **DateTime Serialization Bug**: Fixed JSON serialization errors for all Docker operations
  - Docker SDK returns `datetime` objects that weren't being converted to JSON-compatible strings
  - Added `.isoformat()` conversion for all datetime fields in `docker_client.py`
  - Affected operations: `list-containers`, `create-container`, `list-networks`, `create-network`, `list-volumes`, `create-volume`
  - All datetime fields now properly serialize as ISO 8601 strings (e.g., "2025-10-11T03:49:57.984216+00:00")
  - Resolves: `Object of type datetime is not JSON serializable` errors

- **Missing System Service Implementation**: Fixed "Service function not implemented" errors
  - Created `app/services/system_service.py` with `ping()` and `info()` functions
  - Added system operations to service map in `fastapi_mcp_integration.py`
  - System tools (`ping`, `info`) now fully functional via MCP

### Fixed - Protocol

- **JSON-RPC 2.0 Compliance**: Fixed response serialization to strictly follow JSON-RPC 2.0 specification
  - Responses now include either `result` OR `error`, never both fields simultaneously
  - Implemented custom serialization function `_serialize_jsonrpc_response()` to properly exclude null values
  - This resolves MCP client errors like "Unrecognized key(s) in object: 'error'"

- **Import Conflicts**: Resolved redundant `settings` imports in `fastapi_mcp_integration.py` that were causing Internal Server Errors

- **Endpoint URL**: Clarified that the MCP endpoint requires a trailing slash: `/mcp/v1/`
  - FastAPI redirects `/mcp/v1` to `/mcp/v1/` which can cause connection issues
  - Updated all documentation to reflect the correct URL

### Changed

- Updated README.md with corrected endpoint URL and added Kilo Code / Cursor configuration example
- Updated docs/MCP-CLIENT-SETUP.md with comprehensive configuration examples for all MCP clients
- Updated docs/MCP-QUICK-REFERENCE.md with corrected URLs throughout
- Updated docs/MCP-JSON-RPC-USAGE.md with JSON-RPC 2.0 compliance notes and clarifications
- Updated dev_server.py to display correct endpoint URL with trailing slash notation

### Documentation

- Added new "Protocol" section to README.md explaining JSON-RPC 2.0 implementation
- Added Kilo Code / Cursor configuration examples across all documentation
- Clarified trailing slash requirement in endpoint URLs
- Added JSON-RPC 2.0 compliance badges and notes to MCP-JSON-RPC-USAGE.md

## [0.1.0] - Initial Release

### Added

- HTTP-based Model Context Protocol (MCP) server for Docker operations
- JSON-RPC 2.0 protocol implementation
- 20 Docker management tools across 6 categories:
  - System operations (ping, info)
  - Container operations (list, create, start, stop, remove, logs)
  - Compose stack operations (deploy, list, remove)
  - Swarm service operations (list, scale, remove)
  - Network operations (list, create, remove)
  - Volume operations (list, create, remove)
- Tool gating system with task-type filtering
- Bearer token authentication
- Schema validation for requests and responses
- Docker client support for local socket, TLS, and SSH connections
- Comprehensive documentation and client setup guides

