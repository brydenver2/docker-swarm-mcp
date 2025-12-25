import json
import logging
import subprocess
import sys
import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.constants import APP_NAME, APP_VERSION
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.docker_client import get_docker_client
from app.mcp.fastapi_mcp_integration import router as mcp_jsonrpc_router
from app.mcp.health import router as health_router
from app.mcp.tool_gating import FilterConfig, ToolGateController
from app.mcp.tool_registry import ToolRegistry
from app.routers.containers import router as containers_router
from app.routers.networks import router as networks_router
from app.routers.services import router as services_router
from app.routers.stacks import router as stacks_router
from app.routers.system import router as system_router
from app.routers.volumes import router as volumes_router

logger = logging.getLogger(__name__)


def log_tailscale_status() -> None:
    """
    Log the current Tailscale integration and connection status.
    
    If TAILSCALE_ENABLED is false, logs that Tailscale is disabled. If enabled and the tailscale CLI is present, logs connection state; when connected, logs the first Tailscale IP (if any), the self hostname (if present), and any non-default configuration details (hostname, tags, state_dir). Emits warnings on missing CLI, failed status checks, JSON parse errors, timeouts, or other errors.
    """
    if not settings.TAILSCALE_ENABLED:
        logger.info("Tailscale integration: DISABLED")
        return

    logger.info("Tailscale integration: ENABLED")

    # Check if Tailscale is installed and running
    try:
        # Check if Tailscale is installed
        result = subprocess.run(
            ["which", "tailscale"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            logger.warning("Tailscale is enabled but not installed or not in PATH")
            return

        # Get Tailscale status
        result = subprocess.run(
            ["tailscale", "status", "--json"],
            capture_output=True,
            text=True,
            timeout=settings.TAILSCALE_TIMEOUT
        )

        if result.returncode != 0:
            logger.warning(f"Tailscale status check failed: {result.stderr.strip()}")
            return

        # Parse the JSON output
        try:
            status_data = json.loads(result.stdout)

            # Extract useful information
            if status_data.get("BackendState") == "Running":
                logger.info("Tailscale status: CONNECTED")

                # Get Tailscale IP if available
                if "TailscaleIPs" in status_data and status_data["TailscaleIPs"]:
                    tailscale_ip = status_data["TailscaleIPs"][0]
                    logger.info(f"Tailscale IP address: {tailscale_ip}")
                else:
                    logger.info("Tailscale IP address: Not available")

                # Log hostname if set
                if "Self" in status_data and "HostName" in status_data["Self"]:
                    hostname = status_data["Self"]["HostName"]
                    logger.info(f"Tailscale hostname: {hostname}")

                # Log additional configuration
                config_details = []

                if settings.TAILSCALE_HOSTNAME:
                    config_details.append(f"hostname={settings.TAILSCALE_HOSTNAME}")

                if settings.TAILSCALE_TAGS:
                    config_details.append(f"tags={settings.TAILSCALE_TAGS}")

                if settings.TAILSCALE_STATE_DIR != "/var/lib/tailscale":
                    config_details.append(f"state_dir={settings.TAILSCALE_STATE_DIR}")

                if config_details:
                    logger.info(f"Tailscale configuration: {', '.join(config_details)}")

            else:
                backend_state = status_data.get("BackendState", "Unknown")
                logger.warning(f"Tailscale status: NOT CONNECTED (BackendState: {backend_state})")

        except json.JSONDecodeError:
            logger.warning("Failed to parse Tailscale status JSON output")

    except subprocess.TimeoutExpired:
        logger.warning(f"Tailscale status check timed out after {settings.TAILSCALE_TIMEOUT} seconds")
    except FileNotFoundError:
        logger.warning("Tailscale command not found")
    except Exception as e:
        logger.warning(f"Error checking Tailscale status: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the application's startup and shutdown lifecycle, initializing logging, configuration, and runtime services.
    
    On startup this initializes logging, validates authentication settings, creates and validates the Docker client, builds the tool registry and tool-gating configuration (loading filter-config.json when present), initializes the intent classifier and MCP server, and stores created objects on app.state; on shutdown it logs server termination.
    
    Parameters:
        app (FastAPI): The FastAPI application whose state will be populated with initialized services (docker_client, tool_registry, tool_gate_controller, mcp_server, intent_classifier).
    
    Raises:
        ValueError: If neither TOKEN_SCOPES nor a non-empty MCP_ACCESS_TOKEN is configured.
    """
    setup_logging()
    logger.info("Starting Docker Swarm MCP Server")

    # Log Tailscale status
    log_tailscale_status()

    # Log authentication configuration status (without exposing tokens)
    if settings.TOKEN_SCOPES:
        logger.info("Authentication: Multi-token mode enabled (TOKEN_SCOPES configured)")
    elif settings.MCP_ACCESS_TOKEN:
        token_length = len(settings.MCP_ACCESS_TOKEN)
        logger.info(f"Authentication: Single-token mode enabled (MCP_ACCESS_TOKEN: {token_length} chars)")
    else:
        # This should never happen due to Settings.validate(), but adding for safety
        logger.error("CRITICAL: No authentication configured - server will fail to start")

    try:
        docker_client = get_docker_client()
        logger.info("Docker client validated successfully")
    except RuntimeError as e:
        logger.error(f"Failed to initialize Docker client: {e}")
        sys.exit(1)

    tool_registry = ToolRegistry()
    all_tools = tool_registry.get_all_tools()

    filter_config_path = Path("filter-config.json")
    filter_config_data = None

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
    keyword_mappings = filter_config_data.get("intent_keywords", None) if filter_config_data else None
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

    logger.info("Shutting down Docker Swarm MCP Server")


app = FastAPI(
    title=APP_NAME,
    description="HTTP-based Model Context Protocol server for Docker operations",
    version=APP_VERSION,
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
    """
    Middleware that logs incoming HTTP requests, attaches a unique request_id to the request state, and forwards the request to the next handler.
    
    The function records request start time, warns if a legacy `accessToken` query parameter is present, measures request duration, redacts sensitive headers for logging, categorizes the request by logical tool based on path, and emits a structured log record containing method, path, request_id, duration_ms, status, headers, and inferred tool. The generated `request_id` is stored on `request.state.request_id`.
    
    Parameters:
        request (Request): The incoming FastAPI request object.
        call_next (Callable): The next request handler/callable to invoke to obtain the response.
    
    Returns:
        Response: The HTTP response returned by the next handler.
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    # Emit warning if legacy accessToken query parameter is detected
    if "accesstoken" in {k.lower() for k in request.query_params.keys()}:
        logger.warning(
            "Query parameter authentication is unsupported; remove accessToken from URL",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method
            }
        )

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
    if path.startswith("/api/containers") or path.startswith("/containers"):
        log_record.tool = "container-ops"
    elif path.startswith("/api/stacks") or path.startswith("/stacks"):
        log_record.tool = "compose-ops"
    elif path.startswith("/api/services") or path.startswith("/services"):
        log_record.tool = "service-ops"
    elif path.startswith("/api/networks") or path.startswith("/networks"):
        log_record.tool = "network-ops"
    elif path.startswith("/api/volumes") or path.startswith("/volumes"):
        log_record.tool = "volume-ops"
    elif path.startswith("/api/system") or path.startswith("/system"):
        log_record.tool = "system-ops"
    elif path.startswith("/mcp"):
        log_record.tool = "mcp-discovery"

    logger.handle(log_record)

    return response


register_exception_handlers(app)

app.include_router(health_router, prefix="/mcp", tags=["MCP"])
app.include_router(mcp_jsonrpc_router, prefix="/mcp", tags=["MCP JSON-RPC"])

if settings.ENABLE_REST_API:
    logger.info("REST API enabled: mounting routers under /api/*")
    app.include_router(system_router, prefix="/api/system", tags=["System"])
    app.include_router(containers_router, prefix="/api", tags=["Containers"])
    app.include_router(stacks_router, prefix="/api/stacks", tags=["Stacks"])
    app.include_router(services_router, prefix="/api", tags=["Services"])
    app.include_router(networks_router, prefix="/api", tags=["Networks"])
    app.include_router(volumes_router, prefix="/api", tags=["Volumes"])
else:
    logger.info("REST API disabled; set ENABLE_REST_API=true to expose /api endpoints")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": APP_NAME, "version": APP_VERSION}