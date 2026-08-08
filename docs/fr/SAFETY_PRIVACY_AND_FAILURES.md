<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: fr -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Frontières de sécurité, confidentialité et défaillance

**Source :** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

Cette vue ne remplace ni tests, ni revue de sécurité, ni conseil juridique.

## Sécurité épistémique

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian et TruthGate restent les frontières d’admission. Les requêtes publiques sont
read-only ; l’ingest explicite est l’écriture séparée. Crystal ne garantit ni vérité ni zéro
hallucination : le contenu non soutenu doit être bloqué, étiqueté, refusé ou auditable.

## Frontière locale

L’installation par défaut n’impose ni cloud, LLM, télémétrie ou analytics. SQLite est le
profil actif ordinaire. `auto` durable peut choisir LadybugDB optionnel ou SQLite et verrouille
le choix ; Mock reste un état dev/test explicite. PostgreSQL/pgvector est uniquement une
cible opérateur inactive avec `active=false`.

## Données et extension optionnelle

Peuvent être stockés claims, metadata, provenance, état épistémique, graphe, restrictions,
registrements d’erasure/audit, Receipts, outbox, bundles, backups et exports. Les données
sortent de la frontière locale seulement via Anthropic, Neo4j distant, Wikidata, Redis,
migration PostgreSQL, API élargie ou copies externes explicitement activées.

## Chiffrement et secrets

`VELANTRIM_ENCRYPTION_KEY` protège certains champs L1, pas automatiquement L3, backups,
exports, Receipts, logs ou temporaires. Le chiffrement hôte et la gestion de clés restent
nécessaires. Les credentials ne doivent jamais entrer dans profiles, bundles, receipts,
logs, issues ou Notion.

## API, confidentialité et effacement

Le baseline API utilise authentication et loopback. Une exposition externe exige TLS,
authentification revue, least privilege, limites, monitoring et incident handling. Access,
rectification, restriction, erasure et processing record sont des contrôles techniques,
pas une certification RGPD. Effacer le store actif n’efface pas globalement les copies.

## Réactions sûres aux défaillances

| Classe | Comportement attendu |
|---|---|
| Claim non soutenu | block, label ou bounded refusal |
| Mutation read-only | reject / aucun changement |
| Conflit profile | échec avant cache backend |
| Dépendance absente | erreur explicite, sans Mock caché |
| Import échoue | rollback, `active=false` |
| Evidence mismatch | verification failure |
| Manipulation Receipt/audit | échec digest/hash |
| Migration trop grande | fail closed aux limites |
| Exposition réseau | explicite et authentifiée |
| Copie après erasure | inventaire et suppression séparés |

## Non-revendications

Crystal n’est pas une certification sécurité/juridique/RGPD, une preuve d’échelle arbitraire,
un runtime PostgreSQL actif, un système de migration automatique, une garantie de vérité
parfaite, une AGI/conscience ou la preuve d’un grant NLnet attribué.

Détails : [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md) et [résumé anglais](../SAFETY_PRIVACY_AND_FAILURES.md).
