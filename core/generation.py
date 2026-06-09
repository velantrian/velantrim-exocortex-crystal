# core/generation.py
# Velantrim ExoCortex — Answer Generation (pluggable abstraction)
# v8.5.0-sprint2
#
# Principle: LLM = Language, Graph = Truth. The generator phrases the answer ONLY
# from facts that passed the TruthGate — it adds no external knowledge (anti-hallucination).
#
# Pluggable backend:
#   ExtractiveGenerator (default) — dependency-free: concatenation of claims. CI-safe.
#   AnthropicGenerator — Claude (official SDK). Optional dependency + ANTHROPIC_API_KEY.
#     The FactsPack is placed in system with prompt caching; model claude-opus-4-8,
#     adaptive thinking. Enabled with VELANTRIM_GENERATOR=anthropic.

import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from core._registry import BackendRegistry

logger = logging.getLogger(__name__)

# A9 (LLM call safety): a transient API failure (rate-limit / timeout / overload)
# is retried a bounded number of times with exponential backoff before we degrade
# to the extractive generator. A non-transient error (auth, bad request) is not
# retried. This caps retry storms without adding any dependency.
_TRANSIENT_MARKERS = ("429", "rate_limit", "ratelimit", "timeout", "timed out",
                      "overloaded", "503", "502", "service unavailable")


def _is_transient(err: Exception) -> bool:
    blob = f"{type(err).__name__} {err}".lower()
    return any(m in blob for m in _TRANSIENT_MARKERS)

# Truth-first instruction: answer strictly from the provided facts.
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


# ─── INTERFACE ────────────────────────────────────────────────────────────────

class Generator(ABC):
    """Generator contract: (query, facts) → answer text."""

    @abstractmethod
    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        """Phrase the answer strictly from the provided (verified) facts."""


# ─── EXTRACTIVE (default, dependency-free) ────────────────────────────────────

class ExtractiveGenerator(Generator):
    """Extractive generator: concatenation of claims. Deterministic, CI-safe."""

    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        return " | ".join(f.get("claim", "") for f in facts)


# ─── ANTHROPIC (optional dependency) ─────────────────────────────────────────────

class AnthropicGenerator(Generator):
    """
    Answer generation by the Claude model via the official SDK.

    The FactsPack goes into the system block with prompt caching (stable prefix →
    cache hits on repeats), the user's query — into a user message. Model
    claude-opus-4-8 + adaptive thinking. Answers only from verified
    facts (see _SYSTEM_PROMPT) — the graph remains the source of truth.

    `anthropic` — optional dependency; requires ANTHROPIC_API_KEY. Excluded from
    the coverage gate (CI does not install the SDK and makes no network calls); behavior
    is verified by a test with a stub client.
    """

    def __init__(self, model: str = "claude-opus-4-8", client: Any = None,
                 max_retries: int = 2, backoff_base: float = 1.5) -> None:
        if client is None:  # pragma: no cover - a real client requires the optional dependency
            import anthropic
            client = anthropic.Anthropic()
        self._client = client
        self._model = model
        self._max_retries = max(0, max_retries)   # A9: bounded retries
        self._backoff_base = max(0.0, backoff_base)

    def generate(self, query: str, facts: List[Dict[str, Any]]) -> str:
        system = [{
            "type": "text",
            "text": _SYSTEM_PROMPT + _facts_block(facts),
            "cache_control": {"type": "ephemeral"},  # cache the stable prefix
        }]
        # A9: bounded retry with exponential backoff on transient failures, then
        # degrade to extractive rather than fail (the facts are already verified).
        attempt = 0
        while True:
            try:
                response = self._client.messages.create(
                    model=self._model,
                    max_tokens=1024,                  # bounded output ceiling
                    system=system,
                    thinking={"type": "adaptive"},
                    messages=[{"role": "user", "content": query}],
                )
                return "".join(
                    block.text for block in response.content if block.type == "text"
                ).strip()
            except Exception as e:  # noqa: BLE001 — must not crash the answer
                if _is_transient(e) and attempt < self._max_retries:
                    attempt += 1
                    if self._backoff_base:  # pragma: no cover - real backoff needs a live API
                        time.sleep(self._backoff_base ** attempt)
                    logger.warning(
                        "AnthropicGenerator: transient API failure (%s), "
                        "retry %d/%d", type(e).__name__, attempt, self._max_retries)
                    continue
                logger.warning(
                    "AnthropicGenerator: API failure (%s), falling back to extractive",
                    type(e).__name__,
                )
                return ExtractiveGenerator().generate(query, facts)


# ─── FACTORY / SINGLETON ──────────────────────────────────────────────────────

_GENERATORS = {
    "extractive": ExtractiveGenerator,
    "anthropic": AnthropicGenerator,
}


def _make(name: str) -> Generator:
    if name not in _GENERATORS:
        raise ValueError(
            f"get_generator: unknown backend '{name}'. "
            f"Available: {sorted(_GENERATORS)}"
        )
    return _GENERATORS[name]()


_REGISTRY = BackendRegistry("VELANTRIM_GENERATOR", "extractive", _make)


def get_generator(backend: Optional[str] = None) -> Generator:
    """
    Generator singleton. Backend — via argument or VELANTRIM_GENERATOR
    (default 'extractive').
    """
    return _REGISTRY.get(backend)


def reset_generator() -> None:
    """Reset the singleton (for tests)."""
    _REGISTRY.reset()
