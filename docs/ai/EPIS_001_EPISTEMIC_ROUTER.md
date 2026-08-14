# EPIS-001 — AI Context

```yaml
contract: EPIS-001-v1
status: FROZEN_ARCHITECTURE_CONTRACT
runtime_implemented: false
runtime_authorization: false
tracking_issue: 155
rfc: docs/rfcs/RFC_EPIS_001_EPISTEMIC_ROUTER.md
machine_status: docs/rfcs/EPIS_001_STATUS.json
```

## Read this correctly

EPIS-001 defines a **future read-only evidence-state observability layer**. It does not add runtime code or pipeline wiring.

Frozen diagnostic vocabulary:

```text
KNOWN
PARTIAL
UNKNOWN
```

Never infer:

```text
KNOWN == VERIFIED truth
KNOWN == evidence admission
KNOWN == Canon authority
PARTIAL == permission to fill gaps from model priors
UNKNOWN == contradiction
EpistemicRouter == TruthGate
EpistemicRouter == CanonicalView
EpistemicRouter == Guardian
```

The exact separation is:

```text
evidence_state
  != truth_status
  != epistemic_state
  != CanonicalReadMode
  != Guardian verdict
  != TruthGate verdict
```

## Existing authority remains unchanged

```text
Guardian      → structural integrity gate
TruthGate     → L3 admission boundary
CanonicalView → strict read-time grounding projection
Trace         → provenance record, not truth proof
```

A future router may summarize coverage of already-authorized strict grounding. It may not create a second strict-canon definition, write memory, transition ESM, alter confidence/truth status, admit evidence, adjudicate contradiction, or bypass any existing gate.

## State interpretation

`KNOWN` requires explicit complete coverage of declared answer requirements by facts that independently pass strict CanonicalView. A non-empty FactsPack, high retrieval rank, high confidence, physical L3 membership, or `Validated` ESM state alone cannot establish `KNOWN`.

`PARTIAL` means some strict grounding exists but complete answer coverage is not demonstrated.

`UNKNOWN` means usable strict grounding for the declared answer scope cannot be established; malformed classification inputs must fail closed rather than become `KNOWN`.

## Current implementation truth

There is intentionally **no** `core/epistemic_router.py` and no EPIS-001 runtime call site in this milestone.

Before any future implementation work:

1. resolve live GitHub/Notion state;
2. require a separately selected runtime milestone and explicit diff plan;
3. preserve Guardian → TruthGate admission semantics and CanonicalView read authority;
4. execute the RFC's future implementation test plan;
5. do not treat this frozen architecture contract as runtime authorization.
