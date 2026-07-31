# Reviewer Guide — Velantrim ExoCortex (Crystal)

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md) · 🇯🇵 [日本語](../ja/REVIEWER_GUIDE.md) · 🇮🇳 **हिन्दी**

यह document reviewer को Crystal का scope, execution path, मुख्य epistemic guarantees और
स्पष्ट limitations कम समय में जाँचने देता है। यह कोई नया runtime claim नहीं जोड़ता।

## 1. Crystal क्या है

Crystal, Velantrim का **public, minimal और verifiable memory core** है।

- local-first storage;
- typed claims और TruthGate admission;
- sealed / replayable TRACE और Receipt;
- per-fact provenance / audit mechanisms;
- GDPR-oriented erasure / restriction controls;
- dependency-free default runtime;
- optional API / MCP interfaces।

## 2. Crystal क्या नहीं है

Crystal यह दावा नहीं करता:

- AGI, consciousness, autonomous mind या biological brain implementation;
- zero-hallucination guarantee;
- production-ready Titan console / Research PWA;
- NoeticCore / AttentionRouter / BICA को current runtime बताना;
- Graphiti, Neo4j, OpenAI या cloud LLM को mandatory dependency बताना;
- graph में मौजूद हर entry को verified Canon मानना;
- Full Personal Exo-Cortex को current Crystal runtime या grant deliverable बताना।

Research और cognitive concepts research / RFC-level पर हैं; वे current runtime truth नहीं हैं।

## 3. Authoritative status

- [अंग्रेज़ी Current Status](../STATUS.md)
- [Implementation Status](../IMPLEMENTATION_STATUS.md)
- [Implementation Reality Matrix](../IMPLEMENTATION_REALITY_MATRIX.md)
- [Test Report](../../TEST_REPORT.md)

यदि कोई capability authoritative source में `IMPLEMENTED` नहीं है, तो उसे unimplemented मानें।

## 4. Tests चलाना

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest
```

CI 100% line coverage gate enforce करता है। सटीक count के लिए `TEST_REPORT.md` authoritative है।

## 5. Docker सुरक्षित रूप से चलाना

```bash
export VELANTRIM_API_TOKEN=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
docker compose up --build
curl http://127.0.0.1:8000/health
```

जाँचें:

- token न हो तो fail-closed;
- host loopback publish;
- non-root runtime user;
- named-volume data default;
- image में secrets, local DB, tests या dev extras शामिल न हों।

## 6. Epistemic behavior की जाँच

### TruthGate

Strict policy production default है। केवल `ENABLE_TRUTH_POLICY=off` legacy bypass enable करता है।
`LLM_OUTPUT` अकेले `WORLD_FACT` के रूप में Canon में automatically admitted नहीं होता।

```bash
velantrim invariant-check
```

`invariant-check` existing L3 state का read-only scan है। यह TruthGate admission स्वयं execute नहीं करता।
Authoritative behavior proof `tests/test_truth_gate.py` है।

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

`history` truth-maintenance graph edges पढ़ता है। यह per-fact `ProvenanceChain` के समान view नहीं है।

### Accountable override

Blocked fact का curator force-override, `review_force_approve` और concrete `gate_reason` के साथ record होता है।
Override silent नहीं होता।

## 7. HTTP read-only boundary

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ existing Canon only
→ CanonicalView
→ answer / bounded refusal
```

यह guarantee केवल HTTP `/ask` और `/receipt` तक सीमित है। CLI compatibility path और MCP residual scope तक
इसी zero-mutation claim का विस्तार न करें।

## 8. मुख्य limitations

- `ProvenanceChain` lifecycle wiring में erase path के बाहर follow-up बाकी है;
- knowledge graph data verifier future work है;
- canonical write-path expansion सीमित है;
- RRF rank fusion helper `retrieve()` से connected नहीं है;
- Research Mode / Noetic / Titan console / PWA / BICA runtime नहीं हैं।

## 9. Reviewer checklist

- [ ] diff केवल Markdown है;
- [ ] technical identifiers बदले नहीं गए;
- [ ] relative links सही हैं;
- [ ] हिन्दी claim अंग्रेज़ी authoritative source से अधिक मजबूत नहीं है;
- [ ] funding award, certification या production readiness का नया दावा नहीं है;
- [ ] runtime checkpoint और localization sync marker अलग रखे गए हैं;
- [ ] full CI green है।

## 10. सुझाया reading order

1. [QUICKSTART.md](./QUICKSTART.md)
2. [STATUS.md](./STATUS.md)
3. [GLOSSARY.md](./GLOSSARY.md)
4. [अंग्रेज़ी Reviewer Demo](../REVIEWER_DEMO.md)
5. [Test Report](../../TEST_REPORT.md)
6. [अंग्रेज़ी Architecture](../ARCHITECTURE.md)

---

> 🌐 🇬🇧 [English](../REVIEWER_GUIDE.md) · 🇩🇪 [Deutsch](../de/REVIEWER_GUIDE.md) · 🇫🇷 [Français](../fr/REVIEWER_GUIDE.md) · 🇪🇸 [Español](../es/REVIEWER_GUIDE.md) · 🇮🇹 [Italiano](../it/REVIEWER_GUIDE.md) · 🇷🇺 [Русский](../ru/REVIEWER_GUIDE.md) · 🇨🇳 [简体中文](../zh-CN/REVIEWER_GUIDE.md) · 🇸🇦 [العربية](../ar/REVIEWER_GUIDE.md) · 🇯🇵 [日本語](../ja/REVIEWER_GUIDE.md) · 🇮🇳 **हिन्दी**
