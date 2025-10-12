# ngrok

## Overview
A secure tunneling service that exposes local servers behind NATs and firewalls to the public internet.

## Short Description
ngrok creates secure tunnels from a public endpoint to a locally running web service. It's useful for exposing development servers, testing webhooks, and providing temporary remote access to services.

## Key Features
- HTTPS tunnels to localhost
- TCP and HTTP(S) protocol support
- Custom subdomains (paid plans)
- Request inspection and replay
- Authentication and access control
- Webhook testing

## Security Considerations for Docker Swarm MCP Server
- **Always use authentication**: ngrok tunnels are public by default. Enable HTTP basic auth or use ngrok's built-in authentication
- **Use access tokens**: Configure MCP_ACCESS_TOKEN to protect your Docker operations
- **Monitor tunnel activity**: Use ngrok's dashboard to monitor connections
- **Temporary use only**: ngrok is best for development/testing, not production
- **Rate limiting**: Consider implementing rate limits on your MCP endpoints

## USE DEEPWIKI MCP TO ACCESS DEPENDENCY KNOWLEDGE!
To access the most up-to-date documentation for ngrok, use the DeepWiki MCP to retrieve information directly from https://ngrok.com/docs and use the `ask_question` function with specific queries like "how can I [specific task]" to get targeted guidance.

## Official Source
[https://ngrok.com/docs](https://ngrok.com/docs)

## Quick Start
```bash
ngrok http 8000
```
