# Changelog

All notable changes to the Docker Swarm MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Introduced `pytest-asyncio` to the developer toolchain and set `asyncio_mode=auto` so coroutine-based tests execute natively under pytest.
- Added a Swarm-aware `service-logs` tool/endpoint so MCP clients can stream aggregated task logs without falling back to `docker service logs` manually.

### Changed

- Hardened `Settings` reload semantics to preserve the singleton instance while refreshing environment-driven values.
- Derived deterministic session identifiers from presented auth tokens when `X-Session-ID` is absent, improving tool-gating consistency.
- Tuned meta intent keyword mapping to avoid false positives from generic “query” terms during tool discovery.
- Reworked the MCP endpoint integration tests to use assertions/skip logic instead of returning raw responses, eliminating pytest return warnings and clarifying expectations.
- Migrated all Pydantic schema models to use `model_config = ConfigDict(...)`, removing the deprecated class-based `Config` pattern and silencing upcoming v2 deprecation warnings.
- Normalized `since` parsing in `get-logs` to accept either RFC3339 timestamps or Unix seconds and return clearer guidance when clients accidentally pass service IDs to the container log endpoint.

### Fixed

- Adjusted X-Access-Token authentication to emit 401 vs 403 responses based on the JSON-RPC method being invoked, aligning with test expectations.
- Expanded PEM/certificate redaction so shorter secrets and `_pem` keys are consistently masked in structured logs.
- Added a broad exception guard during Docker client bootstrap to surface non-DockerException failures as “engine unreachable” runtime errors.
- Swarm stack deployments now stamp the standard `com.docker.stack.*` labels on every service (namespace, service name, image), ensuring `docker stack ls` shows stacks created through the MCP endpoint.

### Testing

- Updated retry behavior tests to assert the corrected exponential backoff calculation under the asyncio plugin.
- Swapped the FastAPI `TestClient` fixture for an `httpx.AsyncClient` + `ASGITransport` harness to align with the new transport API and eliminate the deprecated `app=` shortcut warnings during pytest runs.

## [0.5.0] - 2025-10-14

### ⚠️ BREAKING CHANGES

- **Authentication**: Query parameter authentication (`?accessToken=...`) has been removed for security reasons.
- **Migration Required**: Update client configurations to send tokens via headers:
  - Standard: `Authorization: Bearer <token>`
  - Simple: `X-Access-Token: <token>`
- **Reason**: Tokens in URLs leak through server logs, browser history, referrer headers, and network monitoring tools.

### Security

- Eliminated token leakage via URL-based authentication.
- Tokens are now accepted only through headers (Authorization or X-Access-Token).
- Enhanced logging redaction to cover the `X-Access-Token` header.

### Changed

- Updated `HTTPBearerOrQuery` security class to prefer Authorization header and fall back to `X-Access-Token`.
- Refreshed documentation across README and docs to explain header-only authentication.
- Reworked MCP protocol tests to verify header-based authentication paths.
- Updated authentication tests to use `test_client_with_mock` fixture for proper app state initialization.

### Fixed

- **Authentication test design issues**: Tests were checking auth on the public `/mcp/health` endpoint instead of authenticated JSON-RPC endpoints; updated failing cases to target `/mcp/` methods that enforce authentication.
- **Updated 9 authentication tests** to properly validate token checking on authenticated endpoints.
- **Clarified public health endpoint intent** so monitoring and orchestration tools continue to function without credentials.
- **Removed deprecated REST-style `/mcp/tools` endpoint**: Deleted the `mcp_router` import and registration from `app/main.py` that conflicted with the new JSON-RPC endpoint structure introduced in v0.3.0.
- **Standardized test token usage**: Updated all test files to consistently use `"test-token-123"` token for authentication testing.

### Testing

- All 33 authentication tests now pass (11 in `test_auth_simple.py` + 22 in `test_auth_endpoints.py`).
- Tests comprehensively validate authentication on JSON-RPC endpoints, header precedence, token rejection, and security features.
- Documented public health endpoint access as intentional design for monitoring systems.
- Comprehensive coverage of authentication methods (Authorization header, X-Access-Token header).
- Edge case testing includes timing attack resistance, whitespace handling, and multiple header scenarios.

### Documentation

- Updated `docs/AUTH_TEST_RESULTS.md` with comprehensive test coverage summary.
- Clarified test design and authentication validation approach.

### Migration Guide

- See `README.md` and `docs/MCP-CLIENT-SETUP.md` for detailed migration instructions.
- All configurations using `?accessToken=...` must switch to header-based authentication before upgrading.

## [0.4.0] - 2025-10-13

### Added

- **Poetry Script Shortcuts**: Added `poetry run test`, `poetry run test-fast`, and `poetry run test-cov` console entry points for quick test workflows.

### Changed

- **MCP Endpoint Alignment**: JSON-RPC endpoint now lives at `/mcp/` (trailing slash required) to match client documentation.
- **REST API Mount Point**: Optional REST routers are exposed under `/api/*` when `ENABLE_REST_API=true`, keeping MCP transport default.
- **Documentation Refresh**: README and quick reference updated to reflect version 0.5.0 and new routing details.

### Fixed

- **Poetry Execution**: Restored the backing module so `poetry run test` and related scripts execute without import errors.

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
