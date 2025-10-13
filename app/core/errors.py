from typing import Any

from docker.errors import APIError, DockerException, NotFound
from fastapi import Request, status
from fastapi.responses import JSONResponse


async def docker_not_found_handler(request: Request, exc: NotFound) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Resource not found"}
    )


async def docker_api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    status_code = exc.response.status_code if hasattr(exc, 'response') else 424

    if status_code == 400:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Invalid request: {exc.explanation}"}
        )
    elif status_code == 409:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": f"Conflict: {exc.explanation}"}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"detail": f"Docker API error: {exc.explanation}"}
        )


async def docker_exception_handler(request: Request, exc: DockerException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Docker error"}
    )


def register_exception_handlers(app: Any) -> None:
    app.add_exception_handler(NotFound, docker_not_found_handler)
    app.add_exception_handler(APIError, docker_api_error_handler)
    app.add_exception_handler(DockerException, docker_exception_handler)
