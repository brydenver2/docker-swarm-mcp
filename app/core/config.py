import os
from typing import Literal


class Settings:
    DOCKER_HOST: str = os.getenv("DOCKER_HOST", "unix:///var/run/docker.sock")
    DOCKER_TLS_VERIFY: bool = os.getenv("DOCKER_TLS_VERIFY", "0") == "1"
    DOCKER_CERT_PATH: str = os.getenv("DOCKER_CERT_PATH", "")
    
    MCP_ACCESS_TOKEN: str = os.getenv("MCP_ACCESS_TOKEN", "")
    MCP_TRANSPORT: Literal["http", "sse"] = os.getenv("MCP_TRANSPORT", "http")  # type: ignore
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ALLOWED_ORIGINS: list[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    DEBUG: bool = LOG_LEVEL == "DEBUG"


settings = Settings()
