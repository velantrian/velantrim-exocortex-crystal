# Velantrim Crystal — Hands-on Demo Walkthrough

A reproducible, ~5-minute tour of the verifiable memory core, using **only the
CLI** and the **dependency-free runtime** (no LLM, no cloud, no native deps).
Every command and every block of output below was captured from an actual run —
nothing here is mocked.

> **Companion docs:** [`ARCHITECTURE.md`](ARCHITECTURE.md) (how it works),
> [`COMPARISON.md`](COMPARISON.md) (vs vector-only memory),
> [`GRANT_NLNET_SCOPE.md`](GRANT_NLNET_SCOPE.md) (work packages). This file is the
> WP5 grant-facing demonstrator.

---

## 0. Setup

```bash
pip install .                 # exposes the `velantrim` console script; zero mandatory deps
# isolate this demo in a scratch directory so it never touches real data:
export VELANTRIM_L3_PATH=/tmp/velantrim_demo/l3.db
export VELANTRIM_DB=/tmp/velantrim_demo/l1.db
export VELANTRIM_DEMO_SEED=0   # start from an EMPTY canon (production default)
```

On a stdlib-only machine the core announces its dependency-free fallbacks on
first use and keeps working — no install failure, no network:

```
auto L3: LadybugDB unavailable (ImportError), falling back to on-disk SQLite
auto embedder: sbert unavailable (ImportError), falling back to HashingEmbedder
```

---

## 1. Ingest a fact, then ask — a grounded answer **without an LLM**

```bash
velantrim ingest "The Eiffel Tower is in Paris."
```
```json
{"accepted": true, "reinforced": false, "fact_id": "ing:fe37d9fe9778",
 "claim_type": "WORLD_FACT", "truth_status": "USER_CLAIMED", "conflicts": []}
```

```bash
velantrim ask "Where is the Eiffel Tower?"
```
```
The Eiffel Tower is in Paris.
```

The answer comes from the stored fact via extractive retrieval — **no model was
called**. The fact was classified (`WORLD_FACT`), gated, and given an epistemic
state. `velantrim report` confirms the canon:

```
MEMORY REPORT (L3 canonical graph)
  facts: 1  avg_confidence=0.6  avg_significance=0.5
  epistemic_state: {'Validated': 1}
  claim_type:      {'WORLD_FACT': 1}
  truth_status:    {'USER_CLAIMED': 1}
```

---

## 2. Provenance receipt — and replay it against the canon

A receipt seals the answer, the query and every cited fact under a digest:

```bash
velantrim receipt "Where is the Eiffel Tower?" > receipt.json
# top-level keys: version, created_at, query, answer, citations, digest
```

Later — or on another machine — replay it to prove the answer is still grounded:

```bash
velantrim verify-receipt receipt.json
```
```json
{"digest_valid": true, "signature_valid": null,
 "citations": [{"fact_id": "ing:fe37d9fe9778", "status": "ok"}],
 "summary": {"ok": 1}, "verified": true}
```

If a cited fact is later **erased, restricted, modified or contradicted**, replay
reports the drift instead of silently returning a stale answer.

---

## 3. Contradiction detection — deterministic, dependency-free

Ingest `"Water boils at 100 degrees Celsius."`, then check conflicting claims.
The classifier surfaces candidates with the **signal** that triggered them:

```bash
velantrim conflicts "Water does not boil at 100 degrees Celsius."
```
```json
[{"fact_id": "ing:75c4502b0159", "claim": "Water boils at 100 degrees Celsius.",
  "similarity": 0.730, "kind": "CONTRADICTION", "signal": "negation"}]
```

```bash
velantrim conflicts "Water boils at 90 degrees Celsius."
```
```json
[{"fact_id": "ing:75c4502b0159", "claim": "Water boils at 100 degrees Celsius.",
  "similarity": 0.800, "kind": "CONTRADICTION", "signal": "numeric"}]
```

Negation and numeric mismatch are caught behind a same-subject gate — no model,
no probabilities, fully explainable.

---

## 4. Import a knowledge file through the same TruthGate

External knowledge takes the **same** validation path as a typed utterance:

```bash
printf "Marie Curie won two Nobel Prizes.\nThe speed of light is about 299792 km per second.\n" > facts.txt
velantrim learn facts.txt
```
```json
{"source": "facts.txt", "total": 2, "accepted": 2, "reinforced": 0,
 "blocked": 0, "fact_ids": ["ing:af20e9ec3a6a", "ing:04f2222a9adf"],
 "session_id": "imp:3553e9de027e"}
```

Imported facts auto-attach **source-span evidence** (content-light hashes, so the
provenance record carries no payload):

```bash
velantrim evidence ing:af20e9ec3a6a
```
```json
[{"evidence_id": "ev:00dd2518b07c", "fact_id": "ing:af20e9ec3a6a",
  "source_uri": "facts.txt", "source_kind": "file",
  "source_sha256": "d3a60f46…", "claim_sha256": "60747e26…"}]
```

The `session_id` lets a whole import be reviewed, restricted or erased as a batch
(`import-session` / `session-restrict` / `session-erase`).

---

## 5. GDPR in practice — erase + tamper-evident audit

Right to erasure (Art. 17) purges a fact across L0/L1/L3 and the outbox, leaving a
**content-free tombstone**:

```bash
velantrim erase ing:fe37d9fe9778
```
```json
{"fact_id": "ing:fe37d9fe9778", "erased_now": true, "l1_removed": true,
 "l3_removed": true, "reason": "data_subject_request", "actor": "operator",
 "content_hash": "sha256:001835a0…", "erased_at": "2026-06-08T22:31:13Z"}
```

Every erase/restrict event lands in an **append-only hash chain** (Art. 5(2)/30):

```bash
velantrim audit          # → [{"seq":1,"event":"erase",...,"prev_hash":"000…","entry_hash":"f4be3e09…"}]
velantrim audit-verify
```
```json
{"ok": true, "length": 1, "broken_at": null, "verified": false, "signed": false}
```

`audit-verify` recomputes the chain; any tampering breaks it at `broken_at`.
(`signed/verified=false` simply means HMAC signing is off in this demo — it is
opt-in.) Related controls: `restrict`/`unrestrict` (Art. 18), `ropa` (Art. 30),
`redact` (PII), opt-in encryption at rest (Art. 32).

---

## 6. NeuroCore telemetry — the passive plasticity tracker, live

NeuroCore (RFC0068) is off by default. Enable it and the pipeline records a
**surprise tick per query** (surprise ≈ 1 − top retrieval relevance), writing
**only to its own log** — never to the canon (invariant I68):

```bash
VELANTRIM_NEUROCORE=1 velantrim ask "something never seen before xyz"   # cold-start: surprise = 1.0
VELANTRIM_NEUROCORE=1 velantrim neurocore-report
```
```json
{"enabled": true, "phase": 0, "theta": 0.6, "alpha": 0.01,
 "surprise_events": 1, "avg_delta_norm": 1.0, "max_delta_norm": 1.0,
 "by_domain": {"pipeline": 1}}
```

`by_domain: {"pipeline": 1}` confirms the tracker is wired into the live pipeline
and capturing real surprise data (including zero-hit cold-start queries).

---

## 7. Baseline evaluation harness — measurable, not narrative

```bash
velantrim eval
```
```json
{"cases": 4,
 "retrieval": {"hit@1": 1.0, "hit@3": 1.0, "hit@5": 1.0, "mrr": 1.0},
 "trace_completeness": 1.0, "metadata_completeness": 1.0,
 "source_span_coverage": 1.0, "unsupported_provenance": 0,
 "receipt_replay_survival": 1.0,
 "contradiction": {"pairs": 4, "tp": 2, "fp": 0, "fn": 0,
                   "precision": 1.0, "recall": 1.0, "false_positive_rate": 0.0}}
```

A deterministic report over retrieval, trace/metadata completeness, source-span
coverage, contradiction precision/recall and receipt-replay survival. Scaling
this to curated fixture corpora with CI quality gates is grant work package WP3.

---

## 8. Same operations over HTTP (optional FastAPI layer)

The HTTP layer is an **optional extra** (`pip install ".[api]"`); the default
runtime stays standard-library only. It exposes the same operations as the CLI —
no TruthGate-bypassing write path:

```bash
velantrim-api          # 127.0.0.1:8000 (VELANTRIM_API_HOST / VELANTRIM_API_PORT)
```

| Method | Path | Mirrors |
|---|---|---|
| `GET`  | `/health` | liveness/readiness |
| `POST` | `/ingest` | `velantrim ingest` |
| `POST` | `/ask` | `velantrim ask` (blocked → `200` + `answer:null`) |
| `GET`  | `/receipt?q=` | `velantrim receipt` (blocked → `422`) |
| `POST` | `/verify-receipt` | `velantrim verify-receipt` |
| `GET`  | `/evidence/{fact_id}` | `velantrim evidence` |

```bash
curl -s localhost:8000/ask -H 'content-type: application/json' \
     -d '{"query":"Where is the Eiffel Tower?"}'
# → {"answer":"The Eiffel Tower is in Paris.", ...}   (same grounding as §1)
```

---

## What this demo establishes

- **Truth-first:** every write passes Guardian + TruthGate; the LLM never becomes
  the source of truth.
- **Local-first & dependency-free:** the whole tour runs on the Python standard
  library, offline, with no cloud service.
- **Auditable:** answers carry replayable receipts; facts carry source-span
  evidence; deletions carry a tamper-evident hash chain.
- **Honest about scope:** the evaluation harness, span extraction and adapters
  have working baselines today and clearly-scoped extensions in the grant plan.

Reproduce everything above with the commands as written — same machine, no
network required.
