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

Root READMEs and D1–D5 are current across all nine supported locale packs. D2 retains its prior immutable source checkpoint because Reader RC-1/RC-2 did not alter reviewer/safety source semantics; affected Root/D1/D3/D4/D5 families use the 2026-08-10 Reader reconciliation source checkpoint.

The ledger still supports REFRESH_NEEDED translated document packs when future English changes affect public meaning. D3 translation manifest, D4 translation manifest and D5 translation manifest are machine-checked in CI. D5 includes nine Extended Reference Guides. D5 remains a separate inventory phase in policy even though its current translation phase is complete.

## Evidence / grant / security

- [Test report](../TEST_REPORT.md)
- [Machine manifest](./status/implementation-manifest.json)
- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Security](../SECURITY.md)

Grant remains submitted / under review / not awarded. No legal/GDPR/security/native-speaker certification is implied by translation status.
