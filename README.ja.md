# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語**   · 🇮🇳 [हिन्दी](./README.hi.md)
> 📚 [German documentation](./docs/de/README.md) · [Documentation française](./docs/fr/README.md) · [Documentación en español](./docs/es/README.md) · [Documentazione italiana](./docs/it/README.md) · [Документация на русском](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md) · [हिन्दी दस्तावेज़](./docs/hi/README.md)

### *信頼できる AI のための、検証可能・ローカルファースト・オープンソースなメモリ基盤*

`v0.3.0` · 🧪 **1713 passed / 12 skipped** · 🎯 **100% coverage** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal は、単なるチャットボットではなく、検証可能なメモリ層です。
> 事実には出典、認識論的状態、provenance メタデータが付与されます。
> canonical graph への自動登録は、Guardian + TruthGate によって制御されます。

> **正本:** 実装と grant に関する最終的な正本は GitHub `main` 上の英語文書です。
> この日本語版は、日本語話者の reviewer と contributor のための保守された翻訳です。
> 相違がある場合は、英語文書と [TEST_REPORT.md](./TEST_REPORT.md) が優先されます。

---

## 🧭 1分で分かる Crystal

Crystal は、Velantrim の公開・grant-facing コアです。

- ローカル L0/L1 operational memory;
- ローカル L3 canonical graph backend;
- Guardian と TruthGate による admission control;
- CanonicalView による grounding;
- TRACE、provenance、replayable Receipt;
- evidence span、review queue、import session;
- GDPR 関連の削除・処理制限メカニズム;
- deterministic evaluation と CI quality gate;
- optional FastAPI と read-oriented MCP surface。

Crystal は **Titan**、完全な Personal Exo-Cortex、自律的な cognitive OS、
意識プロジェクト、自己改変エージェントではありません。研究アイデアは将来の RFC に
影響する可能性がありますが、現在の runtime capability ではありません。

```text
GitHub Crystal main = 公開実装の正本
Notion Crystal       = 同期された戦略・grant マップ
Titan / Full         = 別の研究トラック
```

---

## 🛡️ Trust boundary

### Admission path

```text
input / document / agent event
→ classification and evidence
→ Guardian + TruthGate
→ L0/L1 operational memory
→ admitted L3 canonical graph
```

### HTTP query path

PR #265 で導入された HTTP query path は、admission path から明確に分離されています。

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ existing Canon only
→ CanonicalView
→ answer / bounded refusal
```

これらの HTTP surface で質問しても、L0/L1 への ingest、ESM transition、
L3 fact/edge write、outbox drain、episode link 記録、embedding fingerprint 初期化、
adaptive verification state の変更は行われません。

### 明示されている残余スコープ

- CLI `ask` と `receipt` は、従来の admission-capable compatibility path を使用します;
- `core.pipeline.run()` は引き続き利用可能です;
- MCP には明示的な canonical write tool はありませんが、search により未設定の
  embedding fingerprint が初期化される可能性があります。

詳細は英語の正本仕様
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md) を参照してください。

---

## 🧠 Memory model

| Layer | 役割 | 境界 |
|---|---|---|
| **L0** | process 内 working cache | 高速・再構築可能 |
| **L1** | SQLite/WAL operational memory | state、restriction、update |
| **L2** | pending / curator review path | 自動で canonical にはならない |
| **L3** | canonical graph | 自動登録は TruthGate 経由のみ |
| **TRACE / Receipt** | proof layer | grounding を説明し drift を検出 |

物理 graph には異なる truth status が存在し得ます。厳密な意味での Canon は、
VERIFIED、TRACE-valid、policy-allowed な projection であり、graph backend に存在する
すべての node を意味しません。

---

## 🚀 クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

基本 CLI:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

dependency-free な永続 L3 backend:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

段階的な手順は [docs/ja/QUICKSTART.md](./docs/ja/QUICKSTART.md) にあります。

---

## 🔌 Optional interfaces

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Method | Path | Contract |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | Guardian + TruthGate を通る admission |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | 現在状態に対する Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

FastAPI と Uvicorn は optional extra です。default runtime は cloud service や
外部 model provider を必須としません。

### MCP

```bash
python -m core.mcp_server
```

MCP は search、memory report、fact history、conflict lookup、Receipt verification などの
inspection-oriented tool を提供します。上記の fingerprint に関する残余境界は残ります。

---

## 🧪 Evaluation

Crystal には deterministic evaluation baseline が含まれています。

- retrieval hit@k / MRR;
- TRACE / metadata completeness;
- source-span coverage;
- Receipt replay survival;
- contradiction precision / recall;
- trust-boundary refusal check;
- CI regression floor / ceiling。

Titan の deterministic replay 実装は prior art として記録されていますが、
Crystal runtime にコピーされてはいません。将来の実装は既存の Crystal evaluation stack を
拡張し、offline・non-authoritative を維持し、funded baseline/delta rule を守る必要があります。

---

## 💶 Grant boundary

このプロジェクトは NLnet NGI0 Commons Fund に提出され、review 中です。
公開 repository は、資金提供が決定したとは主張しません。

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

merge 済みの作業は baseline であり、paid deliverable として再計上されません。
新しい cognitive、neuromorphic、Titan mechanism が Crystal grant scope に暗黙に
追加されることもありません。

日本語概要: [docs/ja/GRANT_OVERVIEW.md](./docs/ja/GRANT_OVERVIEW.md)

正本となる英語文書:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)

---

## ✅ Verification gates

| Gate | 目的 |
|---|---|
| pytest + coverage | 100% line coverage を必須とする full suite |
| Ruff | production / tooling code lint |
| Gitleaks | committed secret 検出 |
| Bandit | Python static security check |
| pip-audit | dependency vulnerability report |
| Docker build | hardened image の再現可能 build |
| eval-gate | retrieval / grounding / contradiction regression control |
| JSONL integrity | corpus structure / duplicate-id check |

これらの control はリスクを低減しますが、あらゆる defect の不存在を証明せず、
法的または security certification を構成しません。

---

## 📚 日本語 reviewer path

1. [docs/ja/REVIEWER_GUIDE.md](./docs/ja/REVIEWER_GUIDE.md)
2. [docs/ja/QUICKSTART.md](./docs/ja/QUICKSTART.md)
3. [docs/ja/STATUS.md](./docs/ja/STATUS.md)
4. [docs/ja/GRANT_OVERVIEW.md](./docs/ja/GRANT_OVERVIEW.md)
5. [docs/ja/GLOSSARY.md](./docs/ja/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — 正本となる test evidence
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — 正本となる architecture

---

## ⚖️ License and contribution

Crystal は **AGPL-3.0** で提供されます。[LICENSE](./LICENSE)、
[CONTRIBUTING.md](./CONTRIBUTING.md)、[GOVERNANCE.md](./GOVERNANCE.md)、
[SECURITY.md](./SECURITY.md)、[PRIVACY.md](./PRIVACY.md) を参照してください。

> **📊 Canon = admitted truth** · **🔗 Provenance = trust** · **🏠 Local-first = control**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](./README.hi.md)
