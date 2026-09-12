from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

SENSITIVE_KEYS = {"token","password","secret","authorization","api_key","apikey"}

def _redact(value):
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if k.lower() in SENSITIVE_KEYS else _redact(v)) for k,v in value.items()}
    if isinstance(value, list):
        return [_redact(v) for v in value]
    return value

def write_evidence(base: Path, kind: str, payload: dict) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    body = json.dumps(_redact(payload), indent=2, sort_keys=True, default=str).encode()
    digest = hashlib.sha256(body).hexdigest()
    path = base / f"{stamp}_{kind}_{digest[:12]}.json"
    path.write_bytes(body)
    return path
