# 🚀 Быстрый старт — Velantrim Crystal

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md)
>
> **Примечание:** команды, имена пакетов, переменные окружения и API paths не
> переводятся. При расхождениях действуют GitHub `main` и английские документы.

## 1. Клонировать репозиторий

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
```

## 2. Создать виртуальное окружение

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

## 3. Установить окружение разработки

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

Стандартный runtime Crystal основан на стандартной библиотеке Python.
Зависимости разработки, API и адаптеров подключаются как опциональные extras.

## 4. Выполнить полную проверку

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
```

Нормативная baseline находится в [TEST_REPORT.md](../../TEST_REPORT.md):

```text
1713 passed
12 skipped
0 failed
6389 measured statements
100.00% coverage
```

Эти числа не заменяют независимый запуск на чистом clone.

## 5. Использовать CLI

### Выполнить ingest claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

Ingest является операцией допуска. Новые claims проходят предусмотренные
границы classification, Guardian и TruthGate.

### Задать вопрос

```bash
velantrim ask "how does water behave"
```

⚠️ CLI-команды `ask` и `receipt` пока используют исторический путь
`core.pipeline.run()`, способный выполнять допуск. Строгая гарантия отсутствия
записи относится к мигрированным HTTP endpoints `/ask` и `/receipt`, а не ко
всем callers.

### Создать и проверить Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
velantrim verify-receipt receipt.json --strict-provenance
```

Receipt — запечатанное доказательство использованных фактов и provenance-ссылок.
Replay сравнивает его с текущим состоянием и может обнаружить drift или подмену.

## 6. Включить постоянное локальное хранилище L3

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

SQLite path остаётся локальным. Crystal не отправляет данные автоматически в
cloud или model provider.

## 7. Запустить опциональный FastAPI

```bash
pip install '.[api]'
export VELANTRIM_API_TOKEN=$(python -c "import secrets;print(secrets.token_urlsafe(32))")
velantrim-api
```

Адрес по умолчанию:

```text
http://127.0.0.1:8000
```

Пример:

```bash
curl http://127.0.0.1:8000/health
```

| Метод | Путь | Поведение |
|---|---|---|
| `POST` | `/ingest` | допуск через Guardian + TruthGate |
| `POST` | `/ask` | строгое чтение существующего Canon |
| `GET` | `/receipt?q=...` | чтение с Receipt |
| `POST` | `/verify-receipt` | replay Receipt |

## 8. Запустить опциональный MCP server

```bash
python -m core.mcp_server
```

MCP не предоставляет явных инструментов канонической записи. Поиск может
инициализировать отсутствующий embedding fingerprint, поэтому MCP не описывается
как полностью mutation-free путь.

## 9. Следующие документы

- [Руководство reviewer](./REVIEWER_GUIDE.md)
- [Текущий статус](./STATUS.md)
- [Обзор гранта](./GRANT_OVERVIEW.md)
- [Глоссарий](./GLOSSARY.md)
- [Нормативная архитектура](../ARCHITECTURE.md)
- [Нормативная оценка](../EVAL.md)

---

> 🌐 🇬🇧 [English](../../README.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md)