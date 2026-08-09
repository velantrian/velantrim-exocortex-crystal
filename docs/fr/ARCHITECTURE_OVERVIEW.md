<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: fr -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — vue d’ensemble de l’architecture

Cette traduction sert d’orientation. En cas de conflit, le code fusionné, les tests exécutables, le CI exact et les contrats anglais prévalent.

## Modèle central

```text
sources + ingest explicite
→ provenance + normalisation
→ contrôles Guardian
→ décision TruthGate
→ état opérationnel L1 + physical L3 multi-statut
→ projection de lecture strict Canon à déni dominant
→ retrieval read-only / réponse / refus borné
```

Un enregistrement dans physical L3 n’appartient pas automatiquement à strict Canon. Le score de retrieval, la similarité vectorielle et le texte d’un modèle ne sont pas des preuves indépendantes.

## Couches mémoire et revue

- **L0 :** contexte éphémère du processus.
- **L1 :** SQLite/WAL pour l’état opérationnel, les preuves, l’audit, les receipts, les sessions d’import/revue et l’outbox.
- **L2 :** staging pending/review pour candidats ou quarantaine ; ce n’est pas une couche de vérité finale.
- **L3 :** stockage graphe multi-statut ; distinct de strict Canon.
- **TrustSnapshot / CanonicalView :** surface de lecture fiable à politique deny-dominant.

## Séparation lecture/écriture

`HTTP /ask`, `CLI ask` et MCP passent en read-only par `core.query_pipeline.query()`. Une requête ne peut ni créer ni renforcer un fait, ni modifier ESM, L3, l’outbox, les liens d’épisodes ou l’identité de l’embedder. Seul `ingest` explicite peut emprunter le chemin d’écriture gouverné par Guardian et TruthGate.

## Profils et portabilité

SQLite est le profil actif local-first ordinaire. Lors du premier `auto` durable, LadybugDB optionnel ou SQLite peut être choisi puis verrouillé avec une identité de locator non secrète. Un fallback silencieux vers Mock éphémère est interdit.

Le chemin PostgreSQL/pgvector vérifié s’arrête à une cible inactive :

```text
bundle SQLite vérifié
→ import PostgreSQL transactionnel
→ re-hash indépendant read-only
→ équivalence exacte
→ active=false
```

Import ou équivalence ne signifient ni activation, ni sélection du backend, ni admission TruthGate, ni cutover, rollback ou dual-write. PostgreSQL est absent de la composition runtime normale.

## Lecture de documents

Les source spans, enregistrements de documents, sessions d’import et flux dry-run/review font partie du baseline implémenté. Un Reader Core dédié, multi-passe, avec cartes de couverture, relecture sensible aux contradictions et synthèse documentaire n’est pas implémenté.

## Non-revendications

Crystal ne revendique ni AGI, ni conscience, ni zéro hallucination, ni runtime PostgreSQL actif, ni switching automatique, ni ANN accepté en production, ni cutover/rollback/dual-write, ni certification sécurité/juridique/GDPR, ni attribution NLnet.

## Sources anglaises

- [Architecture complète](../ARCHITECTURE.md)
- [Limites stockage/autorité](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [État d’implémentation](../IMPLEMENTATION_STATUS.md)
- [Import PostgreSQL inactif](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
