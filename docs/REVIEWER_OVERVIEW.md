# Velantrim Exo-Cortex Crystal — Reviewer Overview

> **Secondary reviewer document.** The canonical reviewer entry point is
> [REVIEWER_GUIDE.md](./REVIEWER_GUIDE.md). For exact current state, see
> [STATUS.md](./STATUS.md), [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
> and [TEST_REPORT.md](../TEST_REPORT.md).

**Current signed architecture checkpoint:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392  
**Post-merge CI:** `31771677028` — **9/9 SUCCESS**  
**Grant status:** NLnet **submitted / under review / not awarded**

## 1. Executive summary

Crystal is open-source, local-first memory, evidence and Reader infrastructure designed to keep **candidate discovery, provenance, evidence, epistemic admission, strict Canon and presentation separate**.

Its core reviewer question is not “does the model sound correct?” but:

> **What artifact produced this candidate, what source/provenance does it preserve, and which component is actually authorized to turn it into evidence or Canon?**

Crystal is not a chatbot, AGI claim or autonomous truth oracle.

## 2. Architecture in one view

```text
Source / document
      ↓
Reader RC-1…RC-7 bounded artifacts
      ↓
RC-9 lexical PRE-ADMISSION discovery
      ↓
RRTIC-v1 typed inspection contract
      ↓
explicit evidence / admission boundary
      ↓
Guardian → TruthGate
      ↓
physical L3 → strict Canon read projection
      ↓
read-only answer / trace / bounded refusal
```

RRTIC-v1 is **not a new runtime stage**. The diagram shows the conceptual contract boundary; no RRTIC provider/model/filter is installed.

## 3. What is actually implemented

| Area | Status | Reviewer meaning |
|---|---|---|
| Typed claims / source / truth status | **Implemented** | machine-readable epistemic categories remain separate |
| TruthGate | **Implemented** | automatic epistemic admission boundary |
| Guardian / Ring Zero | **Implemented bounded baseline** | structural/safety constraints and mutation gate |
| TRACE / Receipt | **Implemented** | replayable/auditable proof surfaces |
| Local-first SQLite storage | **Implemented / active** | ordinary active profile |
| PostgreSQL/pgvector | **Inactive import/equivalence target** | `active=false`; not normal runtime |
| Reader RC-1…RC-7 | **Implemented bounded layers** | source/session/structure/pass/proposition/relation/context/cross-document candidate artifacts |
| Reader RC-9 | **Implemented** | deterministic stdlib BM25 candidate discovery |
| Dedicated/full autonomous Reader | **Not implemented** | `dedicated_reader_core=false` |
| Semantic/hybrid Reader runtime | **Not authorized** | no semantic backend, ANN/vector Reader DB or automatic identity |
| RRTIC-v1 | **Frozen architecture contract** | diagnostic schema only; no runtime provider |

## 4. Reader evidence chain reviewers should understand

### RC-9 — deterministic lexical baseline

Historical RC-9 K=5 result:

- Recall@5 `0.937500`;
- Precision@5 `0.187500`;
- MRR `0.895833`;
- useful hits `15/16`;
- paired hard-negative hits `4/4`;
- classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

This is retrieval evidence, not semantic accuracy.

### Evaluation Surface v2

The later fully judged surface froze 24 queries, 144/144 qrels and a qrel-label-independent candidate identity. RC-9 control on this surface produced useful hits `42/48`, Recall@5 `0.875000`, MRR `0.857639` and hard negatives `38/48`.

### Comparator v1 — frozen FAIL

A pinned multilingual semantic comparator recovered `48/48` useful candidates, but surfaced `41/48` hard negatives.

```text
SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED
```

### NLI neutral-filter v1 — frozen FAIL

Bidirectional NLI filtering reduced hard negatives to `18/48`, but useful candidates regressed to `46/48`, so the frozen no-recall-loss/admissibility gate failed.

```text
NLI_NEUTRAL_FILTER_GATE_FAILED
```

### RRTIC-v1 — contract-first architecture response

The post-NLI reassessment classified the problem as a **relation-contract mismatch**. RRTIC-v1 freezes six suspicion-only relation families and ten qualifier dimensions so future work must describe *how* propositions relate rather than collapse everything to one relevance score.

RRTIC-v1 does not filter, rerank, execute a model, establish identity, admit evidence, adjudicate contradictions, mutate Canon or replace RC-5.

## 5. Authority firewall

```text
retrieval match          != evidence
similarity               != identity
NLI label                != proposition identity
NLI contradiction        != contradiction adjudication
RRTIC suspicion          != adjudicated relation
qualifier mismatch       != truth decision
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
evaluation pass          != runtime authorization
```

This boundary is the most important architectural property to review.

## 6. Current validation

Post-RRTIC workflow `31771677028` completed **9/9 SUCCESS**. The Python 3.11 matrix job collected 2244 tests and completed **2231 passed / 13 skipped / 0 failed** with **100% measured line coverage**.

Reviewer commands:

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/
python scripts/eval_gate.py --out-dir eval-artifacts
```

## 7. Current non-claims

Crystal does not claim:

- universal truth, zero hallucinations, AGI or consciousness;
- a complete autonomous Reader;
- semantic/hybrid Reader runtime;
- automatic proposition identity or contradiction winner selection;
- evidence admission from similarity/NLI/RRTIC diagnostics;
- Reader FTS/ANN/vector DB or active PostgreSQL/pgvector;
- security/legal/GDPR certification;
- awarded NLnet funding.

## 8. Grant and research boundary

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning context only. Work completed before any funding agreement—including RC-1…RC-9, Comparator v1, NLI v1 and RRTIC-v1—remains existing pre-agreement baseline/research history and cannot later be relabeled as newly funded delivery.

## 9. Recommended reviewer path

1. [README](../README.md) — first-impression project truth.
2. [Implementation status](./IMPLEMENTATION_STATUS.md) — implemented vs research vs absent.
3. [Architecture overview](./ARCHITECTURE_OVERVIEW.md) — authority and Reader boundaries.
4. [RRTIC-v1 contract](./architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md) — current architecture decision.
5. [Reviewer demo](./REVIEWER_DEMO.md) — hands-on trust loop.
6. [Test report](../TEST_REPORT.md) — exact current validation evidence.
