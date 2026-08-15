<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- current-translation-source: docs/GLOSSARY.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- d4-locale: ja -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇯🇵 Crystal 用語集

## 📖 Reader

**RC-1 / RC-2 / RC-3 / RC-4 / RC-5 / RC-6 / RC-7** — bounded implemented Reader layers。source-linked skeleton、structural map、multi-pass mechanics、proposition extraction、relation candidates、long-context working sets、cross-document candidate links を順に扱います。

**RC-9** — deterministic lexical **PRE-ADMISSION** candidate discovery。semantic Reader、Evidence Admission、Canon authority ではありません。

**dedicated Reader** — full/autonomous Reader core。現在 **not implemented**、`dedicated_reader_core=false`。

**EXTRACTED_PROPOSITION** — source-linked extracted candidate。`EXTRACTED_PROPOSITION != verified fact`。

**Reader candidate** — Reader が見つけた inspection candidate。`Reader candidate != admitted evidence`。

**contradiction candidate** — adjudication が必要な conflict candidate。`contradiction candidate != confirmed contradiction`。

## 🧬 RC-5 relation vocabulary

RC-5 は proposition presentation category と relation-candidate vocabulary を保持します。

- `POSSIBLE_CONTRADICTION`
- `EXCEPTION`
- `QUALIFICATION`
- `TENSION`

これらは presentation/inspection category であり automatic truth decision ではありません。

**source owner** — source identity / source record に対する provenance owner。truth oracle ではありません。

**proposition presentation category** — proposition/relation candidate の表示分類。Evidence や Canon relation を自動作成しません。

## 🔬 Post-RC-9 research

**Comparator v1** — frozen evaluation; classification `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。

**NLI neutral-filter v1** — frozen evaluation; classification `NLI_NEUTRAL_FILTER_GATE_FAILED`。`NLI label != proposition identity`。

**RRTIC-v1** — Reader Retrieval Typed Inspection Contract v1。architecture-only typed suspicion/qualifier contract。`RRTIC suspicion != adjudicated relation`、`rrtic_runtime_authorization=false`。

## 🏛 Authority / Canon

**Guardian** — structural integrity / structural policy boundary。truth oracle ではありません。

**TruthGate** — L3 admission authority。

**TrustSnapshot** — deny-dominant reconciliation surface。

**CanonicalView** — strict trusted read-time projection。

**physical L3** — physical multi-status graph/storage。`physical L3 != strict Canon`。

**strict Canon** — policy/authority が許可した trusted read projection。保存済みデータ全体と同義ではありません。

## 💾 Storage

**SQLite** — ordinary active local-first path。

**PostgreSQL/pgvector** — optional inactive import/equivalence target。`active=false`。successful import != backend activation。

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

NLnet funding state: **submitted / under review / not awarded**。約 **€50,000** は planning context only。**budget change: none**。`not awarded` を approved/funded と翻訳・再解釈してはいけません。

## 🧾 Certification boundary

`CURRENT` は recorded technical localization parity/freshness を意味します。native-speaker editorial certification、legal certification、GDPR certification、security certification を意味しません。

English terminology source: [`docs/GLOSSARY.md`](../GLOSSARY.md)。