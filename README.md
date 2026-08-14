# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory, evidence and Reader infrastructure for trustworthy AI systems

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not a chatbot and not an autonomous truth oracle. It keeps source identity,
> retrieval candidates, evidence, epistemic state and Canon authority separate so material
> cannot silently gain authority from relevance, repetition or model confidence.

## 💠 Why Crystal exists

AI systems can retrieve plausible context without proving that the context is true, identical
to another claim, corroborating, or safe to admit as evidence. Crystal provides local-first,
source-aware infrastructure where provenance and authority boundaries remain inspectable.

```text
source-linked material
        ↓
bounded Reader artifacts
        ↓
candidate discovery / typed inspection
        ↓
explicit evidence + admission boundary
        ↓
Guardian → TruthGate → strict read projection
```

The core design rule is simple: **discovery proposes what deserves inspection; authority is a
separate decision path.**

## 📌 Current implementation status

**Current signed architecture checkpoint:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, signature `verified=true`, reason `valid`; PR #392 merged Reader Retrieval Typed Inspection Contract v1 (RRTIC-v1). Post-merge CI `31771677028`: **9/9 successful**.  
**Current implemented Reader retrieval baseline:** **RC-9 deterministic lexical PRE-ADMISSION candidate discovery**, merged by PR #376 at signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`.  
**Latest frozen model-backed evaluation:** NLI neutral-filter v1, PR #389, classification `NLI_NEUTRAL_FILTER_GATE_FAILED`; `runtime_authorization=false`.  
**Current architecture/research contract:** **RRTIC-v1**, model-free and diagnostic-only. It adds no runtime provider, model, filter, reranker, evidence admission, identity decision or Canon authority.  
**Dedicated/full autonomous Reader:** **not implemented** (`dedicated_reader_core=false`).

Machine implementation truth remains:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
rrtic_runtime_authorization            = false
```

RC-8 is an architecture/research decision; RC-9 is the measured lexical implementation
baseline. Comparator v1 and NLI v1 are frozen evaluation evidence. RRTIC-v1 is a frozen
inspection contract. None creates a complete autonomous Reader machine flag.

## 📖 Reader Core — RC-1 through RC-9

| Milestone | Delivered boundary |
|---|---|
| **RC-1** | Exact `SourceVersion` / replayable `SourceLocator`, Reader sessions, fidelity, coverage and stale/privacy semantics |
| **RC-2** | Caller-supplied, source-version-bound Structural Document Map; structure is metadata, not truth |
| **RC-3** | Deterministic explicit multi-pass ledger: orientation, broad/focused read, cross-check and targeted reread |
| **RC-4** | Source-linked caller-supplied `EXTRACTED_PROPOSITION` candidates with exact provenance |
| **RC-5** | Same-session/same-version relation candidates: possible contradiction, tension, exception, qualification |
| **RC-6** | Deterministic bounded long-context working sets + caller-supplied `SUMMARY` with direct RC-4 leaf provenance |
| **RC-7** | Explicit cross-document candidate links with exact two-sided provenance |
| **RC-8** | Retrieval architecture decision + frozen adversarial evaluation corpus; lexical baseline required before semantic/vector consideration |
| **RC-9** | Offline stdlib-only deterministic in-memory BM25 candidate discovery + reproducible benchmark runner |

Detailed contracts: [Reader Core architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md),
[RC-7](./docs/architecture/READER_RC7_CROSS_DOCUMENT.md),
[RC-8](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md),
[RC-9](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md), and
[RRTIC-v1](./docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md).

## 🔎 What RC-9 actually provides

RC-9 asks one bounded question:

> Which already extracted Reader proposition candidates are **lexically worth inspecting together**?

It snapshots the public RC-4 proposition surface, applies conservative Unicode NFKC / case /
whitespace normalization and stable tokenization, then ranks candidates with deterministic
in-memory BM25.

```text
RC-4 proposition candidates
        ↓
Reader-safe lexical snapshot
        ↓
deterministic BM25 ranking
        ↓
top-K inspection candidates
        ↓
manual / downstream review
```

RC-9 is **not semantic understanding**. It does not emit identity, truth, corroboration,
contradiction, evidence-sufficiency or Canon verdicts; it auto-registers no RC-7 link.

The retained RC-7 boundary also remains explicit: **no automatic semantic matching**. Reader
cross-document candidates still provide no embeddings/ANN/vector retrieval, no vector DB, and no adjudication.

## 🧪 What happened after RC-9

The post-RC-9 research chain is deliberately preserved, including negative results:

```text
RC-9 lexical baseline
        ↓
Comparator v1
  multilingual semantic similarity
  recall recovered
  proposition discrimination gate FAIL
        ↓
NLI neutral-filter v1
  discrimination improved
  useful-recall safety gate FAIL
        ↓
architecture reassessment
  RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
  typed inspection contract only
  no runtime authorization
```

### Comparator v1 — evaluation only

The pinned multilingual sentence-embedding comparator recovered all useful candidates on the
frozen Evaluation Surface v2 (`48/48`, Recall@5 `1.0`, MRR `1.0`) but also surfaced `41/48`
hard negatives. Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.
This result did **not** authorize a semantic Reader backend.

### NLI neutral-filter v1 — evaluation only

The preregistered bidirectional neutral-neutral NLI filter reduced v2 hard-negative hits to
`18/48`, but useful hits regressed to `46/48` and the frozen no-recall-loss overlay failed.
Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`. The signal is diagnostically useful; the
frozen filter is not admissible as a Reader retrieval stage.

### RRTIC-v1 — architecture contract, not runtime

RRTIC-v1 freezes a model-free typed inspection envelope after the post-NLI reassessment found
that the missing capability is better described as **relation-contract preservation + structural
qualifier discrimination**, not simply “use a larger similarity model”.

Frozen suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Frozen qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

Each qualifier is `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 has **no accept/reject decision, no scalar truth score, no reranking, no model
execution and no runtime provider**. It does not replace or mutate RC-5 relation semantics.

## 🛡️ Authority firewall

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

These are architecture boundaries, not wording preferences. Reader candidate-discovery and
inspection results remain PRE-ADMISSION artifacts.

## 🧪 RC-9 benchmark snapshot

Frozen artifact: [`eval/reader_rc9_lexical_baseline.json`](./eval/reader_rc9_lexical_baseline.json).  
Frozen input: 20 synthetic/adversarial paired cases from RC-8, `K=5`.

| Metric | Frozen result |
|---|---:|
| Recall@5 | **0.937500** |
| Precision@5 | **0.187500** |
| MRR | **0.895833** |
| Paired hard-negative rate@5 | **1.000000** |
| Useful paired hits | **15 / 16** |
| Paired hard-negative hits | **4 / 4** |

Measured classification:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

The lexical baseline retrieves most known useful pairs in the frozen corpus, but misses the
cross-lingual paraphrase `rc8-004`. All four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard
negatives also surface within top-5. This benchmark is deliberately small, synthetic and paired.
Recall@5 is not accuracy, MRR is not correctness, and no metric is adjudication authority.

## 🗄️ Local-first and retrieval domains

Ordinary active storage remains local-first SQLite. PostgreSQL 16 + pgvector exists only as
an **inactive import/equivalence target** with `active=false`; automatic backend switching is
absent.

Crystal also contains older/general **admitted-memory** retrieval infrastructure such as
`core/embedding.py`, `core/query_pipeline.py`, `core/legacy_retrieval.py` and `core/rrf.py`.
That is a different authority/data lifecycle from Reader PRE-ADMISSION RC-9 discovery.
Existing vector-capable admitted-memory code is therefore not a claim that Reader semantic or
vector retrieval is implemented.

## ✅ Reviewer validation

Python 3.11+ is required. The default runtime stays dependency-free; development tooling is
installed through the existing `dev` extra.

Current post-RRTIC `main` validation: CI `31771677028` — **9/9 successful**. The Python 3.11
matrix job collected 2244 tests and completed with **2231 passed / 13 skipped / 0 failed** at
**100% measured line coverage**.

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest -q
python scripts/eval_gate.py --out-dir eval-artifacts
```

Reproduce the frozen RC-9 Reader retrieval result:

```bash
python scripts/bench_reader_rc9_lexical.py \
  --corpus eval/reader_rc8_retrieval_adversarial.jsonl \
  --k 5 \
  --json-out /tmp/reader-rc9-lexical.json
```

The committed comparison target is
[`eval/reader_rc9_lexical_baseline.json`](./eval/reader_rc9_lexical_baseline.json). For the
maintained reviewer demo paths, see [DEMO.md](./DEMO.md) and
[Reviewer Guide](./docs/REVIEWER_GUIDE.md).

## 🚫 Current limitations / non-claims

Crystal does **not** claim:

- semantic understanding or automatic semantic equivalence / claim identity;
- automatic truth verification, corroboration or evidence admission from retrieval;
- automatic contradiction resolution or winner selection;
- semantic/hybrid/vector Reader runtime, ANN/FAISS/HNSW, Reader vector DB or Reader FTS index;
- an NLI runtime filter, CrossEncoder reranker or RRTIC runtime provider;
- a completed dedicated/full autonomous Reader;
- automatic Reader parser/OCR/PDF-layout/multimodal understanding;
- active PostgreSQL runtime selection, pgvector Reader activation or automatic cutover;
- universal objective-truth detection or zero hallucinations;
- legal/GDPR/security certification or “fully secure” operation;
- production-scale retrieval quality from the frozen synthetic evaluation surfaces.

Known residual work remains explicit in [Known Risks](./docs/ai/KNOWN_RISKS.md), including
#155 (Epistemic Router RFC), #165 (exact normalized-id migration/dedupe) and #214
(PII/supply-chain hygiene). Those scopes are not implemented by RRTIC-v1.

## 🎓 Grant / funding status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning
context only, not an approved budget or payment commitment.

Anything merged before a funding agreement is **existing pre-agreement baseline** and cannot
be counted again as future paid delivery. RC-1 through RC-9, Comparator v1, NLI v1 and
RRTIC-v1 are existing pre-agreement repository/research history; none may later be relabeled as
a newly funded runtime delivery.

See [NLnet scope](./docs/GRANT_NLNET_SCOPE.md) and the
[baseline → funded delta matrix](./docs/grants/baseline-funded-delta-matrix.md).

## 🌍 Localization truth

English is the primary source language. The Reader-dependent localized documentation remains
tracked separately in [Translation Status](./docs/TRANSLATION_STATUS.md). This English
post-RRTIC reconciliation does **not** perform a broad translation refresh; localized surfaces
must not be treated as newer than their recorded source checkpoint.

## 📚 Authoritative documentation

- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture overview](./docs/ARCHITECTURE_OVERVIEW.md)
- [Machine-readable implementation manifest](./docs/status/implementation-manifest.json)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-8 retrieval decision](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Comparator v1 result](./eval/reader_retrieval_comparator_v1_result.json)
- [NLI neutral-filter v1 result](./eval/reader_nli_neutral_filter_v1_result.json)
- [RRTIC-v1 typed inspection contract](./docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md)
- [AI current state](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Roadmap](./ROADMAP.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ⏭️ Future work is evidence-gated

No next Reader model or runtime capability is authorized by RRTIC-v1. Any future discriminator,
semantic/hybrid mechanism or runtime proposal requires a separate bounded milestone, a new
experiment identity/preregistration where applicable, fresh validation design, and explicit
privacy/resource/authority review.

Public presentation work must never manufacture a missing capability simply to make Crystal
look more complete.