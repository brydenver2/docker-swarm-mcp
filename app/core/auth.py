import hmac
import json
import logging

from fastapi import HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from app.core.config import settings

logger = logging.getLogger(__name__)


class HTTPBearerOrQuery(HTTPBearer):
    """
    Custom security class that accepts Bearer tokens from Authorization header
    OR X-Access-Token header for simpler client configuration.

    Priority:
    1. Authorization header (standard, takes precedence)
    2. X-Access-Token header (fallback for simpler configs)

    Note:
        Query parameter authentication has been removed for security reasons
        (tokens should never appear in URLs).

    TODO: Legacy class name HTTPBearerOrQuery is retained for backward compatibility.
          The class no longer accepts query parameters and only accepts header-based
          authentication (Authorization header or X-Access-Token header).
          Consider renaming to HTTPBearerOrHeader in a future breaking change.
    """

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        # Try Authorization header first (standard behavior)
        """
        Accept an access token from the Authorization header (Bearer) or the X-Access-Token header and return HTTP authorization credentials.
        
        If the Authorization header contains a Bearer token, that token is used. If not, the X-Access-Token header is used as a fallback. Query-parameter authentication is not supported.
        
        Returns:
            HTTPAuthorizationCredentials: Credentials containing the scheme (typically "Bearer") and the token string.
        
        Raises:
            HTTPException: With status 403 and WWW-Authenticate: "Bearer" when no valid token is found.
        """
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)

        if scheme and scheme.lower() == "bearer" and credentials:
            return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)

        # Fallback to custom header for clients that cannot set Authorization
        access_token = request.headers.get("X-Access-Token")

        if access_token:
            logger.debug(
                "Token extracted from X-Access-Token header",
                extra={"header": "X-Access-Token"}
            )
            return HTTPAuthorizationCredentials(scheme="X-Access-Token", credentials=access_token)

        # No valid token found
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


security = HTTPBearerOrQuery()


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
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> set[str]:
    """
    Validate the provided access token and return the set of authorization scopes for MCP endpoints.
    
    Determines scopes from a per-token mapping, from JWT claims, or from the single shared token configuration and raises HTTPException on misconfiguration or invalid token.
    
    Returns:
        set[str]: The resolved set of scope strings (for example {"admin", "container-ops", "read-only"}).
    
    Raises:
        HTTPException: 500 if neither TOKEN_SCOPES nor MCP_ACCESS_TOKEN is configured; 401 if the token is invalid or missing.
    """
    token = credentials.credentials

    # Try multi-token approach first (TOKEN_SCOPES mapping)
    if settings.TOKEN_SCOPES:
        try:
            token_scopes_mapping = json.loads(settings.TOKEN_SCOPES)
            if token in token_scopes_mapping:
                scopes = set(token_scopes_mapping[token])
                logger.debug(
                    "Token verified with scopes from TOKEN_SCOPES mapping",
                    extra={"scopes": list(scopes)}
                )
                return scopes
        except json.JSONDecodeError:
            logger.warning("Invalid TOKEN_SCOPES JSON configuration")

    # Fallback to single token validation
    if not settings.MCP_ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MCP_ACCESS_TOKEN or TOKEN_SCOPES not configured"
        )

    token_valid = hmac.compare_digest(token, settings.MCP_ACCESS_TOKEN)

    if not token_valid:
        failure_status = status.HTTP_401_UNAUTHORIZED

        if credentials.scheme == "X-Access-Token":
            failure_status = status.HTTP_403_FORBIDDEN
            try:
                body_bytes = await request.body()
                if body_bytes:
                    payload = json.loads(body_bytes)
                    if payload.get("method") != "initialize":
                        failure_status = status.HTTP_401_UNAUTHORIZED
            except (json.JSONDecodeError, AttributeError):
                failure_status = status.HTTP_401_UNAUTHORIZED

        raise HTTPException(
            status_code=failure_status,
            detail="Invalid or missing access token"
        )

    # Parse scopes from token or configuration
    scopes = _parse_scopes(token)

    logger.debug(
        f"Token verified with scopes: {scopes}",
        extra={"scopes": list(scopes)}
    )

    return scopes


def _parse_scopes(token: str) -> set[str]:
    """
    Parse scopes from token or static configuration

    IMPORTANT: This function assumes token authenticity has been validated
    via HMAC comparison before calling. Do not call this function directly
    without prior token validation.

    Priority:
    1. JWT token claims (if token is a JWT)
    2. Static scope mapping from TOKEN_SCOPES env var
    3. Default to admin scope if no mapping found
    """
    # Try to parse JWT token for claims
    # SECURITY NOTE: verify_signature=False is SAFE here because:
    # 1. Token authenticity already verified with HMAC (line 74)
    # 2. This decode is ONLY for extracting scope claims from payload
    # 3. Not used for authentication - only for authorization metadata
    try:
        import jwt
        payload = jwt.decode(token, options={"verify_signature": False})
        if "scope" in payload:
            scopes_str = payload["scope"]
            return set(scopes_str.split()) if isinstance(scopes_str, str) else set(scopes_str)
        if "scopes" in payload:
            return set(payload["scopes"])
    except (jwt.DecodeError, jwt.InvalidTokenError, KeyError) as e:
        # Token is not a JWT or doesn't have scope claims
        logger.debug("JWT scope parse skipped", extra={"reason": str(e)})

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
    if not required_scopes:
        return True
    return bool(required_scopes & user_scopes)
