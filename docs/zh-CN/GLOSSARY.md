<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- current-translation-source: docs/GLOSSARY.md@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- d4-locale: zh-CN -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇨🇳 Crystal 术语表

## 📖 Reader

**RC-1 / RC-2 / RC-3 / RC-4 / RC-5 / RC-6 / RC-7** — bounded implemented Reader layers，分别覆盖 source-linked skeleton、structural map、multi-pass mechanics、proposition extraction、relation candidates、long-context working sets 与 cross-document candidate links。

**RC-9** — deterministic lexical **PRE-ADMISSION** candidate discovery。它不是 semantic Reader、Evidence Admission 或 Canon authority。

**dedicated Reader** — 完整/自主 Reader core；当前 **not implemented**，`dedicated_reader_core=false`。

**EXTRACTED_PROPOSITION** — source-linked extracted candidate；`EXTRACTED_PROPOSITION != verified fact`。

**Reader candidate** — Reader 发现的候选；`Reader candidate != admitted evidence`。

**contradiction candidate** — 需要 adjudication 的冲突候选；`contradiction candidate != confirmed contradiction`。

## 🧬 RC-5 relation vocabulary

RC-5 保留 proposition presentation category 与 relation-candidate vocabulary：

- `POSSIBLE_CONTRADICTION`
- `EXCEPTION`
- `QUALIFICATION`
- `TENSION`

这些都是 presentation/inspection category，不是 automatic truth decision。

**source owner** — 对 source identity / source record 负责的 provenance owner；它不等于 truth oracle。

**proposition presentation category** — 用于组织 proposition/relation candidate 的展示类别，不自动创建 Evidence 或 Canon relation。

## 🔬 Post-RC-9 research

**Comparator v1** — frozen evaluation；classification `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。

**NLI neutral-filter v1** — frozen evaluation；classification `NLI_NEUTRAL_FILTER_GATE_FAILED`。`NLI label != proposition identity`。

**RRTIC-v1** — Reader Retrieval Typed Inspection Contract v1；architecture-only typed suspicion/qualifier contract。`RRTIC suspicion != adjudicated relation`，`rrtic_runtime_authorization=false`。

## 🏛 Authority / Canon

**Guardian** — structural integrity / structural policy boundary；不是 truth oracle。

**TruthGate** — L3 admission authority。

**TrustSnapshot** — deny-dominant reconciliation surface。

**CanonicalView** — strict trusted read-time projection。

**physical L3** — physical multi-status graph/storage；`physical L3 != strict Canon`。

**strict Canon** — policy/authority 允许的 trusted read projection，不等于所有已存储内容。

## 💾 Storage

**SQLite** — ordinary active local-first path。

**PostgreSQL/pgvector** — optional inactive import/equivalence target；`active=false`。successful import != backend activation。

## 🛡 Authority firewall

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

## 💶 Grant

NLnet funding state：**submitted / under review / not awarded**。约 **€50,000** 是 planning context only；**budget change: none**。`not awarded` 不能被翻译或重写成 approved/funded。

## 🧾 Certification boundary

`CURRENT` 表示 technical localization parity/freshness，不表示 native-speaker editorial certification、legal certification、GDPR certification 或 security certification。

英文术语主源：[`docs/GLOSSARY.md`](../GLOSSARY.md)。