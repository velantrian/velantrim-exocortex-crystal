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
candidate discovery / review
        ↓
explicit evidence + admission boundary
        ↓
Guardian → TruthGate → strict read projection
```

The core design rule is simple: **discovery proposes what deserves inspection; authority is a
separate decision path.**

## 📌 Current implementation status

**Current audited `main`:** `430e643a2a3759da793f700617a327d419439dde` — signed/verified merge history, latest push CI `31603785427` **9/9 successful**.  
**Current implemented Reader retrieval baseline:** **RC-9 deterministic lexical PRE-ADMISSION candidate discovery**, merged by PR #376 at signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`.  
**RC-9 exact-head / post-merge CI:** `31593097846` / `31594027040` — **9/9 successful**.  
**RC-10 note:** PR #378 subsequently merged a reuse-compatibility / comparison **preregistration contract only**. It executes no semantic/hybrid comparator and adds no Reader retrieval runtime.  
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
dedicated_reader_core                  = false
```

RC-8 is an architecture/research decision; RC-9 is the measured lexical implementation
baseline. Neither creates a complete autonomous Reader machine flag.

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
[RC-8](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md), and
[RC-9](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md).

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

## 🛡️ Authority firewall

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

These are architecture boundaries, not wording preferences. Reader candidate-discovery
results remain PRE-ADMISSION inspection artifacts.

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

### What the result proves — and what it does not

The lexical baseline retrieves most known useful pairs in the frozen corpus, but misses the
cross-lingual paraphrase `rc8-004`. All four paired `SAME_TOPIC` / `MERELY_SIMILAR` hard
negatives also surface within top-5. High lexical overlap can therefore surface dangerous
false-positive candidates, while cross-lingual or low-overlap meaning can be missed.

This benchmark is deliberately small, synthetic and paired. Precision@5 uses the benchmark's
fixed-K paired definition; it is **not corpus-wide semantic precision**. Recall@5 is **not
accuracy**. MRR is **not correctness**. None of the metrics is adjudication authority.

The result supports measurement-driven future research; it does **not** by itself authorize
embeddings, semantic/hybrid retrieval, ANN/vector DB, entity resolution or automatic claim
identity.

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
[Reviewer Notes](./docs/REVIEWER_NOTES.md).

## 🚫 Current limitations / non-claims

Crystal does **not** claim:

- semantic understanding or automatic semantic equivalence / claim identity;
- automatic truth verification, corroboration or evidence admission from retrieval;
- automatic contradiction resolution or winner selection;
- semantic/hybrid/vector Reader runtime, ANN/FAISS/HNSW, Reader vector DB or Reader FTS index;
- a completed dedicated/full autonomous Reader;
- automatic Reader parser/OCR/PDF-layout/multimodal understanding;
- active PostgreSQL runtime selection, pgvector Reader activation or automatic cutover;
- universal objective-truth detection or zero hallucinations;
- legal/GDPR/security certification or “fully secure” operation;
- production-scale retrieval quality from the 20-case RC-9 benchmark.

Known residual work remains explicit in [Known Risks](./docs/ai/KNOWN_RISKS.md), including
#155 (Epistemic Router RFC), #165 (exact normalized-id migration/dedupe) and #214
(PII/supply-chain hygiene). Those scopes are not implemented by RC-9.

## 🎓 Grant / funding status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning
context only, not an approved budget or payment commitment.

Anything merged before a funding agreement is **existing pre-agreement baseline** and cannot
be counted again as future paid delivery. RC-1 through RC-9 are therefore existing baseline
work. The merged RC-10 preregistration contract is also pre-agreement repository history; it
is not funded delivery and does not create a new Reader runtime capability.

See [NLnet scope](./docs/GRANT_NLNET_SCOPE.md) and the
[baseline → funded delta matrix](./docs/grants/baseline-funded-delta-matrix.md).

## 🌍 Localization truth

English is the primary source language. The Reader-dependent localized documentation remains
tracked separately in [Translation Status](./docs/TRANSLATION_STATUS.md). This English
post-RC-9 reconciliation does **not** perform a broad translation refresh; localized surfaces
must not be treated as newer than their recorded source checkpoint.

## 📚 Authoritative documentation

- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Machine-readable implementation manifest](./docs/status/implementation-manifest.json)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-8 retrieval decision](./docs/architecture/READER_RC8_RETRIEVAL_DECISION.md)
- [RC-9 lexical baseline and benchmark interpretation](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Roadmap](./ROADMAP.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ⏭️ Future work is evidence-gated

The next Reader implementation capability is **not implied by RC-9 metrics**. Any future
semantic/hybrid comparator or runtime proposal requires its own bounded authorization,
pre-registered evaluation, dependency/privacy/resource review and explicit authority review.

Public presentation work must never manufacture a missing capability simply to make Crystal
look more complete.
