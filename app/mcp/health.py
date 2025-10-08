from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def health_check(request: Request) -> dict[str, str | bool]:
    try:
        docker_client = request.app.state.docker_client
        docker_reachable = docker_client.ping()
    except Exception:
        docker_reachable = False
    
    return {
        "status": "healthy" if docker_reachable else "degraded",
        "docker_reachable": docker_reachable,
        "version": "0.1.0"
    }
