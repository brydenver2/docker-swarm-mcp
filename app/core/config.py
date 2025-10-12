import os
import sys
from typing import Literal


class Settings:
    # Docker configuration
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    DOCKER_TLS_VERIFY: bool = os.getenv("DOCKER_TLS_VERIFY", "0") == "1"
    DOCKER_CERT_PATH: str = os.getenv("DOCKER_CERT_PATH", "")

    # MCP configuration
    MCP_ACCESS_TOKEN: str = os.getenv("MCP_ACCESS_TOKEN", "")
    MCP_TRANSPORT: Literal["http", "sse"] = os.getenv("MCP_TRANSPORT", "http")  # type: ignore
    MCP_PROTOCOL_VERSION: str = os.getenv("MCP_PROTOCOL_VERSION", "2024-11-05")
    MCP_TOOL_TIMEOUT: int = int(os.getenv("MCP_TOOL_TIMEOUT", "30"))  # seconds
    ENFORCE_OUTPUT_SCHEMA: bool = os.getenv("ENFORCE_OUTPUT_SCHEMA", "false").lower() == "true"
    STRICT_CONTEXT_LIMIT: bool = os.getenv("STRICT_CONTEXT_LIMIT", "false").lower() == "true"
    
    # Per-tool timeout configurations (seconds)
    MCP_TIMEOUT_READ_OPS: int = int(os.getenv("MCP_TIMEOUT_READ_OPS", "15"))  # list, get, info operations
    MCP_TIMEOUT_WRITE_OPS: int = int(os.getenv("MCP_TIMEOUT_WRITE_OPS", "30"))  # create, start, stop operations
    MCP_TIMEOUT_DELETE_OPS: int = int(os.getenv("MCP_TIMEOUT_DELETE_OPS", "45"))  # remove, delete operations

    # Retry configurations
    RETRY_READ_MAX_ATTEMPTS: int = int(os.getenv("RETRY_READ_MAX_ATTEMPTS", "3"))
    RETRY_READ_BASE_DELAY: float = float(os.getenv("RETRY_READ_BASE_DELAY", "0.1"))
    RETRY_READ_MAX_DELAY: float = float(os.getenv("RETRY_READ_MAX_DELAY", "1.0"))
    RETRY_READ_BACKOFF_FACTOR: float = float(os.getenv("RETRY_READ_BACKOFF_FACTOR", "2.0"))
    RETRY_READ_JITTER: bool = os.getenv("RETRY_READ_JITTER", "true").lower() == "true"
    
    RETRY_WRITE_MAX_ATTEMPTS: int = int(os.getenv("RETRY_WRITE_MAX_ATTEMPTS", "2"))
    RETRY_WRITE_BASE_DELAY: float = float(os.getenv("RETRY_WRITE_BASE_DELAY", "0.2"))
    RETRY_WRITE_MAX_DELAY: float = float(os.getenv("RETRY_WRITE_MAX_DELAY", "1.5"))
    RETRY_WRITE_BACKOFF_FACTOR: float = float(os.getenv("RETRY_WRITE_BACKOFF_FACTOR", "2.0"))
    RETRY_WRITE_JITTER: bool = os.getenv("RETRY_WRITE_JITTER", "true").lower() == "true"

    # Authentication and authorization
    TOKEN_SCOPES: str = os.getenv("TOKEN_SCOPES", "")  # JSON mapping: {"token": ["scope1", "scope2"]}

    # Intent classification configuration
    INTENT_CLASSIFICATION_ENABLED: bool = os.getenv("INTENT_CLASSIFICATION_ENABLED", "true").lower() == "true"
    INTENT_FALLBACK_TO_ALL: bool = os.getenv("INTENT_FALLBACK_TO_ALL", "true").lower() == "true"
    INTENT_MIN_CONFIDENCE: float = float(os.getenv("INTENT_MIN_CONFIDENCE", "0.0"))
    INTENT_PRECEDENCE: Literal["intent", "explicit"] = os.getenv("INTENT_PRECEDENCE", "intent")  # type: ignore

    # Logging and CORS
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Tailscale configuration
    TAILSCALE_ENABLED: bool = os.getenv("TAILSCALE_ENABLED", "false").lower() == "true"
    TAILSCALE_AUTH_KEY: str = os.getenv("TAILSCALE_AUTH_KEY", "")
    TAILSCALE_AUTH_KEY_FILE: str = os.getenv("TAILSCALE_AUTH_KEY_FILE", "")
    TAILSCALE_HOSTNAME: str = os.getenv("TAILSCALE_HOSTNAME", "")
    TAILSCALE_TAGS: str = os.getenv("TAILSCALE_TAGS", "")
    TAILSCALE_EXTRA_ARGS: str = os.getenv("TAILSCALE_EXTRA_ARGS", "")
    TAILSCALE_STATE_DIR: str = os.getenv("TAILSCALE_STATE_DIR", "/var/lib/tailscale")
    TAILSCALE_TIMEOUT: int = int(os.getenv("TAILSCALE_TIMEOUT", "30"))

    DEBUG: bool = LOG_LEVEL == "DEBUG"

    def validate(self):
        """Validate security-critical settings"""
        # Fail fast if both MCP_ACCESS_TOKEN and TOKEN_SCOPES are unset
        if not self.MCP_ACCESS_TOKEN and not self.TOKEN_SCOPES:
            raise ValueError(
                "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES to be set. "
                "Set MCP_ACCESS_TOKEN for single-token auth or TOKEN_SCOPES for multi-token auth"
            )

settings = Settings()
settings.validate()


settings = Settings()
settings.__post_init__()
