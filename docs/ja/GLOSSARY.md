# 📖 用語集 — Velantrim Crystal

> 🌐 🇬🇧 [English](../GLOSSARY.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/GLOSSARY.md)

この用語集は、日本語文書で使用する説明を統一します。contract identifier、code symbol、
CLI command、active environment variable、API path は翻訳しません。

| 用語 | 日本語での説明 |
|---|---|
| **Canon** | verified、TRACE-valid、policy-allowed な canonical projection。graph に存在する全 node ではない。 |
| **CanonicalView** | query 時に policy と verification boundary を適用して Canon を投影する view。 |
| **TruthGate** | claim の automatic admission を判定する side-effect-free gate。absolute truth oracle ではない。 |
| **Guardian** | admission path の structural / safety contract check。 |
| **TRACE** | answer grounding と provenance を説明する proof-oriented trace。 |
| **Receipt** | answer と evidence state を封印し、後から replay / verify できる record。 |
| **Provenance** | fact、source、transition、review、erase などの来歴情報。 |
| **ProvenanceChain** | per-fact append-only hash-chained lifecycle record。現在の wiring 範囲は英語 status を参照。 |
| **Evidence span** | claim を支持する source 内の具体的な範囲。 |
| **Claim** | source、epistemic state、metadata を持つ候補情報。自動的に Canon とは限らない。 |
| **WORLD_FACT** | external world に関する claim type。admission policy を通過する必要がある。 |
| **LLM_OUTPUT** | model output 起源の source status。単独では `WORLD_FACT` admission の independent evidence にならない。 |
| **L0** | process 内 working cache。高速で再構築可能。 |
| **L1** | SQLite/WAL operational memory。state、restriction、update を保持。 |
| **L2** | pending / curator review path。自動で Canon に入らない。 |
| **L3** | graph-backed multi-status memory。physical L3 は strict Canon と同一ではない。 |
| **Admission** | claim を operational / graph state に受け入れる write-capable process。 |
| **Read-only query** | HTTP `/ask`/`/receipt`、CLI `ask`/`receipt`、MCP search の zero-durable-mutation contract。 |
| **Bounded refusal** | evidence または policy boundary が不足する場合に、推測で埋めず限定的に拒否すること。 |
| **Outbox** | deferred write / delivery workflow に使われる operational mechanism。read-only query は操作しない。 |
| **ESM** | epistemic state machine。claim state transition を表す。 |
| **Embedding fingerprint** | embedding configuration/state の整合性確認に使う fingerprint。read-only query は unset fingerprint を初期化しない。 |
| **Audit log** | erase、restriction、override などの accountable event record。 |
| **Gate reason** | TruthGate が block した具体的な理由。force-approve audit に保持される。 |
| **Ring Zero policy** | runtime configuration から弱められない load-bearing invariant。 |
| **Baseline** | grant proposal より前に `main` へ merge 済みの、現在の実装・evidence。 |
| **Funded delta** | baseline から区別され、測定可能かつ独立検証可能な将来 deliverable。 |
| **Runtime checkpoint** | audited implementation behavior を示す commit。localization sync marker とは別。 |
| **Localization sync marker** | 翻訳が同期された `main` の短い commit marker。runtime behavior claim ではない。 |
| **Titan** | Crystal とは分離された研究トラック。現在の Crystal runtime または自動的な grant scope ではない。 |
| **Full Personal Exo-Cortex** | 長期研究 vision。public Crystal baseline と同一ではない。 |

## 翻訳しない identifier

```text
TruthGate
Guardian
CanonicalView
TRACE
Receipt
Canon
ProvenanceChain
L0 / L1 / L2 / L3
WORLD_FACT
LLM_OUTPUT
VELANTRIM_L3_BACKEND
VELANTRIM_L3_PATH
VELANTRIM_API_TOKEN
```

`ENABLE_TRUTH_POLICY` は historical identifier です。現在の runtime はこれを読みません。
`off` を含む旧値は inert であり、TruthGate policy を変更しません。

## 表現上の注意

- 「Canon」を単に「すべての graph data」と訳さない;
- 「verified」を「絶対に真」と強めない;
- 「TruthGate」を objective truth detector と表現しない;
- 「GDPR-relevant mechanism」を「GDPR certified」と訳さない;
- 「security control」を「security certification」と訳さない;
- 「under review」を「funding awarded」と訳さない;
- read-only guarantee は HTTP、CLI query command、MCP search に適用されるが、write command や legacy internal `pipeline.run()` に拡張しない。

---

> 🌐 🇬🇧 [English](../GLOSSARY.md) · 🇩🇪 [Deutsch](../de/GLOSSARY.md) · 🇫🇷 [Français](../fr/GLOSSARY.md) · 🇪🇸 [Español](../es/GLOSSARY.md) · 🇮🇹 [Italiano](../it/GLOSSARY.md) · 🇷🇺 [Русский](../ru/GLOSSARY.md) · 🇨🇳 [简体中文](../zh-CN/GLOSSARY.md) · 🇸🇦 [العربية](../ar/GLOSSARY.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/GLOSSARY.md)
