# Privacy

Velantrim is **local-first and private by design**. This document states plainly
what data is stored, where it lives, and what (if anything) leaves your device.
For the legal mapping to EU data-protection law, see [GDPR.md](./GDPR.md).

## TL;DR

- **Everything runs on your machine by default.** No accounts, no cloud, no
  telemetry, no analytics, no phone-home.
- **No outbound network calls** in the default configuration. The only ways
  data can leave the device are *optional, opt-in* backends you enable yourself
  (see "Optional backends" below).
- **You own the store.** All data lives in a local SQLite file plus an embedded
  graph; delete the files and the data is gone.

## What data is stored

Velantrim stores **facts** that an AI system writes to memory. Each fact record
(`core/memory.py`) contains:

| Field | Purpose |
|-------|---------|
| `fact_id`, `claim` | The statement itself |
| `source`, `source_status` | Where it came from (user-reported / observed / derived / external / LLM-output / unknown) |
| `claim_type` | What kind of claim it is (world-fact / experience / emotion / opinion / preference / goal / interpretation) |
| `epistemic_state` | Verification status (Observed … Validated … Collapsed) |
| `confidence`, `significance` | Weighting used for decay/consolidation |
| `created_at`, `updated_at` | Timestamps |
| `metadata` | Free-form JSON you control |

If you store personal data inside `claim`/`metadata`, treat the store
accordingly — see [GDPR.md](./GDPR.md).

## Where data lives

- **L0** — in-memory LRU cache; exists only for the lifetime of the process.
- **L1** — local SQLite database at `./data/velantrim_memory.db` (WAL mode).
- **L3** — embedded canonical graph (in-memory `mock` by default; on-disk
  LadybugDB if you enable it via `VELANTRIM_L3_PATH`).

The `data/` directory and all `*.db` files are git-ignored and never leave the
repository or your machine on their own.

## What is collected and sent externally

**Nothing, by default.** Velantrim contains no telemetry, no usage analytics,
no crash reporting, and makes no network requests in its default configuration.

### Optional backends that extend the trust boundary

These are **off by default** and require explicit action to enable:

| Backend | What it does | Privacy implication |
|---------|--------------|---------------------|
| Claude generator (`core/generation.py`) | Generates answers via the Anthropic API | Requires installing `anthropic` **and** setting `ANTHROPIC_API_KEY`. When enabled, retrieved facts are sent to Anthropic. The default generator is **extractive and fully local**. |
| sentence-transformers embedder | Higher-quality local embeddings | Local model download on first use; no data sent at inference. The default embedder is a dependency-free local hash. |
| Neo4j L3 backend | External graph database | If pointed at a remote server, facts are stored there. The default (`mock`) and `ladybug` backends are local. |

If you enable the Claude generator, the data you send is subject to Anthropic's
privacy terms; Velantrim has no control over it. Choose local backends to keep
all processing on-device.

## Data subject rights (operational)

- **Access / portability** — `get_all_facts()` and the CLI `report` command
  export the full store; it is plain SQLite/JSON you can read directly.
- **Rectification** — `update_fact()` and the supersede flow in
  `core/reconcile.py` correct or replace facts.
- **Erasure** — facts can be logically collapsed (ESM `Collapsed` state).
  *Physical purge* of collapsed records is on the roadmap; until then, deleting
  the local `data/` files removes everything.

See [GDPR.md](./GDPR.md) for how these map to specific GDPR articles.

## Contact

Privacy questions: **qarythus@gmail.com**.
