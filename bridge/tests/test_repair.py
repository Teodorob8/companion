from bridge.aegis_companion.repair import run_safe_repair

def test_recreate_folder(tmp_path):
    p = tmp_path / "missing"
    result = run_safe_repair("recreate_nonsecret_folder", {"path": str(p)})
    assert p.exists()
    assert result.startswith("folder_present:")

def test_unknown_repair_blocked():
    try:
        run_safe_repair("delete_everything", {})
        assert False
    except ValueError as exc:
        assert "not_authorized" in str(exc)
