# Velantrim ExoCortex — Crystal: production API image (Track 2).
#
# Multi-stage build:
#   1. builder  — installs the package + the [api] extra into an isolated venv.
#   2. runtime  — copies only that venv, runs as a non-root user, fail-closed.
#
# Security posture (see docs/security/DEPLOYMENT_SECURITY.md):
#   - No dev/research/embedding/graph extras: only ".[api]" (fastapi + uvicorn).
#   - No source tree, tests, docs, secrets, or local databases in the image
#     (enforced by .dockerignore + an explicit, minimal COPY surface).
#   - Runs as the unprivileged "velantrim" user.
#   - Fail-closed: the container refuses to start unless VELANTRIM_API_TOKEN is
#     set (see CMD), so an unprotected API can never be launched by accident.

# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

# Isolated venv so the runtime stage can copy a single self-contained tree.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy ONLY what `pip install .` needs to build the wheel: packaging metadata
# (pyproject.toml + README.md for the readme + LICENSE for the license file),
# the `core` package, and the top-level py-module declared in pyproject.toml
# (py-modules = ["epigenetic_adaptation_module"]).
COPY pyproject.toml README.md LICENSE ./
COPY core ./core
COPY epigenetic_adaptation_module.py ./

# Install the runtime + HTTP service layer only (fastapi + uvicorn). NOT [dev].
RUN pip install ".[api]"

# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Runtime defaults. VELANTRIM_API_HOST is 0.0.0.0 INSIDE the container so the
# published port can reach uvicorn; the loopback security boundary is enforced
# on the HOST side by the compose port mapping ("127.0.0.1:8000:8000"). Binding
# 0.0.0.0 within an isolated container is not a public exposure on its own.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    VELANTRIM_API_HOST=0.0.0.0 \
    VELANTRIM_API_PORT=8000 \
    VELANTRIM_DB=/app/data/velantrim_memory.db

# Unprivileged runtime user; /app/data owned by it for the SQLite store.
RUN useradd --create-home --shell /usr/sbin/nologin velantrim \
    && mkdir -p /app/data \
    && chown -R velantrim:velantrim /app

# Bring over the fully-built virtualenv (package + fastapi + uvicorn + scripts).
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
USER velantrim

# Persistent local-first store. Bind-mount or named volume at runtime.
VOLUME ["/app/data"]

EXPOSE 8000

# Liveness probe hits the cheap, DB-free /health endpoint. Uses stdlib urllib
# (curl is intentionally not installed in the slim runtime). 127.0.0.1 works
# here because uvicorn binds 0.0.0.0 and therefore also listens on loopback.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).status==200 else 1)"]

# Fail-closed entrypoint: refuse to start without an operator-provided token.
# `${VAR:?msg}` makes the shell exit non-zero (printing msg) when VAR is unset
# or empty, so the image itself is fail-closed even under a bare `docker run`.
CMD ["sh", "-c", ": \"${VELANTRIM_API_TOKEN:?Set VELANTRIM_API_TOKEN before running}\"; exec velantrim-api"]
