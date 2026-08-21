<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/IMPLEMENTATION_STATUS.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- truthgate-v1-source: docs/IMPLEMENTATION_STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
<!-- d1-locale: ja -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇯🇵 実装状態 — Crystal の現在の能力と明示的 non-claims

## TruthGate v1 — PR #440 後の実装整合

この D1 ページは、`main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` における英語ポリシーの実質的な変更に対して再確認済みです。デフォルトの `WORLD_FACT` admission は固定かつバージョン管理されたポリシーを使用し、`DEFAULT_MIN_CONFIDENCE = 0.05`、`TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"` です。process-local adaptation は telemetry/research のままで、default admission threshold を変更しません。明示的な `min_confidence` は既存の internal/test flow の bounded caller parameter として残ります。これは Reader/RAG/retrieval runtime を追加せず、PostgreSQL/pgvector を有効化せず、Canon を拡張せず、Titan へ authority を移譲しません。以前の source marker は historical provenance として保持されます。

## ✅ Reader implementation boundary

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
nli_reader_runtime_filter = false
```

| Component | Status | Current boundary |
|---|---|---|
| Reader RC-1…RC-7 | ✅ Implemented | bounded Reader layers; automatic epistemic authority なし |
| Reader RC-9 | ✅ Implemented | deterministic lexical PRE-ADMISSION candidate discovery |
| Comparator v1 | 🧊 Frozen evaluation | semantic recall recovered; discrimination gate FAIL |
| NLI neutral-filter v1 | 🧊 Frozen evaluation | discrimination improved; recall-safety gate FAIL |
| RRTIC-v1 | 📐 Frozen architecture contract | typed suspicion/qualifiers; runtime provider なし |
| Guardian / TruthGate | ✅ Implemented | authority boundary; retrieval component ではない |
| TrustSnapshot / CanonicalView | ✅ Implemented | deny-dominant reconciliation / strict trusted projection |
| SQLite ordinary runtime | ✅ Active | local-first ordinary path |
| PostgreSQL/pgvector import target | ⛔ Inactive | `active=false`; normal runtime composition に入らない |
| semantic/hybrid Reader runtime | ❌ Not authorized | Reader FTS/ANN/vector backend なし |
| RRTIC runtime provider | ❌ NOT AUTHORIZED / NOT IMPLEMENTED | architecture contract only |
| NLI Reader runtime filter | ❌ NOT AUTHORIZED / NOT IMPLEMENTED | frozen failed evaluation only |
| dedicated/full autonomous Reader | ❌ Not implemented | bounded layers ≠ autonomous Reader core |

## 🛡 Authority invariants

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

RC-1…RC-7 と RC-9 の implementation は Guardian / TruthGate を bypass できません。retrieval、ranking、NLI label、typed suspicion から strict Canon authority は自動生成されません。

## 🧬 RRTIC-v1 implementation status

RRTIC-v1 は relation suspicion と structural qualifier vocabulary を freeze した architecture contract です。model execution、hard filter、reranking、identity claim、evidence admission、adjudication、truth score、accept/reject policy、Canon writer はありません。

```text
RRTIC contract implemented as architecture documentation = yes
RRTIC runtime provider = NOT AUTHORIZED / NOT IMPLEMENTED
rrtic_runtime_authorization = false
```

## 💾 Storage

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector = INACTIVE
active=false
successful import != backend activation
physical L3 != strict Canon
```

Optional PostgreSQL/pgvector surface は inactive import/equivalence path のみです。automatic switching、cutover、rollback、dual-write、Reader backend activation はありません。

## 💶 Grant truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

約 €50,000 は planning/transparency context であり approved budget や committed funding ではありません。

## 📎 Historical evidence

`bbd816c09dd39a02e6de6c1014438490572f40f6`、`2078 passed / 13 skipped / 0 failed`、`9756 statements / 100.00% line coverage` は historical compatibility evidence として保持されます。現在の repository test count ではありません。

正確な live implementation / CI state は GitHub、[`docs/STATUS.md`](../STATUS.md)、[`TEST_REPORT.md`](../../TEST_REPORT.md)、[machine-readable manifest](../status/implementation-manifest.json) から解決してください。