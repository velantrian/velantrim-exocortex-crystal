<!-- d5-source-policy: CURRENT -->
<!-- d5-inventory-scope: repository-documentation-corpus -->
# D5 extended-reference and retirement policy

## Purpose

D5 gives every documentation-like repository surface an explicit fate without translating
volatile implementation evidence merely to create apparent multilingual parity. English remains
the primary working, source and conflict-resolving language.

The machine-readable inventory is [`status/d5-inventory.json`](status/d5-inventory.json). The
validator resolves its ordered rules against the live repository tree, rejects unclassified
surfaces and prints the authoritative category counts.

## States

| State | Meaning |
|---|---|
| `CURRENT` | Maintained public or routing surface. Localized D1–D4 documents are current against immutable source checkpoints. |
| `REFRESH_NEEDED` | Reader-relevant surface whose current wording is known to lag its governing source. This is never a silent default. |
| `RETIRED` | Preserved historical snapshot or handoff. It is audit history, not current authority, capability or grant evidence. |
| `ENGLISH_ONLY_BY_DESIGN` | Detailed or volatile technical, legal-mapping, security, test, CI, machine-readable, AI-context, research, RFC, ADR or grant-evidence material maintained only in English. |

## Inventory scope and precedence

The inventory covers documentation-like files at repository root, under `docs/`, and under
`.github/`: Markdown, text, JSON, JSONL, YAML and YML. Ordered rules are applied as follows:

1. explicit retired files and archived snapshots;
2. current archive routing and D5 policy/inventory surfaces;
3. supported localized root READMEs and locale D1–D4 packs;
4. stable current English public/source documents;
5. all remaining detailed evidence and technical material as `ENGLISH_ONLY_BY_DESIGN`.

An unmatched eligible file is a validation failure. `REFRESH_NEEDED` may be empty only when the
live-tree validator confirms that no reader-relevant surface is known to require refresh.

## Retirement rules

Retired files are never deleted merely to make the ledger clean. They remain attributable and
are routed to current sources:

- `SPRINT_A_V2_ADDITIONAL_PATCHES.md` → `docs/IMPLEMENTATION_STATUS.md` and `docs/SPRINT_A_STATUS.md`;
- `WORK_SUMMARY.md` → `TEST_REPORT.md`, `docs/STATUS.md` and `docs/IMPLEMENTATION_STATUS.md`;
- `docs/CLAUDE_CODE_HANDOFF_2026_06_17.md` → `docs/ai/CURRENT_STATE.md` and this policy;
- `docs/archive/**` → `docs/archive/README.md`, then current status/architecture documents.

The archive README is a current routing surface; archived payloads beneath it are retired.
Historical material cannot establish implementation, test coverage, maturity, grant status,
Canon membership or deployment readiness.

## Localization decision

D5 localizes one compact **Extended Reference Guide** per supported locale. The guide explains
which detailed English sources exist, why they remain English-only and how retired material is
routed. It does not translate volatile low-level evidence, CI logs, ADR bodies, machine-readable
status, legal mappings or grant evidence.

## Immutable boundaries and non-claims

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
```

SQLite remains the ordinary active local-first profile. Mock remains the explicit development/CI
backend. PostgreSQL/pgvector remains an inactive target with `active=false`. Reader Core is not
implemented. NLnet remains submitted / under review / not awarded; approximate €50,000 is
planning only, not an approved budget or payment commitment; budget change is none. Work merged
before an agreement cannot be counted again as funded delta. No legal, GDPR, security or
native-speaker editorial certification is claimed.
