"""Deterministic CAUSYNC invariants; mocked GenLayer ≠ real consensus."""
import importlib.util
import json
import sys
import types
from dataclasses import dataclass
from pathlib import Path

import pytest


class Address(str):
    def __new__(cls, value):
        if isinstance(value, Address):
            return value
        if not isinstance(value, str) or not value.startswith("0x") or len(value) != 42:
            raise ValueError("invalid address")
        return str.__new__(cls, value.lower())

    @property
    def as_hex(self):
        return str(self)


class UserError(Exception):
    pass


class GenericDict(dict):
    def __class_getitem__(cls, _):
        return cls


class GenericList(list):
    def __class_getitem__(cls, _):
        return cls


def make_fake():
    fake = types.ModuleType("genlayer")
    fake.Address = Address
    fake.u256 = int
    fake.DynArray = GenericList
    fake.TreeMap = GenericDict
    fake.allow_storage = lambda cls: cls
    fake.dataclass = dataclass
    gl = types.SimpleNamespace()
    gl.Contract = object
    gl.vm = types.SimpleNamespace(UserError=UserError)
    gl.public = types.SimpleNamespace(write=lambda fn: fn, view=lambda fn: fn)
    gl.message = types.SimpleNamespace(
        sender_address=Address("0x" + "f"*40), chain_id=61999)
    gl.nondet = types.SimpleNamespace(
        web=types.SimpleNamespace(render=lambda url, mode: ""),
        exec_prompt=lambda prompt: "{}")
    gl.eq_principle = types.SimpleNamespace(
        prompt_comparative=lambda evaluate, principle: evaluate())
    fake.gl = gl
    return fake


@pytest.fixture
def fixture(monkeypatch):
    module = make_fake()
    monkeypatch.setitem(sys.modules, "genlayer", module)
    spec = importlib.util.spec_from_file_location(
        "causync_under_test", Path(__file__).resolve().parents[1] /
        "contracts" / "causync.py")
    c = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = c
    spec.loader.exec_module(c)
    causync = c.Causync()
    causync.cases = {}
    return c, causync, module.gl


A, B, C, STRANGER = (
    Address("0x" + x*40) for x in ("1", "2", "3", "4"))


OBLIGATIONS = (
    "Agent A must deliver a source-verified inventory report to Agent B.\n"
    "Agent B must implement the approved inventory totals without changing quantities.\n"
    "Agent C must validate delivered output against the approved totals."
)

TRACE = (
    "Agent A delivered source-verified inventory quantities with reference IDs.\n"
    "Agent B changed quantity 12 to 21 in the submitted implementation without authorization.\n"
    "Agent C flagged the quantity mismatch during validation."
)


def document(c, index, obligations=OBLIGATIONS, trace=TRACE, chain="61999"):
    return (
        f"CAUSYNC_CASE_V1\nCASE_ID: {index}\nCHAIN_ID: {chain}\n"
        f"AGENT_A: {A}\nAGENT_B: {B}\nAGENT_C: {C}\n\n"
        f"[OBLIGATIONS]\n{obligations}\n[TRACE]\n{trace}"
    )


def opened(fixture, obligations=OBLIGATIONS):
    c, causync, gl = fixture
    idx = causync.create_case(A, B, C, c.sha256(obligations))
    return idx


def submitted(fixture, source):
    c, causync, gl = fixture
    idx = opened(fixture)
    causync.submit_evidence(idx, "https://example.org/pinned/case.txt", c.sha256(source))
    gl.nondet.web.render = lambda url, mode: source
    return idx


def verdict(role, obligation, trace):
    bit = {"A": 1, "B": 2, "C": 4}[role]
    return json.dumps({
        "verdict": "AGENT_FAULT", "fault_mask": bit,
        "support": [{"role": role, "obligation_quote": obligation,
                     "trace_quote": trace}]
    })


def test_create_case_scope_and_permissions(fixture):
    c, causync, gl = fixture
    with pytest.raises(UserError, match="zero agent"):
        causync.create_case("0x"+"0"*40, B, C, c.sha256(OBLIGATIONS))
    with pytest.raises(UserError, match="identities"):
        causync.create_case(A, A, C, c.sha256(OBLIGATIONS))
    with pytest.raises(UserError, match="specification hash"):
        causync.create_case(A, B, C, "bad")
    assert causync.case_count() == 0
    idx = opened(fixture)
    assert idx == 1
    assert causync.can_certify(idx, A) is False
    assert causync.can_certify(idx, STRANGER) is False
    status = json.loads(causync.case_status(idx))
    assert status["state"] == "OPEN"
    assert status["spec_sha256"] == c.sha256(OBLIGATIONS)
    gl.message.sender_address = STRANGER
    with pytest.raises(UserError, match="owner only"):
        causync.create_case(A, B, C, c.sha256(OBLIGATIONS))
    with pytest.raises(UserError, match="owner only"):
        causync.submit_evidence(idx, "https://example.org/doc.txt", c.sha256("fake"))


def test_valid_fault_enforces_case_scoped_consequence(fixture):
    c, causync, gl = fixture
    source = document(c, 1)
    idx = submitted(fixture, source)
    gl.nondet.exec_prompt = lambda _: verdict(
        "B", "Agent B must implement the approved inventory totals without changing quantities.",
        "Agent B changed quantity 12 to 21 in the submitted implementation without authorization.")
    assert causync.resolve_case(idx) == "AGENT_FAULT"
    s = json.loads(causync.case_status(idx))
    assert s["fault_mask"] == 2
    assert s["source_sha256"] == c.sha256(source)
    assert s["state"] == "RESOLVED"
    assert s["support_sha256"] == c.sha256(s["support"])
    assert causync.can_certify(idx, A) is True
    assert causync.can_certify(idx, B) is False
    assert causync.can_certify(idx, C) is True
    assert causync.can_certify(idx, STRANGER) is False
    with pytest.raises(UserError, match="case not awaiting"):
        causync.resolve_case(idx)
    with pytest.raises(UserError, match="already committed"):
        causync.submit_evidence(idx, "https://example.org/other.txt", c.sha256("other"))


def test_source_mismatch_does_not_finalize_and_retry_succeeds(fixture):
    c, causync, gl = fixture
    valid = document(c, 1)
    idx = submitted(fixture, valid)
    gl.nondet.web.render = lambda url, mode: valid.replace("quantity 12", "quantity 13")
    assert causync.resolve_case(idx) == "SOURCE_MISMATCH"
    assert json.loads(causync.case_status(idx))["state"] == "SUBMITTED"
    assert all(not causync.can_certify(idx, who) for who in (A, B, C))
    gl.nondet.web.render = lambda url, mode: valid
    gl.nondet.exec_prompt = lambda _: verdict(
        "B", "Agent B must implement the approved inventory totals without changing quantities.",
        "Agent B changed quantity 12 to 21 in the submitted implementation without authorization.")
    assert causync.resolve_case(idx) == "AGENT_FAULT"
    assert causync.can_certify(idx, A)
    assert not causync.can_certify(idx, B)


def test_unavailable_source_is_retriable_without_grants(fixture):
    c, causync, gl = fixture
    valid = document(c, 1)
    idx = submitted(fixture, valid)
    def unavailable(url, mode):
        raise TimeoutError("temporary network outage")
    gl.nondet.web.render = unavailable
    assert causync.resolve_case(idx) == "SOURCE_UNAVAILABLE"
    assert json.loads(causync.case_status(idx))["state"] == "SUBMITTED"
    assert not causync.can_certify(idx, A)
    gl.nondet.web.render = lambda url, mode: valid
    gl.nondet.exec_prompt = lambda _: json.dumps({
        "verdict": "UNVERIFIABLE", "fault_mask": 0, "support": []})
    assert causync.resolve_case(idx) == "UNVERIFIABLE"
    assert json.loads(causync.case_status(idx))["state"] == "RESOLVED"
    assert not causync.can_certify(idx, A)


def test_scope_mismatch_is_not_blame(fixture):
    c, causync, gl = fixture
    wrong_chain = document(c, 1, chain="1")
    idx = submitted(fixture, wrong_chain)
    gl.nondet.exec_prompt = lambda _: verdict(
        "B", "Agent B must implement the approved inventory totals without changing quantities.",
        "Agent B changed quantity 12 to 21 in the submitted implementation without authorization.")
    assert causync.resolve_case(idx) == "UNVERIFIABLE"
    assert json.loads(causync.case_status(idx))["fault_mask"] == 0


def test_fabricated_citation_cannot_assign_fault(fixture):
    c, causync, gl = fixture
    source = document(c, 1)
    idx = submitted(fixture, source)
    gl.nondet.exec_prompt = lambda _: verdict(
        "B", "Agent B must implement the approved inventory totals without changing quantities.",
        "Agent B intentionally stole every customer's money.")
    assert causync.resolve_case(idx) == "UNVERIFIABLE"
    assert causync.can_certify(idx, B) is False


def test_shared_fault_requires_support_for_all_roles(fixture):
    c, causync, gl = fixture
    source = document(c, 1)
    idx = submitted(fixture, source)
    gl.nondet.exec_prompt = lambda _: json.dumps({
        "verdict": "SHARED_FAULT", "fault_mask": 3,
        "support": [{"role": "B",
            "obligation_quote": "Agent B must implement the approved inventory totals without changing quantities.",
            "trace_quote": "Agent B changed quantity 12 to 21 in the submitted implementation without authorization."}]
    })
    assert causync.resolve_case(idx) == "UNVERIFIABLE"


def test_no_fault_requires_three_affirmative_evidence_pairs(fixture):
    c, causync, gl = fixture
    source = document(c, 1)
    idx = submitted(fixture, source)
    gl.nondet.exec_prompt = lambda _: json.dumps({
        "verdict": "NO_FAULT", "fault_mask": 0, "support": []})
    assert causync.resolve_case(idx) == "UNVERIFIABLE"
    assert all(not causync.can_certify(idx, who) for who in (A, B, C))


def test_no_fault_positive_three_role_evidence(fixture):
    c, causync, gl = fixture
    affirmative = (
        "Agent A delivered source-verified inventory quantities with reference IDs.\n"
        "Agent B implemented the approved inventory totals without changing quantities.\n"
        "Agent C validated the delivered output against the approved totals."
    )
    source = document(c, 1, trace=affirmative)
    idx = submitted(fixture, source)
    gl.nondet.exec_prompt = lambda _: json.dumps({
        "verdict": "NO_FAULT", "fault_mask": 0, "support": [
            {"role": "A",
             "obligation_quote": "Agent A must deliver a source-verified inventory report to Agent B.",
             "trace_quote": "Agent A delivered source-verified inventory quantities with reference IDs."},
            {"role": "B",
             "obligation_quote": "Agent B must implement the approved inventory totals without changing quantities.",
             "trace_quote": "Agent B implemented the approved inventory totals without changing quantities."},
            {"role": "C",
             "obligation_quote": "Agent C must validate delivered output against the approved totals.",
             "trace_quote": "Agent C validated the delivered output against the approved totals."}
        ]})
    assert causync.resolve_case(idx) == "NO_FAULT"
    assert all(causync.can_certify(idx, who) for who in (A, B, C))
    status = json.loads(causync.case_status(idx))
    assert len(json.loads(status["support"])) == 3


def test_unauthorized_resolution_and_bad_inputs(fixture):
    c, causync, gl = fixture
    idx = opened(fixture)
    with pytest.raises(UserError, match="invalid evidence URL"):
        causync.submit_evidence(idx, "http://unsafe.org/data", c.sha256("x"))
    with pytest.raises(UserError, match="digest"):
        causync.submit_evidence(idx, "https://example.org/doc", "ff")
    source = document(c, idx)
    causync.submit_evidence(idx, "https://example.org/pinned.txt", c.sha256(source))
    gl.message.sender_address = STRANGER
    with pytest.raises(UserError, match="owner only"):
        causync.resolve_case(idx)
    gl.message.sender_address = Address("0x"+"f"*40)
    assert json.loads(causync.case_status(idx))["state"] == "SUBMITTED"
    with pytest.raises(UserError, match="unknown case"):
        causync.case_status(99)


def test_terminal_unverifiable_cannot_use_unpinned_source_hash(fixture):
    c, causync, gl = fixture
    source = document(c, 1)
    idx = submitted(fixture, source)
    forged = json.dumps({
        "verdict": "UNVERIFIABLE",
        "fault_mask": 0,
        "source_sha256": "f"*64,
        "support": []})
    gl.eq_principle.prompt_comparative = lambda evaluate, principle: forged
    with pytest.raises(UserError, match="terminal consensus source hash mismatch"):
        causync.resolve_case(idx)
    assert json.loads(causync.case_status(idx))["state"] == "SUBMITTED"
    assert all(not causync.can_certify(idx, who) for who in (A, B, C))
