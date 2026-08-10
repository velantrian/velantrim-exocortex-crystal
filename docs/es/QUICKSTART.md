<!-- translation-source: docs/QUICKSTART.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: es -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🚀 Inicio rápido de Crystal

Esta guía ejecuta la base local sin dependencias obligatorias, ingiere una afirmación
explícita, la consulta mediante la frontera de solo lectura y verifica un Receipt.

## Requisitos

- Python 3.11 o 3.12;
- Git;
- una ubicación local para el repositorio y los datos SQLite.

El runtime predeterminado no exige LLM, proveedor de embeddings ni nube. Los extras de
desarrollo y pruebas instalan paquetes opcionales para la suite completa.

## 1. Instalación

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Verificar el repositorio

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

El checkpoint exacto y las métricas esperadas se mantienen en
[TEST_REPORT.md](../../TEST_REPORT.md), no como requisitos mutables duplicados aquí.

## 3. Elegir almacenamiento local persistente

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite sigue siendo el perfil local-first activo ordinario. PostgreSQL/pgvector es solo
una ruta opcional de importación y equivalencia inactiva; el objetivo permanece
`active=false`.

## 4. Ingerir explícitamente una afirmación

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` escribe. La afirmación entra en estado operativo y pasa por Guardian/TruthGate.
El comando no significa que Crystal demuestre por sí mismo la verdad objetiva; la
admisión depende de evidencia y política.

## 5. Consultar por la frontera de solo lectura

```bash
velantrim ask "how does water behave"
```

El `ask` público usa `core.query_pipeline.query()` y no debe crear ni modificar hechos
L0/L1, cambiar ESM, escribir L3, operar el outbox, guardar enlaces de episodios,
inicializar un fingerprint de embeddings no configurado ni persistir candidatos
desconocidos.

Si falta grounding canónico estricto, se espera una negativa acotada. Es un resultado
válido de la frontera de confianza, no necesariamente un error.

## 6. Crear y verificar un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Un Receipt sella consulta, respuesta e identificadores citados bajo un digest y permite
reproducir las citas frente al estado actual. Detecta manipulación; la firma HMAC
opcional requiere una clave local de procedencia.

## 7. Ejecutar la API opcional

```bash
pip install '.[api]'
velantrim-api
```

| Método | Ruta | Frontera |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | admisión/escritura explícita |
| `POST` | `/ask` | consulta estrictamente de solo lectura |
| `GET` | `/receipt?q=...` | consulta más Receipt |
| `POST` | `/verify-receipt` | reproducción del Receipt |
| `GET` | `/evidence/{fact_id}` | vista de evidencia con política |

La API usa una base de bearer token. No es un modelo completo de autorización
multi-tenant de producción.

## 8. Ejecutar la superficie MCP de inspección

```bash
python -m core.mcp_server
```

MCP ofrece búsqueda de solo lectura, informes de memoria, historial de hechos, conflictos
y verificación de Receipts. No expone una herramienta de escritura canónica.

## Errores comunes de frontera

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

- L3 físico no es Canon estricto.
- Confidence, duplicación o similitud de retrieval no constituyen evidencia independiente.
- Importación o equivalencia satisfactoria no es activación, cutover ni selección de backend.

## Documentos siguientes

- [README](../../README.md)
- [Mapa de documentación](../DOCUMENTATION_MAP.md)
- [Arquitectura](../ARCHITECTURE.md)
- [Estado de implementación](../IMPLEMENTATION_STATUS.md)
- [Informe de pruebas](../../TEST_REPORT.md)
- [Política de seguridad](../../SECURITY.md)
