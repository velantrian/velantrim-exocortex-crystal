# GDPR Alignment

Velantrim is designed as **GDPR-compliant memory infrastructure for Europe**.
This document maps the architecture to the relevant articles and principles of
Regulation (EU) 2016/679 (GDPR). It is an engineering self-assessment, not
legal advice — operators remain responsible for compliant deployment.

> **Key point:** Velantrim is a **local-first library**, not a hosted service.
> In the default configuration the data controller is the operator running it
> on their own device; **no personal data is transmitted to Velantrim's authors
> or any third party** (see [PRIVACY.md](./PRIVACY.md)).

## Principles (Article 5)

| Principle | How Velantrim supports it |
|-----------|---------------------------|
| **Lawfulness, fairness, transparency** | Every fact carries explicit `source` and `source_status`; the provenance trace (`core/trace.py`) makes processing transparent and auditable. |
| **Purpose limitation** | `claim_type` records the nature/purpose of each stored claim; subjective claims are kept separate from world-facts. |
| **Data minimisation** | Stdlib-only local runtime; no telemetry, no analytics, no background collection. The store contains only facts the operator writes. Optional **PII redaction at ingest** (`core/pii.py`, `VELANTRIM_REDACT_PII`) strips emails/phones/cards/IPs/IBANs before storage (Art. 5(1)(c)). |
| **Accuracy** | The TruthGate, ESM verification states, and `reconcile.py` (supersede / contradict / find_conflicts) exist specifically to keep stored facts accurate and to flag conflicts. |
| **Storage limitation** | FSRS-style confidence decay (`core/consolidate.py`) and logical collapse support time-bounded retention. |
| **Integrity & confidentiality** | Single-entry TruthGate, Ring Zero immutability (I6), validated ESM transitions, and the self-healing L3 outbox. See [SECURITY.md](./SECURITY.md). |
| **Accountability** | Provenance trace + audit-oriented test suite (265 tests, 99% coverage) demonstrate and document processing. |

## Data subject rights (Chapter III)

| Right | Article | Status in Velantrim |
|-------|---------|---------------------|
| **Information / transparency** | 13–14 | ✅ Provenance & source status recorded per fact. |
| **Access** | 15 | ✅ `get_all_facts()` / CLI `report` export the full store (plain SQLite/JSON). |
| **Rectification** | 16 | ✅ `update_fact()` and supersede flow (`core/reconcile.py`). |
| **Erasure ("right to be forgotten")** | 17 | ✅ **Physical erasure** (`core/erasure.py`): `erase_fact()` removes the fact from L0, L1, the L3 canonical graph (node + all edges + mentions) and the outbox, then writes a content-free tombstone. CLI: `erase`. |
| **Restriction of processing** | 18 | ✅ `restrict_processing()` / `unrestrict_processing()` (`core/compliance.py`): a per-fact reversible flag that excludes the fact from recall/answers (`pipeline.retrieve`) without deleting it or changing its truth state. CLI: `restrict` / `unrestrict`. |
| **Data portability** | 20 | ✅ Export is standard SQLite + JSON, fully portable. |
| **Object** | 21 | 🟡 Operator-controlled; supported operationally via erasure/restriction. |

## Privacy by design and by default (Article 25)

- **Local-first**: no network listener and no outbound calls by default; personal
  data never leaves the device unless the operator opts into an external backend.
- **Provenance-first**: the system cannot store a fact without recording where it
  came from, satisfying transparency obligations at the data-structure level.
- **Least surprise**: optional backends that change the data-flow boundary
  (Claude generator, remote Neo4j) are **off by default** and documented in
  [PRIVACY.md](./PRIVACY.md).

## Records of processing & security (Articles 30, 32)

- ✅ **Record of processing** (`record_of_processing()` / CLI `ropa`): an
  aggregate, content-free RoPA — processing purpose, controller, data location,
  backends in use, international-transfer flag, category counts (by claim type /
  epistemic state / source status), restriction and erasure registers, and the
  security measures below. Contains **no claim text**.
- The provenance trace and in-process metrics (`core/metrics.py`,
  `core/observe.py`) provide additional raw material for the record.
- The **erasure log** (`erasure_log` table; `erasure_log()` / CLI `erasures`)
  is a content-free record of every Art. 17 deletion — `fact_id`, timestamp,
  reason, actor, and a SHA-256 hash of the erased claim — proving *what* and
  *when* was erased **without retaining the personal data itself**.
- ✅ **Tamper-evident audit log** (`core/audit.py`; CLI `audit` / `audit-verify`):
  an append-only hash chain of compliance events (erase / restrict / unrestrict).
  Each entry seals its content and links to the previous one, so any later edit,
  deletion or reordering is detectable by `verify_audit_log()` — demonstrating
  integrity and accountability (Art. 5(2)(f), Art. 5(2), Art. 24). Optional
  per-entry HMAC signing (`VELANTRIM_AUDIT_KEY`) makes it tamper-*proof* against
  anyone without the key.
- Security measures appropriate to a local single-user library are described in
  [SECURITY.md](./SECURITY.md). ✅ **Application-level encryption at rest**
  (`core/crypto.py`) encrypts the personal-data fields (claim, metadata) of the
  L1 SQLite store when `VELANTRIM_ENCRYPTION_KEY` is set — authenticated
  encryption (Fernet/AES when `cryptography` is installed, otherwise a
  dependency-free HMAC-SHA256 backend). Host full-disk/filesystem encryption is
  still recommended for on-disk L3 backends.

## International transfers (Chapter V)

In the default local configuration there are **no transfers**. Enabling the
optional Claude generator transmits processed facts to Anthropic and is the
operator's decision and responsibility; use a local backend to avoid any
transfer.

## Roadmap to fuller compliance

These are explicit, fundable deliverables (see [ROADMAP.md](./ROADMAP.md)):

1. ✅ **Physical erasure** with content-free tombstoning (Art. 17) —
   `core/erasure.py`, with **cascade erasure** of derived facts (`DERIVED_FROM`).
2. ✅ **Per-fact processing-restriction** (Art. 18) — `core/compliance.py`.
3. ✅ **Exportable record-of-processing** (Art. 30) — `record_of_processing()`.
4. ✅ **Application-level encryption at rest** (Art. 32) — `core/crypto.py`.
5. ✅ **Signed / tamper-evident audit log** (Art. 5(2)/24/30) — `core/audit.py`.

## Contact

Data-protection questions: **qarythus@gmail.com**.

*This assessment reflects the codebase as of 2026 and is maintained alongside it.*
