# Velantrim Crystal — Verifiable Memory Demo

This demo shows the core promise of Velantrim Crystal:

```text
ingest → classify → TruthGate → local L3 graph → retrieve → trace → answer receipt
```

It is intentionally local-first. The default runtime has no mandatory cloud
service, no telemetry and no required LLM call. An LLM can be added later for
phrasing, but the memory, facts, provenance and verification path remain inside
the local core.

## 1. Install

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install .
```

For development and tests:

```bash
pip install -r requirements-dev.txt
pip install -e .
pytest tests/ -v --cov=core --cov-fail-under=95
```

## 2. Ingest a fact

```bash
velantrim ingest "Water boils at 100C at sea level"
```

Expected shape:

```json
{
  "accepted": true,
  "reinforced": false,
  "fact_id": "...",
  "claim_type": "WORLD_FACT",
  "truth_status": "UNVERIFIED",
  "conflicts": []
}
```

The fact is first handled as a claim, not as eternal truth. It is typed,
source-tagged and routed through the same validation path used by the rest of the
system.

## 3. Ask from local memory

```bash
velantrim ask "how does water behave at sea level"
```

The default answerer can answer extractively from local memory. No LLM is needed
for the correctness of the retrieved fact.

## 4. Generate a replayable receipt

```bash
velantrim receipt "how does water behave at sea level" > receipt.json
cat receipt.json
```

The receipt links the answer back to the facts and trace material used to produce
it. This is the audit layer: a downstream system can ask not only *what did the
AI answer?* but also *which local facts supported that answer?*

## 5. Verify the receipt

```bash
velantrim verify-receipt receipt.json
```

Verification detects whether the receipt still matches the local canon. If a fact
is later erased, changed, contradicted or restricted, replay/verification can show
that drift.

## 6. Import a small knowledge file

Create a file:

```bash
mkdir -p knowledge
cat > knowledge/astronomy.md <<'EOF'
# Astronomy notes
- The Earth orbits the Sun.
- The Moon orbits the Earth.
EOF
```

Import it:

```bash
velantrim learn ./knowledge/astronomy.md --source astro-101
```

Expected shape:

```json
{
  "source": "astro-101",
  "total": 2,
  "accepted": 2,
  "reinforced": 0,
  "blocked": 0,
  "fact_ids": ["...", "..."],
  "blocked_reasons": []
}
```

The imported claims are tagged with `source_status = EXTERNAL` and routed through
the TruthGate. Supported dependency-free formats are `.txt`, `.md`, `.json`,
`.jsonl`, `.ndjson` and `.csv`.

## 7. Use persistent local L3 storage

The default backend mode is `auto`:

```text
auto → LadybugDB if installed → on-disk SQLite → in-memory mock
```

For a dependency-free persistent canon, select SQLite explicitly:

```bash
mkdir -p data
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ingest "Vienna is the capital of Austria"
```

Ask later with the same environment:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "what is the capital of Austria"
```

## 8. Erase or restrict a fact

Velantrim includes GDPR-relevant data-subject operations. After you have a
`fact_id`:

```bash
velantrim erase <fact_id> --reason data_subject_request
velantrim erasures
```

Restriction is also available:

```bash
velantrim restrict <fact_id>
velantrim unrestrict <fact_id>
velantrim ropa
```

These actions are recorded in the tamper-evident audit path.

## 9. Read-only MCP memory server

Crystal can expose read-only memory tools to MCP clients:

```bash
python -m core.mcp_server
```

The server is intentionally read-only by default. It lets an agent search,
inspect facts, review history, find conflicts and verify receipts without giving
that agent write access to the canon.

## 10. What this demo proves

| Claim | Demonstrated by |
|---|---|
| Local-first memory | Standard-library runtime, local SQLite and in-memory modes |
| LLM-optional answers | Extractive answerer and local retrieval |
| Graph = Truth | L3 canon is written only through the validation path |
| Provenance-first memory | `source`, `source_status`, trace and receipts |
| External knowledge ingestion | `velantrim learn` through the TruthGate |
| GDPR-relevant control | erase, restrict, record-of-processing and audit log |
| Agent integration | read-only MCP server |

## 11. What this demo does not claim

- It does not claim “zero hallucinations”. It provides provenance and gating so
  unsupported claims cannot silently become canonical memory.
- It does not claim absolute security. It is local-first and auditable, but real
  deployments still need host security, backups, access control and operational
  review.
- It does not require an LLM. If an LLM is connected, it is an optional language
  layer above the memory core.

## Related prototype

Browser/PWA companion prototypes may visually demonstrate the same direction:
local browser memory, notes, files, AI provider settings and offline behaviour.
Those prototypes are not the same security or provenance boundary as this
Crystal core unless connected to a local backend/API.
