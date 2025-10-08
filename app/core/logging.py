import json
import logging
import sys
from datetime import datetime
from typing import Any

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "tool"):
            log_data["tool"] = record.tool
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "status"):
            log_data["status"] = record.status
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        log_data = redact_secrets(log_data)
        
        return json.dumps(log_data)


def redact_secrets(data: dict[str, Any]) -> dict[str, Any]:
    sensitive_keys = {"token", "password", "secret", "api_key", "authorization"}
    
    redacted = {}
    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            redacted[key] = "***REDACTED***"
        elif isinstance(value, dict):
            redacted[key] = redact_secrets(value)
        elif isinstance(value, str) and len(value) > 100:
            if "BEGIN" in value or "-----" in value or "yaml" in key.lower():
                redacted[key] = f"{value[:50]}...***REDACTED***"
            else:
                redacted[key] = value
        else:
            redacted[key] = value
    
    return redacted


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    
    for log_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logging.getLogger(log_name).handlers = []
        logging.getLogger(log_name).propagate = True
