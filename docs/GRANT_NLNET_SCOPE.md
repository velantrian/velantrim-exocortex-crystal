<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# NLnet Scope — Crystal

**Status date:** 2026-08-12  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## Authority boundary

```text
submitted proposal        != awarded grant
planning amount           != approved budget
merged pre-agreement work != future funded delta
```

Approximate €50,000 remains planning only. No payment commitment or approved budget is claimed.

## Existing baseline

The public baseline already includes the trust/evidence/query/storage foundation plus Reader RC-0 through RC-5 because those Reader milestones merged before any agreement.

Reader RC-1/RC-2/RC-3, RC-4 and RC-5 remain bounded layers rather than a dedicated/full autonomous Reader:

- RC-1 — evidence-linked source/session skeleton;
- RC-2 — caller-supplied Structural Document Map;
- RC-3 — explicit multi-pass mechanics;
- RC-4 — source-linked proposition candidates;
- RC-5 — same-session/same-source-version exception/qualification/tension/possible-contradiction relation candidates.

RC-5 preserves exact RC-4 candidate linkage/provenance and explicit rationale but does not resolve contradictions or admit evidence.

```text
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
contradiction candidate != confirmed contradiction
```

## Baseline rule

Work merged before an agreement **cannot be budgeted again as funded delivery**. Reader RC-5 is existing baseline exactly like RC-0–RC-4.

## Potential funded delta after RC-5

RC-6 long-context strategy was separately authorized after RC-5 and is currently being implemented under issue #369 / PR #370. Until it merges, it is a current pre-agreement candidate rather than established merged baseline. Its bounded scope is deterministic same-session/same-version working sets over registered RC-4 candidates plus caller-supplied `SUMMARY` artifacts that preserve direct RC-4 leaf provenance.

RC-6 must not claim automatic summarization, model-token guarantees, comprehension proof, RC-7 cross-document identity/reasoning, evidence admission, contradiction resolution or truth/Canon/ESM authority.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

If RC-6 merges before any funding agreement, RC-6 immediately becomes existing baseline and **cannot be budgeted again**. From that point, only new work after RC-6 may be proposed as funded delta, for example:

- RC-7 cross-document reading with explicit identity/provenance rules;
- independently measured retrieval experiments after those stages, if still justified;
- release/SBOM/audit evidence;
- storage cutover/rollback/operational lifecycle;
- reviewer-facing evidence tooling.

No future-funded work may redefine RC-5 relation candidates as confirmed contradictions, redefine RC-6 summaries as evidence/truth, bypass Guardian/TruthGate, mutate Canon/ESM directly or treat similarity as identity.

## Non-claims

Crystal does not claim awarded funding, approved budget, automatic backend switching, active PostgreSQL runtime, universal truth, zero hallucinations, legal/security/GDPR certification, a dedicated/full autonomous Reader, automatic LLM contradiction detection/summarization or completed RC-7 cross-document Reader reasoning.

See [baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md) and [funding use plan](./grants/funding-use-plan.md).
