# Governed environment and replaceable models

**Role:** design intent and integration review guide, recorded 2026-11-09.
**Status:** documentation proposal; the integration requirements below do not
establish a new runtime, policy owner, enabled feature or verified guarantee.
Existing repository contracts and exact implementation evidence remain authoritative.

## Purpose

Crystal and Titan are developed as components of an environment for working with
replaceable language models. The environment organizes memory, evidence, graph
relationships, tools and permitted effects. A model may interpret, extract, propose
and render; its output does not grant permission to change trusted state.

Model quality still affects usefulness. Replacing a model should preserve the
required admission and action boundaries, not promise identical answers.

## Project roles and relationship

| Component | Responsibility | Boundary |
|---|---|---|
| Crystal | Local evidence/memory infrastructure, explicit admission, strict read views, provenance, TRACE and receipts | Owns its local state and its existing admission rules |
| Titan | Memory and orchestration runtime, retrieval, model/provider and tool calls, local policy/write and provenance mechanisms | Has its own memory; calling Titan does not automatically call Crystal |
| Crystal-Test | Separate laboratory for bounded experiments, including question parsing and context-transfer probes | Laboratory evidence does not establish a merged production integration |

Code reused between projects is not a live service connection. A bridge must name
the owner of each state and operation. Neither repository's local authority
automatically becomes global authority over the other.

Dated source checkpoints for this explanation:

- [Crystal ba8e84a](https://github.com/velantrian/velantrim-exocortex-crystal/tree/ba8e84a4f8f24bdb816ea8fb89485f1dedccd0a3):
  public reads through `core/query_pipeline.py`, explicit object/time applicability
  and evidence/receipt boundaries.
- [Titan 6b45854](https://github.com/velantrian/Velantrim-ExoCortex-Titan/tree/6b45854f57ca90516b86b2c48b284c88857bc2c2):
  independent memory/query paths and optional context limits.
  `ContextReport.sent_facts(facts)` is an internal method; the serialized
  `context_report` is not an exact final-provider-payload journal.
- [Crystal-Test PR #15](https://github.com/velantrian/Velantrim-Exo-Cortex-Crystal-Test/pull/15),
  reviewed snapshot `ceed51c797a79f3a08ddfd7f6e2c38bd6eae585e):
  a laboratory harness directly calls the parser and applicability selector,
  substitutes Titan retrieval and captures prepared messages with a fake provider.
  It does not exercise the complete ordinary Crystal read/admission/receipt path
  or establish real-model answer correctness.

These are fixed evidence references, not evergreen repository-head or PR-status
claims. Re-resolve live state before implementation or deployment decisions.

## Governing principle

A protected change requires positive satisfaction of the applicable permission,
evidence, scope and state-transition contract. The system need not first diagnose
a model as "drifting". Instructions in a prompt assist the model; enforcement
belongs at the owning tool/write boundary, under existing owners.

A candidate can be durably recorded as a candidate with attribution. Persistence
does not promote it to Canon. Proposed graph relationships require their own
applicable admission path. Corrections retain lineage; erasure and retention
continue to follow the existing contract.

Missing evidence and an unavailable mandatory checker are different outcomes.
Neither should silently authorize a protected operation. An authorized operation
whose checks pass can proceed without inventing a new approval step.

For example: a model proposes changing "bridge M is closed" to "open". Without
the required applicable evidence, reject that change and preserve an attributed
proposal/reason where the retention policy permits it. With new admissible
evidence, permit the existing correction procedure. Protecting stored state does
not by itself establish that the user-facing answer is supported.

## Requirements to verify in a future bridge

1. Explicitly assign state ownership and preserve source, claim, object, time,
   restrictions and evidence references. Do not turn a copied confidence or status
   into new evidence.
2. Exercise the normal Crystal evidence/admission/read boundaries; a direct call
   to an applicability function establishes only that function's behavior.
3. Keep the selected evidence distinguishable from Titan's own retrieval or
   auto-save effects. Capture the exact prepared provider messages separately
   from a summary report, and distinguish preparation from delivery/outcome.
4. Define the empty-ground and clarification outcomes. A status request with no
   admissible grounds must not become an unsupported asserted status.
5. Preserve what a Crystal receipt actually attests. It does not automatically
   attest a new model-generated answer or prove semantic use of a source.
6. Apply the owning mutation contract at commit time, with its concurrency,
   recovery, audit and receipt obligations. Inspect background/projection writers
   as well as interactive tools; do not introduce another global policy engine.

These are proposed integration acceptance requirements. This document neither
implements a bridge nor claims that all writer paths have been verified.

## Evaluation

Keep frozen regressions and add unseen materials after fixing criteria. First use
controlled provider outputs to test admitted/rejected operations, unavailable
checks and unchanged state after rejection. Then exercise the complete read,
prompt, answer and permitted-write path with exact version/configuration records.

Measure both violations that escape and useful permitted work that is wrongly
blocked. A system that refuses every operation does not meet the objective.
Model replacement requires repeating the applicable contract and end-to-end checks.

Structural checks can enforce bounded contracts. General semantic truth remains
fallible; agreement between models is not independent evidence. Passing every case
in a finite suite is evidence for that suite, not proof of universal correctness.

## Maintenance

This public explanation is self-contained. Deeper rationale is recorded in the
Notion page titled "Основной принцип Velantrim — управляемая среда и сменяемые модели".
No private workspace access is required to review this document.

The corresponding document in the other repository records the same shared
principle. Coordinate changes to shared meaning while retaining local owners and
repository-specific evidence. Experimental results belong with their exact
artifacts and versions; updating this text does not advance runtime checkpoints.
