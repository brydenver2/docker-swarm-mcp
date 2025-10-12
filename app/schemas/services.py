from pydantic import BaseModel, Field
from typing import Optional


class ServiceScaleRequest(BaseModel):
    replicas: int = Field(..., ge=0, description="Desired replica count (0 = scale down to zero)")


class ServiceResponse(BaseModel):
    id: str
    name: str
    replicas: int
    image: str
    created: str
    mode: Optional[str] = "replicated"
