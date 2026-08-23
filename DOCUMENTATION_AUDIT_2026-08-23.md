# Documentation Audit — 2026-08-23

**Scope:** accuracy/currency (точность и актуальность) and completeness/structure (полнота и структура) of this repository's documentation (`*.md`, README, `docs/`, including the 9-locale translation set), assessed against a snapshot of the default branch on 2026-08-23. This is a documentation snapshot audit, not a code-quality or security review, and does not cover unmerged branches.

## Overall Health Assessment

**Fair.** The corpus is unusually disciplined about *labeling* staleness — machine-readable manifests, checkpoint hashes, explicit "historical/superseded" banners — and the i18n structure is clean at the filename level: all nine locales (ar,de,es,fr,hi,it,ja,ru,zh-CN) carry an **identical 11-file set** with no locale missing or adding files relative to the other eight. Standard root files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE) are all present, and a full repo-wide relative-link scan found zero broken links outside the explicitly-archived snapshot directory. However: a hand-maintained ADR status table contradicts the ADRs it summarizes, one ADR number is duplicated with one copy fully orphaned, the D5 localization policy contradicts the translation ledger it's supposed to feed, and the "V1 complete" framing now dominating English status docs hasn't propagated into any of the nine locale status packs — nor into the one overlay file written to bridge that gap, which is itself unreachable from any navigation path.

## Findings

1. **docs/ADR.md** | accuracy | high | The "Focused ADR index" status column contradicts the Status field inside the ADRs it summarizes for three consecutive entries. | Index lists ADR-017/018/019 as `Accepted`, but each file's own header says `**Status:** Proposed implementation draft in issue #315/#316/#317`.

2. **docs/adr/ADR-015-ADVISORY_FACETS_AND_CURATOR_IAM.md** | completeness | high | ADR number 015 is used twice, and one of the two files is completely un-indexed and unreferenced anywhere in the repo. | docs/adr/ contains both this file and ADR-015-ESM_MACHINE_SPEC.md; docs/ADR.md's index only ever points to the ESM one.

3. **docs/EXTENDED_REFERENCE_POLICY.md** | accuracy | high | The D5 policy's own "Localization decision" section contradicts the freshness ledger it names as authoritative. | Policy says "eight other locale packs remain REFRESH_NEEDED" while docs/TRANSLATION_STATUS.md states D5 is CURRENT in all nine locales.

4. **docs/{9 locales}/STATUS.md and IMPLEMENTATION_STATUS.md** | accuracy | high | All nine locales' status files are pinned to a stale checkpoint and don't reflect the "V1 complete" milestone now defining the English source; the one bridge document meant to patch this is itself orphaned. | Every locale file is 74-156 lines vs English 303/189 lines, none contain "V1 COMPLETE"; docs/status/CRYSTAL_V1_LOCALIZATION_OVERLAY_2026-08-22.md is linked from zero other files, including English docs/STATUS.md itself.

5. **docs/REVIEWER_GUIDE.md** | accuracy | high | Instructs reviewers to check a test file that does not exist: `tests/test_read_only_query_boundary.py` — actual file is `tests/test_read_only_query_surfaces.py`.

6. **docs/TOPIC_FACETS_AND_CURATOR_IAM.md** | completeness | medium | Public-facing doc for a shipped feature is entirely orphaned — not linked from docs/DOCUMENTATION_MAP.md, docs/ADR.md, or anywhere else (pairs with finding #2, its companion ADR is likewise orphaned).

7. **docs/archive/grant-sync/** (5 files) | structure | medium | An entire subdirectory of the archive is missing from the archive's own index, and its files contain the bulk of the repo's broken links. | docs/archive/README.md's "Contents" table never mentions grant-sync/; those 5 files account for 62 of the 63 repo-wide broken relative links found.

8. **CHANGELOG.md** | accuracy | medium | References `docs/Velantrim_V8_Crystal_Sprint1_toc.md` at a path it no longer lives at — file now lives at docs/archive/Velantrim_V8_Crystal_Sprint1_toc.md.

9. **docs/architecture/** (9 files) | completeness | medium | Several architecture docs, including the two newest Reader-research artifacts (READER_POST_RC10_REASSESSMENT.md, READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md), are never linked from docs/DOCUMENTATION_MAP.md or anywhere else; the map's Reader diagram caps at RC-9 and never mentions RC-10.

10. **docs/decisions/D-CR7-tiered-epistemic-diagnostics.md** | structure | medium | One feature (CR-7 tiered epistemic diagnostics) has its documentation scattered across three unrelated top-level directories with no cross-links tying them together, and the primary doc is still labeled "Decision Draft."

11. **docs/architecture/implementation-status.md** | structure | low | A lowercase near-duplicate of the canonical docs/IMPLEMENTATION_STATUS.md sits unlinked in a different directory (self-labeled superseded, but a naming-hygiene hazard).

12. **docs/{locale}/EXTENDED_REFERENCE_GUIDE.md, GRANT_OVERVIEW.md** | structure (i18n) | low | Two of the eleven per-locale filenames don't match their English source filenames, breaking the otherwise-exact 1:1 mirroring (deliberate and traceable via header comments, applied consistently across all 9 locales — not a per-locale defect).

13. **docs/** (no docs/README.md) | structure | low | The English docs tree has no README.md, while every locale's package leads with one; English equivalent role is served by docs/DOCUMENTATION_MAP.md instead.

14. **docs/adr/ADR-020, ADR-021** | accuracy | low | Index wording softens/alters the ADRs' own hedged status language ("Accepted by the accompanying implementation, pending merge evidence" → index just says "Accepted") — same root cause as finding #1, lower severity.

**Positive/confirmatory note:** the i18n parity check found no locale missing or carrying extra files relative to the other eight — the only structural inconsistency across the 9-locale set is the pair of intentional renames in finding #12.

---
*Generated by an automated documentation audit (Claude Code).*
