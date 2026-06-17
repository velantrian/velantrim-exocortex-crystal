# Claude Code Handoff — 2026-06-17

> Scope: work that requires code inspection, tests or controlled runtime changes.
> Status: handoff only. ChatGPT added and corrected docs; Claude Code should handle code with tests.

## Current implementation plan

Use the Claude Code Track 1–3B plan as the current source of implementation order.

```text
Track 1  — ProvenanceChain per-fact event chain
Track 2  — Docker hardening from scratch
Track 3A — TruthPolicy production default
Track 3B — Write-path TruthGate audit/tests
```

Each track must be a separate branch and PR. No bundling.

## Important corrections to earlier docs

### Crystal token variable

Crystal API uses:

```text
VELANTRIM_API_TOKEN
```

Do not use Titan-oriented `VELANTRIM_API_KEY` wording for Crystal Docker/API unless code support is changed.

### ProvenanceChain

Do not treat the Titan `_compute_hash(actor/reason)` TypeError as a confirmed Crystal regression.

Claude Code identified the Crystal task as:

```text
implement missing per-fact ProvenanceChain from Sprint1 P1-5 / I89 spec
```

Crystal already has other provenance/audit mechanisms, but they are not the same thing:

```text
core/audit.py       = global audit chain
core/provenance.py  = per-answer receipt provenance
core/provenance_chain.py = planned per-fact event chain
```

### Docker

Docker files are creation targets:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Do not assume they already exist.

### TruthPolicy

Track 3A and Track 3B are separate:

```text
Track 3A = env default strict behaviour
Track 3B = write-path behavioural tests + gate_reason in review audit
```

Claude Code reported that major write paths already route through TruthGate and no `/facts` POST endpoint exists. Do not frame Track 3B as “all write gates are missing.”

## Track 1 — ProvenanceChain

Create/modify:

```text
CREATE core/provenance_chain.py
MODIFY core/memory.py      # provenance_chain table + index
MODIFY core/erasure.py     # append per-fact provenance after existing audit event
CREATE tests/test_provenance_chain.py
```

Required behaviour:

- `_GENESIS = "0" * 64`;
- per-fact sequence starts at genesis;
- `_compute_hash(..., actor="system", reason="")` hashes all fields consistently;
- `append()` returns bool and never raises into erasure;
- `verify()` returns `empty_chain` with `ok=False` for empty chains;
- non-empty verified chains return `status="ok", ok=True`;
- tampered payload/actor/reason returns `ok=False`.

Required tests:

1. append succeeds for a normal event;
2. verify on non-empty chain succeeds;
3. payload tamper fails;
4. actor tamper fails;
5. reason tamper fails;
6. `erase_fact()` creates an erase event with actor/reason;
7. empty chain is `empty_chain`, not `ok`.

## Track 2 — Docker hardening from scratch

Create:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

Primary required compose line:

```yaml
VELANTRIM_API_TOKEN=${VELANTRIM_API_TOKEN:?Set VELANTRIM_API_TOKEN before running}
```

Required defaults:

```yaml
ports:
  - "127.0.0.1:8000:8000"
VELANTRIM_API_HOST=127.0.0.1
VELANTRIM_DB=/app/data/velantrim_memory.db
```

Dockerfile requirements:

- multi-stage builder -> runtime;
- `pip install '.[api]'`, not `[dev]`;
- create non-root user `velantrim` and run as that user;
- copy any required top-level py-module listed in `pyproject.toml`.

Manual verification:

```bash
docker compose up
# without token: must fail

VELANTRIM_API_TOKEN=dev-local-token docker compose up
curl http://127.0.0.1:8000/health

docker inspect <image> | jq '.[0].Config.User'
# expected: velantrim
```

## Track 3A — TruthPolicy production default

Modify `core/truth_gate.py` inside the `truth_gate()` function body.

Expected behaviour:

```text
ENABLE_TRUTH_POLICY unset -> strict ON
ENABLE_TRUTH_POLICY=on  -> strict ON
ENABLE_TRUTH_POLICY=off -> legacy bypass
```

Tests:

1. ON blocks LLM-origin world fact;
2. OFF permits legacy bypass;
3. unset defaults strict.

## Track 3B — Write-path TruthGate audit/tests

Modify/create:

```text
MODIFY core/review.py                 # add gate_reason to review_force_approve audit detail
CREATE tests/test_write_path_gate.py
MODIFY tests/test_api.py              # POST /ingest gate-block test
```

Tests:

1. force approve still calls TruthGate;
2. force approve audit includes `gate_reason`;
3. `/ingest` blocks LLM-origin world fact;
4. bulk import dry-run blocks LLM-origin world fact.

## Do not do

- Do not import Titan wholesale into Crystal.
- Do not add NoeticCore / AttentionRouter / Research PWA as current runtime.
- Do not add BICA runtime.
- Do not make Graphiti mandatory.
- Do not claim a verified universal graph.
- Do not combine tracks into one PR.
