from pathlib import Path

from bridge.aegis_companion.snapshot import build_snapshot_meta, sha256_file


def test_snapshot_meta_has_version_hashes_and_freshness(tmp_path):
    source = tmp_path / "status.json"
    source.write_text('{"status":"PASS"}\n', encoding="utf-8")
    meta = build_snapshot_meta([source], stale_after_seconds=900)
    assert meta["schema"] == "aegis.companion.status/1.0"
    assert meta["source_count"] == 1
    assert meta["sources"][0]["sha256"] == sha256_file(source)
    assert meta["observed_at_utc"]
    assert meta["age_seconds"] is not None
    assert meta["stale"] is False


def test_snapshot_meta_marks_old_source_stale(tmp_path):
    import os, time
    source = tmp_path / "old.json"
    source.write_text('{}\n', encoding="utf-8")
    old = time.time() - 3600
    os.utime(source, (old, old))
    meta = build_snapshot_meta([source], stale_after_seconds=10)
    assert meta["stale"] is True
