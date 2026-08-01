# 🚀 Crystal Quick Start

This guide runs the local dependency-free baseline, ingests one explicit claim,
queries it through the read-only boundary and verifies a Receipt.

## Requirements

- Python 3.11 or 3.12;
- Git;
- a local filesystem location for the repository and SQLite data.

The default runtime has no mandatory LLM, embedding-provider or cloud dependency.
Development and full-test extras install optional packages used by the complete
repository test suite.

## 1. Install

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Verify the repository

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

The exact verified checkpoint and expected metrics are maintained in
[TEST_REPORT.md](../TEST_REPORT.md), not duplicated as mutable requirements in
this guide.

## 3. Select persistent local storage

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell equivalent:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

## 4. Explicitly ingest a claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

Ingest is a write operation. The claim enters operational state and is evaluated
through the configured Guardian/TruthGate admission path. The command does not
mean that Crystal independently proves the statement's objective truth; admission
remains evidence- and policy-dependent.

## 5. Query through the read-only boundary

```bash
velantrim ask "how does water behave"
```

Public `ask` uses `core.query_pipeline.query()` and must not create/update L0/L1
facts, transition ESM, write L3, operate the outbox, record episode links,
initialize an unset embedding fingerprint or store unknown candidates.

A bounded refusal is expected when strict canonical grounding is insufficient.
Refusal is a valid trust-boundary result, not necessarily a runtime error.

## 6. Create and verify a Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

A Receipt seals the query, answer and cited fact identities under a digest and
can replay citations against current memory state. It is tamper-evident; optional
HMAC signing requires a locally configured provenance key.

## 7. Run the optional API

```bash
pip install '.[api]'
velantrim-api
```

Key routes:

| Method | Route | Boundary |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | explicit admission/write path |
| `POST` | `/ask` | strict read-only query |
| `GET` | `/receipt?q=...` | read-only query plus Receipt |
| `POST` | `/verify-receipt` | Receipt replay |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

The API uses a bearer-token baseline. It is not a complete production
multi-tenant authorization model.

## 8. Run the MCP inspection surface

```bash
python -m core.mcp_server
```

MCP provides inspection-oriented tools such as read-only search, memory reports,
fact history, conflict lookup and Receipt verification. It exposes no canonical
write tool.

## Common boundary mistakes

### Querying is not ingestion

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

### Physical L3 is not strict Canon

A physical graph node may carry a non-verified or non-live state. Confident
factual answers require the strict CanonicalView projection.

### Confidence is not independent evidence

High confidence, frequent duplicate occurrence or retrieval similarity cannot by
themselves promote a claim to verified truth.

## Next documents

- [README](../README.md) — project overview and use cases.
- [Documentation map](./DOCUMENTATION_MAP.md) — routes by audience.
- [Architecture](./ARCHITECTURE.md) — normative trust boundaries.
- [Implementation status](./IMPLEMENTATION_STATUS.md) — implemented versus RFC.
- [Test report](../TEST_REPORT.md) — exact verified evidence.
- [Security policy](../SECURITY.md) and [threat model](./security/threat-model.md).
