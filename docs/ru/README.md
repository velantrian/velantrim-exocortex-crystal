<!-- localization-index-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-status: CURRENT -->
<!-- d2-source: main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- d2-status: CURRENT -->
<!-- d3-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d3-status: CURRENT -->
<!-- d4-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d4-status: CURRENT -->
<!-- d5-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-status: CURRENT -->
<!-- rc6-localization-index-source: main@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc6-status: CURRENT -->
<!-- rc7-localization-index-source: main@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
# 🇷🇺 Русская документация Crystal

Исторические D1–D5 и RC-6 source markers сохранены как immutable audit evidence. Текущий русский Reader-dependent пакет `CURRENT` к RC-7 English checkpoint `main@ab3ad31c437647535030e371d58f456faf14017b`.

- D1: [Quick Start](./QUICKSTART.md), [Status](./STATUS.md), [Implementation Status](./IMPLEMENTATION_STATUS.md)
- D2: [Reviewer Guide](./REVIEWER_GUIDE.md), [Safety/Privacy/Failures](./SAFETY_PRIVACY_AND_FAILURES.md)
- D3: [Architecture Overview](./ARCHITECTURE_OVERVIEW.md), [Storage/Authority](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- D4: [Grant Overview](./GRANT_OVERVIEW.md), [Glossary](./GLOSSARY.md)
- D5: [Extended Reference Guide](./EXTENDED_REFERENCE_GUIDE.md)

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
dedicated_reader_core = false
```

RC-7 = explicit cross-document candidate links между current RC-4 propositions из разных `document_id`, exact two-sided provenance + rationale, без automatic semantic matching/identity/dedupe/evidence admission.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite ordinary active local-first; PostgreSQL `active=false`. NLnet `submitted / under review / not awarded`; ~€50,000 planning only; budget change none. Eight other Reader-dependent locale packs сохраняют rich `REFRESH_NEEDED` translations; D2 и Quick Start остаются CURRENT across all nine supported locales.
