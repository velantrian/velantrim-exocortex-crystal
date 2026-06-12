# Reviewer Notes — Velantrim Crystal

Velantrim Crystal is a local-first, AGPL-licensed memory core for AI systems. It
is not a chatbot and not a hosted SaaS product. Its purpose is to make AI memory
inspectable, source-tracked, replayable, erasable and harder to corrupt silently.

## One-minute summary

Modern AI systems often treat memory as an opaque vector store, a hidden vendor
profile or a long prompt. That makes it difficult to know where a remembered fact
came from, whether it was user-reported, model-generated or externally sourced,
and whether it can be restricted or erased.

Crystal provides a small verifiable memory substrate underneath AI systems:

```text
input / file / agent event
  -> claim extraction and classification
  -> Guardian + TruthGate
  -> local L0/L1 working memory
  -> local L3 canonical graph
  -> retrieval / FactsPack
  -> traceable answer / receipt
```

The LLM is optional. It may phrase the final answer, but the source of truth is
the local graph plus provenance, not model confidence.

## What is implemented today

- Local L0/L1 memory using SQLite/WAL.
- L3 canonical graph adapter with dependency-free SQLite and mock backends, plus
  optional LadybugDB and Neo4j backends.
- Type-aware memory metadata: `claim_type`, `source_status`, epistemic state,
  confidence and significance.
- Guardian + TruthGate path before canonical promotion.
- Trace chains and replayable receipts.
- Evidence span store baseline and Receipt v2 baseline.
- External knowledge ingestion for `.txt`, `.md`, `.json`, `.jsonl`, `.ndjson`
  and `.csv`.
- Import dry-run/session tooling for safer corpus ingestion.
- GDPR-relevant controls: erasure, processing restriction, record of processing,
  tamper-evident audit log, opt-in field-level encryption and PII redaction.
- Read-only MCP server for agent inspection without canonical write access.
- Baseline evaluation harness (`velantrim eval`).
- A fully passing test suite at 100% coverage with a 100% gate (current
  audited baseline in `TEST_REPORT.md`).

## Why this is public-interest infrastructure

Crystal is designed for individuals, schools, libraries, archives, research
teams, small organisations and public-sector users who need AI memory without a
mandatory cloud service or hidden data processor. The default path has no
telemetry and no outbound network calls. Data lives in local files controlled by
the operator.

The project is especially relevant where the reviewer needs to inspect:

- where a remembered fact came from;
- whether the claim is a world fact, opinion, emotion, preference or goal;
- whether a fact can be restricted or physically erased;
- whether an answer can be replayed against the facts that supported it;
- whether an external LLM is optional rather than mandatory.

## How to reproduce the audited state

From a clean clone, with no hidden local state:

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest -q                                    # full suite, 100% gate
python scripts/eval_gate.py --out-dir eval-artifacts   # CI-gated evaluation
git status --short                                     # stays clean
```

Expected: tests pass at the baseline in `TEST_REPORT.md`, the eval gate prints
`PASSED`, and the working tree stays clean (generated artifacts land in the
ignored `eval-artifacts/`).

## How to run a minimal local demo

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install .

velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave at sea level"
velantrim receipt "how does water behave at sea level" > receipt.json
velantrim verify-receipt receipt.json
```

For a dependency-free persistent canon:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "what is stored in memory?"
```

## What grant funding should extend

The strongest grant-scope extensions are:

1. Production-strength evidence spans: line/section/character offsets for PDFs,
   Markdown and imported corpora, with snippet replay.
2. A full L2 curator review queue for observed, low-confidence, quarantined or
   conflicting claims before canonical promotion.
3. Larger evaluation fixtures and release artifacts: `metrics.jsonl`,
   `eval_report.md`, curated retrieval/contradiction/source-span corpora and CI
   regression gates.
4. More institutional adapters: PDF, YAML, RDF/Wikidata and source/licence
   metadata capture.
5. Documentation and demonstrators for local/offline operation and public-sector
   data-sovereignty use cases.

## Explicit non-goals

Crystal does not claim:

- consciousness;
- artificial personhood;
- human-level intelligence;
- zero hallucinations;
- universal truth detection;
- legal certification of GDPR compliance;
- production multi-tenant hosting without a dedicated authentication and access
  control layer.

The measurable goal is narrower: make AI memory local, auditable, replayable,
source-aware and harder to corrupt silently.

## Reviewer checklist

A reviewer can evaluate the project by checking:

- `docs/REVIEWER_OVERVIEW.md` for the one-page reviewer-facing summary
  (problem, solution, invariants, status, roadmap, non-goals);
- `README.md` for positioning and quick start;
- `docs/ARCHITECTURE.md` for the memory and truth boundary;
- `docs/IMPLEMENTATION_STATUS.md` for the honest implemented-vs-RFC-vs-vision
  status map (Crystal core vs full Exo-Cortex vs Velantrim Culture);
- `docs/GRANT_NLNET_SCOPE.md` for work packages;
- `DEMO.md` for the ingest -> trace -> receipt flow;
- `TEST_REPORT.md` and CI for reproducibility;
- `GDPR.md`, `PRIVACY.md` and `SECURITY.md` for privacy/security boundaries;
- `docs/EVAL.md` for baseline metrics and planned evaluation extensions;
- `docs/RFC_HARNESS_REPLAY_OPTIMIZATION.md` for the future (RFC-only, not
  implemented) auditable trajectory-replay / harness-optimization design
  with a mandatory human approval loop.

Review provenance note: automated Codex code review was unavailable for
PR #93–#98 due to usage limits; those changes were manually audited and
CI-gated (full test suite, coverage gate and eval gate on every merge).
