# Build Brief: `docker-swarm-mcp` (No Portainer)

You are building a new **Model Context Protocol (MCP) server** that manages Docker Engine + Docker Swarm directly (no Portainer). It exposes MCP tools over HTTP to let an AI assistant create/manage containers, services, networks, volumes, and Compose stacks. It must work against a **local socket** or a **remote engine** reached over **TLS/SSH** (compatible with tunnels like **ngrok** or **Tailscale**).

## Hard Requirements

* **Language/stack**

  * Python 3.12
  * FastAPI + Uvicorn
  * `docker` (docker-py) SDK
  * Pydantic (request/response schemas), Pytest (tests)
* **Project layout**

  ```
  /app
    /routers         # FastAPI routers, one file per tool-family (containers, services, stacks, networks, volumes, info)
    /schemas         # Pydantic models for request/response
    /core            # bootstrap, settings, error mappers
    /mcp             # tool discovery, tools.yaml loader, health endpoints
    docker_client.py # wrapper around docker SDK (single place for DOCKER_HOST/TLS handling)
  /docs
    /dependencies    # stub md files per dependency (see below)
    /architecture    # high-level diagrams & decisions (stubs ok)
  tools.yaml
  pyproject.toml (or requirements.txt)
  README.md
  tests/
  ```
* **Config (env-first)**

  * `DOCKER_HOST`, `DOCKER_TLS_VERIFY`, `DOCKER_CERT_PATH` respected by `docker_client.DockerClient()`.
  * App env: `MCP_API_KEY` (optional), `ALLOWED_ORIGINS` (CORS), `LOG_LEVEL`.
* **Security**

  * DO NOT expose the raw Docker daemon publicly.
  * Document TLS/SSH usage; warn against non-TLS exposure.
* **MCP interface**

  * An index endpoint that lists tools + JSON Schemas.
  * `tools.yaml` that declares each tool: name, description, method, path, JSON schema.

## Tools to Implement (minimum)

### Containers

* `list-containers` (filters: all, status), `create-container` (image, name, env, ports, volumes, restart_policy), `start-container`, `stop-container`, `remove-container`, `get-logs` (name/id, tail, since).

### Compose/Stacks (Swarm-friendly)

* `deploy-compose` (project_name, compose_yaml string; accept v3+), `remove-compose` (project_name), `list-stacks` (derive from labels or compose projects).
* Optionally map Compose to Swarm services when engine is in Swarm mode.

### Services (Swarm)

* `list-services`, `scale-service` (name, replicas), `remove-service` (name).

### Networks & Volumes

* `list-networks`, `create-network` (name, driver, options), `remove-network`.
* `list-volumes`, `create-volume` (name, driver, opts), `remove-volume`.

### System

* `info` (daemon info), `ping`.

## Docker Client Abstraction

Create `docker_client.DockerClient` that:

* Initializes from env (`from_env`) and/or explicit host/TLS config.
* Exposes thin methods used by routers (e.g., `create_container`, `deploy_compose`, `scale_service`).
* Catches docker SDK exceptions and raises uniform HTTP errors with helpful messages.

## Reference-on-Demand Documentation (Important)

Do **not** load large external docs into the context. Instead:

1. **Create stubs now** under `docs/dependencies/`:

   * `docker.md`, `fastapi.md`, `uvicorn.md`, `pydantic.md`, `pytest.md`, `compose.md`, `swarm.md`, `tls.md`, `ngrok.md`, `tailscale.md`.
2. **Stub template content** for each file:

   * H1 with dependency name.
   * A 3–5 bullet “What we use it for”.
   * A “Key APIs / CLI we rely on” list (empty placeholders OK).
   * A “References” section linking to the upstream repo/docs.
   * A “DeepWiki Notes” section (empty by default).
3. **When you (the AI) need specifics**, use **DeepWiki MCP** to read precisely the relevant page/snippet (e.g., `docker/docker-py` method signatures, Compose v3 schema nuances), then **append a concise summary** to the corresponding `docs/dependencies/<name>.md` under **“DeepWiki Notes”**. Keep each update ≤ 150 lines; prefer exact signatures and minimal examples over prose.
4. Throughout code & tests, **reference these stubs** in comments like:

   ```text
   See docs/dependencies/docker.md#DeepWiki-Notes (ContainerCollection.run)
   ```

   so humans know where to look.

> You are not permitted to paste long documentation blobs into source files. Summarize to the stub files, link to sources, and keep code comments short.

## Testing

* `pytest` unit tests for `docker_client` (mock docker SDK).
* `TestClient` API tests for each router endpoint (200 and failure paths).
* Include sample payload fixtures for tools like:

  * `create-container`: `{ "image": "nginx:alpine", "name": "web", "ports": {"8080/tcp": 8080} }`
  * `deploy-compose`: `{ "project_name": "demo", "compose_yaml": "<inline yaml>" }`

## Dev & Ops

* `README.md` with quickstart:

  * Local: `uvicorn app.main:app --reload`
  * Dockerized server with volume-mount of `/var/run/docker.sock` (local) OR `DOCKER_HOST=ssh://user@host` style remote.
  * Examples for **ngrok** (TCP tunnel) and **Tailscale** (private IP + SSH/TLS) configuration. Warn loudly against exposing unauthenticated TCP.
* Provide `Dockerfile` and a minimal `compose.yaml` to run the MCP server itself.

## Deliverables

* Running MCP server with the tools above.
* `tools.yaml` declaring all tools & schemas.
* `docs/dependencies/*.md` stub set in place + used by code comments/tests.
* Tests passing.
* Clear security notes.

## Explicit Dependencies

Add these to `pyproject.toml` (or `requirements.txt`):

* `fastapi`, `uvicorn[standard]`, `docker`, `pydantic`, `pytest`, `python-dotenv` (optional), `PyYAML` (for compose parsing if needed).

## Non-Goals

* No Portainer client or assumptions about Portainer objects (envs, teams, tags).
* Don’t implement secrets/configs/registries yet (leave as future work; add TODOs).

