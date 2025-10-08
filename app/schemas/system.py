from pydantic import BaseModel


class SystemInfo(BaseModel):
    version: str
    os: str
    architecture: str
    docker_version: str


class PingResponse(BaseModel):
    status: str
    message: str
