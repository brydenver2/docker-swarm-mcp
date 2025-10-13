# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Features

### Authentication & Authorization

- **Bearer Token Authentication**: HMAC constant-time comparison prevents timing attacks
- **Multi-Token Support**: Configurable token scopes via `TOKEN_SCOPES` environment variable
- **Scope-Based Authorization**: Fine-grained access control per tool category
- **JWT Support**: Optional JWT tokens with scope claims (validated after HMAC check)
- **Header-Only Authentication**: Tokens accepted only via headers (`Authorization` or `X-Access-Token`); query parameters rejected as of v0.5.0

### Authentication Security Improvements

- **Removed Query Parameter Tokens**: URLs like `/mcp/?accessToken=...` exposed secrets in web server logs, reverse proxies, browser history, and referrer headers. This vector is eliminated in v0.5.0.
- **Custom Header Support**: The `X-Access-Token` header provides a simple alternative to the `Authorization` header for clients without advanced header configuration.
- **Redaction Enhancements**: Logging filters strip both `Authorization` and `X-Access-Token` headers to prevent accidental leakage in structured logs.
- **Client Guidance**: Documentation and client setup guides now default to header-based authentication patterns to reinforce secure usage.

### Network Security

- **TLS Support**: Full TLS configuration for remote Docker hosts
- **CORS Protection**: Configurable allowed origins (disable wildcards in production)
- **Input Validation**: Pydantic schema validation for all requests
- **Rate Limiting**: Configurable timeouts per operation type

### Container Security

- **Non-Root User (Dockerfile)**: Container image built with user `mcp` (UID 1000)
- **Docker Socket Access**: Requires write access to Docker socket for full functionality
  - ⚠️ **Security Tradeoff**: Docker socket access grants significant privileges
  - 📝 **Why Needed**: Container management requires write operations (create, start, stop, remove)
  - 🔒 **Mitigations**: Strong authentication, network isolation, monitoring
  - 💡 **Alternative**: For read-only monitoring, mount socket as `:ro` and disable write operations
- **Minimal Base Image**: Uses `python:3.12-slim` for reduced attack surface
- **No Unnecessary Privileges**: Container doesn't require privileged mode
- **Tailscale VPN Integration**: Optional secure networking with specific security considerations
  - ⚠️ **NET_ADMIN Capability**: Required for Tailscale network operations
  - 📝 **Why Needed**: Tailscale requires network administration privileges for VPN functionality
  - 🔒 **Mitigations**: Strong Tailscale authentication, ACL policies, network isolation
  - 💡 **Alternative**: Disable Tailscale (`TAILSCALE_ENABLED=false`) if not needed

### Secrets Management

- **Environment Variables**: All secrets configured via environment variables
- .kilocode/ is gitignored. Do not commit client config or tokens there. If a client (e.g., local tools) expects an Authorization header, use a runtime reference such as `Bearer ${MCP_ACCESS_TOKEN}` and rely on environment expansion or a secret manager. Never embed raw tokens in JSON files.

- **Secret Redaction**: Sensitive headers redacted in logs
- **No Hardcoded Credentials**: No default tokens or passwords in code
- **Tailscale Auth Key Security**: Multiple options for secure authentication
  - **File-Based Secrets**: Prefer `TAILSCALE_AUTH_KEY_FILE` over `TAILSCALE_AUTH_KEY`
  - **Docker Secrets**: Use Docker secrets for Tailscale auth keys in production
  - **Key Rotation**: Regular rotation of Tailscale auth keys

### Code Security

- **Dependency Management**: Poetry lock file for reproducible builds
- **Error Handling**: Generic error messages prevent information leakage
- **Input Sanitization**: All Docker SDK inputs validated

## Security Best Practices

> Tokens must be sent via headers. Prefer `Authorization: Bearer <token>` and fall back to `X-Access-Token: <token>` when clients need a simpler header.

### For Production Deployment

1. **Strong Access Tokens**
   ```bash
   # Generate cryptographically secure token
   openssl rand -hex 32
   ```

2. **Restrict CORS Origins**
   ```bash
   export ALLOWED_ORIGINS="https://your-domain.com"
   # NOT: ALLOWED_ORIGINS="*"
   ```

3. **Use TLS for Remote Access**
   - Deploy behind reverse proxy (nginx, Caddy)
   - Or use Tailscale/VPN for private networks
   - Never expose on public internet without TLS

4. **Limit Docker Socket Access**
   ```yaml
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock:ro  # Read-only
   ```

5. **Regular Updates**
   - Keep Docker Engine updated
   - Update Python dependencies regularly
   - Monitor security advisories

6. **Token Rotation**
   - Rotate access tokens periodically
   - Use different tokens for different clients
   - Implement token expiration if using JWT

7. **Network Isolation**
   - Use Docker networks to isolate MCP server
   - Firewall rules to restrict access
   - Consider using Tailscale ACLs

8. **Tailscale Security** (when enabled)
   - Use `TAILSCALE_AUTH_KEY_FILE` instead of environment variable
   - Configure Tailscale ACL policies for fine-grained access control
   - Enable state persistence with named volumes
   - Monitor Tailscale node status and connections
   - Rotate Tailscale auth keys periodically
   - Use appropriate tags for node organization and access control

### Environment Variable Security

**Required:**
```bash
MCP_ACCESS_TOKEN="your-secure-token-here"  # Min 32 characters
```

**Optional but Recommended:**
```bash
TOKEN_SCOPES='{"token1": ["read-only"], "token2": ["admin"]}'  # Scope-based access
ALLOWED_ORIGINS="https://your-domain.com"  # Specific origins only
LOG_LEVEL="INFO"  # Don't use DEBUG in production
```

## Known Security Considerations

- ✅ Query parameter authentication has been removed; tokens are never transmitted in URLs, eliminating a common leakage vector.

### Docker Socket Access

This server requires Docker socket access to manage containers. This grants significant privileges:

- ⚠️ **Full Docker API Access**: Can create/destroy any container
- ⚠️ **Potential Privilege Escalation**: Docker socket access ≈ root access on the host
- ⚠️ **Write Access Required**: Most operations (create, start, stop, remove) need write permissions
- ✅ **Mitigations**:
  - Strong Bearer token authentication (HMAC-verified)
  - Scope-based authorization for fine-grained access control
  - Network isolation (don't expose publicly without VPN/TLS)
  - Audit logging for all operations
  - Regular token rotation
  - Read-only mount (`:ro`) for monitoring-only deployments

### Tailscale VPN Integration

When Tailscale is enabled (`TAILSCALE_ENABLED=true`), additional security considerations apply:

- ⚠️ **NET_ADMIN Capability**: Required for Tailscale network operations
  - Grants network administration privileges to the container
  - Allows modification of network interfaces and routing
  - Required for Tailscale's VPN functionality

- ⚠️ **TUN Device Access**: Required for VPN tunnel creation
  - `/dev/net/tun` device mounted into container
  - Enables creation of network tunnels

- ⚠️ **Tailscale Auth Key**: Sensitive credential that grants network access
  - Must be protected like other authentication tokens
  - Grants access to your Tailscale network

- ✅ **Mitigations**:
  - Use `TAILSCALE_AUTH_KEY_FILE` instead of environment variable for production
  - Implement Tailscale ACL policies to restrict access
  - Use Tailscale tags for fine-grained access control
  - Enable state persistence to maintain node identity
  - Monitor Tailscale connections and node status
  - Regular rotation of Tailscale auth keys
  - Disable Tailscale when not needed (`TAILSCALE_ENABLED=false`)

- 🔒 **Security Benefits**:
  - Encrypted network traffic between nodes
  - Zero-trust networking model
  - Fine-grained access control via ACLs
  - Secure remote access without public exposure

### JWT Decode Without Verification

**File**: `app/core/auth.py` Line 106

The code uses `jwt.decode(token, options={"verify_signature": False})` which Semgrep flags as a security issue.

**This is SAFE because:**
1. Token authenticity is verified with HMAC (constant-time comparison) BEFORE JWT decode
2. JWT decode is ONLY used to extract scope claims from the payload
3. Not used for authentication - only for authorization metadata extraction
4. The decode happens after successful HMAC validation on line 74

### Health Check Endpoint

The `/mcp/health` endpoint is **unauthenticated** by design for monitoring systems.

**Information Exposed:**
- Server status (healthy/unhealthy)
- Docker engine reachability
- Server version

**No Sensitive Data:** Docker details, containers, or configuration are NOT exposed.

## Reporting a Vulnerability

If you discover a security vulnerability, please email security@yourrealdomain.com or open a private security advisory on GitHub.

**Please include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

**Response Time:**
- Initial response: Within 48 hours
- Fix timeline: Varies by severity (critical issues prioritized)
- Public disclosure: After fix is available (coordinated disclosure)

## Security Checklist for Deployment

- [ ] Generated strong random access token (min 32 characters)
- [ ] Set `ALLOWED_ORIGINS` to specific domains (not `*`)
- [ ] Deployed behind TLS reverse proxy or VPN
- [ ] Docker socket mounted read-only where possible
- [ ] Reviewed and configured token scopes
- [ ] Enabled authentication on all endpoints
- [ ] Tested token rotation procedures
- [ ] Configured logging to secure location
- [ ] Set up monitoring for failed auth attempts
- [ ] Documented incident response procedures
- [ ] Regular security updates scheduled
- [ ] Backup and disaster recovery tested

## Security Audit History

- **2025-10-11**: Initial security review with Semgrep
  - 1 false positive (JWT decode) - documented and safe
  - Fixed: Root user in docker-compose (removed `user: "0:0"`)
  - Fixed: Health check endpoint path mismatch
  - Added: Read-only Docker socket mount

## Dependencies

Security advisories monitored for:
- FastAPI
- uvicorn
- docker (Python SDK)
- pydantic
- PyJWT (optional)

Updates tracked via Dependabot and Poetry.
