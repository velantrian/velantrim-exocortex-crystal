# 🧪 Velantrim Crystal — Test & Verification Report

**Status date:** 2026-08-14  
**Current signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — `verified=true`, reason `valid`  
**Architecture milestone:** Reader Retrieval Typed Inspection Contract v1 / PR #392  
**Exact validated RRTIC PR head:** `a39dc1b624254c99d1955fc77d916488d76f76c0`  
**RRTIC exact-head CI:** `31754798549` — **9/9 SUCCESS**  
**RRTIC post-merge CI:** `31771677028` — **9/9 SUCCESS**  
**Repository-head rule:** resolve live GitHub for the newest docs-only merge SHA; this report keeps architecture/runtime verification checkpoints distinct from later documentation reconciliation.

## RRTIC architecture checkpoint verification

The RRTIC-v1 post-merge push workflow completed all nine permanent CI jobs successfully:

```text
code-quality                  SUCCESS
Python 3.11                   SUCCESS
Python 3.12                   SUCCESS
jsonl-integrity               SUCCESS
eval-gate                     SUCCESS
security                      SUCCESS
docker-build                  SUCCESS
Ring Zero mutation gate       SUCCESS
docs-status                   SUCCESS
```

Python 3.11 exact RRTIC post-merge result:

```text
2244 collected
2231 passed
13 skipped
0 failed
11997 measured statements
0 missed statements
100.00% measured line coverage
```

Python 3.12 also completed successfully under the same exact RRTIC post-merge workflow. This report does not invent an independent count where the workflow conclusion is the evidence being cited.

## What this verification means

The cited architecture checkpoint verifies the repository state after RRTIC-v1 was frozen and merged. RRTIC-v1 itself is an architecture/research contract plus structural evidence tests; it is **not** a new Reader runtime provider. The separate post-RRTIC documentation reconciliation is validated by its own PR exact-head and post-merge CI and does not redefine these architecture/runtime numbers.

```text
RRTIC-v1 frozen contract        VERIFIED
runtime_authorization           false
semantic/hybrid Reader runtime  NOT AUTHORIZED
NLI runtime filter              NOT AUTHORIZED
Reader FTS / ANN / vector DB    NOT AUTHORIZED
PostgreSQL/pgvector Reader      active=false
```

The current Reader implementation baseline remains bounded RC-1…RC-7 plus RC-9 deterministic lexical PRE-ADMISSION candidate discovery. Comparator v1 and NLI neutral-filter v1 remain frozen evaluation evidence with failed gates.

## Retained storage-runtime verification checkpoint — PR #337

The earlier storage/runtime compatibility checkpoint remains immutable evidence rather than being rewritten as current-head validation:

```text
signed runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
validated PR head:          d7af7c80722274f9217bc5545d150f92e9363f37
exact-head CI:              31256316536
PostgreSQL integration CI:  31256316532
```

Historical exact-head Python result at that checkpoint:

```text
2078 passed
13 skipped
0 failed
9756 measured statements
100.00% measured line coverage
```

PostgreSQL 16 + pgvector verification at that checkpoint established inactive import/equivalence only. It did not establish active PostgreSQL runtime, automatic backend switching, cutover, dual-write or Reader vector runtime.

## Reader evaluation evidence retained

### RC-9 lexical baseline

```text
Recall@5:                  0.937500
Precision@5:               0.187500
MRR:                       0.895833
Useful hits:               15 / 16
Paired hard-negative hits:  4 / 4
classification:            LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

### Evaluation Surface v2

Frozen surface SHA-256:
`753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`

RC-9 control: useful `42/48`, Recall@5 `0.875000`, MRR `0.857639`, hard negatives `38/48`.

### Comparator v1

Comparator v1 recovered `48/48` useful v2 candidates but surfaced `41/48` hard negatives.
Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

### NLI neutral-filter v1

NLI v1 reduced v2 hard-negative hits to `18/48`, but useful hits regressed to `46/48`; frozen recall-safety/admission gates failed.
Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

These measurements are retrieval/evaluation evidence only. They are not truth accuracy, proposition-identity accuracy or runtime authorization.

## Authority verification boundary

```text
retrieval match          != evidence
similarity               != identity
NLI label                != proposition identity
NLI contradiction        != contradiction adjudication
RRTIC suspicion          != adjudicated relation
qualifier mismatch       != truth decision
candidate discovery      != candidate adjudication
evaluation pass          != runtime authorization
```

## Reproduce locally

```bash
python -m pip install -e '.[dev]'
pytest tests/
python scripts/eval_gate.py --out-dir eval-artifacts
```

Reproduce the frozen RC-9 lexical benchmark:

```bash
python scripts/bench_reader_rc9_lexical.py \
  --corpus eval/reader_rc8_retrieval_adversarial.jsonl \
  --k 5 \
  --json-out /tmp/reader-rc9-lexical.json
```

## Current non-claims

This verification does not claim:

- a dedicated/full autonomous Reader;
- semantic/hybrid Reader runtime;
- an NLI/CrossEncoder/RRTIC runtime provider;
- automatic proposition identity, contradiction adjudication or evidence admission;
- Reader FTS/ANN/vector DB or active PostgreSQL/pgvector;
- security/legal/GDPR certification;
- awarded NLnet funding.

NLnet remains **submitted / under review / not awarded**; approximate €50,000 is planning context only.
