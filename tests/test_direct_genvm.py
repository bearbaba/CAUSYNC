"""Official GenLayer SDK DirectVM smoke checks (not consensus/finality proof)."""
import json
import pytest


@pytest.fixture
def causync(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    return direct_deploy("contracts/causync.py")


def test_constructor_and_unknown_case(causync):
    assert causync.case_count() == 0
    with pytest.raises(Exception):
        causync.case_status(1)


def test_nonowner_cannot_create_case(causync, direct_vm, direct_alice):
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("owner only"):
            causync.create_case(
                "0x1111111111111111111111111111111111111111",
                "0x2222222222222222222222222222222222222222",
                "0x3333333333333333333333333333333333333333",
                "a"*64)


def test_directvm_create_submit_and_permission_denied_before_verdict(causync):
    """Covers actual GenVM TreeMap/dataclass storage writes, not a Python shim."""
    assert causync.create_case(
        "0x1111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222",
        "0x3333333333333333333333333333333333333333",
        "a"*64) == 1
    first = json.loads(causync.case_status(1))
    assert first["state"] == "OPEN"
    assert first["spec_sha256"] == "a"*64
    assert causync.can_certify(
        1, "0x1111111111111111111111111111111111111111") is False
    assert causync.submit_evidence(
        1, "https://example.org/case-1.txt", "b"*64) == "SUBMITTED"
    latest = json.loads(causync.case_status(1))
    assert latest["state"] == "SUBMITTED"
    assert latest["evidence_sha256"] == "b"*64
    assert causync.case_count() == 1


def test_nonowner_cannot_submit_or_resolve(causync, direct_vm, direct_alice):
    """Real GenVM sender checks: unauthorized writes leave case state unchanged."""
    a = "0x1111111111111111111111111111111111111111"
    b = "0x2222222222222222222222222222222222222222"
    c = "0x3333333333333333333333333333333333333333"
    url = "https://example.org/frozen-evidence.txt"
    assert causync.create_case(a, b, c, "a" * 64) == 1

    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("owner only"):
            causync.submit_evidence(1, url, "b" * 64)
    initial = json.loads(causync.case_status(1))
    assert initial["state"] == "OPEN"
    assert initial["evidence_url"] == ""
    assert initial["evidence_sha256"] == ""

    assert causync.submit_evidence(1, url, "b" * 64) == "SUBMITTED"
    before = causync.case_status(1)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("owner only"):
            causync.resolve_case(1)
    after = causync.case_status(1)
    assert before == after
    assert json.loads(after)["state"] == "SUBMITTED"
    assert causync.can_certify(1, a) is False
    assert causync.can_certify(1, b) is False
    assert causync.can_certify(1, c) is False
