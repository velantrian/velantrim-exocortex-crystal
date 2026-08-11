<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# Crystal Glossary

**Status date:** 2026-08-11

## Authority and storage

**Physical L3** — multi-status graph/storage state. Physical presence is not strict Canon membership.

**Strict Canon** — deny-dominant trusted read projection governed by current evidence/policy.

**Guardian** — structural/safety policy boundary used by admission-capable paths.

**TruthGate** — admission-policy gate; not an oracle that independently knows objective truth.

**TrustSnapshot / CanonicalView** — immutable/read-policy surfaces used for trusted grounding.

**`active=false`** — PostgreSQL target state proving it is not the ordinary active runtime backend.

## Reader terms

**Reader Core RC-1** — bounded evidence-linked source/session skeleton with exact version/provenance, fidelity and coverage.

**Reader Core RC-2** — bounded caller-supplied Structural Document Map with explicit structural state.

**Reader Core RC-3** — bounded explicit multi-pass process ledger over declared structural targets.

**Reader Core RC-4** — bounded source-linked pre-admission proposition candidate registration.

**Reader Core RC-5** — bounded same-session/same-exact-source-version explicit relation candidate registry over valid RC-4 candidates.

**`EXTRACTED_PROPOSITION`** — RC-4 fidelity class meaning a proposition was extracted/registered from source-linked Reader context. It does not mean verified fact.

**Source owner** — explicit attribution indicating whose statement/presentation the proposition represents.

**Proposition presentation category** — RC-4 classification such as factual assertion, author opinion, hypothesis, conditional, example, quoted speech, reported position, definition or uncertain assertion. Category describes source presentation, not Crystal verification.

**`POSSIBLE_CONTRADICTION`** — RC-5 symmetric suspicion that two Reader propositions may conflict. Not a confirmed contradiction.

**`TENSION`** — RC-5 symmetric relation indicating tension without asserting contradiction.

**`EXCEPTION`** — RC-5 directional relation: right candidate is registered as an exception to left candidate.

**`QUALIFICATION`** — RC-5 directional relation: right candidate narrows/refines left candidate.

**relation rationale** — explicit text recording why the caller registered an RC-5 relation. It is audit context, not truth proof.

**Dedicated/full Reader Core** — autonomous or comprehensive Semantic Reading capability. It remains not implemented; `dedicated_reader_core=false`.

## Critical distinctions

```text
Reader coverage         != comprehension proof
pass completion         != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

## Grant/localization terms

**Funded delta** — new measurable work performed under an agreement beyond the verified existing baseline. Merged pre-agreement work cannot be counted again.

**NLnet state** — submitted / under review / not awarded.

**Native-speaker editorial certification** — independent human language-quality review by a qualified native speaker; not claimed merely because a translation exists.

**`CURRENT` translation** — localized surface current against its explicit source checkpoint.

**`REFRESH_NEEDED` translation** — rich translation preserved but known to lag its governing English source.
