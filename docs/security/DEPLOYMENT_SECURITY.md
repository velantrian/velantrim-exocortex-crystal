# Deployment Security Notes

> Date: 2026-06-17
> Scope: deployment hardening note for Crystal
> Status: docs-only. This file records required defaults and review items; it does not claim the runtime is already hardened.

## Principle

Crystal deployment must fail closed. Development convenience must not become a public default.

```text
No known default API key.
No public bind by accident.
No root container where avoidable.
No secrets or local databases copied into images.
```

## Required safe defaults

### API key

Deployment must require an operator-provided secret.

Recommended compose pattern:

```yaml
VELANTRIM_API_KEY=${VELANTRIM_API_KEY:?Set VELANTRIM_API_KEY}
```

Avoid:

```yaml
VELANTRIM_API_KEY=${VELANTRIM_API_KEY:-dev-key-change-me}
```

A known fallback key makes the server appear protected while exposing a public secret.

### Network binding

Local/demo compose should bind to loopback by default:

```yaml
ports:
  - "127.0.0.1:8000:8000"
```

Public exposure should require an explicit override file and reverse proxy configuration.

### Container user

Production images should not run as root unless explicitly justified.

Recommended direction:

```dockerfile
USER 1000:1000
```

### Build context hygiene

A `.dockerignore` should exclude:

```text
.env
.git/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
data/*.db
data/*.sqlite
data/*.kuzu
*.log
```

### Dependency profile

Production images should avoid installing development and research extras by default.

Avoid bundling test/dev/audio/embedding/graph-lab dependencies into the production image unless the deployment explicitly needs them.

## Public endpoints

Public unauthenticated endpoints should be minimal. Debug endpoints should be disabled or protected in production.

Recommended policy:

```text
/health       public minimal status only, no corpus statistics
/metrics      disabled or protected unless explicitly exposed
/debug/*      disabled by default or requires auth
/console/*    demo/dev unless hardened
```

## Error messages

Production HTTP responses should not leak raw exceptions, SQL fragments, stack traces, upstream provider messages, or local filesystem paths.

Recommended pattern:

```json
{"error": "internal_server_error"}
```

Detailed diagnostics belong in server logs.

## Claude Code follow-up

Claude Code should verify and patch:

1. compose requires `VELANTRIM_API_KEY` and binds to loopback by default;
2. Dockerfile uses a non-root user;
3. `.dockerignore` excludes secrets, caches and local databases;
4. dev/test/research extras are not installed in the production image by default;
5. public health/debug endpoints do not expose sensitive internals.
