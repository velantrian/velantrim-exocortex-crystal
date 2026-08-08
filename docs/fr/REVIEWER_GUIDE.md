<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: fr -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Guide du relecteur — Velantrim Exo-Cortex Crystal

**Checkpoint anglais :** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
Ce guide est une orientation maintenue. Les preuves d’implémentation restent le code de
`main`, les tests exécutables, le CI exact, [TEST_REPORT.md](../../TEST_REPORT.md) et le
[manifest](../status/implementation-manifest.json).

## 1. Objet de la revue

Crystal est une infrastructure publique, local-first, liée aux sources et auditable pour la
mémoire des systèmes d’IA. La base vérifiée inclut claims typés, Guardian/TruthGate, une
projection stricte Canon au-dessus du L3 multi-états, des requêtes publiques read-only, un
chemin ingest explicite séparé, des Receipts et une provenance auditable.

Crystal ne revendique ni AGI, ni conscience, ni vérité universelle, ni zéro hallucination,
ni runtime PostgreSQL actif, ni switching automatique, ni multi-tenancy de production,
ni certification sécurité/RGPD, ni attribution du financement NLnet.

## 2. Reproduire la base

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Les métriques variables se lisent uniquement dans le rapport de tests anglais.

## 3. Frontière lecture/écriture

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explicite, attribué et audité
```

Le `ask` public utilise `core.query_pipeline.query()` et ne doit modifier ni facts, ESM,
L3, outbox, liens d’épisode, identité d’embedding ni candidats inconnus. Un refus borné
quand le grounding strict manque est un comportement sûr attendu.

`ingest` écrit, mais l’admission dépend toujours des evidence, du type de claim, de la policy
et de TruthGate. La sortie du modèle ne peut pas s’auto-certifier comme fait mondial vérifié.

## 4. Storage et migration

SQLite est le profil actif local-first ordinaire. Un premier `auto` durable peut choisir
LadybugDB optionnel s’il est installé, sinon SQLite ; le choix et le locator non secret sont
verrouillés. Le fallback silencieux vers Mock éphémère est interdit.

PostgreSQL/pgvector est une voie opérateur séparée : bundle vérifié → preflight version/TLS
→ nouveau schema inactif → import sérialisable → re-hash indépendant read-only → équivalence
exacte ; la cible reste `active=false`.

Import/equivalence n’est ni activation, ni sélection, ni admission TruthGate, ni strict
Canon, ni cutover, rollback, dual-write ou production readiness.

## 5. Sécurité et confidentialité

Le fonctionnement par défaut n’exige ni cloud, LLM, telemetry ou analytics. Neo4j distant,
Anthropic, Wikidata, Redis, migration PostgreSQL, API élargie et copies backup/export
étendent la frontière uniquement par décision opérateur.

`VELANTRIM_ENCRYPTION_KEY` protège certains champs L1, pas automatiquement tous les L3,
backups, bundles, Receipts, logs ou temporaires. Credentials et DSN secrets ne doivent pas
entrer dans profiles, bundles, receipts, logs, issues ou Notion.

L’effacement du store local actif ne supprime pas automatiquement backups, exports, copies
opérateur, systèmes distants ou données tierces.

## 6. Échecs fail-closed

- Claims non soutenus : blocage, étiquette ou refus borné.
- Conflit profile/locator : échec avant mise en cache du backend.
- Échec d’import : rollback et cible `active=false`.
- Evidence mismatch et manipulation Receipt/audit détectés.
- Entrée surdimensionnée rejetée par les limites.
- Dépendance optionnelle absente sans switch durable caché.
- Exposition externe exige TLS, authentication, least privilege et monitoring.

## 7. Checklist

- [ ] `main` et CI exact identifiés.
- [ ] Query read-only séparée de l’ingest explicite.
- [ ] L3 physique séparé du strict Canon.
- [ ] Import PostgreSQL inactif séparé de l’activation.
- [ ] Réseau, secrets, encryption et erasure vérifiés.
- [ ] Aucune certification, production readiness ou attribution de grant déduite.

Sources anglaises : [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md) et
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md).
