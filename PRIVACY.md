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
accordingly — see [GDPR.md](./GDPR.md). You can additionally **encrypt these
fields at rest** by setting `VELANTRIM_ENCRYPTION_KEY` (see *Encryption at rest*
below).

## Where data lives

- **L0** — in-memory LRU cache; exists only for the lifetime of the process.
- **L1** — local SQLite database at `./data/velantrim_memory.db` (WAL mode;
  redirect with `VELANTRIM_DB`).
- **L3** — embedded canonical graph. The default `auto` mode tries LadybugDB if
  installed, then falls back to the dependency-free **on-disk SQLite** backend
  (path via `VELANTRIM_L3_PATH`, default `./data/velantrim_l3.db`), and uses
  the in-memory `mock` only as a last-resort/dev fallback if no persistent
  backend can open. In other words: by default the canonical graph **may be
  persisted on disk**, locally.

The `data/` directory and all `*.db` files are git-ignored and never leave the
repository or your machine on their own.

## Encryption at rest (optional)

Set `VELANTRIM_ENCRYPTION_KEY` (a passphrase or a Fernet key) to encrypt the
personal-data fields (`claim`, `metadata`) of the L1 SQLite store. The database
file then holds ciphertext for those fields; reads decrypt transparently. With
the optional `cryptography` package this uses Fernet (AES); otherwise a
dependency-free authenticated HMAC-SHA256 cipher. Off by default. See
[SECURITY.md](./SECURITY.md) and [GDPR.md](./GDPR.md) (Art. 32). On-disk L3
backends are not yet covered — use host disk encryption for those.

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

### Optional HTTP API and review UI

The opt-in FastAPI service (`pip install ".[api]"`) exposes stored claims —
including the pre-canonical review queue with sources, confidence and curator
decisions — over HTTP to whoever can reach the port. It binds to
`127.0.0.1` by default, and the `/review/*` endpoints support an opt-in Bearer
token guard (`VELANTRIM_API_TOKEN`, see [SECURITY.md](./SECURITY.md)). If you
bind it more widely, you are publishing local memory contents within whatever
network can reach that address — set the token and front it with TLS/auth
before doing so.

## Data subject rights (operational)

- **Access / portability** — `get_all_facts()` and the CLI `report` command
  export the full store; it is plain SQLite/JSON you can read directly.
- **Rectification** — `update_fact()` and the supersede flow in
  `core/reconcile.py` correct or replace facts.
- **Erasure** — `erase_fact()` (`core/erasure.py`, CLI `erase`) physically
  removes a fact from every layer (L0/L1/L3 + outbox) and records a content-free
  tombstone; `--cascade` also erases facts derived from it. Facts can also be
  logically collapsed (ESM `Collapsed`) when you want to retain a non-active
  record, and deleting the local `data/` files removes everything at once.
- **Restriction** — `restrict_processing()` / `unrestrict_processing()`
  (`core/compliance.py`, CLI `restrict` / `unrestrict`) reversibly excludes a
  fact from recall and answers without deleting it.
- **Record of processing** — `record_of_processing()` (CLI `ropa`) exports an
  aggregate, content-free overview of what is stored and how.

See [GDPR.md](./GDPR.md) for how these map to specific GDPR articles.

## Contact

Privacy questions: **qarythus@gmail.com**.
