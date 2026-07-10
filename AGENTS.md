# AGENTS.md

Short working guide for AI coding agents (Codex, Copilot, Claude, and similar) in
this repository. For full detail, start with `README.md` and
`docs/REVIEWER_GUIDE.md`.

## What this is

Velantrim Exo-Cortex Crystal is a local-first, standard-library-only AI memory
infrastructure: it stores source-grounded facts in a canonical graph, admits new
knowledge only through a TruthGate, and emits replayable traces/receipts so
answers can be audited. This repository is the public open core (reviewer-preview).

## Scope & boundaries

- This is the public Crystal core — not Titan, Full Exo-Cortex, or Research Mode.
- The canonical graph is the source of truth, and the TruthGate is the only entry
  into it. Do not write to the canon directly or bypass the TruthGate.
- Traces/receipts are the proof layer; keep them intact.

## Setup, build & test

- Python >= 3.11.
- Install with dev extras: `pip install -e '.[dev]'`
- Run the suite with the coverage gate: `pytest tests/ --cov=. --cov-fail-under=100`
- The runtime path is pure standard library. Do not add mandatory third-party
  dependencies; optional features go through extras in `pyproject.toml`.

## Working conventions

- Make small, reviewable changes and keep the coverage gate green.
- Match the existing style and module structure under `core/`.
- Do not bypass the TruthGate or mutate canonical state outside its path.
- For command/usage examples, see `README.md` and `DEMO.md` — do not invent
  commands.

## Claims discipline

Avoid unsupported capability, compliance, production-readiness,
biological-cognition, or absolute-reliability claims in code, comments, or docs.
Defer status claims to `README.md`, `TEST_REPORT.md`, and CI.

## Where to look

- `README.md` — overview, quick start, positioning.
- `docs/REVIEWER_GUIDE.md` — canonical reviewer entry point.
- `docs/ARCHITECTURE.md` — architecture and memory/backends/privacy boundaries.
- `docs/EVAL.md` — evaluation harness, metrics, and CI gate (authoritative).
- `DEMO.md` and `docs/DEMO.md` — hands-on walkthroughs and command examples.

## Cursor Cloud specific instructions

Pure-Python project (Python 3.12 here; requires >=3.11). Dev dependencies are
installed by the startup update script, so a fresh cloud VM is ready to test
without extra setup. Standard commands live in `README.md` / `CONTRIBUTING.md`
/ `.github/workflows/ci.yml`; only the non-obvious cloud caveats are below.

- Console scripts (`velantrim`, `velantrim-api`, `velantrim-mcp`) install to
  `~/.local/bin`, which is not on `PATH` by default. Either prepend it
  (`export PATH="$HOME/.local/bin:$PATH"`) or call the modules directly
  (`python -m core.cli ...`, `python -m core.api`, `python -m core.mcp_server`).
- The default runtime is dependency-free; on first use it prints harmless
  `auto L3: LadybugDB unavailable ... falling back to on-disk SQLite` and
  `auto embedder: sbert unavailable ... falling back to HashingEmbedder`. These
  are expected fallbacks, not errors.
- Run against a scratch canon to avoid touching repo state:
  `export VELANTRIM_L3_PATH=/tmp/velantrim_demo/l3.db VELANTRIM_DB=/tmp/velantrim_demo/l1.db`.
- The FastAPI layer (`velantrim-api`, serves `127.0.0.1:8000`) needs `uvicorn`,
  which is in the `[api]` extra (not `[dev]`); the update script installs both.
- Full suite takes ~4 min and enforces a 100% coverage gate
  (`pytest tests/ --cov=. --cov-fail-under=100`); do not commit changes that
  drop coverage. Security lint mirrors CI: `bandit -r core/ scripts/ -ll -q`.
- `CONTRIBUTING.md` — contributor setup and PR expectations.
