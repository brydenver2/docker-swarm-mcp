import json
import logging
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.docker_client import get_docker_client
from app.mcp.health import router as health_router
from app.mcp.tool_gating import FilterConfig, ToolGateController
from app.mcp.tool_registry import ToolRegistry, router as mcp_router
from app.mcp.fastapi_mcp_integration import router as mcp_jsonrpc_router
from app.routers.system import router as system_router
from app.routers.containers import router as containers_router
from app.routers.stacks import router as stacks_router
from app.routers.services import router as services_router
from app.routers.networks import router as networks_router
from app.routers.volumes import router as volumes_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    logger.info("Starting Docker MCP Server")
    
    # Validate authentication configuration
    if not settings.TOKEN_SCOPES and not settings.MCP_ACCESS_TOKEN:
        logger.error("Security requires either MCP_ACCESS_TOKEN or TOKEN_SCOPES to be configured")
        sys.exit(1)
    
    if not settings.TOKEN_SCOPES and not settings.MCP_ACCESS_TOKEN.strip():
        logger.error("MCP_ACCESS_TOKEN cannot be empty when TOKEN_SCOPES is not configured")
        sys.exit(1)
    
    try:
        docker_client = get_docker_client()
        logger.info("Docker client validated successfully")
    except RuntimeError as e:
        logger.error(f"Failed to initialize Docker client: {e}")
        sys.exit(1)
    
    tool_registry = ToolRegistry()
    all_tools = tool_registry.get_all_tools()
    
    filter_config_path = Path("filter-config.json")
    if filter_config_path.exists():
        try:
            with filter_config_path.open() as f:
                filter_config_data = json.load(f)
            filter_config = FilterConfig(**filter_config_data)
            
            invalid_blocklist = [
                tool_name for tool_name in filter_config.blocklist
                if tool_name not in all_tools
            ]
            if invalid_blocklist:
                logger.warning(
                    f"filter-config.json blocklist references non-existent tools: {invalid_blocklist}"
                )
            
            for task_type, tool_names in filter_config.task_type_allowlists.items():
                invalid_tools = [
                    tool_name for tool_name in tool_names
                    if tool_name not in all_tools
                ]
                if invalid_tools:
                    logger.warning(
                        f"filter-config.json task-type '{task_type}' references non-existent tools: {invalid_tools}"
                    )
            
            logger.info(f"Loaded filter config with {len(filter_config.task_type_allowlists)} task types")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in filter-config.json: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to load filter-config.json: {e}")
            sys.exit(1)
    else:
        logger.warning("filter-config.json not found, using defaults")
        filter_config = FilterConfig(
            task_type_allowlists={},
            max_tools=10,
            blocklist=[]
        )
    
    tool_gate_controller = ToolGateController(
        all_tools=all_tools,
        config=filter_config
    )

    # Initialize IntentClassifier
    from app.mcp.intent_classifier import KeywordIntentClassifier
    
    # Load keyword mappings from filter-config.json or use defaults
    keyword_mappings = filter_config_data.get("intent_keywords", None) if 'filter_config_data' in locals() else None
    intent_classifier = KeywordIntentClassifier(keyword_mappings=keyword_mappings)
    logger.info(f"Intent classifier initialized with {len(intent_classifier.get_keyword_mappings())} task types")

    # Initialize DynamicToolGatingMCP once at startup
    from app.mcp.fastapi_mcp_integration import DynamicToolGatingMCP
    mcp_server = DynamicToolGatingMCP(tool_registry, tool_gate_controller, intent_classifier)

    app.state.docker_client = docker_client
    app.state.tool_registry = tool_registry
    app.state.tool_gate_controller = tool_gate_controller
    app.state.mcp_server = mcp_server
    app.state.intent_classifier = intent_classifier
    
    if "*" in settings.ALLOWED_ORIGINS:
        logger.warning(
            "CORS configured with wildcard origin (*). "
            "This is insecure for production. "
            "Set ALLOWED_ORIGINS to specific domains."
        )
    else:
        logger.info(f"CORS configured with origins: {', '.join(settings.ALLOWED_ORIGINS)}")
    
    logger.info("Application startup complete")
    
    yield
    
    logger.info("Shutting down Docker MCP Server")


app = FastAPI(
    title="Docker MCP Server",
    description="HTTP-based Model Context Protocol server for Docker operations",
    version="0.2.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = time.time()
    
    response = await call_next(request)
    
    duration_ms = int((time.time() - start_time) * 1000)
    
    # Create log record with redacted headers
    log_record = logging.LogRecord(
        name=__name__,
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=f"{request.method} {request.url.path}",
        args=(),
        exc_info=None
    )
    log_record.request_id = request_id
    log_record.duration_ms = duration_ms
    log_record.status = response.status_code
    
    # Redact sensitive headers before logging
    from app.core.logging import redact_secrets
    headers_dict = dict(request.headers)
    redacted_headers = redact_secrets(headers_dict)
    log_record.headers = redacted_headers
    
    path = request.url.path
    if path.startswith("/containers"):
        log_record.tool = "container-ops"
    elif path.startswith("/stacks"):
        log_record.tool = "compose-ops"
    elif path.startswith("/services"):
        log_record.tool = "service-ops"
    elif path.startswith("/networks"):
        log_record.tool = "network-ops"
    elif path.startswith("/volumes"):
        log_record.tool = "volume-ops"
    elif path.startswith("/system"):
        log_record.tool = "system-ops"
    elif path.startswith("/mcp"):
        log_record.tool = "mcp-discovery"
    
    logger.handle(log_record)
    
    return response


register_exception_handlers(app)

app.include_router(health_router, prefix="/mcp", tags=["MCP"])
app.include_router(mcp_router, prefix="/mcp", tags=["MCP"])
app.include_router(mcp_jsonrpc_router, prefix="/mcp/v1", tags=["MCP JSON-RPC"])
app.include_router(system_router, prefix="/system", tags=["System"])
app.include_router(containers_router, tags=["Containers"])
app.include_router(stacks_router, prefix="/stacks", tags=["Stacks"])
app.include_router(services_router, tags=["Services"])
app.include_router(networks_router, tags=["Networks"])
app.include_router(volumes_router, tags=["Volumes"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Docker MCP Server", "version": "0.2.0"}
