# Reviewer Guide — Velantrim ExoCortex (Crystal)

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/REVIEWER_GUIDE.md)

この文書は reviewer が Crystal の範囲、実行方法、主要な epistemic guarantee、
明示された limitation を短時間で確認するための経路です。新しい runtime claim は追加しません。

## 1. Crystal とは何か

Crystal は Velantrim の **公開・最小・検証可能な memory core** です。

- local-first storage;
- typed claim と TruthGate admission;
- sealed / replayable TRACE と Receipt;
- per-fact provenance / audit mechanism;
- GDPR-oriented erasure / restriction control;
- dependency-free default runtime;
- optional API / MCP interface。

## 2. Crystal ではないもの

Crystal は次を主張しません。

- AGI、意識、自律的な mind、biological brain implementation;
- zero hallucination guarantee;
- production-ready Titan console / Research PWA;
- NoeticCore / AttentionRouter / BICA を現在の runtime とすること;
- Graphiti、Neo4j、OpenAI、cloud LLM を mandatory dependency とすること;
- graph に存在する全 entry が verified Canon であること;
- Full Personal Exo-Cortex を現在の Crystal runtime または grant deliverable とすること。

研究・cognitive concept は research / RFC-level であり、現在の runtime truth ではありません。

## 3. 正本となる status

- [英語 Current Status](../STATUS.md)
- [Implementation Status](../IMPLEMENTATION_STATUS.md)
- [Implementation Reality Matrix](../IMPLEMENTATION_REALITY_MATRIX.md)
- [Test Report](../../TEST_REPORT.md)

capability が正本で `IMPLEMENTED` とされていない場合、未実装として扱ってください。

## 4. Test の実行

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest
```

CI は 100% line coverage gate を強制します。正確な count は `TEST_REPORT.md` が正本です。

## 5. Docker の安全な実行

```bash
export VELANTRIM_API_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

確認点:

- token がなければ fail-closed;
- host loopback publish;
- non-root runtime user;
- named-volume data default;
- secret、local DB、test、dev extra を image に含めない。

## 6. Epistemic behavior の確認

### TruthGate

`LLM_OUTPUT` は、それ単独では `WORLD_FACT` として admission されません。
この Ring Zero rule は non-configurable です。旧 `ENABLE_TRUTH_POLICY` の値
（`off` を含む）は現在 inert で、process environment から無効化できません。
Test、demo、migration は gate を弱めず、正直な independent provenance または
適切な non-world-fact type を使用する必要があります。

正本となる behavior proof は `tests/test_truth_gate.py`、decision record は
[`ADR-011`](../adr/ADR-011-NON_CONFIGURABLE_TRUTH_POLICY.md) です。

```bash
velantrim invariant-check
```

`invariant-check` は既存 L3 state の read-only scan です。TruthGate admission 自体を
実行しないため、この command だけでは LLM-origin block の proof になりません。

### Receipt

```bash
velantrim receipt "your question" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

### Audit / history

```bash
velantrim history <fact_id>
velantrim audit
velantrim audit-verify
```

`history` は truth-maintenance graph edge を読みます。per-fact `ProvenanceChain` と同一の view ではありません。

### Accountable override

blocked fact の curator force-override は `review_force_approve`、actor、reason、
具体的な `gate_reason` とともに記録されます。override は TruthGate decision を
変更せず、別の明示的 governance action です。

## 7. Read-only query boundary

```text
HTTP /ask, /receipt
CLI ask, receipt
MCP search
→ core.query_pipeline
→ existing L3 facts only
→ CanonicalView for confident answers
→ answer / bounded refusal / inspection rows
```

これらの query/search surface は L0/L1 fact を作成せず、ESM transition、L3 mutation、
outbox operation、episode recording、unset embedding fingerprint initialization を行いません。
MCP search は inspection surface であり、全 L3 node が strict Canon であるという claim ではありません。

## 8. 主要 limitation

- `ProvenanceChain` lifecycle wiring は erase path 以外に follow-up が残る;
- knowledge graph data verifier は future work;
- physical L3 と strict CanonicalView は同一ではない;
- adaptive confidence threshold は context-dependent のまま;
- Research Mode / Noetic / Titan console / PWA / BICA は runtime ではない。

## 9. Reviewer checklist

- [ ] technical identifier が変更されていないか;
- [ ] relative link が正しいか;
- [ ] 日本語 claim が英語正本より強くなっていないか;
- [ ] funding award、certification、production readiness を追加していないか;
- [ ] runtime checkpoint と localization sync marker を混同していないか;
- [ ] full CI が green か。

## 10. 推奨読書順

1. [QUICKSTART.md](./QUICKSTART.md)
2. [STATUS.md](./STATUS.md)
3. [GLOSSARY.md](./GLOSSARY.md)
4. [英語 Reviewer Demo](../REVIEWER_DEMO.md)
5. [Test Report](../../TEST_REPORT.md)
6. [英語 Architecture](../ARCHITECTURE.md)

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](../hi/REVIEWER_GUIDE.md)
