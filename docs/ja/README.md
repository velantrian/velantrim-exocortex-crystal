<!-- localization-index-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- current-localization-source: main@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- d1-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-status: CURRENT -->
<!-- d2-source: main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- d2-status: CURRENT -->
<!-- d3-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d3-status: CURRENT -->
<!-- d4-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d4-status: CURRENT -->
<!-- d5-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-status: CURRENT -->
# 🇯🇵 Crystal 日本語ドキュメント

日本語の公開 README と D1/D3/D4/D5 Reader-dependent detail surfaces は、現在の **post-RC-9 / post-NLI / RRTIC-v1** 公開アーキテクチャ truth に更新されています。D2 reviewer/safety と Quick Start の governing source semantics は変わっていないため、ファイル自体は変更しません。

## 🧭 ドキュメント経路

- Root: [`README.ja.md`](../../README.ja.md) — human-first project entry
- D1: [`QUICKSTART.md`](./QUICKSTART.md) — `CURRENT`（変更なし） · [`STATUS.md`](./STATUS.md) — `CURRENT` · [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) — `CURRENT`
- D2: [`REVIEWER_GUIDE.md`](./REVIEWER_GUIDE.md) — `CURRENT`（変更なし） · [`SAFETY_PRIVACY_AND_FAILURES.md`](./SAFETY_PRIVACY_AND_FAILURES.md) — `CURRENT`（変更なし）
- D3: [`ARCHITECTURE_OVERVIEW.md`](./ARCHITECTURE_OVERVIEW.md) — `CURRENT` · [`STORAGE_AND_AUTHORITY_BOUNDARIES.md`](./STORAGE_AND_AUTHORITY_BOUNDARIES.md) — `CURRENT`
- D4: [`GRANT_OVERVIEW.md`](./GRANT_OVERVIEW.md) — `CURRENT` · [`GLOSSARY.md`](./GLOSSARY.md) — `CURRENT`
- D5: [`EXTENDED_REFERENCE_GUIDE.md`](./EXTENDED_REFERENCE_GUIDE.md) — `CURRENT`

## 📎 Historical localization compatibility

過去の RC-6 localization checkpoint では、日本語の Reader-dependent 文書は `REFRESH_NEEDED` でした。この exact literal は古い executable provenance / compatibility evidence として保持されるだけで、**現在の freshness state ではありません**。現在の state は上記 D1/D3/D4/D5 `CURRENT` markers、machine manifests、translation ledger で決まります。

## 🧠 現在の Reader truth

```text
RC-1…RC-7 = bounded implemented Reader layers
RC-9 = deterministic lexical PRE-ADMISSION candidate discovery
Comparator v1 = frozen evaluation · discrimination gate FAIL
NLI neutral-filter v1 = frozen evaluation · recall-safety gate FAIL
RRTIC-v1 = architecture contract only · no runtime authorization
```

```text
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
physical L3 != strict Canon
```

English remains the primary/source language. Machine state と translation freshness は [Localization policy](../LOCALIZATION_POLICY.md) と [Translation status](../TRANSLATION_STATUS.md) を参照してください。AI / agent は [Special for AI](../ai/README.md) から開始してください。