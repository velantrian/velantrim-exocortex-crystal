# core/adapters.py
# Velantrim ExoCortex — External-ingestion format adapters (grant WP4)
# v8.27.0-sprint5
#
# Extends `learn` (core/knowledge.py) to more knowledge formats while keeping the
# DEFAULT runtime dependency-free:
#
#   - N-Triples (.nt) RDF       → STDLIB (line-based `<s> <p> <o> .`), always on.
#   - YAML (.yaml / .yml)       → optional `pip install '.[yaml]'` (PyYAML).
#   - PDF (.pdf)                → optional `pip install '.[pdf]'` (pypdf).
#
# Every format still flows through the SAME Guardian → TruthGate path with source
# provenance; adapters only turn a file into claim records. Full Turtle/RDF-XML /
# Wikidata and layout-aware PDF spans remain funded future work.

import importlib
import re
from typing import Any, Dict, List

# ─── N-Triples (dependency-free RDF subset) ───────────────────────────────────
# One triple per line: `<subject> <predicate> <object> .`  Object may be a URI,
# a blank node, or a quoted literal ("text"@lang / "text"^^<type>).
_NT_LINE = re.compile(
    r'^\s*(<[^>]*>|_:\S+)\s+(<[^>]*>)\s+(.+?)\s*\.\s*$')


def _local_name(term: str) -> str:
    """Human-readable local name of a URI/blank node: <http://ex/orbits> → orbits."""
    t = term.strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1]
        tail = re.split(r"[/#]", t)[-1]
        return tail or t
    if t.startswith("_:"):
        return t[2:]
    return t


def _nt_object(term: str) -> str:
    """Object term → readable text (literal value, or local name of a URI)."""
    t = term.strip()
    if t.startswith('"'):
        m = re.match(r'^"((?:[^"\\]|\\.)*)"', t)
        return m.group(1) if m else t.strip('"')
    return _local_name(t)


def extract_ntriples(content: str) -> List[Dict[str, Any]]:
    """Parse N-Triples text into claim records `{claim: "subject predicate object"}`."""
    out: List[Dict[str, Any]] = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _NT_LINE.match(line)
        if not m:
            continue
        claim = f"{_local_name(m.group(1))} {_local_name(m.group(2))} " \
                f"{_nt_object(m.group(3))}".strip()
        if claim:
            out.append({"claim": claim})
    return out


# ─── Optional adapters (clear error when the extra is not installed) ───────────

def _require(module: str, extra: str):
    """Import an optional dependency or raise a clear, actionable ImportError."""
    try:
        return importlib.import_module(module)
    except ImportError as e:
        raise ImportError(
            f"The '{module}' package is required for this format. "
            f"Install it with: pip install '.[{extra}]'") from e


def extract_yaml(content: str) -> List[Dict[str, Any]]:
    """Parse YAML into claim records (optional; needs `.[yaml]`)."""
    yaml = _require("yaml", "yaml")
    from core.knowledge import _normalise_records   # lazy: avoids import cycle
    return _normalise_records(yaml.safe_load(content))


def extract_pdf_text(path: str) -> str:
    """Extract text from a PDF file (optional; needs `.[pdf]`)."""
    pypdf = _require("pypdf", "pdf")
    reader = pypdf.PdfReader(path)
    return "\n".join((page.extract_text() or "") for page in reader.pages)
