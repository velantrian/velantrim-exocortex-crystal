# Deployment Security Notes

> Date: 2026-06-17
> Scope: deployment hardening note for Crystal
> Status: docs-only. This file records required defaults and review items; it does not claim the runtime is already hardened.

## Correction after Claude Code plan

Crystal uses the API token environment variable:

```text
VELANTRIM_API_TOKEN
```

Do not use the Titan-oriented `VELANTRIM_API_KEY` wording for Crystal deployment docs unless the code is changed to support it.

Docker hardening (Track 2) is implemented: `Dockerfile`, `docker-compose.yml`,
and `.dockerignore` were added by PR #170 (`feat(docker): Track 2 — fail-closed
local-first container deployment`) and hardened further by PR #171
(`fix(docker): address Codex review findings on Track 2`). This file's
remaining sections describe what those files already implement, kept here as
the reviewable spec for that behaviour.

## Principle

Crystal deployment must fail closed. Development convenience must not become a public default.

```text
No known default API token.
No public bind by accident.
No root container where avoidable.
No secrets or local databases copied into images.
```

## Required safe defaults

### API token

Deployment must require an operator-provided token.

Required compose pattern:

```yaml
VELANTRIM_API_TOKEN=${VELANTRIM_API_TOKEN:?Set VELANTRIM_API_TOKEN before running}
```

Avoid known fallback tokens such as:

```yaml
VELANTRIM_API_TOKEN=${VELANTRIM_API_TOKEN:-dev-key-change-me}
```

A known fallback token makes the server appear protected while exposing a public secret.

### Network binding

Docker compose should bind to loopback by default:

```yaml
ports:
  - "127.0.0.1:8000:8000"
```

The API host should remain local by default:

```yaml
VELANTRIM_API_HOST=127.0.0.1
```

Public exposure should require an explicit override file and reverse proxy configuration.

### Container user

Production images should not run as root unless explicitly justified.

Recommended direction:

```dockerfile
RUN useradd --create-home --shell /usr/sbin/nologin velantrim
USER velantrim
```

### Build context hygiene

A `.dockerignore` should exclude:

```text
.env
.git/
__pycache__/
**/__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
data/*.db
data/*.sqlite
data/*.kuzu
*.log
venv/
.venv/
```

### Dependency profile

Track 2 (PR #170, hardened in #171) uses the API extra only:

```dockerfile
pip install '.[api]'
```

Do not install `[dev]`, research, audio, graph-lab, or embedding extras in the production image by default.

## Track 2 deliverables

Delivered in PR #170 and #171:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Requirements (all implemented):

1. multi-stage builder -> runtime image;
2. `pip install '.[api]'`, not `[dev]`;
3. copy any top-level py-module required by `pyproject.toml` into runtime;
4. non-root `velantrim` user;
5. loopback bind by default;
6. fail-fast `VELANTRIM_API_TOKEN`;
7. data volume mounted at `/app/data`;
8. `VELANTRIM_DB=/app/data/velantrim_memory.db`.

## Manual verification

```bash
docker compose up
# without VELANTRIM_API_TOKEN: must fail fast

VELANTRIM_API_TOKEN=dev-local-token docker compose up
curl http://127.0.0.1:8000/health

docker inspect <image> | jq '.[0].Config.User'
# expected: velantrim
```

## Public endpoints

Public unauthenticated endpoints should be minimal. Debug endpoints should be disabled or protected in production.

Recommended policy:

```text
/health       public minimal status only, no corpus statistics
/metrics      disabled or protected unless explicitly exposed
/debug/*      disabled by default or requires auth
```

## Error messages

Production HTTP responses should not leak raw exceptions, SQL fragments, stack traces, upstream provider messages, or local filesystem paths. Detailed diagnostics belong in server logs.
