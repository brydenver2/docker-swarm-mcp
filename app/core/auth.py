import hmac
import json
import logging
from typing import Any

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """Verify token without scope parsing (for backward compatibility)"""
    if not settings.MCP_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MCP_ACCESS_TOKEN not configured"
        )

    token_valid = hmac.compare_digest(
        credentials.credentials,
        settings.MCP_ACCESS_TOKEN
    )

    if not token_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token"
        )

    return credentials.credentials


async def verify_token_with_scopes(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> set[str]:
    """
    Verify token and extract scopes for MCP endpoint authorization

    Scopes can come from:
    1. JWT token claims (if using JWT)
    2. Static scope mapping based on token
    3. Environment variable scope configuration

    Returns:
        Set of scope strings (e.g., {"admin", "container-ops", "read-only"})
    """
    if not settings.MCP_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MCP_ACCESS_TOKEN not configured"
        )

    token_valid = hmac.compare_digest(
        credentials.credentials,
        settings.MCP_ACCESS_TOKEN
    )

    if not token_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing access token"
        )

    # Parse scopes from token or configuration
    scopes = _parse_scopes(credentials.credentials)

    logger.debug(
        f"Token verified with scopes: {scopes}",
        extra={"scopes": list(scopes)}
    )

    return scopes


def _parse_scopes(token: str) -> set[str]:
    """
    Parse scopes from token or static configuration

    Priority:
    1. JWT token claims (if token is a JWT)
    2. Static scope mapping from TOKEN_SCOPES env var
    3. Default to admin scope if no mapping found
    """
    # Try to parse JWT token for claims
    try:
        import jwt
        # Don't verify signature here, already validated with HMAC
        payload = jwt.decode(token, options={"verify_signature": False})
        if "scope" in payload:
            scopes_str = payload["scope"]
            return set(scopes_str.split()) if isinstance(scopes_str, str) else set(scopes_str)
        if "scopes" in payload:
            return set(payload["scopes"])
    except Exception:
        # Token is not a JWT or doesn't have scope claims
        pass

    # Try static scope mapping from environment
    if settings.TOKEN_SCOPES:
        try:
            scope_mapping = json.loads(settings.TOKEN_SCOPES)
            if token in scope_mapping:
                return set(scope_mapping[token])
        except json.JSONDecodeError:
            logger.warning("Invalid TOKEN_SCOPES JSON configuration")

    # Default: grant admin scope for backward compatibility
    return {"admin"}


def check_scopes(required_scopes: set[str], user_scopes: set[str]) -> bool:
    """
    Check if user has required scopes

    Args:
        required_scopes: Set of required scopes (any match grants access)
        user_scopes: Set of user's scopes

    Returns:
        True if user has any of the required scopes or has "admin" scope
    """
    if "admin" in user_scopes:
        return True
    return bool(required_scopes & user_scopes)
