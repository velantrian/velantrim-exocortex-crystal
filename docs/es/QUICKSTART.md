# 🚀 Inicio rápido — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md)
>
> **Nota:** los comandos, nombres de paquetes, variables de entorno y rutas de API
> no se traducen. En caso de discrepancia, GitHub `main` y los documentos en inglés
> son autoritativos.

## 1. Clonar el repositorio

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. Crear un entorno virtual

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Instalar el entorno de desarrollo

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

El runtime predeterminado de Crystal se basa en la biblioteca estándar de Python.
Las dependencias de desarrollo, API y adaptadores son extras opcionales.

## 4. Ejecutar la verificación completa

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

La baseline normativa se encuentra en [TEST_REPORT.md](../../TEST_REPORT.md). El
checkpoint documentado es:

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Estas cifras no sustituyen una ejecución independiente sobre un clon limpio.

## 5. Utilizar la CLI

### Ingerir un claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

La ingestión es una operación de admisión. Los claims nuevos atraviesan las
fronteras previstas de clasificación, Guardian y TruthGate.

### Formular una pregunta

```bash
velantrim ask "how does water behave"
```

⚠️ Los comandos CLI `ask` y `receipt` todavía utilizan la ruta histórica
`core.pipeline.run()`, capaz de admisión. La garantía estricta de cero escrituras
se aplica actualmente a los endpoints HTTP migrados `/ask` y `/receipt`, no a
todos los callers.

### Generar y verificar un Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Un Receipt es una prueba sellada de los hechos y referencias de procedencia
utilizados. Su replay compara la prueba con el estado actual y puede revelar
deriva o manipulación.

## 6. Activar almacenamiento L3 local persistente

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

La ruta SQLite permanece local. Crystal no envía datos automáticamente a un
proveedor cloud o de modelos.

## 7. Iniciar la interfaz FastAPI opcional

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

Dirección predeterminada:

```text
http://127.0.0.1:8000
```

Ejemplo:

```bash
curl http://127.0.0.1:8000/health
```

| Método | Ruta | Comportamiento |
|---|---|---|
| `POST` | `/ingest` | admisión mediante Guardian + TruthGate |
| `POST` | `/ask` | lectura estricta del Canon existente |
| `GET` | `/receipt?q=...` | lectura con Receipt |
| `POST` | `/verify-receipt` | replay del Receipt |

## 8. Iniciar el servidor MCP opcional

```bash
python -m core.mcp_server
```

MCP no ofrece herramientas explícitas de escritura canónica. Sin embargo, una
búsqueda puede inicializar una huella de embedding ausente; por ello MCP no se
describe como una ruta completamente libre de mutaciones.

## 9. Documentos siguientes

- [Guía para reviewers](./REVIEWER_GUIDE.md)
- [Estado actual](./STATUS.md)
- [Resumen de subvención](./GRANT_OVERVIEW.md)
- [Glosario](./GLOSSARY.md)
- [Arquitectura normativa](../ARCHITECTURE.md)
- [Evaluación normativa](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 [Русский](../ru/QUICKSTART.md) · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md)