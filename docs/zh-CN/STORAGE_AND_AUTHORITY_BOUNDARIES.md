<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- d3-locale: zh-CN -->
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
# 🇨🇳 存储与 Authority 边界

## 🧩 不同身份，不自动继承权限

```text
storage profile     = deployment identity
physical L3         = multi-status physical storage
strict Canon        = trusted read projection
migration bundle    = operation-integrity evidence
retrieval score     = ranking signal
model output        = generated text
Reader candidate    = inspection candidate
```

这些身份彼此不同。任何一个身份都不会自动授予另一个身份的 authority。

## 📖 Reader 与 storage 的边界

RC-1、RC-2、RC-3、RC-4、RC-5、RC-6、RC-7 是 bounded implemented Reader layers；RC-9 是 deterministic lexical PRE-ADMISSION discovery。它们都不能绕过 Evidence Admission / TruthGate。

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

`dedicated_reader_core = false`。Semantic/hybrid Reader runtime、NLI runtime filter 与 RRTIC runtime provider 均未授权。

## 🏛 physical L3 与 strict Canon

`physical L3 != strict Canon`。

physical L3 可以包含 VERIFIED、USER_CLAIMED、UNVERIFIED、HYPOTHESIS、SUBJECTIVE、contested、superseded 或 restricted records。strict Canon 是由 authority/policy 允许的 trusted read projection，而不是“已经持久化”的同义词。

```text
stored != trusted
retrieved != admitted
ranked highly != epistemically authoritative
```

## 💬 读取与写入

Public query 通过：

```text
HTTP /ask / CLI ask / MCP search
              ↓
core.query_pipeline.query()
              ↓
strict read-only canonical projection
```

它不会创建 facts、改变 ESM 或写入 L3。Explicit ingest/review 是独立 write path；Guardian 与 TruthGate 继续施加 structural 与 epistemic boundaries。

## 💾 SQLite 与 PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first path

PostgreSQL/pgvector
└── optional inactive import/equivalence target
    └── active=false
```

successful import != backend activation。Import success 不能推出 runtime selection、Reader activation、automatic switching、cutover、rollback、dual-write 或 ANN acceptance。

## 🔐 Authority components

```text
Guardian      = structural integrity / structural policy boundary
TruthGate     = L3 admission authority
TrustSnapshot = deny-dominant reconciliation surface
CanonicalView = strict trusted read-time projection
TRACE         = provenance / replay evidence, not proof of truth
```

Guardian 不是 truth oracle；provenance 也不是 truth proof。

## 🔬 Evaluation / inspection 不改变 authority

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

Comparator v1 classification：`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI neutral-filter v1 classification：`NLI_NEUTRAL_FILTER_GATE_FAILED`。  
RRTIC-v1：architecture contract only。

## 💶 Grant boundary

NLnet 仍是 **submitted / under review / not awarded**；约 €50,000 仅用于 planning/transparency context。

## 📚 相关合同

- [完整架构](../ARCHITECTURE.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)