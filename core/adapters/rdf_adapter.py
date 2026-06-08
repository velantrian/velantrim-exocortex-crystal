# core/adapters/rdf_adapter.py
# Velantrim ExoCortex — RDF / Linked Data adapter (grant WP4)
# v8.27.0-sprint6
#
# Parses RDF graphs (Turtle .ttl, N-Triples .nt, N3 .n3, RDF/XML .rdf, OWL
# .owl) via rdflib and converts each triple to a natural-language claim string
# "{subject} {predicate} {object}". Namespace prefixes and CamelCase predicate
# names are normalised to readable lowercase tokens. Blank-node subjects are
# skipped so every emitted claim has a named subject.
#
# This is the foundation for importing Wikidata / DBpedia exports and any
# Linked-Data corpus into the verifiable canon (TruthGate still applies —
# nothing is blindly trusted because it arrived as RDF).
#
# Install: pip install "velantrim-exocortex-crystal[rdf]"
from __future__ import annotations

import re
from typing import Any, Dict, List

try:
    import rdflib as _rdflib
except ImportError as _exc:
    raise ImportError(
        "RDF adapter requires rdflib. "
        'Install with: pip install "velantrim-exocortex-crystal[rdf]"'
    ) from _exc

from core.adapters import register

_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_UNDER_RE = re.compile(r"[_\-]+")


def _local(uri: str) -> str:
    """Strip namespace → local name, un-camelCase, lowercase."""
    local = uri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    local = _CAMEL_RE.sub(" ", local)
    local = _UNDER_RE.sub(" ", local)
    return local.lower().strip()


def extract_rdf_claims(path: str) -> List[Dict[str, Any]]:
    """Parse an RDF file and return one claim dict per named-subject triple."""
    g = _rdflib.Graph()
    g.parse(path)
    claims: List[Dict[str, Any]] = []
    for s, p, o in g:
        if isinstance(s, _rdflib.BNode):
            continue
        subj = _local(str(s))
        pred = _local(str(p))
        if isinstance(o, _rdflib.URIRef):
            obj = _local(str(o))
        elif isinstance(o, _rdflib.Literal):
            obj = str(o).strip()
        else:
            continue  # skip blank-node objects too
        claim = f"{subj} {pred} {obj}"
        if len(claim) >= 10:
            claims.append({"claim": claim})
    return claims


for _ext in ("ttl", "n3", "nt", "rdf", "owl"):
    register(_ext, extract_rdf_claims)
