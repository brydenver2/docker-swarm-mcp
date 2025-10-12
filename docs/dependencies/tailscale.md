# Tailscale

## Overview
A zero-config VPN built on WireGuard that creates secure private networks between devices.

## Short Description
Tailscale creates encrypted point-to-point connections between devices in your network. It's ideal for secure remote access to services without exposing them to the public internet, using WireGuard for fast, secure connections.

## Key Features
- Zero-config VPN based on WireGuard
- Peer-to-peer encrypted connections
- No public exposure required
- ACL-based access control
- MagicDNS for easy hostname resolution
- Cross-platform support (Linux, macOS, Windows, mobile)
- Subnet routing for accessing entire networks

## Security Considerations for Docker Swarm MCP Server
- **Private network**: Tailscale creates a private network, devices outside your Tailnet cannot access your MCP server
- **ACLs**: Use Tailscale ACLs to restrict which devices can access your Docker host
- **Still use authentication**: Configure MCP_ACCESS_TOKEN even on Tailscale networks for defense in depth
- **Device authorization**: Review and authorize devices joining your Tailnet
- **Better than public exposure**: Tailscale is significantly more secure than exposing Docker MCP to the public internet

## USE DEEPWIKI MCP TO ACCESS DEPENDENCY KNOWLEDGE!
To access the most up-to-date documentation for Tailscale, use the DeepWiki MCP to retrieve information directly from https://tailscale.com/kb/ and use the `ask_question` function with specific queries like "how can I [specific task]" to get targeted guidance.

## Official Source
[https://tailscale.com/kb/](https://tailscale.com/kb/)

## Quick Start
```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
