from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Iterable

STATUS_SCHEMA = "aegis.companion.status/1.0"
DEFAULT_STALE_AFTER_SECONDS = 900


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_snapshot_meta(paths: Iterable[Path], stale_after_seconds: int = DEFAULT_STALE_AFTER_SECONDS) -> dict:
    now = datetime.now(timezone.utc)
    sources = []
    newest_mtime = None
    for path in paths:
        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
        newest_mtime = modified if newest_mtime is None or modified > newest_mtime else newest_mtime
        sources.append({
            "path": str(path),
            "sha256": sha256_file(path),
            "modified_at_utc": modified.isoformat(),
        })
    age_seconds = None if newest_mtime is None else max(0.0, (now - newest_mtime).total_seconds())
    stale = True if age_seconds is None else age_seconds > stale_after_seconds
    return {
        "schema": STATUS_SCHEMA,
        "observed_at_utc": now.isoformat(),
        "age_seconds": age_seconds,
        "stale_after_seconds": stale_after_seconds,
        "stale": stale,
        "source_count": len(sources),
        "sources": sources,
    }
