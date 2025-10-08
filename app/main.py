import json
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.docker_client import get_docker_client
from app.mcp.health import router as health_router
from app.mcp.tool_gating import FilterConfig, ToolGateController
from app.mcp.tool_registry import ToolRegistry, router as mcp_router
from app.routers.system import router as system_router
from app.routers.containers import router as containers_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    logger.info("Starting Docker MCP Server")
    
    try:
        docker_client = get_docker_client()
        logger.info("Docker client validated successfully")
    except RuntimeError as e:
        logger.error(f"Failed to initialize Docker client: {e}")
        sys.exit(1)
    
    tool_registry = ToolRegistry()
    
    filter_config_path = Path("filter-config.json")
    if filter_config_path.exists():
        with filter_config_path.open() as f:
            filter_config_data = json.load(f)
        filter_config = FilterConfig(**filter_config_data)
    else:
        logger.warning("filter-config.json not found, using defaults")
        filter_config = FilterConfig(
            task_type_allowlists={},
            max_tools=10,
            blocklist=[]
        )
    
    tool_gate_controller = ToolGateController(
        all_tools=tool_registry.get_all_tools(),
        config=filter_config
    )
    
    app.state.docker_client = docker_client
    app.state.tool_registry = tool_registry
    app.state.tool_gate_controller = tool_gate_controller
    
    logger.info("Application startup complete")
    
    yield
    
    logger.info("Shutting down Docker MCP Server")


app = FastAPI(
    title="Docker MCP Server",
    description="HTTP-based Model Context Protocol server for Docker operations",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health_router, prefix="/mcp", tags=["MCP"])
app.include_router(mcp_router, prefix="/mcp", tags=["MCP"])
app.include_router(system_router, prefix="/system", tags=["System"])
app.include_router(containers_router, tags=["Containers"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Docker MCP Server", "version": "0.1.0"}
