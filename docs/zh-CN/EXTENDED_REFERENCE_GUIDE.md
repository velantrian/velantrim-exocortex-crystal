<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- current-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- d5-locale: zh-CN -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
# 🇨🇳 Crystal 扩展参考指南

本页是简体中文的 extended reference surface。它保留历史 RC-5 compatibility vocabulary，同时明确当前 post-RC-9 / post-NLI / RRTIC-v1 architecture truth。

## 📖 Reader progression

```text
RC-1 source-linked skeleton
→ RC-2 structural map
→ RC-3 multi-pass mechanics
→ RC-4 proposition extraction
→ RC-5 relation candidates
→ RC-6 bounded long-context working sets
→ RC-7 explicit cross-document candidates
→ RC-9 deterministic lexical PRE-ADMISSION discovery
```

RC-1…RC-7 与 RC-9 是 bounded implemented components/layers；`dedicated_reader_core=false`。

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

## 🧩 Historical RC-5 relation vocabulary

这些 presentation/inspection categories 保留为 compatibility vocabulary：

```text
POSSIBLE_CONTRADICTION
EXCEPTION
QUALIFICATION
TENSION
```

它们不代表 adjudicated truth，也不会自动产生 Evidence Admission 或 Canon mutation。

## 🔬 Current post-RC-9 evidence chain

```text
RC-9 lexical baseline
        ↓
Comparator v1
semantic recall recovered · discrimination FAIL
        ↓
NLI neutral-filter v1
discrimination improved · recall-safety FAIL
        ↓
architecture reassessment
        ↓
RRTIC-v1
architecture contract only
```

Comparator classification：`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI classification：`NLI_NEUTRAL_FILTER_GATE_FAILED`。

RRTIC-v1 是 typed suspicion/qualifier inspection contract，不提供 model、reranker、truth score、accept/reject policy、Evidence Admission、Contradiction Adjudication 或 Canon writer。

## 🛡 Authority firewall

```text
retrieval match != evidence
similarity != identity
repetition != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

## 🏛 Authority roles

```text
Guardian      = structural integrity / structural policy boundary
TruthGate     = L3 admission authority
TrustSnapshot = deny-dominant reconciliation surface
CanonicalView = strict trusted read-time projection
TRACE         = provenance / replay evidence, not proof of truth
```

Discovery/inspection components 不能继承这些 authority roles。

## 💾 Storage truth

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector = INACTIVE
active=false
successful import != backend activation
physical L3 != strict Canon
```

PostgreSQL/pgvector 只是 inactive import/equivalence target，不代表 active Reader backend、automatic cutover、rollback 或 dual-write。

## 💶 Grant truth

NLnet NGI0 Commons Fund：**submitted / under review / not awarded**。约 **€50,000** 是 planning context；**budget change: none**。

## 🌍 Localization state vocabulary

`CURRENT` = technical parity/freshness against the recorded source contract。  
`REFRESH_NEEDED` = translation remains useful but its Reader-dependent semantics lag the current source。  
这些状态都不等于 native-speaker editorial certification。

Simplified Chinese 本页完成刷新后进入 `CURRENT`；仍需刷新的是 Arabic、Hindi、Japanese Reader-dependent root/detail surfaces。

## 🚫 Non-claims

本扩展参考不声称 semantic/hybrid/vector Reader runtime、NLI runtime filter、RRTIC runtime provider、active PostgreSQL/pgvector Reader selection、automatic proposition identity、automatic corroboration、universal truth、zero hallucinations 或 legal/security/GDPR certification。

英文 policy 主源：[`docs/EXTENDED_REFERENCE_POLICY.md`](../EXTENDED_REFERENCE_POLICY.md)。