"""Tests for core/generation.py — the swappable answer generator."""
import pytest

from core.generation import (
    ExtractiveGenerator,
    AnthropicGenerator,
    get_generator,
    reset_generator,
)


def test_extractive_generator_joins_claims():
    g = ExtractiveGenerator()
    out = g.generate("q", [{"claim": "A"}, {"claim": "B"}])
    assert out == "A | B"


def test_factory_default_is_extractive_singleton():
    reset_generator()
    g1 = get_generator()
    assert isinstance(g1, ExtractiveGenerator)
    assert get_generator() is g1


def test_factory_unknown_backend_raises():
    with pytest.raises(ValueError, match="unknown backend"):
        get_generator(backend="gpt")


# ─── AnthropicGenerator (injected fake client — no SDK, no network) ───────────

class _FakeBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeResponse:
    def __init__(self, text):
        self.content = [_FakeBlock(text)]


class _FakeMessages:
    def __init__(self):
        self.captured = None

    def create(self, **kwargs):
        self.captured = kwargs
        return _FakeResponse("DNA stores genetic information.")


class _FakeClient:
    def __init__(self):
        self.messages = _FakeMessages()


def test_anthropic_generator_builds_truthful_request():
    fake = _FakeClient()
    gen = AnthropicGenerator(client=fake)
    facts = [{"claim": "DNA encodes genetic information",
              "source": "biology", "truth_status": "VERIFIED"}]

    out = gen.generate("How does DNA work?", facts)

    assert out == "DNA stores genetic information."
    kw = fake.messages.captured
    assert kw["model"] == "claude-opus-4-8"           # skill default
    assert kw["thinking"] == {"type": "adaptive"}
    # FactsPack is grounded in the system prefix, with prompt caching enabled
    system_text = kw["system"][0]["text"]
    assert "DNA encodes genetic information" in system_text
    assert "ONLY" in system_text                       # truth-first instruction
    assert kw["system"][0]["cache_control"] == {"type": "ephemeral"}
    # the user turn carries the query
    assert kw["messages"][0]["content"] == "How does DNA work?"


def test_anthropic_generator_concatenates_text_blocks_only():
    class MultiBlockMessages(_FakeMessages):
        def create(self, **kwargs):
            self.captured = kwargs
            resp = _FakeResponse("answer")
            thinking = _FakeBlock("ignored")
            thinking.type = "thinking"
            resp.content = [thinking, _FakeBlock("answer")]
            return resp

    fake = _FakeClient()
    fake.messages = MultiBlockMessages()
    out = AnthropicGenerator(client=fake).generate("q", [{"claim": "c"}])
    assert out == "answer"  # thinking block excluded


def test_anthropic_generator_falls_back_to_extractive_on_api_error():
    class BoomMessages:
        def create(self, **kwargs):
            raise RuntimeError("rate limited")

    fake = _FakeClient()
    fake.messages = BoomMessages()
    out = AnthropicGenerator(client=fake).generate("q", [{"claim": "A"}, {"claim": "B"}])
    assert out == "A | B"  # graceful degradation, not a crash
