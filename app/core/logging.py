import json
import logging
import sys
from datetime import datetime
from typing import Any

from app.core.config import settings


class SensitiveDataFilter(logging.Filter):
    """Filter to redact sensitive headers and tokens from log records"""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Redacts sensitive headers, cookies, and token-like values on a LogRecord before it is emitted.
        
        This method removes common authorization and access-token headers from record.headers, replaces record.cookies with a redacted placeholder, and replaces string attributes that contain token-like or key-like values (including Bearer tokens, JWT-like strings, and long strings whose attribute names include "token" or "key") with a redacted placeholder. The record is modified in place.
        
        Parameters:
            record (logging.LogRecord): The log record to redact.
        
        Returns:
            bool: `True` to allow the (redacted) record to be processed/handled by the logging system.
        """
        import re

        # Redact Authorization header and tokens from extra data
        if hasattr(record, "headers"):
            headers = record.headers
            if isinstance(headers, dict):
                # Drop Authorization header entirely
                headers.pop("authorization", None)
                headers.pop("Authorization", None)
                # Drop custom access token header variants
                headers.pop("X-Access-Token", None)
                headers.pop("x-access-token", None)
                record.headers = headers

        if hasattr(record, "cookies"):
            # Redact all cookies
            record.cookies = "***REDACTED***"

        # Patterns to detect tokens
        bearer_pattern = re.compile(r'^Bearer\s+\S+', re.IGNORECASE)
        jwt_pattern = re.compile(r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$')

        # Redact any tokens in extra data
        for attr in dir(record):
            if not attr.startswith("_"):
                value = getattr(record, attr, None)
                if isinstance(value, str):
                    # Check for Bearer tokens
                    if bearer_pattern.match(value):
                        setattr(record, attr, "***REDACTED***")
                        continue

                    # Check for JWT tokens
                    if len(value) > 20 and jwt_pattern.match(value):
                        setattr(record, attr, "***REDACTED***")
                        continue

                    # Check if attribute name suggests sensitive data
                    if len(value) > 20:
                        if "token" in attr.lower() or "key" in attr.lower():
                            setattr(record, attr, "***REDACTED***")

        return True


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
    """
    Recursively redact sensitive values in a mapping intended for logging.
    
    Processes the provided mapping and returns a copy where keys that indicate secrets (for example, tokens, passwords, API keys, authorization headers, and similar) are replaced with "***REDACTED***". Special cases:
    - "query_params" dictionaries: any parameter named "accesstoken" or "access_token" is redacted while other params are preserved.
    - Nested dictionaries and lists of dictionaries are processed recursively.
    - Long string values (>100 chars) containing certificate/PEM markers ("BEGIN", "-----") or when the key contains "yaml" are truncated to the first 50 characters and appended with "...***REDACTED***"; other long strings are preserved.
    
    Parameters:
        data (dict[str, Any]): The mapping to inspect and redact for sensitive information.
    
    Returns:
        dict[str, Any]: A redacted copy of the input mapping with sensitive values replaced or truncated as described.
    """
    sensitive_keys = {
        "token", "password", "secret", "api_key", "authorization",
        "bearer", "credentials", "auth", "access_token", "refresh_token",
        "accesstoken",  # Handle camelCase query parameter (legacy)
        "x-access-token"  # Ensure custom header is always redacted
    }

    redacted = {}
    for key, value in data.items():
        # Redact if key contains sensitive terms
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            redacted[key] = "***REDACTED***"
        # Special handling for query parameters with accessToken
        elif key == "query_params" and isinstance(value, dict):
            redacted_params = {}
            for param_key, param_value in value.items():
                if param_key.lower() in ["accesstoken", "access_token"]:
                    redacted_params[param_key] = "***REDACTED***"
                else:
                    redacted_params[param_key] = param_value
            redacted[key] = redacted_params
        # Recursively redact nested dicts
        elif isinstance(value, dict):
            redacted[key] = redact_secrets(value)
        # Recursively redact lists of dicts
        elif isinstance(value, list):
            redacted[key] = [
                redact_secrets(item) if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, str):
            contains_pem_marker = value.startswith("-----BEGIN ") or ("-----" in value and "BEGIN" in value)
            if contains_pem_marker:
                redacted[key] = f"{value[:50]}...***REDACTED***"
            # Redact long strings that might contain secrets
            elif len(value) > 100:
                if "BEGIN" in value or "-----" in value or "yaml" in key.lower():
                    redacted[key] = f"{value[:50]}...***REDACTED***"
                else:
                    redacted[key] = value
            else:
                redacted[key] = value
        else:
            redacted[key] = value

        # Ensure shorter YAML-encoded secrets (by key hint) are redacted consistently
        if isinstance(value, str) and key.lower().endswith("_pem") and "***REDACTED***" not in redacted[key]:
            redacted[key] = f"{value[:50]}...***REDACTED***"

    return redacted


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Add sensitive data filter to all handlers
    sensitive_filter = SensitiveDataFilter()
    logger.addFilter(sensitive_filter)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    for log_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logging.getLogger(log_name).handlers = []
        logging.getLogger(log_name).propagate = True
        logging.getLogger(log_name).addFilter(sensitive_filter)
