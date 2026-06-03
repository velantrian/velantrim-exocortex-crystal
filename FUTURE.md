# Velantrim ExoCortex — Future Work & Research

This document captures **deferred improvements** and **research directions** that
came out of the code audit. It is intentionally honest: each item explains *why*
it matters and *where* in the code it bites, so future work starts from facts,
not vibes.

It is split into three parts:

1. **Done in the audit** — what was just fixed (for the record).
2. **Engineering improvements** — concrete, near-term, low-research hardening.
3. **Research directions** — bigger, open-ended bets from the hybrid vision.

---

## 1. Done in the audit (✅ shipped on `claude/code-audit-review`)

These were genuine bugs, not future work — listed so the history is clear.

- **Recall no longer erodes canonical confidence.** `build_facts_pack` used to
  write the retrieval rank (`sim × confidence`) into the fact's `confidence`
  field, which then flowed into the L3 canon via `merge_fact`. Every recall
  shrank the node's stored confidence (since `sim ≤ 1`). Fixed by keeping
  `confidence` (epistemic certainty) and `_score` (relevance rank) on separate
  axes; only the persistent record reaches the canon (`pipeline._l3_payload`).
- **SleepCycle now decays facts from the ingest/run path.** Previously the
  pipeline merged a bare in-memory fact with no `created_at`/`metadata`, so
  `consolidate()` found no baseline timestamp and skipped the node forever
  (decay only ran after a `reconcile` touch). Fixed by merging the persistent
  L0/L1 record (`pipeline._l3_payload`), used by both `run()` and `ingest()`.
- Regression coverage: `tests/test_audit_regressions.py`.
- Removed a build-artifact trigger file and un-tracked generated JSON reports
  that were both committed and `.gitignore`d; collapsed the duplicate
  `get_full_status`/`get_full_stats` alias.

---

## 2. Engineering improvements (near-term hardening)

### 2.1 Single source of version truth
**Why:** versions disagree across the repo — `pyproject.toml` says `0.1.0-mvp`,
`README.md` says `v8.1.0-hybrid`, module headers say `v8.7.0`/`v8.9.0`. A reader
can't tell what they're running.
**Do:** keep the version only in `pyproject.toml`; derive it at runtime
(`importlib.metadata.version`) and reference it from the README. Drop the
per-file `vX.Y.Z` header comments (they rot on every edit).

### 2.2 Embedder-mismatch guard on a persistent L3 store
**Why:** `core/embedding.py:16` already warns that hashing vectors and sbert
vectors are not cosine-comparable. On a persistent LadybugDB/Neo4j store, mixing
embedders silently corrupts `vector_search` ranking — the hardest class of bug
to notice (results just get subtly worse).
**Do:** stamp the embedder id/dim on each node (or a store-level metadata row)
and refuse (or warn loudly) when the active embedder differs at query time.

### 2.3 `created_at` as a first-class Ladybug column (nicety) — functional gap CLOSED ✅
**Status:** the SleepCycle decay is now backend-agnostic. `consolidate()`
self-heals a node with no baseline timestamp (e.g. LadybugDB, whose `_COLS`
whitelist drops `created_at`) by starting its decay clock in `metadata`
(persisted by every backend) on first sight, instead of skipping it forever.
See `core/consolidate.py` + `tests/test_consolidate.py::
test_consolidate_starts_clock_for_baseline_less_node`.
**Remaining (optional):** add `created_at`/`updated_at` to
`LadybugL3Graph._COLS` (`core/l3_graph.py`) + the schema DDL so the timestamp is
directly queryable on Ladybug for observability — not required for correctness
anymore. Untestable in CI (LadybugDB is an opt-in dependency), so deferred.

### 2.4 L3 ↔ SQLite transactionality (outbox)
**Why:** `pipeline.run()` already documents (lines ~470) that the canon (L3) and
the pending store (SQLite) share no transaction; a failed L3 merge leaves a
Validated SQLite fact with no graph node. Today this is patched by "MERGE is
idempotent, re-run re-merges" — fine for a sync MVP, fragile under crashes.
**Do:** a small outbox table (pending L3 writes) drained idempotently on
startup / next request, so partial state self-heals without manual re-runs.

### 2.5 Don't leak the internal `_score` in public results
**Why:** `generate_answer` returns `facts` that now carry the transient `_score`
rank. Harmless but leaky — consumers shouldn't depend on an internal field.
**Do:** strip `_`-prefixed keys when shaping the public result (the Neo4j
backend's `_props` already does this for nodes — make it a shared helper).

### 2.6 CI should mirror the local quality gate
**Why:** `pyproject.toml` enforces `--cov-fail-under=95`, but `.github/workflows/ci.yml`
runs plain `pytest tests/ -v`. The optional backends (LadybugDB, sbert, Neo4j,
Anthropic) are excluded only via `# pragma: no cover`, which is brittle — a real
gap in a non-pragma path could slip if coverage isn't actually gated in CI.
**Do:** run the same `pytest` invocation in CI (coverage gate included), and add
an optional matrix leg that installs the extras to exercise the real backends.

### 2.7 Relocate the spec/metadata tooling
**Why:** `audit_metadata.py`, `check_rfc_duplicates.py`, `fill_dependencies.py`,
`velantrim_migrate_v3_1.py` (~670 lines) operate on the JSONL spec, not the
runtime memory system. They sit in the repo root next to `core/`, blurring
"the product" vs "the spec toolchain", and the ~1.9 MB spec files
(`Velantrim_V8_Crystal_Sprint1.jsonl` + `_toc.md`) bloat every clone.
**Do:** move the tooling under `tools/` and the large spec artifacts to Git LFS
or a release asset.

### 2.8 Thread-safety when the pipeline goes async
**Why:** `core/metrics.py` and the module-level singletons (`BackendRegistry`,
L0 LRU `OrderedDict`) assume a single synchronous caller. The ROADMAP already
plans an async pipeline + Redis queue (S2 remainder).
**Do:** revisit the counters and caches for concurrency before async lands
(atomic counters / per-request scoping).

---

## 3. Research directions (hybrid vision, open-ended)

These map to the biological RFCs in the README/ROADMAP. They are **research**,
not scheduled engineering — each needs a design spike before code.

### 3.1 Automatic contradiction detection (Immune / CRISPR — RFC0072)
**Today:** `reconcile.find_conflicts` only surfaces *candidates* (semantically
close WORLD_FACTs) and deliberately never auto-acts — embedding proximity can't
tell "refinement" from "contradiction". `immune_crispr_memory_guard.py` is a
substring-match prototype, not wired into the pipeline.
**Research:** a lightweight NLI step (entailment / contradiction / neutral) over
candidate pairs to drive `supersede()` vs `contradict()` automatically, with a
human-review fallback above an uncertainty band. Open question: how to keep
false-positive contradictions from poisoning the canon.

### 3.2 Graph-walk retrieval beyond 1–2 hops (HippoRAG-style)
**Today:** `pipeline.retrieve` does a personalized-PageRank-lite spread over
`Validated` neighbors with a fixed 2-hop depth and 0.5 damping. It's a good
seed but untuned.
**Research:** evaluate spreading-activation depth/damping against a retrieval
benchmark; consider edge-type-weighted walks (an `CONTRADICTS` edge should not
spread activation the way a `CO_OCCURRED` edge does).

### 3.3 Integrate (or retire) the biological prototypes
**Today:** only the epigenetic module is wired (`core/adaptation.py`). The
fractal (`prototypes/fractal_memory_layer.py`), neurogenesis
(`prototypes/neurogenesis_dynamic_growth.py`) and immune
(`prototypes/immune_crispr_memory_guard.py`) modules are standalone prototypes
with `print()`-style demos — tested in isolation, but the core pipeline never
calls them. They now live under `prototypes/` (moved out of the repo root) so
the layering is explicit: `prototypes/` may depend on `core/`, never the
reverse.
**Research:** decide per module — wire it into the pipeline with a real
contract (like adaptation was), or keep it as an explicit prototype. Concretely:
- **Fractal (RFC0070):** what does multi-scale anchoring buy retrieval that the
  significance-weighted `vector_search` doesn't already approximate?
- **Neurogenesis (RFC0073):** map "new neurons" onto a concrete capacity/
  plasticity policy for L0/L3, or it stays a metaphor.

### 3.4 Concept emergence & analogy (RFC0066 / RFC0067)
**Today:** designed in the spec, not coded (ROADMAP S3/S4).
**Research:** Hebbian co-activation → ProtoConcepts from the `CO_OCCURRED`
episodic edges already being written by `_link_episode`; an analogy graph /
semantic-bridge engine on top of the canonical graph.

### 3.5 Real consolidation policy (FSRS, not just exponential decay)
**Today:** `consolidate()` is a clean exponential half-life weighted by
significance — a stand-in for the full FSRS-style scheduler named in the
ROADMAP.
**Research:** a proper spaced-repetition model with retrievability/stability
state per fact, and a `mature_neurons`-style stability-grows-with-recall loop.

---

> **Principle for everything above:** Graph = Truth. Any new path into the canon
> goes through TruthGate; any new behavior is testable and degrades to a
> dependency-free default. No silent corruption of stored truth.
