FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Tailscale
RUN curl -fsSL https://tailscale.com/install.sh | sh

RUN pip install poetry==1.7.1

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

COPY app/ ./app/
COPY tools.yaml filter-config.json ./
COPY scripts/entrypoint.sh ./scripts/

# Create Tailscale state directory and set permissions
RUN mkdir -p /var/lib/tailscale && \
    chmod +x /app/scripts/entrypoint.sh

# Note: Container runs as root (user: "0:0" in docker-compose.yaml) to access Docker socket
# This is required for Docker API access and is secured via MCP_ACCESS_TOKEN authentication

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    MCP_TRANSPORT=http

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/mcp/health || exit 1

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
