# core/demo_seed.py
# Demonstration seed corpus for Velantrim Crystal.
#
# This module is opt-in only. The production pipeline loads it exclusively when
# VELANTRIM_DEMO_SEED=1 is set in the environment. By default the canonical
# graph starts empty and all facts must be ingested through the normal
# ingest() / velantrim learn path.
#
# Facts here carry source_status=EXTERNAL (curated reference knowledge, not
# user reports) so they pass TruthGate as VERIFIED — appropriate for a small
# set of well-known physical/scientific constants used in demos.
#
# Do NOT import this module directly from production code paths. Load via
# core/pipeline.py → _load_demo_seed() which checks the env flag.

DEMO_FACTS = [
    {
        "id": "f1",
        "text": "Water boils at 100°C at sea level",
        "source": "physics",
        "confidence": 0.99,
        "source_status": "EXTERNAL",
    },
    {
        "id": "f2",
        "text": "Quantum entanglement links particles",
        "source": "physics",
        "confidence": 0.85,
        "source_status": "EXTERNAL",
    },
    {
        "id": "f3",
        "text": "Earth revolves around the Sun",
        "source": "astronomy",
        "confidence": 0.99,
        "source_status": "EXTERNAL",
    },
    {
        "id": "f4",
        "text": "The human brain has ~86 billion neurons",
        "source": "neuroscience",
        "confidence": 0.90,
        "source_status": "EXTERNAL",
    },
    {
        "id": "f5",
        "text": "DNA encodes genetic information",
        "source": "biology",
        "confidence": 0.99,
        "source_status": "EXTERNAL",
    },
]
