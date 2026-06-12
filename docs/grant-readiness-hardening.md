# Grant Readiness Hardening

This document explains the quality and validation layer added to the Velantrim Crystal repository as part of grant-readiness preparation.

## Why metadata validation exists

Every fact stored in Velantrim carries `claim_type`, `source_status`, `truth_status`, `epistemic_state`, `confidence` and provenance fields. These are not decorative: the pipeline uses them to decide whether a fact is eligible to answer a query.

A fact without `source_status` cannot be routed to the correct `truth_status` by TruthGate. A fact without `epistemic_state` cannot be filtered for the `Validated` / `Supported` grounding gate that blocks answer generation when evidence is insufficient. A fact without `confidence` cannot be ranked during retrieval.

The JSON schemas in `schemas/` pin the canonical **enum values** for these fields as they exist in the codebase (`core/memory.py`). They serve as machine-readable documentation and allow external tools to validate exported or imported data without reading the Python source. Structurally, the schemas were aligned with the actual runtime artifacts in the T2 schema pass: `trace.schema.json` describes the trace items and sealed receipts the runtime really emits, while `metadata.schema.json` is explicitly labeled a **target** provenance envelope (current-vs-target fields are marked in the schema descriptions, and reserved fields such as `guardian_verified` are labeled as not yet emitted by the runtime).

## Why JSONL validation exists

Knowledge corpora are stored as JSONL (one JSON object per line). Silent corruption — a missing field, a truncated line, a duplicated chunk ID — can cause retrieval to silently degrade rather than fail visibly. The CI `jsonl-integrity` job validates every line of the primary corpus on every push:

- valid JSON parse
- required fields present (`chunk_id`, `title`, `content`)
- no duplicate `chunk_id` values

Run locally:

```bash
python -c "
import json, sys
REQUIRED = ['chunk_id', 'title', 'content']
path = 'docs/Velantrim_V8_Crystal_Sprint1.jsonl'
errors, seen = [], {}
with open(path) as f:
    for i, line in enumerate(f, 1):
        if not line.strip(): continue
        try: obj = json.loads(line)
        except Exception as e: errors.append(f'Line {i}: {e}'); continue
        for field in REQUIRED:
            if not obj.get(field): errors.append(f'Line {i}: missing {field}')
        cid = obj.get('chunk_id')
        if cid in seen: errors.append(f'Line {i}: duplicate chunk_id {cid}')
        elif cid: seen[cid] = i
if errors: [print(e) for e in errors]; sys.exit(1)
print(f'OK — {len(seen)} chunks')
"
```

## Why source_ref and trace_id are mandatory (provenance metadata)

Velantrim Crystal issues replayable receipts for every answered query. A receipt is only useful if it can be traced back to:

1. the facts that grounded the answer (`trace_id`);
2. the document or session that contributed those facts (`source_ref`).

Without `source_ref`, an auditor cannot verify where a claim came from. Without `trace_id`, the receipt cannot be replayed to confirm that the answer was derived from stored facts rather than hallucinated. The `metadata.schema.json` therefore marks both fields as required.

## How this supports trustworthy AI memory

The architecture enforces a strict flow:

```
ingest → TruthGate → L3 canonical graph → retrieval → grounding → answer → receipt
```

Every stage leaves a traceable artefact:

- `source_status` records how a claim entered the system.
- `truth_status` records what TruthGate decided.
- `epistemic_state` records the current validation level.
- The trace receipt records which facts grounded each answer.

The schemas make this flow auditable by an external reviewer without running the system: they can check that exported facts conform to the expected structure and that no `LLM_OUTPUT` claim was promoted to `VERIFIED` without human or external-source evidence.

## How to run validation locally

```bash
# Install test dependencies
pip install -r requirements-dev.txt
pip install -e .

# Run the full test suite with coverage gate (100%)
pytest tests/ --cov=. --cov-fail-under=100

# Run security lint
bandit -r core/ -ll -q

# Run dependency audit
pip-audit --ignore-vuln PYSEC-2022-42969
```

## How to add new regression cases

1. Add a test file in `tests/` using the existing pytest fixtures in `tests/conftest.py`.
2. Use the `isolated_db` autouse fixture — it gives every test its own SQLite file and a clean module state.
3. Set `VELANTRIM_DEMO_SEED=1` if your test needs the seed corpus, or leave it at the default `0` to start from an empty graph.
4. Pin the deterministic backends (already done by `conftest.py`): `VELANTRIM_EMBEDDER=hashing`, `VELANTRIM_GENERATOR=extractive`, `VELANTRIM_L3_BACKEND=mock`.
5. Run `pytest tests/your_test.py -v` before pushing.

## Canonical enum values

These values are defined in `core/memory.py` (`claim_type` and `source_status` are enforced at every `store_fact` call; `truth_status` is assigned by the pipeline's source-aware mapping, never set directly by the caller). The schemas in `schemas/` use exactly these enum values — no aliases, no abbreviations. In particular, `FACT` is a human-facing alias only: the machine `truth_status` value is `VERIFIED`.

### epistemic_state (ESM)

| Value | Meaning |
|---|---|
| `Observed` | Raw input, not yet classified |
| `Hypothesized` | Accepted, not yet confirmed |
| `Supported` | Evidence exists |
| `Validated` | Verified by TruthGate — eligible to ground answers |
| `Contradicted` | Conflicts with another fact |
| `Deprecated` | Obsolete |
| `Collapsed` | Logically removed |
| `ImmutableCore` | Ring Zero — cannot be transitioned |

### claim_type

`WORLD_FACT` · `USER_EXPERIENCE` · `EMOTION` · `INTERPRETATION` · `OPINION` · `GOAL` · `PREFERENCE`

### source_status

`EXTERNAL` · `USER_REPORTED` · `DERIVED` · `OBSERVED` · `LLM_OUTPUT` · `UNKNOWN`

### truth_status (assigned by TruthGate)

| Value | When assigned |
|---|---|
| `VERIFIED` | WORLD_FACT + EXTERNAL/DERIVED/OBSERVED source |
| `USER_CLAIMED` | WORLD_FACT + USER_REPORTED source |
| `UNVERIFIED` | WORLD_FACT + LLM_OUTPUT or UNKNOWN source |
| `HYPOTHESIS` | INTERPRETATION claim type |
| `SUBJECTIVE` | All other subjective claim types |
