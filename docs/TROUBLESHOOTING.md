# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Docker Swarm MCP Server.

## Authentication Issues

### Error: "Invalid or missing access token"

This error occurs when the server receives a request with an invalid or missing authentication token.

**Symptom:**
```
INFO POST /mcp/ | status=401
{"detail":"Invalid or missing access token"}
```

**Common Causes:**

1. **MCP_ACCESS_TOKEN not set in the environment**
   
   **Solution:** Create a `.env` file or set the environment variable:
   ```bash
   # Generate a secure token
   openssl rand -hex 32
   
   # Add to .env file
   echo "MCP_ACCESS_TOKEN=<your-generated-token>" > .env
   
   # Or export as environment variable
   export MCP_ACCESS_TOKEN=<your-generated-token>
   ```

2. **Client using a different token than the server**
   
   **Solution:** Ensure your client is configured with the same token:
   ```bash
   # Check server logs for token length (without exposing the actual token)
   docker logs <container-name> | grep "Authentication: Single-token mode"
   
   # Verify your client configuration uses the correct token
   # For example, in MCP client config:
   {
     "headers": {
       "Authorization": "Bearer YOUR_TOKEN_HERE"
     }
   }
   ```

3. **Token has leading/trailing whitespace**
   
   **Solution:** Ensure the token has no extra spaces:
   ```bash
   # Bad (has trailing space)
   MCP_ACCESS_TOKEN="abc123 "
   
   # Good
   MCP_ACCESS_TOKEN="abc123"
   ```

4. **Using query parameter authentication (deprecated)**
   
   **Solution:** Use header-based authentication instead:
   ```bash
   # Bad (deprecated, won't work)
   curl "http://localhost:8000/mcp?accessToken=abc123"
   
   # Good (use Authorization header)
   curl -H "Authorization: Bearer abc123" http://localhost:8000/mcp/
   
   # Good (use X-Access-Token header)
   curl -H "X-Access-Token: abc123" http://localhost:8000/mcp/
   ```

### Error: Server fails to start with "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES"

This error occurs when the server starts without proper authentication configuration.

**Symptom:**
```
ValueError: Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES to be configured.
HINT: Create a .env file with MCP_ACCESS_TOKEN=your-secure-token
```

**Solution:**

1. **For docker-compose deployments:**
   ```bash
   # Create .env file in the same directory as docker-compose.yaml
   cat > .env << EOF
   MCP_ACCESS_TOKEN=$(openssl rand -hex 32)
   EOF
   
   # Restart the service
   docker-compose down
   docker-compose up -d
   ```

2. **For Docker Swarm stack deployments:**
   ```bash
   # Set environment variable before deploying
   export MCP_ACCESS_TOKEN=$(openssl rand -hex 32)
   
   # Deploy with environment variable
   docker stack deploy -c docker-swarm-mcp.yml mcp-server
   ```

3. **For production (using Docker secrets):**
   ```bash
   # Create a secret with your token
   openssl rand -hex 32 | docker secret create mcp_token -
   
   # Update your stack file to use the secret file:
   version: '3.8'
   services:
     mcp-server:
       image: brydenver2/docker-swarm-mcp:latest
       environment:
         # Use MCP_ACCESS_TOKEN_FILE to read from Docker secret
         - MCP_ACCESS_TOKEN_FILE=/run/secrets/mcp_token
       secrets:
         - mcp_token
   
   secrets:
     mcp_token:
       external: true
   
   # Deploy the stack
   docker stack deploy -c docker-swarm-mcp.yml mcp-server
   ```

4. **Using MCP_ACCESS_TOKEN_FILE (recommended for production):**
   ```bash
   # Create a token file
   openssl rand -hex 32 > /secure/path/mcp_token.txt
   chmod 600 /secure/path/mcp_token.txt
   
   # Set the file path environment variable
   export MCP_ACCESS_TOKEN_FILE=/secure/path/mcp_token.txt
   
   # MCP_ACCESS_TOKEN_FILE takes precedence over MCP_ACCESS_TOKEN
   # This is safer as the token is not exposed in process listings
   ```

### Debugging Authentication

**Enable DEBUG logging to see detailed authentication information:**

1. Set `LOG_LEVEL=DEBUG` in your environment or .env file
2. Restart the server
3. Check logs for authentication details:
   ```bash
   docker logs <container-name> 2>&1 | grep -i auth
   ```

**Server logs will show:**
- Token length (without exposing the actual token)
- Whether TOKEN_SCOPES or MCP_ACCESS_TOKEN is being used
- Token validation failures with hints

**Example debug output:**
```
INFO Authentication: Single-token mode enabled (MCP_ACCESS_TOKEN: 64 chars)
WARNING Authentication failed: Invalid token provided | token_length_received=32 | token_length_expected=64
```

## Docker Connection Issues

### Error: "Cannot connect to Docker daemon"

**Solution:**
- Ensure Docker socket is mounted: `-v /var/run/docker.sock:/var/run/docker.sock`
- For remote Docker, set `DOCKER_HOST` environment variable
- Check permissions on Docker socket

## Network Issues

### Error: "Connection refused" when accessing the server

**Solution:**
- Verify the container is running: `docker ps`
- Check port mapping: Container port 8000 should be published
- Verify firewall rules allow access to port 8000
- For Tailscale deployments, ensure `TAILSCALE_ENABLED=true` and auth key is set

## Configuration Issues

### Server starts but tools don't work

**Check:**
1. Docker socket is accessible (test with `docker ps` from inside container)
2. Authentication is configured correctly
3. CORS settings allow your client origin (set `ALLOWED_ORIGINS`)

## Getting Help

If you're still experiencing issues:

1. Check server logs: `docker logs <container-name>`
2. Verify environment variables: `docker inspect <container-name> | grep -A 20 Env`
3. Test authentication manually:
   ```bash
   # Health check (no auth required)
   curl http://localhost:8000/mcp/health
   
   # Tools list (auth required)
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":"1","method":"tools/list","params":{}}' \
        http://localhost:8000/mcp/
   ```
4. Review the [Security Guide](SECURITY.md) for production deployment best practices
5. Check [GitHub Issues](https://github.com/brydenver2/docker-swarm-mcp/issues) for similar problems
