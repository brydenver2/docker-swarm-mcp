from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VolumeCreateRequest(BaseModel):
    name: str = Field(..., description="Volume name")
    driver: Optional[str] = Field("local", description="Volume driver")
    options: Optional[dict[str, str]] = Field(None, description="Driver-specific options")
    labels: Optional[dict[str, str]] = Field(None, description="Volume metadata labels")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "my-volume",
                "driver": "local",
                "labels": {
                    "environment": "production",
                    "project": "web-app"
                }
            }
        }
    )


class VolumeResponse(BaseModel):
    name: str = Field(..., description="Volume name")
    driver: str = Field(..., description="Volume driver")
    mountpoint: str = Field(..., description="Host path where volume is mounted")
    created: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "my-volume",
                "driver": "local",
                "mountpoint": "/var/lib/docker/volumes/my-volume/_data",
                "created": "2025-10-07T12:34:56Z"
            }
        }
    )
