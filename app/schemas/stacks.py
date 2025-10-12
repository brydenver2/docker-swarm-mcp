from pydantic import BaseModel, Field


class ComposeDeployRequest(BaseModel):
    project_name: str = Field(..., pattern=r"^[a-z0-9-]+$", description="Stack identifier")
    compose_yaml: str = Field(..., description="Compose v3+ YAML content")
    force_recreate: bool = Field(default=False, description="Recreate existing services")


class ComposeDeployResponse(BaseModel):
    project_name: str
    services: list[str]
    mode: str
    created: str


class StackSummary(BaseModel):
    project_name: str
    services: list[str]
    service_count: int
