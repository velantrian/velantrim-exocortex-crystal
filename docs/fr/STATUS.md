<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: fr -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — état actuel

**Date :** 2026-08-08  
**Checkpoint runtime vérifié :** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Arbre vérifié :** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Head validé :** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**PR / CI :** #337 / `31256316536`  
**CI PostgreSQL :** `31256316532`

## Vérification

- Python 3.11 : **2078 passed / 13 skipped / 0 failed** ;
- Python 3.12 : **2078 passed / 13 skipped / 0 failed** ;
- **9756 statements / 100.00% line coverage** ;
- `core/postgresql_migration.py` : **44/44 statements** ;
- `core/postgresql_migration_impl.py` : **336/336 statements** ;
- **7/7** mutants Ring Zero éliminés ;
- **9/9** jobs CI permanents réussis ;
- **1/1** intégration réelle PostgreSQL/pgvector réussie.

Preuves : [TEST_REPORT.md](../../TEST_REPORT.md) et
[manifest](../status/implementation-manifest.json).

## Frontière de capacité vérifiée

Crystal conserve la base SQLite local-first et implémente la phase 1 de l’issue #332 :

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

Le pilote PostgreSQL est optionnel et chargé paresseusement uniquement par commande
opérateur explicite. L’installation par défaut reste en bibliothèque standard pure.
La cible importée n’est pas enregistrée dans le runtime ordinaire, reste
`active=false` et ne sert aucune lecture ou écriture normale.

## Frontière d’autorité

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot et CanonicalView restent inchangés.

## Toujours absent

- runtime PostgreSQL actif en lecture/écriture ;
- évaluation exact-vs-ANN et seuils ANN acceptés ;
- activation, cutover, fencing, rollback ou dual-write ;
- cycle backup/restore/upgrade, pooling de production et fencing distribué ;
- IdP/multi-tenancy de production ou certification juridique, sécurité ou RGPD ;
- Reader Core vérifié dédié.

## Statut de la subvention

Le projet est soumis et en cours d’examen. **Aucune attribution ni modification du budget
n’est revendiquée.** La PR #337 et l’issue #332 sont déjà la base fusionnée et ne peuvent
pas être comptées à nouveau comme travail futur financé.
