#!/bin/bash

# Docker Swarm MCP Server Entrypoint Script
# Handles conditional Tailscale activation and Uvicorn startup

set -euo pipefail

# Default values
TAILSCALE_ENABLED="${TAILSCALE_ENABLED:-false}"
TAILSCALE_STATE_DIR="${TAILSCALE_STATE_DIR:-/var/lib/tailscale}"
TAILSCALE_TIMEOUT="${TAILSCALE_TIMEOUT:-30}"
TAILSCALE_SOCK="/tmp/tailscaled.sock"
UVICORN_CMD="uvicorn app.main:app --host 0.0.0.0 --port 8000"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

# Error handling function
error_exit() {
    log "ERROR: $*"
    exit 1
}

# Cleanup function for graceful shutdown
cleanup() {
    log "Received shutdown signal, cleaning up..."
    if [[ "${TAILSCALE_ENABLED}" == "true" ]]; then
        log "Stopping Tailscale..."
        tailscale down 2>/dev/null || true
        pkill -f tailscaled 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Function to read from file or environment variable
get_config_value() {
    local var_name="$1"
    local file_var_name="${var_name}_FILE"
    local file_path="${!file_var_name:-}"
    
    if [[ -n "${file_path}" && -f "${file_path}" ]]; then
        cat "${file_path}"
    else
        echo "${!var_name:-}"
    fi
}

# Function to validate Tailscale configuration
validate_tailscale_config() {
    log "Validating Tailscale configuration..."
    
    local auth_key
    auth_key=$(get_config_value "TAILSCALE_AUTH_KEY")
    
    if [[ -z "${auth_key}" ]]; then
        error_exit "TAILSCALE_AUTH_KEY is required when Tailscale is enabled"
    fi
    
    log "Tailscale configuration validated successfully"
}

# Function to start Tailscaled daemon
start_tailscaled() {
    log "Starting Tailscaled daemon..."
    
    # Create state directory if it doesn't exist
    mkdir -p "${TAILSCALE_STATE_DIR}"
    
    # Start tailscaled with custom socket
    tailscaled \
        --state="${TAILSCALE_STATE_DIR}" \
        --socket="${TAILSCALE_SOCK}" \
        --port=41641 \
        --tun=userspace-networking &
    
    local tailscaled_pid=$!
    log "Tailscaled started with PID: ${tailscaled_pid}"
    
    # Wait for socket to be created
    local wait_time=0
    while [[ ! -S "${TAILSCALE_SOCK}" ]] && [[ $wait_time -lt ${TAILSCALE_TIMEOUT} ]]; do
        sleep 1
        wait_time=$((wait_time + 1))
    done
    
    if [[ ! -S "${TAILSCALE_SOCK}" ]]; then
        error_exit "Tailscaled socket not found after ${TAILSCALE_TIMEOUT} seconds"
    fi
    
    log "Tailscaled socket is ready at ${TAILSCALE_SOCK}"
}

# Function to connect to Tailscale
connect_tailscale() {
    log "Connecting to Tailscale..."
    
    local auth_key
    auth_key=$(get_config_value "TAILSCALE_AUTH_KEY")
    
    local hostname="${TAILSCALE_HOSTNAME:-docker-mcp-server}"
    local tags="${TAILSCALE_TAGS:-}"
    local extra_args="${TAILSCALE_EXTRA_ARGS:-}"
    
    # Build tailscale up command
    local cmd="tailscale up"
    cmd="${cmd} --authkey=${auth_key}"
    cmd="${cmd} --hostname=${hostname}"
    
    if [[ -n "${tags}" ]]; then
        cmd="${cmd} --tags=${tags}"
    fi
    
    if [[ -n "${extra_args}" ]]; then
        cmd="${cmd} ${extra_args}"
    fi
    
    # Set socket for tailscale command
    export TAILSCALED_SOCKET="${TAILSCALE_SOCK}"
    
    # Execute tailscale up
    if ! eval "${cmd}"; then
        error_exit "Failed to connect to Tailscale"
    fi
    
    log "Successfully connected to Tailscale"
}

# Function to get and log Tailscale IP
log_tailscale_ip() {
    log "Retrieving Tailscale IP address..."
    
    # Set socket for tailscale command
    export TAILSCALED_SOCKET="${TAILSCALE_SOCK}"
    
    local tailscale_ip
    tailscale_ip=$(tailscale ip -4 2>/dev/null || echo "")
    
    if [[ -z "${tailscale_ip}" ]]; then
        log "WARNING: Could not retrieve Tailscale IPv4 address"
    else
        log "========================================"
        log "TAILSCALE IP: ${tailscale_ip}"
        log "========================================"
    fi
}

# Function to wait for Tailscale to be ready
wait_for_tailscale() {
    log "Waiting for Tailscale to be ready..."
    
    local wait_time=0
    local max_wait=${TAILSCALE_TIMEOUT}
    
    # Set socket for tailscale command
    export TAILSCALED_SOCKET="${TAILSCALE_SOCK}"
    
    while [[ $wait_time -lt $max_wait ]]; do
        if tailscale status >/dev/null 2>&1; then
            log "Tailscale is ready"
            return 0
        fi
        
        sleep 2
        wait_time=$((wait_time + 2))
        log "Waiting for Tailscale... (${wait_time}/${max_wait}s)"
    done
    
    error_exit "Tailscale did not become ready within ${max_wait} seconds"
}

# Function to start Uvicorn
start_uvicorn() {
    log "Starting Uvicorn server..."
    log "Command: ${UVICORN_CMD}"
    
    # Start uvicorn in the foreground
    exec ${UVICORN_CMD}
}

# Main execution logic
main() {
    log "Docker Swarm MCP Server starting..."
    log "Tailscale enabled: ${TAILSCALE_ENABLED}"
    
    if [[ "${TAILSCALE_ENABLED}" == "true" ]]; then
        # Validate configuration
        validate_tailscale_config
        
        # Start Tailscaled
        start_tailscaled
        
        # Connect to Tailscale
        connect_tailscale
        
        # Wait for Tailscale to be ready
        wait_for_tailscale
        
        # Log IP address
        log_tailscale_ip
        
        log "Tailscale setup complete, starting application..."
    else
        log "Tailscale disabled, starting application directly..."
    fi
    
    # Start Uvicorn (this will replace the shell process)
    start_uvicorn
}

# Execute main function
main "$@"