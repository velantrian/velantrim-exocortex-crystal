<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: fr -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# État de l’implémentation : Crystal et travaux futurs

**Date :** 2026-08-08  
**Checkpoint :** `bbd816c` / PR #337  
**Preuves :** [TEST_REPORT.md](../../TEST_REPORT.md)  
**État lisible par machine :** [manifest](../status/implementation-manifest.json)

| Composant | État | Frontière actuelle |
|---|---|---|
| Guardian / TruthGate / projection stricte | Implémenté | stockage et migration ne contournent pas l’autorité |
| Requêtes HTTP/CLI/MCP | Implémenté | les requêtes ordinaires ne modifient pas Canon |
| Backup/verify/restore inactif SQLite | Implémenté et testé | restore inactif, jamais une admission |
| Export logique SQLite borné | Implémenté et testé | bundle canonique neutre au backend |
| Dépendance et preflight PostgreSQL | Implémenté et testé | extra explicite, chargement paresseux |
| Import PostgreSQL/pgvector inactif | Implémenté et testé | nouveau schéma inactif, aucun I/O ordinaire |
| Équivalence exacte de la cible | Implémenté et testé | re-hash indépendant en lecture seule |
| Adaptateur PostgreSQL runtime actif | Non implémenté | cible absente de la composition normale |
| Switching SQLite/PostgreSQL automatique | Interdit | disponibilité/import ne sélectionnent pas |
| Évaluation exact-vs-ANN | Non implémentée | phase ultérieure séparée |
| Cutover / rollback / dual-write | Non implémenté | phases explicites ultérieures |
| Cycle serveur PostgreSQL | Non implémenté | backup/restore/upgrade/pooling futurs |
| Reader Core / Semantic Reading Layer | Non implémenté | couche candidate avant admission |

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Les issues #331 et #332 ont été réalisées par les PR #335 et #337. PostgreSQL reste
une voie opérateur optionnelle avec `active=false`. Une équivalence réussie ne peut
ni activer un backend ni modifier Guardian, TruthGate ou le Canon strict.

Travaux futurs :

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal ne revendique ni backend PostgreSQL actif, ni migration automatique, ni
multi-tenancy de production, ni vérité universelle, ni zéro hallucination, ni
certification juridique/sécurité, ni conscience.
