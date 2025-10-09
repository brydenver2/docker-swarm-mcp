import os
from typing import Literal


class Settings:
    # Docker configuration
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    DOCKER_TLS_VERIFY: bool = os.getenv("DOCKER_TLS_VERIFY", "0") == "1"
    DOCKER_CERT_PATH: str = os.getenv("DOCKER_CERT_PATH", "")

    # MCP configuration
    MCP_ACCESS_TOKEN: str = os.getenv("MCP_ACCESS_TOKEN", "")
    MCP_TRANSPORT: Literal["http", "sse"] = os.getenv("MCP_TRANSPORT", "http")  # type: ignore

    # Authentication and authorization
    TOKEN_SCOPES: str = os.getenv("TOKEN_SCOPES", "")  # JSON mapping: {"token": ["scope1", "scope2"]}

    # Logging and CORS
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    DEBUG: bool = LOG_LEVEL == "DEBUG"


settings = Settings()
