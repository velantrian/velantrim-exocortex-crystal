"""Tests for utils/rfc_parser.py RFC extraction helpers."""
import pytest

from utils.rfc_parser import extract_rfc, extract_rfc_mentions


@pytest.mark.parametrize("text, expected", [
    ("see RFC0067 v2.0 for details", "RFC0067 v2.0"),
    ("RFC 67", "RFC0067"),               # zero-padded to 4 digits
    ("rfc12 here", "RFC0012"),           # case-insensitive, padded
    ("RFC1234 v10.3", "RFC1234 v10.3"),
    ("no rfc reference at all", None),
    ("", None),
])
def test_extract_rfc(text, expected):
    assert extract_rfc(text) == expected


def test_extract_rfc_returns_first_only():
    assert extract_rfc("RFC0001 and RFC0002") == "RFC0001"


def test_extract_rfc_mentions_dedups_preserving_order():
    text = "RFC0070, RFC0071 v1.0, RFC0070 again, RFC0072"
    assert extract_rfc_mentions(text) == ["RFC0070", "RFC0071 v1.0", "RFC0072"]


def test_extract_rfc_mentions_empty_when_none():
    assert extract_rfc_mentions("plain text") == []
