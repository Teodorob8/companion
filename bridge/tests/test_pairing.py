from datetime import datetime, timezone, timedelta

from bridge.aegis_companion.pairing import PairingManager


def test_pairing_code_is_single_use():
    now = datetime.now(timezone.utc)
    manager = PairingManager()
    code = manager.issue_code(now)
    credential = manager.redeem(code, now)
    assert credential and len(credential) > 20
    assert manager.redeem(code, now) is None


def test_pairing_code_expires_and_locks_after_failures():
    now = datetime.now(timezone.utc)
    manager = PairingManager(ttl_seconds=10, max_failures=2)
    code = manager.issue_code(now)
    assert manager.redeem("000000", now) is None
    assert manager.redeem("111111", now) is None
    assert manager.redeem(code, now) is None

    manager = PairingManager(ttl_seconds=10)
    code = manager.issue_code(now)
    assert manager.redeem(code, now + timedelta(seconds=11)) is None
