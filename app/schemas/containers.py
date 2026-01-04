from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ContainerCreateRequest(BaseModel):
    image: str = Field(..., description="Docker image name")
    name: Optional[str] = Field(None, description="Container name (auto-generated if omitted)")
    environment: Optional[dict[str, str]] = Field(None, description="Environment variables")
    ports: Optional[dict[str, int]] = Field(None, description="Port mappings (container_port -> host_port)")
    volumes: Optional[dict[str, dict[str, str]]] = Field(None, description="Volume mounts")
    restart_policy: Optional[str] = Field("no", description="Restart policy")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "image": "nginx:alpine",
                "name": "web-server",
                "environment": {"ENV": "production", "PORT": "8080"},
                "ports": {"80/tcp": 8080},
                "restart_policy": "always"
            }
        }
    )


class ContainerResponse(BaseModel):
    id: str = Field(..., description="Container ID (short form)")
    name: str = Field(..., description="Container name")
    status: str = Field(..., description="Container status")
    image: str = Field(..., description="Image name")
    created: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "e90e34656806",
                "name": "web-server",
                "status": "running",
                "image": "nginx:alpine",
                "created": "2025-10-07T12:34:56Z"
            }
        }
    )


class PortMapping(BaseModel):
    private_port: int
    public_port: Optional[int] = None
    type: str = "tcp"


class ContainerSummary(ContainerResponse):
    ports: Optional[list[PortMapping]] = Field(None, description="Port mappings")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "e90e34656806",
                "name": "web-server",
                "status": "running",
                "image": "nginx:alpine",
                "created": "2025-10-07T12:34:56Z",
                "ports": [
                    {"private_port": 80, "public_port": 8080, "type": "tcp"}
                ]
            }
        }
    )
