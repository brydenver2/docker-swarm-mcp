import os
from typing import Literal, cast


def get_env_int(name: str, default: int) -> int:
    """Fetch an int environment variable with clear error reporting."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be an integer, got {raw!r}") from exc


def get_env_float(name: str, default: float) -> float:
    """Fetch a float environment variable with clear error reporting."""
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"Environment variable {name} must be a float, got {raw!r}") from exc


def read_token_from_file_or_env(env_var: str, file_env_var: str) -> str:
    """
    Read a token from a file path specified in file_env_var, or fall back to env_var.

    Args:
        env_var: Name of environment variable containing the token directly
        file_env_var: Name of environment variable containing path to file with token

    Returns:
        The token string, or empty string if neither is set

    Raises:
        ValueError: If file path is specified but file cannot be read
    """
    # First check if file path is specified
    file_path = os.getenv(file_env_var, "")
    if file_path:
        try:
            with open(file_path, encoding="utf-8") as f:
                token = f.read().strip()
                if not token:
                    raise ValueError(f"Token file {file_path} is empty")
                return token
        except FileNotFoundError as exc:
            raise ValueError(f"Token file not found: {file_path}") from exc
        except PermissionError as exc:
            raise ValueError(f"Permission denied reading token file: {file_path}") from exc
        except Exception as exc:
            raise ValueError(f"Error reading token file {file_path}: {exc}") from exc

    # Fall back to environment variable
    return os.getenv(env_var, "").strip()


class Settings:
    # Docker configuration
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    DOCKER_TLS_VERIFY: bool = os.getenv("DOCKER_TLS_VERIFY", "0") == "1"
    DOCKER_CERT_PATH: str = os.getenv("DOCKER_CERT_PATH", "")

    # MCP configuration
    MCP_ACCESS_TOKEN: str = read_token_from_file_or_env("MCP_ACCESS_TOKEN", "MCP_ACCESS_TOKEN_FILE")
    TOKEN_SCOPES: str = os.getenv("TOKEN_SCOPES", "")
    MCP_TRANSPORT: Literal["http", "sse"] = cast(
        Literal["http", "sse"], os.getenv("MCP_TRANSPORT", "http")
    )
    MCP_PROTOCOL_VERSION: str = os.getenv("MCP_PROTOCOL_VERSION", "2024-11-05")
    MCP_TOOL_TIMEOUT: int = get_env_int("MCP_TOOL_TIMEOUT", 30)  # seconds
    ENFORCE_OUTPUT_SCHEMA: bool = os.getenv("ENFORCE_OUTPUT_SCHEMA", "false").lower() == "true"
    STRICT_CONTEXT_LIMIT: bool = os.getenv("STRICT_CONTEXT_LIMIT", "false").lower() == "true"
    ENABLE_REST_API: bool = os.getenv("ENABLE_REST_API", "false").lower() == "true"

    # Per-tool timeout configurations (seconds)
    MCP_TIMEOUT_READ_OPS: int = get_env_int("MCP_TIMEOUT_READ_OPS", 15)
    MCP_TIMEOUT_WRITE_OPS: int = get_env_int("MCP_TIMEOUT_WRITE_OPS", 30)
    MCP_TIMEOUT_DELETE_OPS: int = get_env_int("MCP_TIMEOUT_DELETE_OPS", 45)

    # Retry configurations
    RETRY_READ_MAX_ATTEMPTS: int = get_env_int("RETRY_READ_MAX_ATTEMPTS", 3)
    RETRY_READ_BASE_DELAY: float = get_env_float("RETRY_READ_BASE_DELAY", 0.1)
    RETRY_READ_MAX_DELAY: float = get_env_float("RETRY_READ_MAX_DELAY", 1.0)
    RETRY_READ_BACKOFF_FACTOR: float = get_env_float("RETRY_READ_BACKOFF_FACTOR", 2.0)
    RETRY_READ_JITTER: bool = os.getenv("RETRY_READ_JITTER", "true").lower() == "true"

    RETRY_WRITE_MAX_ATTEMPTS: int = get_env_int("RETRY_WRITE_MAX_ATTEMPTS", 2)
    RETRY_WRITE_BASE_DELAY: float = get_env_float("RETRY_WRITE_BASE_DELAY", 0.2)
    RETRY_WRITE_MAX_DELAY: float = get_env_float("RETRY_WRITE_MAX_DELAY", 1.5)
    RETRY_WRITE_BACKOFF_FACTOR: float = get_env_float("RETRY_WRITE_BACKOFF_FACTOR", 2.0)
    RETRY_WRITE_JITTER: bool = os.getenv("RETRY_WRITE_JITTER", "true").lower() == "true"

    # Intent classification configuration
    INTENT_CLASSIFICATION_ENABLED: bool = (
        os.getenv("INTENT_CLASSIFICATION_ENABLED", "true").lower() == "true"
    )
    INTENT_FALLBACK_TO_ALL: bool = (
        os.getenv("INTENT_FALLBACK_TO_ALL", "true").lower() == "true"
    )
    INTENT_MIN_CONFIDENCE: float = get_env_float("INTENT_MIN_CONFIDENCE", 0.0)
    INTENT_PRECEDENCE: Literal["intent", "explicit"] = cast(
        Literal["intent", "explicit"], os.getenv("INTENT_PRECEDENCE", "intent")
    )

    # Security and debugging settings
    EXPOSE_ENDPOINTS_IN_HEALTHZ: bool = (
        os.getenv("EXPOSE_ENDPOINTS_IN_HEALTHZ", "false").lower() == "true"
    )

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
    TAILSCALE_TIMEOUT: int = get_env_int("TAILSCALE_TIMEOUT", 30)

    DEBUG: bool = LOG_LEVEL == "DEBUG"

    def validate(self) -> None:
        """
        Validate runtime-dependent configuration values and normalize enums.

        Checks performed:
        - Requires either `MCP_ACCESS_TOKEN` or `TOKEN_SCOPES` to be set.
        - If `TOKEN_SCOPES` is set, it must be valid JSON and parse to a dict.
        - Ensures `MCP_TRANSPORT` is one of "http" or "sse" and casts it to that Literal.
        - Ensures `INTENT_PRECEDENCE` is one of "intent" or "explicit" and casts it to that Literal.

        Raises:
            ValueError: If neither `MCP_ACCESS_TOKEN` nor `TOKEN_SCOPES` is set; if `TOKEN_SCOPES`
                contains invalid JSON or parses to a non-dict; if `MCP_TRANSPORT` or
                `INTENT_PRECEDENCE` contain invalid values.
        """
        # Validate authentication configuration
        has_token = bool(self.MCP_ACCESS_TOKEN and self.MCP_ACCESS_TOKEN.strip())
        has_token_scopes = bool(self.TOKEN_SCOPES and self.TOKEN_SCOPES.strip())
        
        if not has_token and not has_token_scopes:
            raise ValueError(
                "Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES to be configured.\n"
                "HINT: Create a .env file with MCP_ACCESS_TOKEN=your-secure-token\n"
                "      or set the environment variable before starting the server.\n"
                "Generate a secure token with: openssl rand -hex 32"
            )

        if self.TOKEN_SCOPES:
            import json

            try:
                scopes_dict = json.loads(self.TOKEN_SCOPES)
            except json.JSONDecodeError as exc:
                raise ValueError(f"TOKEN_SCOPES contains invalid JSON: {exc}") from None
            if not isinstance(scopes_dict, dict):
                raise ValueError("TOKEN_SCOPES must be a JSON object/dict")

        allowed_transports: tuple[str, ...] = ("http", "sse")
        if self.MCP_TRANSPORT not in allowed_transports:
            raise ValueError(
                f"MCP_TRANSPORT must be one of {allowed_transports}, got {self.MCP_TRANSPORT!r}"
            )
        self.MCP_TRANSPORT = cast(Literal["http", "sse"], self.MCP_TRANSPORT)

        allowed_precedence: tuple[str, ...] = ("intent", "explicit")
        if self.INTENT_PRECEDENCE not in allowed_precedence:
            raise ValueError(
                f"INTENT_PRECEDENCE must be one of {allowed_precedence}, "
                f"got {self.INTENT_PRECEDENCE!r}"
            )
        self.INTENT_PRECEDENCE = cast(Literal["intent", "explicit"], self.INTENT_PRECEDENCE)


# Maintain a singleton Settings instance across reloads so references stay live.
_settings_instance: Settings | None = globals().get("_settings_instance")  # type: ignore[assignment]

if _settings_instance is None:
    new_settings = Settings()
    new_settings.validate()
    _settings_instance = new_settings
else:
    # Refresh existing instance in place so other modules retain the same object reference.
    refreshed_settings = Settings()
    refreshed_settings.validate()
    for attr in dir(refreshed_settings):
        if attr.isupper():
            setattr(_settings_instance, attr, getattr(refreshed_settings, attr))

settings = _settings_instance
globals()["_settings_instance"] = _settings_instance
