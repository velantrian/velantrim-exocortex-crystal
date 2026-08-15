<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
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
# 🇯🇵 Storage と Authority の境界

## 🧩 Identity が違えば authority も自動継承しない

```text
storage profile     = deployment identity
physical L3         = multi-status physical storage
strict Canon        = trusted read projection
migration bundle    = operation-integrity evidence
retrieval score     = ranking signal
model output        = generated text
Reader candidate    = inspection candidate
```

これらの identity は別物です。どれか一つを持つことが、別の authority を自動的に与えることはありません。

## 📖 Reader と storage の境界

RC-1、RC-2、RC-3、RC-4、RC-5、RC-6、RC-7 は bounded implemented Reader layers。RC-9 は deterministic lexical PRE-ADMISSION discovery です。いずれも Evidence Admission / TruthGate を bypass できません。

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

`dedicated_reader_core = false`。Semantic/hybrid Reader runtime、NLI runtime filter、RRTIC runtime provider は authorized されていません。

## 🏛 physical L3 と strict Canon

`physical L3 != strict Canon`。

physical L3 は VERIFIED、USER_CLAIMED、UNVERIFIED、HYPOTHESIS、SUBJECTIVE、contested、superseded、restricted records を保持できます。strict Canon は authority/policy が許可する trusted read projection であり、「persist されたすべて」と同義ではありません。

```text
stored != trusted
retrieved != admitted
ranked highly != epistemically authoritative
```

## 💬 Read / write boundary

Public query は次を通ります。

```text
HTTP /ask / CLI ask / MCP search
              ↓
core.query_pipeline.query()
              ↓
strict read-only canonical projection
```

fact を作成せず、ESM を変更せず、L3 に書き込みません。Explicit ingest/review は独立 write path で、Guardian / TruthGate が structural / epistemic boundary を維持します。

## 💾 SQLite と PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first path

PostgreSQL/pgvector
└── optional inactive import/equivalence target
    └── active=false
```

successful import != backend activation。Import success から runtime selection、Reader activation、automatic switching、cutover、rollback、dual-write、ANN acceptance を導くことはできません。

## 🔐 Authority components

```text
Guardian      = structural integrity / structural policy boundary
TruthGate     = L3 admission authority
TrustSnapshot = deny-dominant reconciliation surface
CanonicalView = strict trusted read-time projection
TRACE         = provenance / replay evidence, not proof of truth
```

Guardian は truth oracle ではなく、provenance も truth proof ではありません。

## 🔬 Evaluation / inspection は authority を変更しない

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

Comparator v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI neutral-filter v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`。  
RRTIC-v1: architecture contract only。

## 💶 Grant boundary

NLnet は **submitted / under review / not awarded**。約 €50,000 は planning/transparency context だけです。

## 📚 Related contracts

- [Full architecture](../ARCHITECTURE.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)