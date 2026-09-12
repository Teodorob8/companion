from bridge.aegis_companion.idempotency import DuplicateSuppressor

def test_duplicate_is_suppressed():
    d = DuplicateSuppressor()
    assert d.first_seen("abcdefgh")
    assert not d.first_seen("abcdefgh")
