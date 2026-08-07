from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "f03e24c85922d0bb46d6d9dfee98338972135908"
SHORT = "f03e24c"
TREE = "abf75283b382697b323ab69cfa7235b47171dace"
HEAD = "17ce10ffe12da93be50434c73d08f05a70a5922b"
CI = 31224184351
BENCH = 31224005804
PR = 335
PASSED = 2059
SKIPPED = 12
STATEMENTS = 9361


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {text.count(old)}")
    return text.replace(old, new, 1)


# README: preserve the broad public overview; update only current evidence and storage truth.
readme = read("README.md")
readme = replace_once(
    readme,
    "`v0.3.0` · 🧪 **2047 passed / 12 skipped** · 🎯 **100.00% coverage**",
    "`v0.3.0` · 🧪 **2059 passed / 12 skipped** · 🎯 **100.00% coverage**",
    "README metrics",
)
readme = re.sub(
    r"\*\*Verified runtime checkpoint:\*\* `[^`]+` — merged PR #\d+\.  \n"
    r"\*\*Validated implementation head / CI:\*\* `[^`]+` / `\d+` — 9/9 successful\.",
    f"**Verified runtime checkpoint:** `{COMMIT}` — merged PR #{PR}.  \n"
    f"**Validated implementation head / CI:** `{HEAD}` / `{CI}` — 9/9 successful.",
    readme,
    count=1,
)
old_start = readme.index("PR #330 adds a canonical backend-neutral JSONL export")
old_end = readme.index("\n## 🛡️ Central non-claims", old_start)
storage = f"""PR #{PR} advances the canonical backend-neutral JSONL path to a bounded-streaming
implementation. Source rows are consumed in fixed cursor batches; canonical edge ordering
and referential checks use private disk-backed SQLite state; verification hashes and parses
from the same descriptor without retaining complete datasets or global identifier sets in
the production path.

The bundle remains operation evidence only: it is not claim evidence, TruthGate admission
or backend activation.

The merged implementation retains the explicit local-first resource envelope:

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| one canonical record | 1 MiB |
| records per dataset | 200,000 |
| one dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

Issue #331 is implemented by PR #{PR}. Reproducible local-first resource evidence is recorded
in [SQLite Logical Migration — Bounded Resource Evidence](./docs/benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md):
an approximately 8x synthetic corpus increase changed Python-traced peak from 1,338,163 to
1,339,001 bytes. This is not a production SLO or institution-scale certification.

Issue #332 tracks the separate future phase: optional inactive PostgreSQL/pgvector import
and exact-state equivalence. Cutover, rollback, dual-write and automatic backend switching
remain absent.
"""
readme = readme[:old_start] + storage.rstrip() + readme[old_end:]
write("README.md", readme)

write(
    "TEST_REPORT.md",
    f"""# Crystal Verification Report

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `{COMMIT}`  
**Verified tree:** `{TREE}`  
**Validated implementation head:** `{HEAD}`  
**Pull request:** #{PR}  
**Exact-head CI:** `{CI}`  
**Resource benchmark CI:** `{BENCH}`

This is evidence for the tested repository state. It is not a production, legal, security,
PostgreSQL-readiness or institution-scale certification.

## Result

| Gate | Result |
|---|---:|
| Python 3.11 | {PASSED} passed / {SKIPPED} skipped / 0 failed |
| Python 3.12 | {PASSED} passed / {SKIPPED} skipped / 0 failed |
| Measured statements | {STATEMENTS} |
| Line coverage | 100.00% |
| `core/storage_migration.py` | 626 / 626 statements |
| Ring Zero declared mutants | 7/7 killed |
| Permanent CI jobs | 9/9 successful |
| Resource benchmark jobs | 2/2 successful |

## Runtime delta verified in PR #{PR}

- fixed-batch SQLite cursor iteration;
- incremental canonical JSONL write, count and SHA-256;
- private disk-backed canonical edge sorting;
- same-descriptor hash-first and incremental parse verification;
- private disk-backed node/entity/reference checks;
- bounded dangling-reference diagnostics;
- temporary-disk preflight and handled-failure cleanup;
- preserved schema, vector, canonical-ordering, file-identity and TOCTOU checks.

## Resource evidence

Benchmark run `{BENCH}` compared 1,025 and 8,193 primary-record corpora.

| Metric | 1,025 records | 8,193 records |
|---|---:|---:|
| Source SQLite | 450,560 B | 3,141,632 B |
| Bundle | 360,629 B | 2,869,434 B |
| Export including internal verify | 0.649478 s | 5.424900 s |
| Second independent verify | 0.361907 s | 3.131820 s |
| Python traced peak | 1,338,163 B | 1,339,001 B |
| Linux process max RSS | 23,324 KiB | 25,600 KiB |

See [the full resource report](./docs/benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md).
These measurements support bounded behavior for the tested synthetic local-first corpora;
they are not a production SLO or proof for every payload shape or maximum accepted bundle.

## Active fail-closed limits

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| one canonical record | 1 MiB |
| records per dataset | 200,000 |
| one dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

## Authority and future-work boundary

```text
physical L3 state       != strict Canon
logical bundle          != claim evidence
successful verification != backend activation
bounded local migration != PostgreSQL runtime
benchmark result        != production SLO
```

Issue #331 is implemented by PR #{PR}. PostgreSQL/pgvector runtime, inactive target import,
exact target equivalence, cutover, rollback, dual-write and distributed fencing remain
absent. Issue #332 governs only the next inactive-import/equivalence phase.

## Reproduction

```bash
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
bash scripts/storage_migration_resource_benchmark.sh 1025 result-1025.json
bash scripts/storage_migration_resource_benchmark.sh 8193 result-8193.json
```
""",
)

write(
    "docs/STATUS.md",
    f"""# Velantrim Crystal — Current Status

**Status date:** 2026-08-08  
**Version:** `0.3.0`  
**Verified runtime checkpoint:** `{COMMIT}`  
**Verified tree:** `{TREE}`  
**Validated implementation head:** `{HEAD}`  
**Runtime PR / CI:** #{PR} / `{CI}`  
**Resource benchmark CI:** `{BENCH}`

## Verification

- Python 3.11: **{PASSED} passed / {SKIPPED} skipped / 0 failed**;
- Python 3.12: **{PASSED} passed / {SKIPPED} skipped / 0 failed**;
- **{STATEMENTS} statements / 100.00% line coverage**;
- `core/storage_migration.py`: **626/626 statements**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **2/2** resource benchmark jobs successful.

Exact evidence: [`TEST_REPORT.md`](../TEST_REPORT.md), the
[machine-readable manifest](./status/implementation-manifest.json), and the
[resource report](./benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md).

## Current verified capability boundary

Crystal retains its prior trust, evidence, query, review, authorization and SQLite lifecycle
capabilities. PR #{PR} additionally provides bounded-streaming logical export and independent
verification inside the existing local-first envelope:

```text
locked SQLite profile
→ fixed cursor batches
→ incremental canonical JSONL
→ disk-backed canonical edge sort
→ same-descriptor hash-first verification
→ disk-backed referential checks
→ exact completed bundle
```

Issue #331 is implemented. The production verifier no longer retains complete datasets or
global identifier sets. Temporary storage is private, preflighted and cleaned on handled
initialization failure.

## Resource boundary

The active limits remain 1 MiB control/record, 64 MiB source/dataset, 200,000 records per
dataset and 384 MiB aggregate JSONL. Benchmark `{BENCH}` covers 1,025 and 8,193-record
synthetic corpora; it is local-first evidence, not a production SLO or institution-scale
certification.

## Still absent

- PostgreSQL/pgvector runtime, inactive import and exact target equivalence (#332);
- activation, cutover, rollback, dual-write or automatic backend switching;
- distributed fencing and production IdP/multi-tenancy;
- dedicated verified Reader Core;
- legal/security/GDPR certification.

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful verification != backend activation
```

## Grant status

The project is submitted and under review. **No award or budget change** is claimed. The
bounded-streaming work in PR #{PR} is now merged baseline and cannot be counted again as
future funded delta. Future storage funding begins with #332 and separately reviewed later
cutover/rollback/server-lifecycle phases.
""",
)

write(
    "docs/IMPLEMENTATION_STATUS.md",
    f"""# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `{SHORT}` / PR #{PR}  
**Exact evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | storage and migration cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented and tested | restore is inactive and never admission |
| SQLite logical export/verify | Implemented and tested | canonical backend-neutral bundle |
| Bounded-streaming logical migration | Implemented and tested | fixed batches, disk-backed sort/reference checks, same-descriptor verification |
| Resource benchmark evidence | Observed | 1,025 and 8,193 synthetic corpora; not a production SLO |
| PostgreSQL/pgvector institutional profile | Proposed | #332; no driver, schema, importer or runtime adapter |
| Inactive PostgreSQL import / exact equivalence | Not implemented | next separately reviewed phase |
| Automatic SQLite/PostgreSQL switching | Forbidden | backend availability is not migration |
| Cutover / rollback / dual-write | Not implemented | later explicit phases only |
| Reader Core / Semantic Reading Layer | Not implemented | candidate layer upstream of normal admission |

## Current storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ fixed cursor batches
→ deterministic canonical JSONL
→ disk-backed canonical edge ordering
→ same-descriptor independent verification
→ disk-backed referential integrity
```

Issue #331 is implemented by PR #{PR}. Active limits remain 64 MiB source/dataset, 200,000
records per dataset and 384 MiB aggregate JSONL. The benchmark is evidence for tested
local-first corpora, not arbitrary scale or a production SLO.

Future work:

```text
inactive PostgreSQL/pgvector import (#332)
→ exact state equivalence
→ exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ optional explicit rollback
→ server backup/restore/upgrade lifecycle
```

Crystal does not claim PostgreSQL runtime, automatic migration, production multi-tenancy,
universal truth, zero hallucinations, legal/security certification or consciousness.
""",
)

write(
    "docs/ai/CURRENT_STATE.md",
    f"""# Crystal Current State

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `{COMMIT}`  
**Verified tree:** `{TREE}`  
**Validated runtime head:** `{HEAD}`  
**Runtime PR / CI:** #{PR} / `{CI}`  
**Resource benchmark:** `{BENCH}`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale and history; it does not override repository evidence.

## 1. Verified evidence

- Python 3.11 and 3.12: **{PASSED} passed / {SKIPPED} skipped / 0 failed**;
- **{STATEMENTS} statements / 100.00% coverage**;
- storage migration module: **626/626 statements**;
- **7/7** Ring Zero mutants killed;
- **9/9** permanent CI jobs and **2/2** benchmark jobs successful.

## 2. Current storage runtime

```text
locked durable SQLite profile
→ backup / verify / inactive restore
→ fixed-batch deterministic logical export
→ private disk-backed edge ordering
→ completed canonical JSONL bundle
→ same-descriptor independent verification
→ private disk-backed referential checks
```

Issue #331 is implemented by PR #{PR}. The production path is bounded-memory inside the
existing local-first size envelope. Benchmark results for 1,025 and 8,193 synthetic corpora
are recorded in `docs/benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md`; they are not
a production SLO or institution-scale certification.

## 3. Authority boundary

```text
physical L3      != strict Canon
migration bundle != claim evidence
verification     != backend activation
benchmark        != deployment certification
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## 4. PostgreSQL/pgvector position

SQLite remains the verified local-first profile. PostgreSQL/pgvector is proposed future
work under #332. No driver, importer, target schema, activation, cutover, rollback,
dual-write or automatic fallback is implemented.

## 5. Grant and remaining limitations

The project is submitted and under review; no award or budget change is claimed. PR #{PR}
is merged baseline and must not be counted again as funded delta. Remaining work includes
#332, later cutover/rollback/server lifecycle, distributed coordination, production IdP,
supply-chain hardening and a dedicated Reader Core.

English is the sole authoritative actively maintained GitHub documentation language during
engineering. Localized READMEs remain frozen snapshots.
""",
)

# Manifest: retain frozen localization hashes and prior non-storage boundaries.
manifest_path = ROOT / "docs/status/implementation-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["status_date"] = "2026-08-08"
manifest["verified_runtime_checkpoint"] = {
    "commit": COMMIT,
    "short": SHORT,
    "tree": TREE,
    "validated_head": HEAD,
    "pull_request": PR,
    "ci_run": CI,
    "description": "Bounded-streaming SQLite logical export and independent verification with disk-backed ordering and reference checks",
}
manifest["tests"].update(
    passed=PASSED,
    skipped=SKIPPED,
    failed=0,
    measured_statements=STATEMENTS,
    coverage_percent=100.0,
)
manifest["implemented_boundaries"]["bounded_streaming_logical_migration"] = True
manifest["implemented_boundaries"]["sqlite_logical_export_resource_contract"] = "bounded-streaming-local-first"
limits = manifest["storage_resource_limits"]
limits.pop("streaming_follow_up_issue", None)
limits.update(
    bounded_streaming_issue_completed=331,
    resource_benchmark_ci=BENCH,
    benchmark_primary_records=[1025, 8193],
    benchmark_is_production_slo=False,
    institution_scale_claim=False,
    postgresql_follow_up_issue=332,
)
manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n", encoding="utf-8")

# Known risks and work log: prepend current, evidence-bearing entries.
known = read("docs/ai/KNOWN_RISKS.md")
known = re.sub(r"\*\*Verified runtime checkpoint:\*\* `[^`]+`", f"**Verified runtime checkpoint:** `{COMMIT}`", known, count=1)
known_entry = f"""## 2026-08-08 — Bounded migration checkpoint

- #331 is implemented by PR #{PR}; fixed cursor batches and disk-backed ordering/reference checks remove complete-dataset/global-ID retention from the production path.
- Existing local-first size limits remain active. Benchmark `{BENCH}` is not a production SLO or institution-scale certification.
- #332 remains open for optional inactive PostgreSQL/pgvector import and exact-state equivalence; activation and cutover remain absent.
- Resource exhaustion, temporary-disk capacity, interruption cleanup and maximum-envelope testing remain operational concerns for larger deployments.
- GDPR language remains **GDPR-oriented controls**, not legal compliance or certification.
- PR #334 remains historical grant/status baseline context; the current runtime authority is PR #{PR}.

"""
anchor = known.index("This register is an orientation layer")
anchor = known.index("\n", anchor) + 1
known = known[:anchor] + "\n" + known_entry + known[anchor:]
write("docs/ai/KNOWN_RISKS.md", known)

work = read("docs/ai/WORK_LOG.md")
work_entry = f"""## 2026-08-08 — PR #{PR} bounded migration merged

- Merge: `{COMMIT}`; validated head `{HEAD}`; exact-head CI `{CI}` 9/9.
- Evidence: {PASSED} passed / {SKIPPED} skipped, {STATEMENTS} statements, 100.00% coverage; benchmark `{BENCH}` 2/2.
- Implemented fixed cursor batches, disk-backed canonical edge sorting, same-descriptor incremental verification, disk-backed referential checks and failure cleanup.
- First CI runs exposed SHA-diagnostic precedence and missing fail-closed branch coverage; both were fixed before merge.
- Impact classification: `GITHUB_AND_NOTION`.
- #331 becomes merged baseline after this status synchronization; #332 remains the next inactive PostgreSQL import/equivalence phase.

"""
insert = work.index("Add new entries at the top")
insert = work.index("\n", insert) + 1
work = work[:insert] + "\n" + work_entry + work[insert:]
write("docs/ai/WORK_LOG.md", work)

# Grant scope: #331 is baseline, not future funded work.
write(
    "docs/GRANT_NLNET_SCOPE.md",
    f"""# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-08  
**Baseline checkpoint:** `main@{COMMIT}`  
**Validated head / CI:** `{HEAD}` / `{CI}`  
**Grant status:** submitted / under review / not awarded

Velantrim Crystal is open-source, local-first verifiable memory infrastructure. References
to GDPR mean **GDPR-oriented technical controls**, not automatic legal compliance or
certification.

## Current verified baseline

The prior trust/evidence/query/review baseline now also includes PR #{PR}:

- fixed-batch SQLite logical export;
- incremental canonical JSONL write/hash/count;
- private disk-backed canonical edge ordering;
- same-descriptor hash-first independent verification;
- private disk-backed referential-integrity checks;
- bounded diagnostics, disk preflight and handled-failure cleanup;
- reproducible local-first resource evidence.

Verification:

```text
Python 3.11 / 3.12: {PASSED} passed / {SKIPPED} skipped / 0 failed
{STATEMENTS} statements / 100.00% coverage
7/7 Ring Zero mutants killed
9/9 permanent CI jobs successful
2/2 resource benchmark jobs successful
```

The active envelope remains 64 MiB source/dataset, 200,000 records per dataset and 384 MiB
aggregate JSONL. Benchmark `{BENCH}` covers 1,025 and 8,193-record synthetic corpora. It is
not a production SLO or institution-scale certification.

## Proposed funded delta after the new baseline

Already merged #331 work cannot be budgeted again. Preferred future packages begin with:

1. **Inactive PostgreSQL/pgvector import and exact equivalence** (#332)
   - optional driver/version policy and secret-free profile identity;
   - inactive target only;
   - exact identifiers, payloads, vectors, edges, metadata, restrictions and provenance;
   - failure cleanup and receipts; no activation on import success.
2. **Exact-vs-ANN retrieval evaluation**
   - exact search reference and versioned HNSW/IVFFlat corpus;
   - recall, latency, index size and rebuild evidence;
   - ANN remains a rebuildable non-authoritative projection.
3. **Explicit cutover and rollback proof**
   - source/target fencing, immutable receipts, rollback window and crash tests.
4. **Server lifecycle and security**
   - TLS, least-privilege roles, credential rotation, backup/restore/upgrade drills.
5. **Release and audit evidence**
   - reproducible artifacts, checksums, SBOM and independent review.

## Critical distinctions and exclusions

```text
physical L3          != strict Canon
migration bundle     != claim evidence
successful import    != activation
benchmark result     != production SLO
GDPR-oriented design != legal certification
```

No current PostgreSQL runtime, automatic backend switching, production multi-tenancy,
distributed exactly-once, universal truth, zero hallucinations, AGI or consciousness is
claimed. The baseline/funding rule remains: merged capabilities cannot be counted again as
paid future work.

See the [M1–M9 matrix](./grants/baseline-funded-delta-matrix.md).
""",
)

matrix = read("docs/grants/baseline-funded-delta-matrix.md")
matrix = matrix.replace("2026-08-07", "2026-08-08", 1)
matrix = matrix.replace("main@c612c1f7de067b05ed7d01ad82d47a7bc39af23a", f"main@{COMMIT}", 1)
matrix = matrix.replace("e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560", f"{HEAD}` / `{CI}", 1)
matrix = matrix.replace("2047 passed / 12 skipped / 9219 statements", f"{PASSED} passed / {SKIPPED} skipped / {STATEMENTS} statements", 1)
m2_start = matrix.index("## M2 —")
m2_end = matrix.index("\n## M3 —", m2_start)
m2 = f"""## M2 — Bounded portable storage state

**Baseline already present**

- backend-neutral canonical JSONL bundle schema;
- PR #{PR} fixed cursor batches and incremental write/hash/count;
- disk-backed canonical edge ordering and referential checks;
- same-descriptor hash-first incremental verification;
- disk preflight, cleanup and bounded diagnostics;
- benchmark `{BENCH}` for 1,025 and 8,193-record synthetic corpora.

**Funded delta**

- no duplicate billing of #331 / PR #{PR};
- independently reviewed maximum-envelope and interruption benchmarks if limits are raised;
- optional operational tooling only when it produces new measurable artifacts.

**Acceptance**

- existing local-first limits and non-SLO wording remain explicit;
- any larger envelope requires reproducible memory, disk, time and cleanup evidence;
- no institution-scale or production-SLO claim is inferred from the current benchmark.
"""
matrix = matrix[:m2_start] + m2.rstrip() + matrix[m2_end:]
write("docs/grants/baseline-funded-delta-matrix.md", matrix)

write(
    "ROADMAP.md",
    f"""# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Current verified baseline:** `main@{COMMIT}`  
**Validated head / CI:** `{HEAD}` / `{CI}`

## ✅ Delivered baseline

Crystal includes the trust/evidence/query/storage lifecycle baseline plus:

- deterministic bounded-streaming SQLite logical export;
- disk-backed canonical edge ordering and referential checks;
- same-descriptor independent verification;
- cleanup and resource preflight;
- {PASSED} tests, {STATEMENTS} statements, 100% coverage and 9/9 CI;
- benchmark `{BENCH}` 2/2 with explicit non-SLO limits.

## ✅ Completed — issue #331 / PR #{PR}

The production path no longer retains complete datasets or global identifier sets. Existing
64 MiB source/dataset, 200,000-record and 384 MiB aggregate limits remain active. Raising
them requires a separate evidence-backed change.

## P1 — Inactive PostgreSQL/pgvector import (#332)

Next phase only:

```text
verified bundle
→ PostgreSQL preflight
→ inactive target import
→ exact state equivalence
→ import/equivalence receipts
```

No activation, cutover, rollback, dual-write or automatic switching.

## P2 — Exact/ANN evaluation, cutover and rollback

- exact pgvector search reference;
- versioned HNSW/IVFFlat evaluation;
- source/target fencing and explicit cutover receipt;
- rollback proof and expiry policy.

## P2 — Server lifecycle and security

- least-privilege roles, TLS and credential rotation;
- backup/restore/upgrade drills;
- transaction/retry policy and observability;
- no certification or distributed exactly-once overclaim.

## P2/P3 — Release evidence and Reader Core research

- reproducible artifacts, checksums, SBOM and dependency pinning;
- source-linked Reader Core prototype only upstream of Guardian/TruthGate.

**No grant award** or budget change is claimed. PostgreSQL runtime, automatic switching,
production multi-tenancy, universal truth, zero hallucinations and legal certification
remain out of scope.
""",
)

write(
    "SECURITY.md",
    f"""# Security Policy

## Supported security baseline

The current verified baseline is `main@{COMMIT}` (PR #{PR}, CI `{CI}`). Evidence includes
Python 3.11/3.12 tests, 100% coverage, Ruff, Bandit, dependency audit, secret scanning,
Docker, evaluation, JSONL integrity, docs-status and Ring Zero mutation checks.

This is research-grade open infrastructure, **not a security, legal or GDPR certification**.

## Reporting

Do not publish secrets, private data or exploitable details in a public issue. Use the
repository security-reporting channel and include the affected commit, component,
reproduction, impact and suggested mitigation.

## Authority model

```text
physical L3 storage != strict Canon
migration bundle     != claim evidence
successful verify    != backend activation
benchmark result     != production SLO
```

TruthGate and Guardian remain the authority boundaries. Storage, retrieval, migration,
topic metadata and model output cannot bypass them.

## Storage and migration security

PR #{PR} implements issue #331 with fixed cursor batches, incremental write/hash/count,
private disk-backed canonical edge sorting, same-descriptor hash-first verification,
disk-backed referential checks, bounded diagnostics, disk preflight and cleanup on handled
temporary-index initialization failure.

The active envelope remains:

```text
control/record <= 1 MiB
source/dataset <= 64 MiB
records per dataset <= 200,000
aggregate JSONL <= 384 MiB
```

Benchmark `{BENCH}` is bounded local-first evidence, not a production SLO or arbitrary-scale
proof. Operators must still protect database, profile, bundle and temporary paths, monitor
disk/memory and use encrypted storage where sensitive data requires it.

## PostgreSQL/pgvector

PostgreSQL/pgvector is proposed, not current runtime. Issue #332 must define optional
dependencies, supported versions, TLS, least-privilege roles, credential rotation,
transaction/retry policy, schema ownership, audit redaction, backup/restore/upgrade and
inactive-import cleanup. Credentials must never enter profiles, bundles, receipts, logs or
Notion.

Automatic switching, live dual-write, activation on import success, production
multi-tenancy and distributed exactly-once behavior are not implemented.

## Supply chain and deployment

The default runtime remains pure standard library. Optional dependencies require isolated
extras and version bounds. Remaining work includes immutable action pins, reviewed
constraints, checksums/SBOM and scheduled maintenance.

Before network exposure, require TLS, authenticated access, least privilege, protected
storage, restore drills, secret rotation, resource monitoring and independent review.
""",
)

# Update the documentation status gate to the new exact checkpoint and markers.
validator = read("scripts/check_docs_status.sh")
validator = validator.replace("c612c1f7de067b05ed7d01ad82d47a7bc39af23a", COMMIT)
validator = validator.replace("e70c31bf517039f0dd3f77f7bc4b6d3f03936736", HEAD)
validator = validator.replace("31213056560", str(CI))
validator = validator.replace("checkpoint does not match merged PR #330", "checkpoint does not match merged PR #335")
validator = validator.replace("validated head does not match PR #330 evidence", "validated head does not match PR #335 evidence")
validator = validator.replace("checkpoint.get(\"pull_request\") != 330", "checkpoint.get(\"pull_request\") != 335")
validator = validator.replace("manifest pull request must be 330", "manifest pull request must be 335")
validator = validator.replace('"passed": 2047', f'"passed": {PASSED}')
validator = validator.replace('"measured_statements": 9219', f'"measured_statements": {STATEMENTS}')
validator = validator.replace('"2047 passed / 12 skipped"', '"2059 passed / 12 skipped"')
validator = validator.replace('"2047 passed / 12 skipped / 0 failed"', '"2059 passed / 12 skipped / 0 failed"')
validator = validator.replace('"PR #330"', '"PR #335"')
validator = validator.replace('"c612c1f"', '"f03e24c"')
validator = validator.replace('"logical export must remain documented as bounded-local-first"', '"logical export must remain documented as bounded-streaming-local-first"')
validator = validator.replace('boundaries.get("sqlite_logical_export_resource_contract") != "bounded-local-first"', 'boundaries.get("sqlite_logical_export_resource_contract") != "bounded-streaming-local-first"')
validator = validator.replace(
    'if limits.get("streaming_follow_up_issue") != 331:\n    errors.append("streaming migration follow-up must remain issue #331")',
    'if limits.get("bounded_streaming_issue_completed") != 331:\n    errors.append("bounded streaming issue completion must be #331")\nif boundaries.get("bounded_streaming_logical_migration") is not True:\n    errors.append("bounded streaming logical migration must be implemented")\nif limits.get("resource_benchmark_ci") != 31224005804:\n    errors.append("resource benchmark CI must match exact evidence")\nif limits.get("benchmark_is_production_slo") is not False:\n    errors.append("resource benchmark must not be recorded as a production SLO")',
)
validator = validator.replace("tests=2047/12, statements=9219", "tests=2059/12, statements=9361")
validator = validator.replace('"Issue #331",\n        "Issue #332"', '"Issue #331",\n        "Issue #332",\n        "bounded-streaming"')
validator = validator.replace('"#331",\n        "#332",\n        "PostgreSQL/pgvector institutional profile"', '"#331",\n        "#332",\n        "PostgreSQL/pgvector institutional profile",\n        "Bounded-streaming logical migration"')
validator = validator.replace('"#331",\n        "#332",\n        "No award or budget change"', '"#331",\n        "#332",\n        "No award or budget change",\n        "2059 passed / 12 skipped / 0 failed"')
validator = validator.replace('"#331",\n        "PostgreSQL/pgvector is proposed, not current runtime"', '"#331",\n        "PostgreSQL/pgvector is proposed, not current runtime",\n        "bounded local-first evidence"')
validator = validator.replace(
    '"2019 passed / 12 skipped",',
    '"2019 passed / 12 skipped",\n    "2047 passed / 12 skipped",\n    "9219 statements",\n    "c612c1f7de067b05ed7d01ad82d47a7bc39af23a",\n    "31213056560",',
)
write("scripts/check_docs_status.sh", validator)

# Remove this patcher; the invoking workflow removes itself in the same commit.
Path(__file__).unlink()
