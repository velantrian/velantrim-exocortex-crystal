<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/ARCHITECTURE_OVERVIEW.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- d3-locale: ja -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: nlnet-not-awarded -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
# 🇯🇵 Crystal アーキテクチャ概要

## 🧠 中核原則

Crystal は **Discovery、Evidence、Authority、Canon、Presentation** を分離します。Reader が candidate を生成しても、retrieval、similarity、ranking、typed inspection によって truth authority を獲得することはありません。

```text
📥 Sources
   ↓
📖 Reader RC-1 → RC-2 → RC-3 → RC-4 → RC-5 → RC-6 → RC-7
   ↓
🔎 RC-9 deterministic lexical PRE-ADMISSION candidate discovery
   ↓
🧬 RRTIC-v1 typed inspection contract
   ↓
🧾 evidence / admission boundary
   ↓
🛡 Guardian → TruthGate
   ↓
🏛 physical L3 → TrustSnapshot → CanonicalView → strict Canon
   ↓
💬 grounded answer / bounded refusal
```

## 📖 Reader layers

- **RC-1** — source-linked Reader skeleton;
- **RC-2** — version-bound Structural Document Map;
- **RC-3** — bounded multi-pass mechanics;
- **RC-4** — source-linked proposition extraction;
- **RC-5** — typed relation candidates;
- **RC-6** — bounded long-context working-set strategy;
- **RC-7** — explicit cross-document candidates;
- **RC-9** — deterministic lexical **PRE-ADMISSION** candidate discovery.

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
```

RC-7 は automatic semantic matching を提供しません。RC-9 も Evidence Admission、identity engine、Canon authority ではありません。

## 🔬 Post-RC-9 research

```text
RC-9 lexical baseline
        ↓
Comparator v1
semantic recall recovered · discrimination FAIL
        ↓
NLI neutral-filter v1
discrimination improved · recall-safety FAIL
        ↓
RRTIC-v1
architecture contract only
```

Comparator classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`。

RRTIC-v1 は model-free typed inspection contract です。runtime model、reranker、NLI engine、semantic retrieval engine、proposition identity engine、Evidence Admission authority、adjudicator、Canon writer ではありません。

## 🛡 Authority roles

```text
Guardian      = structural integrity / structural policy boundary
TruthGate     = L3 admission authority
TrustSnapshot = deny-dominant reconciliation surface
CanonicalView = strict trusted read-time projection
TRACE         = provenance / replay evidence, not proof of truth
```

Guardian は truth oracle ではありません。`physical L3 != strict Canon`。

## 💬 Public query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

Public query は facts を作成せず、ESM を変更せず、L3 に書き込みません。Explicit ingest/review は独立した write path です。

## 💾 Storage

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector import/equivalence target = INACTIVE
active=false
successful import != backend activation
```

PostgreSQL/pgvector surface は automatic backend switching、Reader activation、ANN acceptance、cutover、rollback、dual-write を提供しません。

## 🛡 Authority Firewall

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

## 💶 Grant

NLnet NGI0 Commons Fund: **submitted / under review / not awarded**。約 €50,000 は planning context であり approved funding ではありません。

英語の詳細 architecture contract: [`docs/ARCHITECTURE.md`](../ARCHITECTURE.md)。日本語の storage/authority 境界: [`STORAGE_AND_AUTHORITY_BOUNDARIES.md`](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)。