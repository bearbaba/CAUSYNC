"""Official GenLayer SDK DirectVM smoke checks (not consensus/finality proof)."""
import json
import pytest


@pytest.fixture
def jury(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    return direct_deploy("contracts/tracejury.py")


def test_constructor_and_unknown_case(jury):
    assert jury.case_count() == 0
    with pytest.raises(Exception):
        jury.case_status(1)


def test_nonowner_cannot_create_case(jury, direct_vm, direct_alice):
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert("owner only"):
            jury.create_case(
                "0x1111111111111111111111111111111111111111",
                "0x2222222222222222222222222222222222222222",
                "0x3333333333333333333333333333333333333333",
                "a"*64)
