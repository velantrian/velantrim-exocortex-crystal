# Crystal Documentation Map

English is the primary source/conflict resolver. GitHub merged code, executable tests, exact CI and machine-readable status are implementation truth.

## Public entry points

- [Root README](../README.md)
- Localized root READMEs: Russian is `CURRENT` against the RC-4 Reader checkpoint; Arabic, German, Spanish, French, Hindi, Italian, Japanese and Simplified Chinese preserve full prior content and are explicit `REFRESH_NEEDED` until RC-4 semantic refresh
- [Quick Start](./QUICKSTART.md)
- [Status](./STATUS.md)
- [Implementation Status](./IMPLEMENTATION_STATUS.md)
- [Translation status](./TRANSLATION_STATUS.md)
- [Localization policy](./LOCALIZATION_POLICY.md)

## Reviewer / safety / privacy / failures (D2)

D2 uses the stable English Reviewer Guide and safety/privacy/failure source family. Reader RC-1/RC-2/RC-3/RC-4 do not change this source contract, so D2 retains its previous immutable source checkpoint and remains current in all nine supported locale packs.

- [Reviewer Guide](./REVIEWER_GUIDE.md)
- [Safety, privacy and failures](./SAFETY_PRIVACY_AND_FAILURES.md)
- [Failure modes](./FAILURE_MODES.md)
- [Security policy](../SECURITY.md)
- [Privacy policy](../PRIVACY.md)

## Architecture / Reader

- [Architecture](./ARCHITECTURE.md)
- [Architecture overview](./ARCHITECTURE_OVERVIEW.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- `core/reader_core.py` — RC-1 bounded evidence-linked skeleton
- `core/reader_structure.py` — RC-2 bounded Structural Document Map
- `core/reader_passes.py` — RC-3 bounded explicit multi-pass mechanics
- `core/reader_extraction.py` — RC-4 bounded source-linked proposition candidate extraction

Machine distinction:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core = false
```

RC-4 remains upstream of normal admission. It creates source-linked `EXTRACTED_PROPOSITION` candidates only from eligible completed substantive Reader regions. It does not call `core.evidence.attach_evidence()`, write fact evidence, mutate truth/ESM/Canon or bypass Guardian/TruthGate.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

## Storage

- SQLite ordinary active local-first runtime and lifecycle
- Bounded logical export/verification
- Inactive PostgreSQL import and exact-state equivalence
- PostgreSQL/pgvector target remains `active=false`
- No automatic backend switching, cutover, rollback or dual-write

## Multilingual families

The immutable RC-4 Reader localization source checkpoint is `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86`.

The Russian root README and Reader-dependent D1/D3/D4/D5 detail pack are fully refreshed and `CURRENT`. D2 and all localized Quick Start documents remain `CURRENT` across all nine supported locales because RC-4 does not change those source semantics.

The eight other supported locale packs retain their rich earlier translations, but both their root READMEs and Reader-dependent D1 Status/Implementation, D3 Architecture/Storage, D4 Grant/Glossary and D5 Extended Reference Guide documents are explicitly `REFRESH_NEEDED` until a full RC-4 semantic refresh is completed. These are preserved rich translations, not shortened replacements and not current implementation evidence.

The authoritative freshness map is [`TRANSLATION_STATUS.md`](./TRANSLATION_STATUS.md). Locale indexes expose the same mixed status. D3 translation manifest, D4 translation manifest, D5 translation manifest and the D5 source inventory are machine-checked in CI. The D5 inventory intentionally classifies **64 localized documents** as `REFRESH_NEEDED`: eight localized root READMEs plus seven Reader-dependent detail types across those eight locales. This is tracked translation debt, not an unclassified failure.

## Evidence / grant / security

- [Test report](../TEST_REPORT.md)
- [Machine manifest](./status/implementation-manifest.json)
- [Grant scope — NLnet](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Security](../SECURITY.md)

Grant remains submitted / under review / not awarded. Approximate €50,000 remains planning only; budget change is none. Reader RC-0/RC-1/RC-2/RC-3 and RC-4, if merged before any agreement, are existing baseline rather than future funded delivery. No legal/GDPR/security/native-speaker certification is implied by translation status.
