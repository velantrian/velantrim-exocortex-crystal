# core/adapters/__init__.py
# Velantrim ExoCortex — Optional knowledge-source adapters (grant WP4)
# v8.27.0-sprint6
#
# The stdlib runtime (core/knowledge.py) handles .txt/.md/.json/.jsonl/.csv.
# WP4 adds optional adapters for heavier formats. Each adapter module
# self-registers here on first import; knowledge.ingest_file() auto-loads
# the right module when an unknown extension is encountered.
#
# Install adapters:
#   pip install "velantrim-exocortex-crystal[yaml]"   → .yaml / .yml
#   pip install "velantrim-exocortex-crystal[pdf]"    → .pdf
#   pip install "velantrim-exocortex-crystal[rdf]"    → .ttl / .n3 / .nt / .rdf
#   pip install "velantrim-exocortex-crystal[adapters]" → all three

from typing import Any, Callable, Dict, List, Optional

# path → list of {claim: str, ...} dicts (same shape as knowledge.extract_claims)
AdapterFn = Callable[[str], List[Dict[str, Any]]]

_REGISTRY: Dict[str, AdapterFn] = {}

# Maps file extension (without dot) → adapter module to auto-import on demand.
_MODULE_FOR: Dict[str, str] = {
    "yaml": "core.adapters.yaml_adapter",
    "yml":  "core.adapters.yaml_adapter",
    "pdf":  "core.adapters.pdf_adapter",
    "ttl":  "core.adapters.rdf_adapter",
    "n3":   "core.adapters.rdf_adapter",
    "nt":   "core.adapters.rdf_adapter",
    "rdf":  "core.adapters.rdf_adapter",
    "owl":  "core.adapters.rdf_adapter",
}


def register(ext: str, fn: AdapterFn) -> None:
    """Register an adapter for a file extension (without leading dot)."""
    _REGISTRY[ext.lower().lstrip(".")] = fn


def get(ext: str) -> Optional[AdapterFn]:
    """Return the adapter for `ext` (without dot), or None if not registered."""
    return _REGISTRY.get(ext.lower().lstrip("."))


def load(ext: str) -> AdapterFn:
    """Auto-import the adapter module for `ext` and return its function.

    Raises ImportError (with an install hint) when the optional dependency is
    missing, and ValueError for wholly unsupported extensions.
    """
    ext = ext.lower().lstrip(".")
    fn = _REGISTRY.get(ext)
    if fn is not None:
        return fn
    mod_name = _MODULE_FOR.get(ext)
    if mod_name is None:
        raise ValueError(
            f"No adapter registered for .{ext}. "
            f"Supported adapter extensions: {sorted(_MODULE_FOR)}"
        )
    import importlib
    importlib.import_module(mod_name)  # triggers self-registration; may raise ImportError
    fn = _REGISTRY.get(ext)
    if fn is None:  # pragma: no cover
        raise RuntimeError(f"Adapter module {mod_name!r} did not register .{ext}")
    return fn


def known_extensions() -> List[str]:
    """File extensions that have a known adapter module (with leading dot)."""
    return [f".{e}" for e in sorted(_MODULE_FOR)]
