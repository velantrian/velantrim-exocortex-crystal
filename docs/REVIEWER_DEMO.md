# Velantrim Crystal — 10-Minute Reviewer Demo

A hands-on path for a first-time reviewer. In about ten minutes you will see
the full trust loop of Velantrim Crystal on your own machine, offline, with no
LLM and no cloud service:

```text
ingest → evidence → trace → answer → receipt → strict replay → tamper check → eval gate
```

All command output below was **captured at the current audited baseline** (see
[TEST_REPORT.md](../TEST_REPORT.md)). Fact ids are content-derived and
deterministic; timestamps will differ on your machine.

## What this demo proves

- A factual answer can be produced **without any LLM**, grounded in local,
  typed memory.
- Every stored claim carries machine-readable `claim_type`, `source_status`
  and `truth_status` — a user statement is `USER_CLAIMED`, not silently
  "true"; an externally sourced claim with evidence reaches `VERIFIED`.
- Answers come with a sealed, replayable **receipt** whose citations point to
  evidence spans — and a modified receipt is detected, not trusted.
- The same trust boundaries are **enforced in an evaluation gate**, not only
  described in documentation.

## Prerequisites

Python 3.11+, git, a POSIX shell (on Windows, use WSL or adapt the
`venv` activation line).

## Clean setup

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .                       # stdlib-only runtime, no extras needed
mkdir -p demo-data
export VELANTRIM_DB=./demo-data/l1.db
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./demo-data/l3.db
```

The environment variables isolate the demo in `demo-data/` (git-ignored),
so nothing touches your real data and `git status` stays clean.

> You may see `auto embedder: sbert unavailable … falling back to
> HashingEmbedder` on stderr — that is the expected dependency-free default,
> not an error.

## Step 1 — Ingest a claim

```bash
velantrim ingest "The Eiffel Tower is in Paris."
```
```json
{"accepted": true, "reinforced": false, "fact_id": "ing:fe37d9fe9778",
 "claim_type": "WORLD_FACT", "truth_status": "USER_CLAIMED", "conflicts": []}
```

The claim passed classification and the TruthGate — but note the honesty:
a user statement about the world is stored as **`USER_CLAIMED`**, not
`VERIFIED`. Verification requires an independent source.

## Step 2 — Ask, and get an answer without an LLM

```bash
velantrim ask "Where is the Eiffel Tower?"
```
```text
The Eiffel Tower is in Paris.
```

No model was called: the default answerer is extractive and deterministic.
The graph, not a language model, is the source of the answer.

## Step 3 — Inspect the typed canon

```bash
velantrim report
```
```text
MEMORY REPORT (L3 canonical graph)
  facts: 1  avg_confidence=0.6  avg_significance=0.5
  epistemic_state: {'Validated': 1}
  claim_type:      {'WORLD_FACT': 1}
  truth_status:    {'USER_CLAIMED': 1}
  edges:           0 {}
  contradicted:    0
  deprecated:      0
  weak confidence: 0
```

Memory is observable: every fact's epistemic state and truth status is
visible in one call.

## Step 4 — Import sourced knowledge (evidence spans)

```bash
cat > demo-data/notes.md <<'EOF'
Water boils at 100 degrees Celsius at sea level.
EOF
velantrim learn demo-data/notes.md
```
```json
{"source": "notes.md", "total": 1, "accepted": 1, "reinforced": 0, "blocked": 0,
 "fact_ids": ["ing:ac6d9bb4f5da"], "blocked_reasons": [],
 "session_id": "imp:dcf3ebec1a35"}
```

Imported claims go through the **same** Guardian → TruthGate path as user
utterances, carry `source_status = EXTERNAL` with the file as provenance, and
get a source-span evidence record.

## Step 5 — Get a sealed receipt for an answer

```bash
velantrim receipt "what temperature does water boil at" > demo-data/receipt.json
head -c 600 demo-data/receipt.json
```
```json
{
  "version": 2,
  "created_at": "…",
  "query": "what temperature does water boil at",
  "answer": "Water boils at 100 degrees Celsius at sea level.",
  "citations": [
    {
      "fact_id": "ing:ac6d9bb4f5da",
      "claim_sha256": "dabc3f821a47cfa826bdf66cee6237b19b119414bd464d8a4e1317f0574c0124",
      "source": "notes.md",
      "epistemic_state": "Validated",
      "truth_status": "VERIFIED",
      "evidence": [ { "evidence_id": "ev:6b1e6edbd784", "source_uri": "notes.md", … } ]
```

Two things to notice: the externally sourced claim reached **`VERIFIED`**
(unlike the user claim in Step 1), and the receipt seals the citation with a
content hash plus its exact evidence span. The receipt is identified by its
content digest — there is no separate receipt id to spoof.

## Step 6 — Strict replay: re-verify the receipt against the canon

```bash
velantrim verify-receipt demo-data/receipt.json --strict-provenance
```
```json
{"digest_valid": true, "signature_valid": null,
 "citations": [{"fact_id": "ing:ac6d9bb4f5da", "status": "ok",
   "evidence": [{"evidence_id": "ev:6b1e6edbd784", "source_uri": "notes.md", "status": "ok"}]}],
 "summary": {"ok": 1}, "verified": true}
```

With `--strict-provenance`, a VERIFIED citation must still be backed by
source-span evidence — otherwise the replay fails.

## Step 7 — Controlled receipt-integrity check (on a copy)

A controlled tamper demonstration on a **copied** receipt: change one number
in the copy and replay it.

```bash
cp demo-data/receipt.json demo-data/tampered.json
python - <<'PY'
from pathlib import Path
p = Path("demo-data/tampered.json")
p.write_text(p.read_text().replace("100 degrees", "50 degrees"), encoding="utf-8")
PY
velantrim verify-receipt demo-data/tampered.json --strict-provenance
```
```json
{"digest_valid": false, "signature_valid": null,
 "citations": [{"fact_id": "ing:ac6d9bb4f5da", "status": "ok", "evidence": [{"…": "ok"}]}],
 "summary": {"ok": 1}, "verified": false}
```

The sealed fields no longer hash to the recorded digest: **`digest_valid:
false`, `verified: false`**. A modified answer cannot silently keep its
proof.

## Step 8 — Run the evaluation gate

```bash
python scripts/eval_gate.py --out-dir eval-artifacts
```
```text
Velantrim evaluation gate
  cases:        22
  retrieval:    hit@1=0.9091 hit@3=0.9545 hit@5=1.0 mrr=0.9356
  grounding:    trace=1.0 metadata=1.0 span=1.0 receipts=1.0 unsupported=0
  contradiction: precision=0.8889 recall=1.0 fpr=0.1429
  boundary:     cases=15 refusal_correctness=1.0 violations=0
✅ quality gate PASSED
```

The gate runs in its own isolated, ephemeral canon (your demo data is not
touched) and **enforces** the trust boundaries you just saw by hand: 15
boundary cases pin abstention on unsupported queries, the LLM_OUTPUT
promotion ban and subjective-claim typing — `violations = 0` is a hard
ceiling, not a report.

## Expected result

```bash
git status --short      # → clean (demo data and eval artifacts are ignored)
```

Tests pass at the audited baseline ([TEST_REPORT.md](../TEST_REPORT.md)), the
eval gate prints `PASSED`, and the working tree stays clean.

## What this demo does NOT claim

- It does not claim zero hallucinations or guaranteed truth — it shows that
  unsupported claims are **labelled, blocked or auditable** rather than
  silently promoted.
- It does not claim production readiness, AGI, consciousness or brain-like
  cognition.
- The LLM (if you later attach one) remains a speech layer: it may phrase
  answers, it never becomes the source of truth.

## Where to go next

- [docs/DEMO.md](./DEMO.md) — the full technical walkthrough (contradictions,
  curator review queue, GDPR erasure, NeuroCore telemetry, HTTP layer).
- [docs/REVIEWER_OVERVIEW.md](./REVIEWER_OVERVIEW.md) — the one-page reviewer
  overview with the implementation-status table.
- [docs/DEMO_UI.md](./DEMO_UI.md) — the review UI / PWA companion boundary.