from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class IPAMConfig(BaseModel):
    Subnet: str
    IPRange: Optional[str] = None
    Gateway: Optional[str] = None


class IPAM(BaseModel):
    Driver: Optional[str] = Field(default="default")
    Config: Optional[list[IPAMConfig]] = None
