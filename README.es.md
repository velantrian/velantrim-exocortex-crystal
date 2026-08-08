# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### Infraestructura local-first y verificable de memoria, evidencia y decisiones para sistemas de IA confiables

`v0.3.0` · 🧪 **2078 aprobadas / 13 omitidas / 0 fallidas** · 🎯 **9756 sentencias / 100,00 % de cobertura de líneas** · 🧬 **7/7 mutantes Ring Zero eliminados** · ✅ **9 tareas CI permanentes** · 🐍 **runtime predeterminado solo con la biblioteca estándar de Python** · ⚖️ **AGPL-3.0**

> Crystal no es otro chatbot ni un «oráculo de verdad» autónomo. Es una frontera de memoria, evidencia y decisión que registra qué es una afirmación, de dónde proviene, en qué estado epistémico se encuentra, si puede fundamentar una respuesta y cómo se resolvió una contradicción mediante una decisión explícita y auditable.

**Checkpoint runtime verificado:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337 fusionada.  
**Head validado / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 correctas.  
**Integración PostgreSQL:** `31256316532` — PostgreSQL 16 y pgvector 0.8.2.  
**Evidencia primaria:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) y el [manifest legible por máquina](./docs/status/implementation-manifest.json).

> **Contrato de traducción:** este archivo pretende ser una presentación completa, visual y semántica en español, no un resumen. El inglés sigue siendo la fuente de trabajo principal. Los demás documentos se traducen gradualmente; consulta la [política de localización](./docs/LOCALIZATION_POLICY.md) y el [estado de traducciones](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Por qué existe Crystal

Muchos sistemas de IA mezclan documentos fuente, declaraciones del usuario, salidas del modelo, hipótesis, fragmentos recuperados y memoria duradera en un mismo contexto o almacén vectorial. Así, un texto convincente puede adquirir una autoridad que su evidencia no respalda.

```text
Una afirmación fluida no es automáticamente confiable.
Un nodo del grafo físico no es automáticamente Canon estricto.
Una puntuación de retrieval no es evidencia.
Una salida del modelo no es una fuente factual independiente.
Una contradicción no elige por sí sola al ganador.
Una etiqueta temática no es un veredicto de verdad.
Una importación correcta no activa el backend.
```

## 🧠 Qué proporciona Crystal

- afirmaciones tipadas y ciclo de vida epistémico explícito;
- identidad de fuente, tramos exactos de evidencia y procedencia;
- fronteras de admisión Guardian y TruthGate;
- grafo físico L3 multiestado separado del Canon estricto;
- `TrustSnapshot` inmutable y deny-dominant;
- consultas públicas HTTP, CLI y MCP de solo lectura;
- TRACE y Receipts reproducibles y resistentes a alteraciones;
- restricciones, borrado, auditoría y sesiones de importación;
- colas de revisión y sesiones reanudables;
- informes de contradicción inmutables;
- decisiones `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`;
- capacidades scoped de curador y leases locales al proceso;
- TopicFacet asesor, sin autoridad sobre la verdad;
- evaluación determinista, cobertura del 100 % y mutation gate Ring Zero;
- backup/restore SQLite y migración lógica acotada verificados;
- importación PostgreSQL/pgvector inactiva con equivalencia exacta independiente.

## 🏛️ Arquitectura en tres vistas

### 🧠 Mapa mental

```text
🧠 Crystal
├── 🎯 Propósito
│   ├── memoria verificable para IA
│   ├── infraestructura de confianza local-first
│   └── respuestas y decisiones vinculadas a evidencia
├── 🏛️ Memoria
│   ├── L0 — caché de trabajo rápido
│   ├── L1 — estado operativo y ciclo de vida
│   ├── L2 — frontera de espera/revisión
│   └── L3 — grafo físico multiestado
├── 🛡️ Confianza
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidencia
│   ├── fuente + tramo exacto
│   ├── procedencia
│   ├── TRACE
│   └── Receipt
├── ⚖️ Contradicción
│   ├── cola/sesión de revisión
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Almacenamiento
│   ├── SQLite — perfil local-first ordinario
│   └── PostgreSQL/pgvector — destino inactivo
└── 📊 Verificación
    ├── Python 3.11 / 3.12
    ├── cobertura 100 %
    ├── mutación / seguridad / Docker
    └── evidencia CI exacta
```

### 🏗️ Flujo de información

```text
📥 ingest explícito
        ↓
🧾 tipo de claim + fuente + tramo exacto de evidencia
        ↓
🧠 estado observado en L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restricciones
        ↓                         ↓
⏳ revisión L2              🏛️ grafo físico L3
        └──────────────┬──────────┘
                       ↓
             📐 TrustSnapshot inmutable
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 respuesta fundada     🚫 rechazo justificado
                  ↓
             🧾 Receipt reproducible
```

### 🌳 Árbol de módulos

```text
🌳 Crystal
├── 🧠 Memory: L0 / L1 / L2 / L3
├── 🛡️ Trust: Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence: Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review: Queue / Session / ContradictionReport / Disposition
├── 🔎 Query: HTTP / CLI / MCP
├── 🗄️ Portability: SQLite lifecycle / bundle lógico / import PostgreSQL inactivo
└── 📊 Verification: tests / cobertura / mutación / seguridad / Docker / docs-status
```

## 🧭 Distinciones centrales

```text
grafo físico L3     != Canon estricto
query               != ingest
confidence          != evidencia independiente
salida LLM          != fuente factual independiente
detectar conflicto  != ganador automático
relevancia TopicFacet != verdad
Receipt de migración != evidencia de claim
importación correcta != activación del backend
lease local          != coordinación distribuida
```

TruthGate es una puerta de política de admisión, no un oráculo. El Canon estricto es una proyección de lectura permitida por la política sobre evidencia, estado, ESM, forma de confidence y restricciones de procesamiento.

## 🧱 Superficies de memoria y evidencia

| Superficie | Función | Límite crítico |
|---|---|---|
| L0 | caché de trabajo en proceso | rápido y reconstruible |
| L1 | memoria operativa SQLite/WAL | ciclo de vida y restricciones |
| L2 | frontera lógica de revisión | no es Canon automático |
| L3 | memoria física multiestado | presencia ≠ confianza |
| TrustSnapshot | reconciliación inmutable | resolución deny-dominant |
| CanonicalView | proyección estricta | solo lecturas permitidas |
| TRACE / Receipt | prueba y replay | grounding, deriva, manipulación |
| ContradictionReport | conflicto inmutable | confidence no decide |
| TopicFacet | navegación | no cambia verdad ni Canon |

## 🗄️ SQLite y PostgreSQL/pgvector

```text
SQLite
└── runtime local-first ordinario
    ├── lecturas/escrituras
    ├── backup/restore
    ├── recuperación de locks
    └── exportación lógica canónica acotada

PostgreSQL 16 + pgvector
└── perfil opcional de migración/equivalencia
    ├── extra opcional [postgresql]
    ├── carga diferida del driver
    ├── nuevo esquema de destino
    ├── active=false
    ├── importación SERIALIZABLE
    └── equivalencia independiente count/byte/SHA-256
```

El destino PostgreSQL no forma parte de la composición runtime ordinaria y no sirve lecturas ni escrituras normales. El éxito de la importación no implica activación, selección automática, cutover, rollback, dual-write, admisión TruthGate, pertenencia al Canon, aceptación ANN ni multi-tenancy de producción.

## 🔎 Crystal frente a RAG clásico

| Pregunta | RAG clásico | Crystal |
|---|---|---|
| Encontrar material relevante | fortaleza principal | adaptadores de retrieval |
| Separar afirmación del usuario y hecho verificado | lógica de aplicación | frontera tipada explícita |
| Seguir ciclo de vida y contradicciones | normalmente externo | estados e informes de primer nivel |
| Evitar que texto generado sea su propia fuente | no inherente | invariante Ring Zero |
| Reproducir evidencia de una respuesta | opcional | TRACE y Receipt |
| Resolver contradicciones responsablemente | específico de la app | disposiciones autorizadas |
| Funcionar sin proveedor cloud/modelo obligatorio | variable | base local-first pure-stdlib |

## 🛡️ Frontera pública de solo lectura

`HTTP /ask`, `HTTP /receipt`, `CLI ask`, `CLI receipt` y `MCP search` comparten `core.query_pipeline`. No crean hechos, no cambian el estado ESM, no escriben L3 y no modifican el Canon.

## ⚖️ Decisión explícita de contradicciones

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "las afirmaciones describen contextos diferentes" \
  --expected-report-id REPORT_ID
```

`CuratorLeaseRegistry` coordina solo dentro de un proceso. Un despliegue distribuido necesita un adaptador externo de leases.

## 🚀 Inicio rápido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Herramientas PostgreSQL inactivas opcionales: `pip install -e '.[postgresql]'`.

## 📚 Navegación

- [Índice español](./docs/es/README.md)
- [Mapa inglés](./docs/DOCUMENTATION_MAP.md)
- [Informe de pruebas](./TEST_REPORT.md)
- [Estado](./docs/STATUS.md)
- [Estado de implementación](./docs/IMPLEMENTATION_STATUS.md)
- [Arquitectura](./docs/ARCHITECTURE.md)
- [Seguridad](./SECURITY.md)
- [Ámbito NLnet](./docs/GRANT_NLNET_SCOPE.md)
- [Política de localización](./docs/LOCALIZATION_POLICY.md)
- [Estado de traducciones](./docs/TRANSLATION_STATUS.md)

## ✅ Base verificada

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 correcta
```

## 🚧 Límite de las afirmaciones

Crystal no afirma detección universal de verdad, cero alucinaciones, certificación jurídica GDPR/seguridad, multi-tenancy lista para producción, locking distribuido, AGI o conciencia, runtime PostgreSQL activo, switching automático, cutover/rollback ni un Reader Core dedicado terminado. La propuesta NLnet sigue **submitted / under review / not awarded**.

## 🤝 Contribución y licencia

Consulta [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md), [GOVERNANCE.md](./GOVERNANCE.md) y [AGPL-3.0](./LICENSE).
