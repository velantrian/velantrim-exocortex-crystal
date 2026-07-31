"""Packaging contract: the project builds into a coherent, installable surface."""
import os
import tomllib

import pytest

import core


_PYPROJECT = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")


@pytest.fixture(scope="module")
def pyproject():
    with open(_PYPROJECT, "rb") as f:
        return tomllib.load(f)


def test_core_exposes_version():
    assert isinstance(core.__version__, str) and core.__version__


def test_version_matches_pyproject(pyproject):
    assert pyproject["project"]["version"] == core.__version__


def test_version_is_pep440_valid(pyproject):
    # No "-mvp"-style local suffixes that break sdist/wheel builds.
    import re
    assert re.fullmatch(r"\d+\.\d+\.\d+([abrc]\d+|\.post\d+|\.dev\d+)?",
                        pyproject["project"]["version"])


def test_console_script_target_is_importable(pyproject):
    target = pyproject["project"]["scripts"]["velantrim"]
    assert target == "core.cli:main"
    module, _, func = target.partition(":")
    import importlib
    entry = getattr(importlib.import_module(module), func)
    assert callable(entry)


def test_declared_packages_cover_runtime_imports(pyproject):
    # The runtime is `core` plus the top-level module core.adaptation imports.
    st = pyproject["tool"]["setuptools"]
    assert "core" in st["packages"]
    assert "adaptive_threshold_module" in st["py-modules"]


def test_no_runtime_dependencies(pyproject):
    # Local-first, stdlib-only runtime: the base install pulls nothing in.
    assert pyproject["project"]["dependencies"] == []