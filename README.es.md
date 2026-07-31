# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md)   · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md)
> 📚 [Documentación en español](./docs/es/README.md) · [Documentazione italiana](./docs/it/README.md) · [Документация на русском](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md)

### *Infraestructura de memoria verificable, local-first y de código abierto para una IA digna de confianza*

`v0.3.0` · 🧪 **1713 superados / 12 omitidos** · 🎯 **100 % de cobertura** · 🐍 **runtime predeterminado basado en la biblioteca estándar** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal es una capa de memoria verificable, no otro chatbot. Cada claim conserva
> su fuente, estado epistémico y metadatos de procedencia. La admisión automática
> en el grafo canónico sigue gobernada por **Guardian + TruthGate**.

> **Fuente normativa:** el código fusionado en GitHub `main` y los documentos en
> inglés determinan la implementación y el alcance de la subvención. Esta versión
> española es una traducción mantenida para reviewers, instituciones y personas
> colaboradoras hispanohablantes. En caso de discrepancia, prevalecen
> [README.md](./README.md), [docs/STATUS.md](./docs/STATUS.md) y
> [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal en un minuto

Crystal es el núcleo público de Velantrim orientado a la subvención:

- memoria operativa local L0/L1;
- backends locales para el grafo canónico L3;
- controles de admisión Guardian y TruthGate;
- `CanonicalView` para respuestas estrictamente fundamentadas;
- TRACE, procedencia y Receipts reproducibles;
- Evidence Spans, colas de revisión y sesiones de importación;
- mecanismos técnicos de borrado y limitación del tratamiento relacionados con el RGPD;
- evaluación determinista y puertas de calidad en CI;
- interfaces opcionales FastAPI y MCP.

Crystal **no es** Titan, el Personal ExoCortex completo, un sistema operativo
cognitivo autónomo, un proyecto de conciencia ni un agente que se automodifica.
Las ideas de investigación pueden alimentar RFC futuros, pero no son capacidades
actuales del runtime.

```text
GitHub Crystal main = verdad pública de implementación
Notion Crystal       = mapa sincronizado de estrategia y subvención
Titan / Full         = línea de investigación separada
```

---

## 🛡️ Frontera de confianza actual

### Ruta de admisión

```text
entrada / documento / evento de agente
→ clasificación y evidencia
→ Guardian + TruthGate
→ memoria operativa L0/L1
→ grafo canónico L3 admitido
```

### Ruta de consulta HTTP

El PR #265 introdujo un contrato HTTP estricto y separado para consultas de solo
lectura:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ únicamente el Canon existente
→ CanonicalView
→ respuesta o rechazo acotado
```

En estas superficies HTTP, formular una pregunta no ingiere contenido en L0/L1,
no transiciona ESM, no escribe hechos ni aristas L3, no procesa la outbox, no
registra enlaces episódicos, no inicializa una huella de embedding y no modifica
el estado de verificación adaptativa.

### Alcance residual declarado explícitamente

- los comandos CLI `ask` y `receipt` todavía utilizan la ruta histórica capaz de admisión;
- `core.pipeline.run()` continúa disponible;
- MCP no expone herramientas explícitas de escritura canónica, pero una búsqueda
  puede inicializar una huella de embedding ausente.

La garantía de solo lectura es deliberadamente precisa y no se generaliza a todos
los callers. Véase la especificación normativa
[read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Modelo de memoria

| Capa | Función | Frontera |
|---|---|---|
| **L0** | caché de trabajo en memoria | rápida, reconstruible |
| **L1** | memoria operativa SQLite/WAL | estados, restricciones y actualizaciones |
| **L2** | claims pendientes y revisión curatorial | no es automáticamente canónica |
| **L3** | grafo canónico | admisión automática únicamente mediante TruthGate |
| **TRACE / Receipt** | capa de prueba | explica la fundamentación y detecta deriva |

El grafo físico puede contener varios estados de verdad. En sentido estricto, el
**Canon** es únicamente la proyección verificada, válida según TRACE y permitida
por la política; no todo nodo existente en un backend de grafo.

---

## 🚀 Inicio rápido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Uso básico de la CLI:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Backend L3 SQLite persistente y local:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Guía detallada: [docs/es/QUICKSTART.md](./docs/es/QUICKSTART.md).

---

## 🔌 Interfaces opcionales

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Método | Ruta | Contrato |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | admisión mediante Guardian + TruthGate |
| `POST` | `/ask` | consulta canónica estrictamente de solo lectura |
| `GET` | `/receipt?q=...` | lectura con Receipt |
| `POST` | `/verify-receipt` | replay del Receipt frente al estado actual |
| `GET` | `/evidence/{fact_id}` | vista pública de evidencia según la política |

FastAPI y Uvicorn son extras opcionales. El runtime predeterminado no requiere un
servicio cloud ni un proveedor externo de modelos.

### MCP

```bash
python -m core.mcp_server
```

MCP proporciona herramientas de inspección para búsqueda, informes de memoria,
historial de hechos, conflictos y verificación de Receipts. Sigue aplicándose la
limitación residual de la huella de embedding.

---

## 🧪 Evaluación

Crystal ya incluye una baseline determinista:

- retrieval `hit@k` y MRR;
- completitud de TRACE y metadatos;
- cobertura de Evidence Spans;
- supervivencia del Receipt replay;
- precisión y recall de contradicciones;
- comprobaciones de rechazo en fronteras de confianza;
- mínimos y máximos de regresión en CI.

La implementación de replay determinista de Titan se revisó como trabajo previo,
no como runtime Crystal copiado. Cualquier implementación futura debe ampliar el
stack de evaluación existente, permanecer offline y no autoritativa, y preservar
TruthGate y las fronteras de consulta.

---

## 💶 Frontera de la subvención

El proyecto se presentó al **NLnet NGI0 Commons Fund** y está en evaluación. El
repositorio no afirma que la financiación haya sido concedida.

```text
BASELINE ACTUAL
    +
DELTA FINANCIADO MEDIBLE
    =
ENTREGABLE VERIFICABLE DE FORMA INDEPENDIENTE
```

El trabajo ya fusionado permanece en la baseline y no se vuelve a contabilizar
como entrega pagada. Los mecanismos cognitivos, neuromórficos o de Titan no se
incorporan silenciosamente al alcance de Crystal.

Resumen español: [docs/es/GRANT_OVERVIEW.md](./docs/es/GRANT_OVERVIEW.md)  
Fuentes normativas:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)

---

## ✅ Puertas de verificación

| Gate | Función |
|---|---|
| pytest + coverage | suite completa con umbral obligatorio de cobertura del 100 % |
| Ruff | lint del código y las herramientas del repositorio |
| Gitleaks | detección de secretos versionados |
| Bandit | análisis estático de seguridad en Python |
| pip-audit | auditoría de vulnerabilidades de dependencias |
| Docker build | construcción reproducible de la imagen endurecida |
| eval-gate | control de regresiones de retrieval, grounding y contradicciones |
| JSONL integrity | estructura del corpus e identificadores duplicados |

Estos controles reducen el riesgo; no demuestran la ausencia de todos los defectos
ni constituyen una certificación jurídica o de seguridad.

---

## 📚 Ruta para reviewers en español

1. [docs/es/REVIEWER_GUIDE.md](./docs/es/REVIEWER_GUIDE.md)
2. [docs/es/QUICKSTART.md](./docs/es/QUICKSTART.md)
3. [docs/es/STATUS.md](./docs/es/STATUS.md)
4. [docs/es/GRANT_OVERVIEW.md](./docs/es/GRANT_OVERVIEW.md)
5. [docs/es/GLOSSARY.md](./docs/es/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — resultados normativos
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — arquitectura normativa

---

## ⚖️ Licencia y contribución

Crystal se distribuye bajo **AGPL-3.0**. Véanse [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) y [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = verdad admitida** · **🔗 Procedencia = confianza** · **🏠 Local-first = control**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md)