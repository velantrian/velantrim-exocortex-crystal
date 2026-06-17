# Claude Code P0 Tasks

> Date: 2026-06-17
> Scope: code tasks that require repository inspection, tests and controlled diffs.
> This file supersedes earlier Titan-oriented wording.

## Track order

Do these as separate branches and PRs:

1. Track 1 — ProvenanceChain per-fact event chain.
2. Track 2 — Docker hardening from scratch.
3. Track 3A — TruthPolicy production default.
4. Track 3B — Write-path TruthGate audit/tests.

No bundling.

---

## Track 1 — ProvenanceChain

Crystal should implement the missing per-fact event chain described by the Sprint1 P1-5 / I89 design.

Important correction:

```text
This is not a confirmed Crystal regression.
The Titan audit reported an actor/reason TypeError in Titan.
In Crystal, Claude Code identified the per-fact ProvenanceChain as absent/planned.
```

Create/modify:

```text
CREATE core/provenance_chain.py
MODIFY core/memory.py      # provenance_chain table + index
MODIFY core/erasure.py     # append provenance event after existing audit event
CREATE tests/test_provenance_chain.py
```

Required interface:

```python
def _compute_hash(
    prev_hash,
    event_type,
    fact_id,
    from_state,
    to_state,
    payload_str,
    created_at,
    actor: str = "system",
    reason: str = "",
) -> str:
    ...
```

`append()` must never block erasure by propagating exceptions.

Required tests:

1. append succeeds for a normal event;
2. verify on non-empty chain returns `status="ok", ok=True`;
3. tamper `payload_str` -> verify fails;
4. tamper `actor` -> verify fails;
5. tamper `reason` -> verify fails;
6. `erase_fact()` creates an `erase` event with actor/reason;
7. empty chain returns `status="empty_chain", ok=False`.

---

## Track 2 — Docker hardening from scratch

Important correction:

```text
Dockerfile, docker-compose.yml and .dockerignore are creation targets.
Do not assume they already exist.
Crystal API token env var is VELANTRIM_API_TOKEN.
```

Create:

```text
Dockerfile
docker-compose.yml
.dockerignore
```

First mandatory compose line:

```yaml
VELANTRIM_API_TOKEN=${VELANTRIM_API_TOKEN:?Set VELANTRIM_API_TOKEN before running}
```

Required defaults:

```yaml
ports:
  - "127.0.0.1:8000:8000"
```

Runtime requirements:

- multi-stage Dockerfile;
- `pip install '.[api]'`, not `[dev]`;
- non-root `velantrim` user;
- `ENV VELANTRIM_API_HOST=127.0.0.1`;
- `VELANTRIM_DB=/app/data/velantrim_memory.db`;
- volume `./data:/app/data`;
- copy top-level `epigenetic_adaptation_module.py` if required by `pyproject.toml`.

Manual verification:

```bash
docker compose up
# without VELANTRIM_API_TOKEN: must fail

VELANTRIM_API_TOKEN=dev-local-token docker compose up
curl http://127.0.0.1:8000/health

docker inspect <image> | jq '.[0].Config.User'
# expected: velantrim
```

---

## Track 3A — TruthPolicy production default

Add explicit, testable TruthPolicy default behaviour.

Expected behaviour:

```text
ENABLE_TRUTH_POLICY unset -> strict ON
ENABLE_TRUTH_POLICY=on  -> strict ON
ENABLE_TRUTH_POLICY=off -> legacy bypass
```

Implementation note:

Read the env var inside the `truth_gate()` function body so `monkeypatch.setenv()` works in tests.

Required tests:

1. `ENABLE_TRUTH_POLICY=on` blocks `LLM_OUTPUT + WORLD_FACT` where policy requires blocking;
2. `ENABLE_TRUTH_POLICY=off` confirms legacy bypass for the same case;
3. unset env enforces strict default.

PR title:

```text
test/config: define strict TruthPolicy production default
```

---

## Track 3B — Write-path TruthGate audit

Important correction:

```text
Do not assume all write paths are missing TruthGate.
Claude Code found major write paths already routed through TruthGate.
No /facts POST endpoint exists.
```

Scope:

- add behavioural pin tests;
- add `gate_reason` to force-approve audit detail;
- test `/ingest` gate-block behaviour;
- test bulk import blocks LLM-origin world facts.

Create/modify:

```text
MODIFY core/review.py                 # add gate_reason to review_force_approve audit detail
CREATE tests/test_write_path_gate.py
MODIFY tests/test_api.py              # add POST /ingest gate-block test
```

Required tests:

1. force approve still calls TruthGate;
2. force approve audit includes `gate_reason`;
3. POST `/ingest` with `source_status="LLM_OUTPUT"` and `claim_type="WORLD_FACT"` returns blocked/accepted false;
4. bulk import dry-run with LLM_OUTPUT world fact returns blocked verdict.

PR title:

```text
feat: enforce write-path TruthGate for fact ingestion
```

---

## Hard constraints

Do not add:

```text
NoeticCore
AttentionRouter
Research PWA
BICA runtime
Graphiti as mandatory backend
Titan console as Crystal production UI
verified-universal-graph claims
```

Do not combine tracks into one PR.
