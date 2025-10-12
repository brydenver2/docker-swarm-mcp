from fastapi import APIRouter, Depends, status

from app.core.auth import verify_token
from app.docker_client import DockerClient, get_docker_client
from app.schemas.stacks import ComposeDeployRequest, ComposeDeployResponse, StackSummary

router = APIRouter()


@router.post("/deploy", response_model=ComposeDeployResponse, dependencies=[Depends(verify_token)])
def deploy_stack(request: ComposeDeployRequest, client: DockerClient = Depends(get_docker_client)):
    result = client.deploy_compose(
        project_name=request.project_name,
        compose_yaml=request.compose_yaml,
        force_recreate=request.force_recreate
    )
    return result


@router.get("", response_model=list[StackSummary], dependencies=[Depends(verify_token)])
def list_stacks(client: DockerClient = Depends(get_docker_client)):
    return client.list_stacks()


@router.delete("/{project_name}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
def remove_stack(project_name: str, client: DockerClient = Depends(get_docker_client)):
    client.remove_compose(project_name)
