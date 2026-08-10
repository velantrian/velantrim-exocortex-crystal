# Crystal Documentation Map

English is the primary source/conflict resolver. GitHub merged code, executable tests, exact CI and machine-readable status are implementation truth.

## Public entry points

- [Root README](../README.md)
- CURRENT full-parity localized READMEs: Arabic, German, Spanish, French, Hindi, Italian, Japanese, Russian and Simplified Chinese
- [Quick Start](./QUICKSTART.md)
- [Status](./STATUS.md)
- [Implementation Status](./IMPLEMENTATION_STATUS.md)
- [Translation status](./TRANSLATION_STATUS.md)
- [Localization policy](./LOCALIZATION_POLICY.md)

## Reviewer / safety / privacy / failures (D2)

D2 uses the stable English Reviewer Guide and safety/privacy/failure source family. Reader RC-1/RC-2 did not change this source contract, so D2 retains its previous immutable source checkpoint and remains current in all nine supported locale packs.

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

Machine distinction:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

## Storage

- SQLite ordinary active local-first runtime and lifecycle
- Bounded logical export/verification
- Inactive PostgreSQL import and exact-state equivalence
- PostgreSQL/pgvector target remains `active=false`
- No automatic backend switching, cutover, rollback or dual-write

## Multilingual families

All nine root README translations remain `CURRENT` full-parity public presentations against the 2026-08-10 Reader reconciliation checkpoint. D2 and all localized Quick Start documents remain `CURRENT` because RC-1/RC-2 did not change those source semantics.

The Russian D1/D3/D4/D5 detail pack has been fully refreshed and is `CURRENT`. The eight other supported locale packs retain their rich pre-Reader translations, but their Reader-dependent D1 Status/Implementation, D3 Architecture/Storage, D4 Grant/Glossary and D5 Extended Reference Guide documents are explicitly `REFRESH_NEEDED` until a full RC-1/RC-2 semantic refresh is completed.

The authoritative freshness map is [`TRANSLATION_STATUS.md`](./TRANSLATION_STATUS.md). Locale indexes expose the same mixed status. D3 translation manifest, D4 translation manifest, D5 translation manifest and the D5 source inventory are machine-checked in CI. The D5 inventory intentionally classifies 56 Reader-dependent localized detail documents as `REFRESH_NEEDED`; this is tracked translation debt, not an unclassified failure.

## Evidence / grant / security

- [Test report](../TEST_REPORT.md)
- [Machine manifest](./status/implementation-manifest.json)
- [Grant scope — NLnet](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Security](../SECURITY.md)

Grant remains submitted / under review / not awarded. No legal/GDPR/security/native-speaker certification is implied by translation status.
