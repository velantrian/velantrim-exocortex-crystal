# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Infraestructura de memoria verificable y local-first para sistemas de IA fiables

`v0.3.0` · 🧪 **1853 pruebas superadas / 12 omitidas** · 🎯 **100 % de cobertura** · 🧬 **7/7 mutantes declarados eliminados** · ✅ **9 tareas de CI** · 🐍 **runtime predeterminado basado únicamente en la biblioteca estándar de Python** · ⚖️ **AGPL-3.0**

> Crystal no es otro chatbot. Es una frontera de memoria, evidencia y decisiones
> que registra qué es una afirmación, de dónde procede, en qué estado epistémico
> se encuentra, si puede fundamentar una respuesta y cómo se resolvió de forma
> explícita una contradicción.

**Checkpoint de runtime verificado:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 fusionado.  
**Evidencia exacta:** [TEST_REPORT.md](./TEST_REPORT.md) y el
[manifiesto de implementación](./docs/status/implementation-manifest.json).

> Esta traducción conserva los mismos límites funcionales, de seguridad y de
> estado que el README en inglés. Los identificadores estables de API se
> mantienen en su forma de código.

---

## 🎯 Por qué existe Crystal

Muchos sistemas de IA mezclan documentos fuente, afirmaciones del usuario,
salidas del modelo, hipótesis, fragmentos recuperados y memoria duradera en un
mismo contexto o almacén vectorial. Así, un texto convincente puede adquirir una
autoridad que sus evidencias no respaldan.

```text
Una afirmación convincente no es automáticamente fiable.
Un nodo del grafo no pertenece automáticamente al Canon estricto.
Un score de retrieval no es evidencia.
La salida de un modelo no es una fuente independiente.
Una contradicción no elige por sí misma un ganador.
Una etiqueta temática no es un veredicto de verdad.
```

## 🧠 Capacidades principales

- afirmaciones tipadas y ciclo de vida epistémico explícito;
- metadatos de fuente, evidence spans y procedencia;
- fronteras de admisión Guardian y TruthGate;
- grafo físico L3 multiestado separado del Canon estricto;
- reconciliación de lectura `TrustSnapshot` inmutable y deny-dominant;
- consultas públicas HTTP, CLI y MCP estrictamente de solo lectura;
- TRACE y Receipts reproducibles con detección de manipulación;
- restricciones, borrado, auditoría y sesiones de importación;
- colas de revisión y sesiones reanudables;
- informes de contradicción tipados e inmutables;
- decisiones explícitas `COEXIST`, `CONTEXTUALIZE` y `SUPERSEDE`;
- resolución de conflictos mediante CLI y HTTP autenticado;
- roles de curador limitados por scope y leases locales de decisión;
- facetas temáticas consultivas que nunca conceden autoridad;
- especificación ESM legible por máquina;
- evaluación determinista, cobertura del 100 % y mutation gate Ring Zero;
- historial versionado de benchmarks L3.

## 🏛️ Arquitectura

```text
ingestión explícita
→ clasificación + evidencia
→ estado Observed en L0/L1
→ Guardian → TruthGate → controles de restricción/contradicción
→ grafo físico L3 multiestado

consulta pública
→ retrieval de solo lectura
→ TrustSnapshot inmutable
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ respuesta / rechazo / Receipt

contradicción sin resolver
→ ContradictionReport inmutable
→ autorización de actor/rol/scope + decision lease
→ decisión explícita del curador + motivo
→ ruta de escritura canónica auditable

navegación temática
→ TopicFacet consultiva
→ solo filtrado/agrupación — nunca admisión al Canon
```

```text
Grafo físico L3 ≠ Canon estricto
consulta ≠ ingestión
confianza ≠ evidencia independiente
salida LLM ≠ fuente factual independiente
relevancia temática ≠ verdad
lease local ≠ coordinación distribuida garantizada
```

TruthGate es una puerta de política de admisión, no un oráculo que conozca la
verdad objetiva. El Canon estricto es una proyección de lectura autorizada por
la política sobre evidencia, estado, ESM y restricciones de tratamiento.

## 🛡️ Frontera pública de solo lectura

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` y `MCP search` comparten
`core.query_pipeline`. No crean hechos, no cambian ESM, no escriben en L3, no
procesan la outbox y no inicializan una huella de embedding.

Véase [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Resolución explícita de contradicciones

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "las afirmaciones describen contextos distintos" \
  --expected-report-id REPORT_ID
```

En FastAPI, `POST /review/resolve-conflict` debe registrarse con la autenticación
de la aplicación anfitriona. `core.curator_auth` verifica el actor, las
capacidades y el scope. `CuratorLeaseRegistry` protege un único proceso; un
despliegue distribuido necesita un adaptador de lease externo.

Véanse [las superficies de resolución](./docs/CONFLICT_RESOLUTION_SURFACES.md) y
[las facetas temáticas y curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ Facetas temáticas consultivas

`core.topic_facets` proporciona etiquetas normalizadas para navegación, filtrado
y agrupación. Su score expresa únicamente relevancia temática; no modifica el
estado de verdad, la evidencia, ESM ni la pertenencia al Canon estricto.

## 🚀 Inicio rápido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Documentación

- [Mapa de documentación](./docs/DOCUMENTATION_MAP.md)
- [Estado actual](./docs/STATUS.md)
- [Arquitectura](./docs/ARCHITECTURE.md)
- [Informe de pruebas](./TEST_REPORT.md)
- [Evaluación](./docs/EVAL.md)
- [Alcance NLnet](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Baseline verificada

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 Límite de las afirmaciones

Crystal no afirma detectar universalmente la verdad, eliminar todas las
alucinaciones, aportar certificación GDPR o de seguridad, estar listo para un
servicio multi-tenant de producción, realizar conciencia artificial ni
implementar Titan/Full ExoCortex. Los leases actuales son locales al proceso; la
coordinación distribuida y la integración con un proveedor de identidad siguen
siendo trabajos independientes.

## 🤝 Contribución y licencia

Véanse [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) y [AGPL-3.0](./LICENSE).
