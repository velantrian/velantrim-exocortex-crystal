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

## 🏛️ Arquitectura de un vistazo

Los tres mapas muestran el mismo sistema desde perspectivas complementarias:
**propósito**, **flujo de información** y **relaciones entre módulos**.

### 🧠 Mindmap — propósito y límites de capacidad

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Propósito
│   ├── Memoria verificable para IA
│   ├── Infraestructura de confianza local-first
│   └── Respuestas y decisiones respaldadas por evidencia
│
├── 🏛️ Modelo de memoria
│   ├── L0 — caché de trabajo dentro del proceso
│   ├── L1 — memoria operativa del ciclo de vida
│   ├── L2 — frontera de pendientes y revisión
│   └── L3 — memoria multiestado basada en grafo
│
├── 🛡️ Frontera de confianza
│   ├── Guardian — controles estructurales y de política
│   ├── TruthGate — frontera de política de admisión
│   ├── TrustSnapshot — reconciliación de lectura inmutable
│   └── CanonicalView — proyección estricta de confianza
│
├── 📜 Evidencia y auditoría
│   ├── Procedencia y evidence spans
│   ├── TRACE — linaje de fundamentación
│   └── Receipt — reproducción y evidencia de manipulación
│
├── ⚖️ Revisión y contradicciones
│   ├── Colas y sesiones reanudables de revisión
│   ├── ContradictionReport inmutable
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ Navegación consultiva
│   └── TopicFacet — metadato multietiqueta no autoritativo
│
├── 🔐 Gobierno y coordinación
│   ├── Roles y capacidades de curador con scope
│   ├── Vinculación con actor autenticado
│   └── Leases de decisión locales al proceso
│
└── 📊 Verificación
    ├── Pruebas y evaluación deterministas
    ├── Cobertura de líneas del 100 %
    ├── Mutation gate Ring Zero
    └── Historial versionado de benchmarks
```

### 🏗️ Arquitectura ASCII — cómo fluye la información

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│      Infraestructura local-first de memoria verificable para IA    │
└─────────────────────────────────────────────────────────────────────┘

                         📥 Ingestión explícita
                                  │
                                  ▼
               🧾 Tipo de afirmación + fuente + evidence span
                                  │
                                  ▼
                       🧠 Estado Observed L0 / L1
                                  │
                                  ▼
            🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restricciones
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ⏳ L2 pendiente / revisión   🏛️ Grafo físico L3
                    │                           │
                    │                           ▼
                    │                 📜 procedencia / TRACE
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                      📐 TrustSnapshot inmutable
                                  │
                                  ▼
                    🛡️ Guardian + CanonicalView STRICT
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
            💬 Respuesta fundamentada   🚫 Rechazo acotado
                     │
                     ▼
              🧾 Receipt reproducible

⚖️ Contradicción sin resolver
        │
        ▼
📋 ContradictionReport inmutable
        │
        ▼
🔐 principal con scope + capacidad + decision lease
        │
        ▼
🧑‍⚖️ COEXIST / CONTEXTUALIZE / SUPERSEDE explícito
        │
        ▼
📜 ruta de escritura canónica auditable

🏷️ Metadatos TopicFacet ──► navegación / filtrado / agrupación
                           └─► nunca autoridad sobre verdad, ESM, evidencia o Canon
```

### 🌳 Árbol de relaciones — cómo se conectan los módulos

```text
🌳 Relaciones del sistema Crystal
│
├── 🧠 Capa de memoria
│   ├── L0 ──► caché de trabajo rápida y reconstruible
│   ├── L1 ──► ciclo de vida, restricciones y trabajo pendiente
│   ├── L2 ──► frontera lógica de revisión
│   └── L3 ──► almacenamiento multiestado basado en grafo
│
├── 🛡️ Capa de confianza
│   ├── Guardian ──► validación estructural y de política
│   ├── TruthGate ──► decisión de admisión
│   ├── TrustSnapshot ──► reconciliación L1/L3 deny-dominant
│   └── CanonicalView ──► proyección estricta de fundamentación
│
├── 📜 Capa de evidencia
│   ├── Metadatos de fuente
│   ├── Evidence spans
│   ├── Procedencia
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Capa de revisión
│   ├── Cola de revisión
│   ├── Sesión reanudable de revisión
│   ├── ContradictionReport
│   └── Disposición explícita
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Capa de autorización
│   ├── CuratorPrincipal
│   ├── Rol y capacidad con scope
│   ├── Coincidencia con actor autenticado
│   └── Decision lease local al proceso
│
├── 🏷️ Capa consultiva
│   └── TopicFacet
│       ├── multietiqueta
│       ├── score solo de relevancia
│       └── sin autoridad sobre verdad o admisión
│
├── 🔎 Capa pública de consultas
│   ├── HTTP /ask y /receipt
│   ├── CLI ask y receipt
│   └── MCP search
│       └── pipeline compartido de solo lectura
│
└── 📊 Capa de verificación
    ├── Pruebas Python 3.11 / 3.12
    ├── Gate de cobertura
    ├── Mutation gate Ring Zero
    ├── Comprobaciones de seguridad y contenedor
    └── Historial de benchmarks
```

### Distinciones centrales

```text
Grafo físico L3 ≠ Canon estricto
consulta ≠ ingestión
confianza ≠ evidencia independiente
salida LLM ≠ fuente factual independiente
contradicción ≠ ganador automático
relevancia temática ≠ verdad o calidad de evidencia
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
