# 🗺️ Crystal Documentation Map

**Status date:** 2026-08-14  
**Purpose:** route humans, AI agents and auditors to the right representation of the same project truth.

GitHub merged `main` + executable tests + exact CI remain implementation truth. This map explains **where to read**, not what to trust over live evidence.

## 🧬 One project truth, four interfaces

```text
                     ONE PROJECT TRUTH
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     👤 HUMAN VIEW      🤖 AI VIEW       ⚙ MACHINE VIEW
       README             docs/ai          manifest
       OVERVIEW
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                            ▼
                       🧾 EVIDENCE
              STATUS · TEST_REPORT · CI · eval
```

These are presentation interfaces, not separate sources of truth.

---

## 👤 Human path

Use this path to understand the project before reading internal evidence ledgers.

1. [`../README.md`](../README.md) — short human landing page; architecture in one view, project tree, current-state table, non-claims and navigation.
2. [`OVERVIEW.md`](./OVERVIEW.md) — deep human system overview; concepts, mindmap, authority model, examples and dated external comparison.
3. [`ARCHITECTURE_OVERVIEW.md`](./ARCHITECTURE_OVERVIEW.md) — tighter technical architecture entry point.
4. [`ARCHITECTURE.md`](./ARCHITECTURE.md) — full architecture contracts.

Human-readable diagrams explain the system; they do not override machine flags or evidence.

---

## 🤖 AI / agent path

Start at [`ai/README.md`](./ai/README.md) — **Special for AI**.

Required orientation then routes through:

- [`../AGENTS.md`](../AGENTS.md)
- [`status/implementation-manifest.json`](./status/implementation-manifest.json)
- [`STATUS.md`](./STATUS.md)
- [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md)
- [`ai/CURRENT_STATE.md`](./ai/CURRENT_STATE.md)
- [`ai/COMPONENT_MAP.md`](./ai/COMPONENT_MAP.md)
- [`ai/KNOWN_RISKS.md`](./ai/KNOWN_RISKS.md)
- relevant architecture, tests, exact CI and evaluation artifacts

The AI entry point contains the exact authority hierarchy, forbidden inferences, change classification and stop boundaries.

---

## ⚙ Machine-readable truth

Primary machine surface:

- [`status/implementation-manifest.json`](./status/implementation-manifest.json)

Use it for capability flags, authorization state, architecture checkpoint identity, grant flags and retained runtime checkpoints.

Machine-readable fields must not be inferred from emojis, diagrams, narrative summaries or external comparisons.

---

## 🧾 Current state and evidence

- [`STATUS.md`](./STATUS.md) — current public implementation/evidence state.
- [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) — detailed capability and non-implementation matrix.
- [`../TEST_REPORT.md`](../TEST_REPORT.md) — verification evidence and checkpoint interpretation.
- [`../eval/`](../eval/) — frozen evaluation surfaces, preregistrations and results.
- GitHub exact CI / signed commits — live evidence when validating a checkpoint.

Historical SHA/CI evidence belongs here or in owning architecture/history surfaces, not at the top of the human README unless it is necessary to explain current meaning.

---

## 📖 Reader architecture

Current Reader position:

```text
RC-1…RC-7     implemented bounded layers
RC-8          architecture/research decision
RC-9          implemented deterministic lexical PRE-ADMISSION discovery
Comparator v1 frozen evaluation / discrimination gate FAIL
NLI v1        frozen evaluation / recall-safety gate FAIL
RRTIC-v1      frozen typed inspection architecture contract
semantic/hybrid Reader runtime  NOT AUTHORIZED
dedicated_reader_core=false
```

Key documents:

- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [RC-7 cross-document contract](./architecture/READER_RC7_CROSS_DOCUMENT.md)
- [RC-8 retrieval decision](./architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline](./architecture/READER_RC9_LEXICAL_BASELINE.md)
- [RRTIC-v1 typed inspection contract](./architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md)

```text
retrieval match          != evidence
similarity               != identity
candidate discovery      != candidate adjudication
evaluation pass          != runtime authorization
```

---

## 🛡 Reviewer / safety / privacy — D2

D2 uses the stable English Reviewer Guide and safety/privacy/failure source contract. This documentation-architecture milestone does not change D2 reviewer procedure semantics, so existing D2 translation status remains governed by its recorded contract rather than by the new human README layout.

- [Reviewer Guide](./REVIEWER_GUIDE.md)
- [Reviewer Overview](./REVIEWER_OVERVIEW.md)
- [Safety, privacy and failures](./SAFETY_PRIVACY_AND_FAILURES.md)
- [Privacy](../PRIVACY.md)
- [Security](../SECURITY.md)

Review/safety documents define validation and risk boundaries. They are not substitutes for exact CI when a claim depends on a specific commit.

---

## 🗄 Storage / authority

- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [SQLite storage lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)

Ordinary storage truth remains local-first SQLite. PostgreSQL/pgvector is not an active Reader backend and remains `active=false` where documented.

---

## 🎓 Grant / governance — D4

Grant truth remains **submitted / under review / not awarded**; approximate €50,000 remains planning context only.

- [Project, grant and governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Roadmap](../ROADMAP.md)
- [Glossary](./GLOSSARY.md)

Existing pre-agreement work must not be relabeled as newly funded delivery.

---

## 🌍 Localization / reference — D5

- [Localization policy](./LOCALIZATION_POLICY.md)
- [Translation status](./TRANSLATION_STATUS.md)
- [Extended reference policy](./EXTENDED_REFERENCE_POLICY.md)
- [D5 inventory](./status/d5-inventory.json)

English is the primary source language. Localized documents remain valid only to their recorded source checkpoints.

The historical Spanish root README is a useful example of human-first visual organization, but it is **not** the source of current RRTIC-era technical truth. Layout ideas may be reused; stale implementation claims may not.

This Human / AI / Machine documentation architecture milestone does not perform a broad translation refresh.

---

## 🔄 Maintenance rule

When documentation changes, classify the change first:

```text
STRUCTURAL_CHANGE → refresh affected human + AI + machine/evidence representations
STATE_CHANGE      → remove stale current-state claims from affected top surfaces
EVIDENCE_ONLY     → update evidence/checkpoints; preserve still-correct conceptual visuals
```

Always preserve the separation:

```text
overview != current state != machine truth != evidence != history
```
