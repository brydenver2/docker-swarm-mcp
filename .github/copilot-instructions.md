# GitHub Copilot Instructions

These guardrails keep Copilot suggestions aligned with the Docker Swarm MCP Server’s standards. Follow them for **all** completions, even when the user does not restate them.

## Repository Goals
- First-class support for Docker **Swarm** (services, stacks, networks, volumes) with optional fallbacks to standalone Docker.
- Secure, observable MCP surface area: every endpoint must have authentication, logging context, and schema validation in place.
- Keep context windows lean. Prefer surfacing just-in-time guidance (meta tools, discoverable docs) over dumping every capability by default.

## Implementation Priorities
1. **Security before convenience**: never suggest storing secrets in source control; prefer env vars, Docker secrets, or secret files.
2. **Swarm parity**: when you add a container-only feature, show how it maps to Swarm (service logs, stack labels, etc.).
3. **Resilient retries**: use `app.utils.retry` decorators (`retry_read`, `retry_write`, `retry_none`) to wrap Docker interactions.
4. **Structured logging**: rely on `logging.getLogger(__name__)` and include contextual `extra` payloads for sensitive operations.
5. **Schema-first APIs**: FastAPI routes must expose response models or documented schemas; MCP tools need both request and response schemas.

## Coding Standards
- Python 3.12+, Pydantic v2. Use `ConfigDict` (`model_config = ConfigDict(...)`) instead of legacy `class Config`.
- Type hints are required. Prefer `dict[str, Any]` over `Dict` unless compatibility demands otherwise.
- Keep functions small; extract helpers in `app/services/*` rather than bloating routers.
- Normalize inputs (timestamps, labels, env vars) near the transport boundary so downstream code can assume sane types.
- When touching Docker stacks/services, always populate `com.docker.stack.*` labels so `docker stack ls` behaves correctly.

## Security Requirements
- Authentication: use `HTTPBearerOrQuery` / `verify_token_with_scopes`. Never add unauthenticated endpoints.
- Secrets & tokens must **never** appear in logs; use `SensitiveDataFilter` helpers or redact manually.
- Reject insecure patterns (query-param tokens, plaintext secrets in docs, disabling TLS verification without warnings).

## Testing Expectations
- Add or update pytest coverage for every behavioral change. Tests live under `tests/` and should use the httpx + ASGI transport harness.
- Use `pytest.mark.asyncio` for coroutine tests. Avoid `asyncio.run` inside tests; rely on the configured asyncio mode.
- When adding retry/backoff code, include deterministic tests that patch `asyncio.sleep`.

## Documentation & Changelog
- Update `README.md` for user-facing behavior changes (new tools, instructions, environment variables).
- Every change that affects behavior must be recorded under the `[Unreleased]` section of `CHANGELOG.md` with **Added/Changed/Fixed/Testing** placement.

## Communication Style
- Be explicit about limitations (“Swarm managers only”, “requires TLS certificates”). Offer migration notes when deprecating behavior.
- Prefer actionable suggestions (“Run `docker stack ls` to confirm labels”) over vague advice.

Following these rules keeps Copilot’s output consistent with the project’s quality bar. Ignore or override them only when the maintainer explicitly asks you to do so.
