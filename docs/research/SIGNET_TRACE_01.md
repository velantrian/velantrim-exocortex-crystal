# SIGNET-TRACE-01 — End-to-End Protocol Trace

**Date opened:** 2026-09-27  
**Date run:** 2026-09-28  
**Runner:** Grok 4.6 (manual / source-grounded / no runtime)  
**Protocol:** v0.1 DESIGN HYPOTHESIS  
**Status after run:** `TRACE_COMPLETE_ON_AVAILABLE_RECORD · PRIMARY_RAW_SOURCE_NOT_RECOVERED · NOT CANON · NOT RUNTIME · NOT GENERAL VALIDATION`

Overall verdict:

`SIGNET-TRACE-01 COMPLETE`

`Observed protocol gaps found`

`Minimal Protocol v0.2 candidate justified`

`ONE TRACE ≠ GENERAL VALIDATION`

This run does **not** promote Protocol v0.1 to Canon.  
This run does **not** authorize runtime implementation.  
This run does **not** invent a missing user act.

---

## Frozen case (unchanged)

Known form of the case:

- ASSISTANT: «Я бы не интегрировал Signet напрямую.»
- Later derived state / summaries / examples presented this approximately as:  
  `MODEL_PROPOSAL → USER_DECISION → confirmed → authority=user → rejected`
- No separate user act establishing that decision was shown in the available record.
- Bounded current research status:  
  `direct_signet_integration = NOT_ESTABLISHED_IN_AVAILABLE_RECORD`
- Signet: `DONOR / COMPARATOR CANDIDATE`

This state does **not** mean `USER_REJECTED_SIGNET`.  
This state does **not** mean `USER_SELECTED_SIGNET`.

---

## Source search performed

Searched, in this run:

1. Google Drive full-text for the exact quote and Signet integration terms.
2. Notion semantic search for the exact quote and `NOT_ESTABLISHED_IN_AVAILABLE_RECORD`.
3. GitHub repo `velantrian/velantrim-exocortex-crystal` for `Signet`, `direct_signet`, the Russian quote.
4. Issue #489, Draft PR #490, branch `research/signet-trace-01-protocol-v0-1-20260927`.
5. TCE evidence page and its Google Drive companion.
6. Protocol v0.1 Drive + Git copies.

**Not found:** raw conversation export, message IDs, timestamps, surrounding USER turns immediately before/after the recommendation, or the specific derived summary that performed the alleged promotion.

---

## SOURCE MANIFEST

Available derived records: SRC-001 TCE Admission checkpoint 2026-09-27; SRC-002 Protocol v0.1 example payload; SRC-003 SIGNET-TRACE-01 freeze doc; SRC-004 Issue #489; SRC-005 this TZ.

Absent: SRC-NEG-001 raw primary assistant message; SRC-NEG-002 explicit user select/reject act; SRC-NEG-003 inspectable promoting derived-summary object.

`AVAILABLE_SOURCE_WINDOW` = 2026-09-27 research records that quote or freeze the case + protocol example + TZ.  
`MISSING_SOURCE_WINDOW` = original conversation, adjacent user turns, timestamps/message IDs/hashes, promoting summary file.  
`COVERAGE_STATUS` = `partial_or_unverified`.

Critical question: is there primary basis for `UserSelected(Signet)` or `UserRejected(Signet)`? **NO. Do not create such an event.**

---

## STEP 0 — RAW SOURCE

**INPUT:** search for most primary Signet-case material; known quote «Я бы не интегрировал Signet напрямую.»  
**SOURCE:** attempted primary; recovered only derived/freeze/example records.  
**RULE_USED:** Protocol v0.1 Step 0 `source_record` (actor, time, hash, protected URI); source-first priority.  
**OUTPUT:** source manifest. No `source_record` can be built for the original assistant utterance with required `occurred_at`, `content_hash`, `message_id`, speaking-assistant `actor_id`. Research records can be stored, but their actor is the documenter.  
**SUPPORTED_BY:** SRC-001..005; SRC-NEG-001.  
**UNCERTAINTY:** original full turn, adjacent user speech, conditionality/scope of «напрямую».  
**COVERAGE:** Drive, Notion TCE, Git research branch, Issue #489, PR #490. Not all unexported chats.  
**MISSING_RULE_OR_FAILURE:** v0.1 assumes incoming messages already captured; no backfill rule for reported historical speech.  
**CLASSIFICATION:** `BLOCKED_BY_SOURCE_GAP`

---

## STEP 1 — CONTEXTUAL EVIDENCE BUNDLE

**INPUT:** isolated quote Q1 + later promotion description in SRC-001.  
**SOURCE:** derived.  
**RULE_USED:** `evidence_quote` + offsets + one `source_id`; admission checks 2–5. No reply_target / prior_proposal fields.  
**OUTPUT:** Q1 on a *primary assistant* record could support a narrow assistant recommendation. Q1 cannot support a user decision. Q1 cannot fix reply target, prior question, or whether scope is `direct_signet_integration` vs donor/comparator use. Failure candidate label only: `ADMISSION_UNIT_CONTEXT_GAP`.  
**UNCERTAINTY:** whether the original turn had more sentences.  
**MISSING_RULE_OR_FAILURE:** no contextual evidence bundle object in v0.1 (H1).  
**CLASSIFICATION:** `FAILED_IN_TRACE` for isolated quote as sole admission unit when scope/referent must be preserved; `SUPPORTED_IN_TRACE` that Q1 cannot warrant UserRejected.

---

## STEP 2 — `memory.propose_event_interpretation`

**INPUT:** SRC-001 quote attributed to assistant; adversarial UserRejected readings.  
**RULE_USED:** proposal ≠ ledger; actor must match source metadata; ambiguity → `proposed_unknown` / `needs_human_review`; invariant 1.  
**OUTPUT:**  
- P-ASSIST-REC from missing primary source = `proposed_unknown_pending_primary_source`.  
- P-USER-REJ from Q1 = must not propose (actor would be assistant).  
- P-USER-REJ from derived summary = must not use as sole evidence (check 7).  
- P-ASSIST-REC from SRC-001 with actor=assistant = `proposed_unknown` (documenter actor ≠ assistant).  
**CLASSIFICATION:** `SUPPORTED_IN_TRACE` for refusing UserRejected; `BLOCKED_BY_SOURCE_GAP` for primary RecommendationIssued; `UNDERDETERMINED` for original scope_key.  
No UserSelected / UserRejected event created.

---

## STEP 3 — ADMISSION

**RULE_USED:** admission checks 1–10.  
**OUTPUT:**  
- UserRejected from Q1 → REJECT (actor mismatch, invariant 1).  
- UserRejected from summary → REJECT (check 7).  
- RecommendationIssued from SRC-NEG-001 → cannot admit (check 1).  
- RecommendationIssued from SRC-001 with actor=assistant → REJECT (check 3).  
Admitted historical Signet decision events: **none**.  
**CLASSIFICATION:** `SUPPORTED_IN_TRACE` for rejecting UserRejected; `BLOCKED_BY_SOURCE_GAP` for positive primary admission; `NOT_EXERCISED` for runtime `submit_admission`.  
Absence of admitted UserRejected is not proof that no such act exists outside the searched window.

---

## STEP 4 — CURRENT STANDING

**INPUT:** admitted events = ∅.  
**RULE_USED:** event ≠ standing; absence ≠ negative decision; invariant 8 vs example payload of `memory.get_decision_state`.  
**OUTPUT:**  
`decision_state = unknown`  
`coverage_state = partial_or_unverified`  
`basis_event_ids = []`  
Prohibited: user_rejected_signet, user_selected_signet, complete_for_scope, treating no_confirmed_user_decision as proven absence.  
**OBSERVED PROTOCOL TENSION:** example uses `no_confirmed_user_decision` + `complete_for_scope` on the same quote. Licensed only if coverage is independently complete. This window is not. v0.1 has no algorithm that computes coverage.  
**CLASSIFICATION:** `FAILED_IN_TRACE` for coverage semantics; `SUPPORTED_IN_TRACE` for refusing selected/rejected.  
Research shorthand `NOT_ESTABLISHED_IN_AVAILABLE_RECORD` is closer to unknown + partial than to the example payload.

---

## STEP 5 — WORKING CAPSULE

Task: current status of direct Signet integration.

- SCOPE / STANDING = DERIVED_PROJECTION (`unknown` + `partial_or_unverified`).  
- EVIDENCE: SRC-001/002/003 = EXTERNAL_REFERENCE / DERIVED_PROJECTION.  
- PRIMARY_EVENT: none recovered.  
- CONFLICT: protocol example vs invariant 8.  
- OPEN_QUESTION: can raw turn + adjacent user turns be exported?  
- PROHIBITED_CLAIMS: user rejected/selected; confirmed absence; treating SRC-001 as original assistant source_record.  
**CLASSIFICATION:** `SUPPORTED_IN_TRACE` for provenance labels; `UNDERDETERMINED` for LLM obedience; `NOT_EXERCISED` for runtime builder.

---

## STEP 6 — STRUCTURED AUTHORITY CLAIM

Experimental candidate, **not** declared part of v0.1.

C-VALID: claim_type=decision_status; actor=user; state=NOT_ESTABLISHED; protocol_equivalent unknown + partial_or_unverified; basis=[].  
C-BAD negative control: state=rejected.  
**CLASSIFICATION:** `NOT_EXERCISED` as v0.1-mandated component; exercised as H7 candidate.

---

## STEP 7 — VALIDATION

C-VALID: VALID on available record.  
C-BAD: INVALID (no UserRejected; assistant quote cannot warrant user rejection; coverage incomplete).  
Hypothetical complete no-decision: INVALID/UNDERDETERMINED on this window.  
**CLASSIFICATION:** `SUPPORTED_IN_TRACE` that C-BAD must fail; `FAILED_IN_TRACE` for existence of a deterministic validator in v0.1; `NOT_EXERCISED` for runtime gate.

---

## STEP 8 — RENDERED ANSWER

Allowed render:

«В доступной записи есть поздние research-документы, которые цитируют рекомендацию ассистента не интегрировать Signet напрямую. Подтверждённого пользовательского решения в первичном материале этого прогона не установлено. Исходный разговор с этой фразой не восстановлен, поэтому покрытие истории частичное, а не полное.»

Rejected: «Вы решили отказаться от Signet.» / «Signet отклонён.» / «история полная.»  
**CLASSIFICATION:** `SUPPORTED_IN_TRACE` for careful manual render; `NOT_EXERCISED` for live CASE D follow-through.

---

## Negative checks

- CASE A: assistant quote → UserRejected blocked by invariant 1. `SUPPORTED_IN_TRACE` at rule level.  
- CASE B: derived summary as sole evidence blocked by check 7. Rule supported; promoting file not recovered (`UNDERDETERMINED` as artifact).  
- CASE C: partial history ≠ complete no-decision. Invariant 8 agrees; example disagrees. `FAILED_IN_TRACE` internal consistency.  
- CASE D: live LLM follow-through. `NOT_EXERCISED`.

---

## Review hypotheses

| ID | EXERCISED? | REQUIRED BY TRACE? |
|---|---|---|
| H1 admission unit utterance vs bundle | YES | YES |
| H2 UserRevoked vs EventInvalidated | NO | NO |
| H3 coverage_state semantics | YES | YES |
| H4 evidence redaction/tombstone | NO | NO |
| H5 admitted_by trust | NO | UNDERDETERMINED |
| H6 basis_event_ids JSON vs FK | NO | NO |
| H7 typed → validate → render | YES as candidate | UNDERDETERMINED |

---

## Result classification

`TRACE_COMPLETE` · `NOT PROTOCOL_VALIDATED_GENERALLY`

Bucket **B** (observed protocol gaps, minimal v0.2 candidate) plus source limitation: standing cannot leave `unknown` + `partial_or_unverified` without new primary source.

---

## A–H summary

**A. Worked:** no invented user decision; assistant quote not promoted; summary not sole evidence; absence ≠ rejection; selected/rejected unused; C-BAD invalid; failure classes kept distinct.

**B. Failed:** raw conversation not restored; cannot admit recommendation from documents that quote it; coverage semantics non-deterministic; example vs invariant 8; admission unit cannot store referent context.

**C. Underdetermined:** hidden user act; future complete window; live LLM obedience; H2/H4/H5/H6.

**D. Source gaps:** no message_id/time/hash for Q1; no adjacent turns; no promoting summary file.

**E. Protocol gaps:** COVERAGE_SEMANTICS_GAP; ADMISSION_UNIT_CONTEXT_GAP; REPORTED_SPEECH_SOURCE_GAP; no mandatory typed renderer gate.

**F. Hypotheses triggered:** H1, H3; H7 candidate only.

**G. Minimal v0.2 deltas (observed failure only):**  
1. Coverage rule: `complete_for_scope` only via deterministic capture or human coverage attestation; `no_confirmed_user_decision` only with complete coverage; align/remove the Signet example.  
2. Admission unit: evidence bundle **or** `needs_human_review` when scope/candidate is not in the quoted span.  
3. Reported speech: later quote ≠ original source_record; backfill needs raw message or human attestation.  
Do not add H2/H4/H5/H6 from this trace.

**H. Not justified:** general validation; runtime change; merge PR #490; Signet selected/rejected/authorized; typed-claim as Canon; UNSELECTED_STATE_LOSS as universal mechanism.

---

## Owner next action

To leave `unknown` + `partial_or_unverified`, export the raw conversation that contains «Я бы не интегрировал Signet напрямую.» including adjacent user turns.
