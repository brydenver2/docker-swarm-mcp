FROM alpine:3.20

USER root

WORKDIR /app

# Install Python 3.13, pip, and other dependencies
RUN apk update && \
    apk add --no-cache bash python3 py3-pip curl tailscale iptables && \
    python3 --version

# Install Poetry
RUN pip install --break-system-packages poetry==1.7.1

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

COPY app/ ./app/
COPY tools.yaml filter-config.json ./
COPY scripts/entrypoint.sh ./scripts/

# Create non-root user with docker group access
# Use existing docker group (GID 999 already exists in Alpine 3.20) or create with different GID
RUN (addgroup -g 998 dockergroup || true) && \
    adduser -D -u 1000 mcp && \
    addgroup mcp dockergroup && \
    chown -R mcp:mcp /app

# Create Tailscale state directory and set permissions
RUN mkdir -p /var/lib/tailscale && \
    chown -R mcp:mcp /var/lib/tailscale && \
    chmod +x /app/scripts/entrypoint.sh

# Switch to non-root user
USER mcp

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    MCP_TRANSPORT=http

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/mcp/health || exit 1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
