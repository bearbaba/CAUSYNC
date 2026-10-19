"""Offline CASE file validator + SHA-256 calculator for Studio.

Usage: python scripts/prepare_case.py examples/case_01_fault.txt
This script never sends data to a blockchain or external endpoint.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys


def digest(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def parse(path: pathlib.Path) -> tuple[int, str, str]:
    data = path.read_bytes()
    assert 0 < len(data) <= 8192, "document must fit 8192 bytes"
    assert b"\r" not in data and b"\x00" not in data, "noncanonical newlines"
    text = data.decode("utf-8")
    assert text.startswith("CAUSYNC_CASE_V1\n"), "wrong evidence magic"
    header, delimiter, body = text.partition("\n[OBLIGATIONS]\n")
    assert delimiter, "missing obligations section"
    obligations, sep, trace = body.partition("\n[TRACE]\n")
    assert sep, "missing trace section"
    assert "\n[TRACE]\n" not in trace, "duplicate trace section"
    assert 30 <= len(obligations) <= 3500, "invalid obligations length"
    assert 30 <= len(trace) <= 3500, "invalid trace length"
    for role in ("A", "B", "C"):
        assert re.search(r"(?m)^Agent " + role + r"\b", obligations), f"missing {role}"
    lines = header.splitlines()
    assert len(lines) == 6, "expected case ID, chain and three agents"
    assert lines[0] == "CAUSYNC_CASE_V1"
    assert lines[1].startswith("CASE_ID: ")
    case_id = int(lines[1].split(": ", 1)[1])
    assert case_id >= 1 and str(case_id) == lines[1].split(": ", 1)[1]
    assert lines[2] == "CHAIN_ID: 61999", "example targets Studionet"
    for i, role in enumerate(("A", "B", "C"), 3):
        assert re.fullmatch(
            "AGENT_" + role + r": 0x[0-9a-f]{40}", lines[i]), f"bad agent {role}"
    return case_id, obligations, text


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/prepare_case.py <case-evidence.txt>")
        return 2
    path = pathlib.Path(sys.argv[1])
    case_id, obligations, document = parse(path)
    print(f"case_id: {case_id}")
    print(f"spec_sha256: {digest(obligations)}")
    print(f"evidence_sha256: {digest(document)}")
    print(f"bytes: {len(document.encode('utf-8'))}")
    print("Both hashes are of exact UTF-8 content; don't edit the hosted file after pinning.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
