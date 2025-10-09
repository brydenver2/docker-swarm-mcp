from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class NetworkCreateRequest(BaseModel):
    name: str = Field(..., description="Network name")
    driver: Optional[str] = Field("bridge", description="Network driver (bridge, overlay, macvlan, host, none)")
    ipam: Optional[Dict[str, Any]] = Field(None, description="IP address management configuration")
    options: Optional[Dict[str, str]] = Field(None, description="Driver-specific options")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "my-network",
                "driver": "bridge",
                "ipam": {
                    "Config": [
                        {
                            "Subnet": "172.20.0.0/16",
                            "Gateway": "172.20.0.1"
                        }
                    ]
                }
            }
        }


class NetworkResponse(BaseModel):
    id: str = Field(..., description="Network ID (short form)")
    name: str = Field(..., description="Network name")
    driver: str = Field(..., description="Network driver")
    scope: str = Field(..., description="Network scope (local, swarm, global)")
    created: datetime = Field(..., description="Creation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4e5f6",
                "name": "my-network",
                "driver": "bridge",
                "scope": "local",
                "created": "2025-10-07T12:34:56Z"
            }
        }
