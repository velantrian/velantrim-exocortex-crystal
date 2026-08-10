<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Velantrim Crystal — NLnet Grant Scope

**Baseline date:** 2026-08-10  
**Frozen runtime checkpoint:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

This document describes public technical scope. It is not an award notice, signed agreement,
approved budget or payment commitment. References to GDPR mean GDPR-oriented technical controls,
not automatic legal compliance or certification.

## Current verified baseline

The trust/evidence/query/review/storage baseline includes Guardian, TruthGate, read-only public
query surfaces, source spans/document records/import sessions, SQLite ordinary active local-first,
bounded logical export, inactive PostgreSQL 16 / pgvector import with exact equivalence and
`active=false`, TRACE/Receipt, review/contradiction governance and all work already merged before
an agreement.

Reader RC-1/RC-2 and RC-3, if merged before an agreement, are existing pre-agreement baseline:

```text
reader_core_rc1_skeleton             = true
reader_core_rc2_structural_map       = true
reader_core_rc3_multi_pass_mechanics = true
dedicated_reader_core                = false
```

RC-1 provides the bounded evidence-linked source/session skeleton. RC-2 provides the bounded
caller-supplied Structural Document Map. RC-3 provides deterministic explicit pass mechanics over
those exact source/structure layers. They retain no source body, add no Reader API/CLI/worker or
durable Reader storage schema and have no truth/Canon/ESM/planner authority. They do not provide an
automatic parser/OCR, autonomous Reader LLM/provider agent, embeddings/ANN/vector DB or automatic
cross-document reasoning engine. Pass completion is not comprehension proof.

The retained runtime checkpoint remains:

```text
Python 3.11 / 3.12: 2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% coverage
7/7 Ring Zero mutants killed
9/9 permanent CI jobs successful
1/1 PostgreSQL integration job successful
```

Later Reader milestones carry separate exact-head and post-merge CI evidence.

## Current documentation baseline

English is the working/source/conflict-resolving language. RC-3 advances the Reader public-source
checkpoint. Russian Reader-dependent public/detail surfaces are refreshed against that checkpoint;
other locale Reader surfaces remain explicit translation debt until fully refreshed. D2/QuickStart
semantics remain unchanged.

Any localization, Reader RC-0/RC-1/RC-2/RC-3, storage or governance work merged before a grant
agreement is existing baseline and cannot be budgeted again as funded delivery.

## Baseline and funded-delta control

```text
verified existing baseline
+
new measurable funded delta
=
independently verifiable public deliverable
```

If `main` advances before an agreement, the baseline/funded-delta matrix must be reconciled so each
funded package remains genuinely additional and independently auditable.

## Potential funded delta after RC-3

Qualifying future packages may include:

1. reproducible release artifacts, checksums, SBOM and clean-machine verification;
2. exact-vs-ANN evaluation with versioned thresholds and reproducible reports;
3. explicit source/target fencing, cutover receipts and rollback proof;
4. PostgreSQL production roles, backup/restore/upgrade lifecycle and observability;
5. reviewer-facing evidence/TRACE inspection UX;
6. maintenance, claim lint and independent audit evidence;
7. **Reader work strictly beyond RC-3**, beginning only as separately reviewed new delta.

For Reader, the next candidate after RC-3 is separately bounded evidence extraction work. A
dedicated/full autonomous Reader / Semantic Reading runtime remains not implemented. Any funded
Reader milestone must exclude RC-0 architecture, RC-1 skeleton, RC-2 Structural Document Map and
RC-3 explicit pass mechanics already merged pre-agreement.

## Critical distinctions and exclusions

```text
physical L3          != strict Canon
migration bundle     != claim evidence
successful import    != activation
exact equivalence    != production runtime
Reader artifact      != admitted fact
Reader coverage      != comprehension proof
Reader pass complete != comprehension proof
Reader structure     != epistemic authority
GDPR-oriented design != legal certification
submitted proposal   != awarded grant
```

No automatic backend switching, active PostgreSQL runtime selection, ANN production acceptance,
cutover, rollback, dual-write, production multi-tenancy, distributed exactly-once, universal truth,
zero hallucinations, AGI, consciousness or completed dedicated/full autonomous Reader is claimed.

## Budget and award control

The public funding-use plan discusses an approximate €50,000 request. It remains planning and
transparency material until verified external communication establishes an agreement. Award or
budget state may change only from authoritative external evidence such as a signed grant agreement
or Memorandum of Understanding.

## Authoritative supporting documents

- [Project, grant and governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary and claim discipline](./GLOSSARY.md)
- [Baseline → funded delta → acceptance matrix](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Current status](./STATUS.md)
- [Test report](../TEST_REPORT.md)
