# core/generation.py
# Velantrim ExoCortex — Answer Generation (сменная абстракция)
# v8.5.0-sprint2
#
# Принцип: LLM = Language, Graph = Truth. Генератор формулирует ответ ТОЛЬКО из
# фактов, прошедших TruthGate — он не добавляет внешнее знание (анти-галлюцинация).
#
# Backend сменный:
#   ExtractiveGenerator (дефолт) — без зависимостей: склейка claim'ов. CI-safe.
#   AnthropicGenerator — Claude (официальный SDK). Опц. зависимость + ANTHROPIC_API_KEY.
#     FactsPack кладётся в system с prompt caching; модель claude-opus-4-8,
#     adaptive thinking. Включается VELANTRIM_GENERATOR=anthropic.

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

# Truth-first инструкция: отвечать строго по переданным фактам.
_SYSTEM_PROMPT = (
    "You are Velantrim's answer generator. Answer the user's question using ONLY "
    "the verified facts listed below. Do not add information from your own "
    "knowledge, do not speculate, and do not contradict the facts. If the facts "
    "do not contain the answer, say so plainly. Be concise.\n\n"
    "VERIFIED FACTS:\n"
)


def _facts_block(facts: List[Dict[str, Any]]) -> str:
    lines = []
    for f in facts:
        ts = f.get("truth_status", "UNVERIFIED")
        src = f.get("source", "unknown")
        lines.append(f"- [{ts}|{src}] {f.get('claim', '')}")
    return "\n".join(lines)


# ─── ИНТЕРФЕЙС ────────────────────────────────────────────────────────────────

class Generator(ABC):
    """Контракт генератора: (запрос, факты) → текст ответа."""

    @abstractmethod
    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        """Сформулировать ответ строго по переданным (проверенным) фактам."""


# ─── EXTRACTIVE (дефолт, без зависимостей) ────────────────────────────────────

class ExtractiveGenerator(Generator):
    """Экстрактивный генератор: склейка claim'ов. Детерминированный, CI-safe."""

    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        return " | ".join(f.get("claim", "") for f in facts)


# ─── ANTHROPIC (опц. зависимость) ─────────────────────────────────────────────

class AnthropicGenerator(Generator):
    """
    Генерация ответа моделью Claude по официальному SDK.

    FactsPack уходит в system-блок с prompt caching (стабильный префикс →
    кэш-хиты при повторах), запрос пользователя — в user-сообщение. Модель
    claude-opus-4-8 + adaptive thinking. Отвечает только по верифицированным
    фактам (см. _SYSTEM_PROMPT) — графа остаётся источником истины.

    `anthropic` — опц. зависимость; нужен ANTHROPIC_API_KEY. Исключено из
    coverage-гейта (CI не ставит SDK и не делает сетевых вызовов); поведение
    проверяется тестом с подставным клиентом.
    """

    def __init__(self, model: str = "claude-opus-4-8", client: Any = None) -> None:
        if client is None:  # pragma: no cover - реальный клиент требует опц. зависимость
            import anthropic
            client = anthropic.Anthropic()
        self._client = client
        self._model = model

    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        system = [{
            "type": "text",
            "text": _SYSTEM_PROMPT + _facts_block(facts),
            "cache_control": {"type": "ephemeral"},  # кэшируем стабильный префикс
        }]
        response = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            thinking={"type": "adaptive"},
            messages=[{"role": "user", "content": query}],
        )
        return "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()


# ─── ФАБРИКА / SINGLETON ──────────────────────────────────────────────────────

_GENERATORS = {
    "extractive": ExtractiveGenerator,
    "anthropic": AnthropicGenerator,
}

_INSTANCE: Optional[Generator] = None


def get_generator(backend: Optional[str] = None) -> Generator:
    """
    Singleton генератора. Backend — аргументом или VELANTRIM_GENERATOR
    (по умолчанию 'extractive').
    """
    global _INSTANCE
    if _INSTANCE is not None and backend is None:
        return _INSTANCE
    name = backend or os.environ.get("VELANTRIM_GENERATOR", "extractive")
    if name not in _GENERATORS:
        raise ValueError(
            f"get_generator: неизвестный backend '{name}'. "
            f"Доступно: {sorted(_GENERATORS)}"
        )
    instance = _GENERATORS[name]()
    if backend is None:
        _INSTANCE = instance
    return instance


def reset_generator() -> None:
    """Сбросить singleton (для тестов)."""
    global _INSTANCE
    _INSTANCE = None
