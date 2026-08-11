<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d5-locale: ru -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
# 🇷🇺 D5 — расширенная справка

D5 различает `CURRENT`, `REFRESH_NEEDED`, `RETIRED`, `ENGLISH_ONLY_BY_DESIGN`. `REFRESH_NEEDED` — честный translation debt, а не разрешение удалять богатый перевод и заменять его summary.

Reader machine boundary:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

RC-5 сохраняет valid RC-4 candidate linkage, exact provenance и rationale для `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` в одном session/source version. Он не выполняет semantic resolution.

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

SQLite ordinary active local-first; PostgreSQL target `active=false`. NLnet: submitted / under review / not awarded; €50,000 planning only; budget change: none.

Русский Reader-dependent пакет `CURRENT` на RC-5 source checkpoint. Остальные 8 locale Reader/root surfaces — `REFRESH_NEEDED`; 64 docs остаются tracked debt. D2 и Quick Start current во всех девяти.

Нет security/legal/GDPR/native-speaker certification, dedicated Reader, automatic contradiction resolution, cross-document semantic identity или PostgreSQL activation.
