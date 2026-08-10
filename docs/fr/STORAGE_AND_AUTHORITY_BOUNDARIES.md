<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: fr -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Limites du stockage et de l’autorité

## Identités séparées

```text
storage profile = identité de déploiement
physical L3 = état graphe multi-statut
strict Canon = projection de lecture fiable
migration bundle = preuve d’intégrité opérationnelle
retrieval score = signal de classement
model output = texte généré
```

Aucune de ces identités ne confère automatiquement l’autorité d’une autre.

## Profil durable

SQLite est le profil actif local-first ordinaire. Un premier `auto` durable peut sélectionner LadybugDB optionnel ou SQLite, puis verrouiller le backend et le locator non secret. Les conflits ultérieurs échouent en mode fail-closed. Mock reste un état explicite de développement/CI.

## physical L3 et strict Canon

physical L3 peut contenir VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded ou restricted. strict Canon est une projection deny-dominant fondée sur les preuves et politiques actuelles. Stockage, retrieval ou score élevé ne suffisent pas.

## Lecture et écriture

Les requêtes publiques passent en read-only par `core.query_pipeline.query()`. `ingest` explicite est le chemin capable d’écrire ; Guardian et TruthGate appliquent ensuite les limites structurelles et épistémiques.

## Cycle SQLite et migration

Sont implémentés : backup, vérification indépendante, inactive restore, logical export déterministe borné et vérification du bundle. Les datasets physical-L3 approuvés peuvent être importés dans un nouveau schéma PostgreSQL inactif puis comparés exactement ; la cible reste `active=false`.

Il ne s’agit pas d’une migration complète de L1, audit/outbox, métadonnées de chiffrement, configuration ou copies indépendantes. Aucun runtime PostgreSQL actif, aucune acceptation ANN, aucun switching automatique, cutover, fencing, rollback ou dual-write n’existe.

## Secrets et copies

Mots de passe, tokens, clés privées et DSN contenant des secrets ne doivent entrer ni dans profiles, bundles, receipts, logs, GitHub ou Notion. Backups, exports et migrations créent d’autres copies ; supprimer le store actif ne les efface pas automatiquement. Le chiffrement sélectif de champs L1 n’est pas universel.

## Preuves opérationnelles

| Événement | Prouve | Ne prouve pas |
|---|---|---|
| enregistrement dans L3 | persistance physique | appartenance à strict Canon |
| résultat de retrieval | pertinence candidate | suffisance des preuves |
| backup vérifié | intégrité du backup | vérité d’une affirmation |
| import réussi | intégrité de l’import | activation ou sélection runtime |
| exact equivalence | égalité des datasets approuvés | préparation production ou cutover |

Le Reader Core dédié n’est pas implémenté ; NLnet reste submitted / under review / not awarded.

## Contrats anglais détaillés

- [Architecture complète](../ARCHITECTURE.md)
- [Profil de stockage durable](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Contrat de migration](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Import PostgreSQL inactif](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
