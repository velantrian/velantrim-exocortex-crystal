<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
# 🇷🇺 Crystal — проект, грант и governance

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

Около €50,000 — planning amount, не approved budget и не payment commitment.

Crystal разделяет physical L3 и strict Canon. SQLite остаётся ordinary active local-first; PostgreSQL/pgvector — inactive target `active=false`.

Reader RC-1, RC-2, RC-3, RC-4 и RC-5 — bounded pre-admission layers. RC-5 регистрирует `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` только между valid RC-4 candidates в одном session/version domain.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-5 не имеет truth/Canon/ESM authority, не вызывает `core.evidence.attach_evidence()`, не обходит Guardian/TruthGate, не выбирает winner и не создаёт cross-document identity.

Любая работа, merged до grant agreement, является existing baseline. RC-0..RC-5, merged pre-agreement, нельзя позже повторно представить как funded delta. Dedicated/full autonomous Reader остаётся not implemented.
