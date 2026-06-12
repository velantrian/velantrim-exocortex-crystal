# Velantrim Crystal — Demo Index

> **Pointer note:** this file used to carry a full demo of its own; that
> content is superseded by the maintained walkthroughs below, kept in one
> place so the demos cannot drift apart.

Velantrim Crystal demonstrates one loop:

```text
ingest → classify → TruthGate → local L3 graph → retrieve → trace → answer receipt
```

Pick your path:

| Demo | Time | What it shows |
|---|---|---|
| **[docs/REVIEWER_DEMO.md](./docs/REVIEWER_DEMO.md)** | ~10 min | The reviewer fast path: ingest → evidence → trace → answer → sealed receipt → strict replay → controlled tamper check → eval gate |
| **[docs/DEMO.md](./docs/DEMO.md)** | ~30 min | Full technical walkthrough with captured output: grounded answers without an LLM, receipt replay, contradiction detection, knowledge import, curator review queue, GDPR erase + tamper-evident audit, NeuroCore telemetry, eval harness, optional HTTP layer |
| **[docs/DEMO_UI.md](./docs/DEMO_UI.md)** | — | Review UI / browser-PWA companion boundary (not the same security/provenance boundary as the core unless connected to a local backend/API) |

For installing and reproducing the audited test/eval state, see the
**Reviewer validation** section in [README.md](./README.md) and
[docs/REVIEWER_NOTES.md](./docs/REVIEWER_NOTES.md).
