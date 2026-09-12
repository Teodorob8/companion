"""Separate development API for the read-only phone Companion.

This module is intentionally not mounted by the legacy foundation app yet.
"""

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
from pydantic import BaseModel, Field

from .pairing import PairingManager


app = FastAPI(title="Aegis Companion Read-only API", version="0.1.0")
pairing = PairingManager()
_credentials: set[str] = set()


class PairRequest(BaseModel):
    code: str = Field(min_length=6, max_length=6)


@app.get("/health")
def health():
    return {"status": "READY", "mode": "READ_ONLY", "live_authority": False}


@app.get("/pairing", response_class=HTMLResponse)
def pairing_page():
    return '''<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aegis Companion Pairing</title><main style="font:18px system-ui;max-width:32rem;margin:4rem auto;padding:1rem">
<h1>Aegis Companion</h1><p>Enter the one-time pairing code shown on the laptop.</p>
<form id="f"><input id="c" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]{6}" required>
<button>Pair read-only device</button></form><pre id="o"></pre>
<script>f.onsubmit=async e=>{e.preventDefault();o.textContent='Pairing…';let r=await fetch('/companion/pairing/redeem',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({code:c.value})});let x=await r.json();if(r.ok){localStorage.setItem('aegis_companion_credential',x.credential);o.textContent='Paired read-only device. Loading status…';let s=await fetch('/companion/companion/status',{headers:{Authorization:'Bearer '+x.credential}});o.textContent=s.ok?'Paired. Read-only Companion is connected.':'Paired, but status was unavailable.';}else{o.textContent=x.detail||'Pairing failed';}}</script></main>'''


@app.post("/pairing/issue")
def issue_pairing_code(request: Request):
    # Code issuance is a laptop-local action; it is never available remotely.
    if request.client is None or request.client.host not in {"127.0.0.1", "::1"}:
        raise HTTPException(status_code=403, detail="local_pairing_required")
    return {"code": pairing.issue_code()}


@app.post("/pairing/redeem")
def redeem_pairing_code(payload: PairRequest):
    credential = pairing.redeem(payload.code)
    if credential is None:
        raise HTTPException(status_code=401, detail="pairing_failed")
    _credentials.add(credential)
    return {"credential": credential, "scope": "read_only"}


@app.get("/companion/status")
def companion_status(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="credential_required")
    if authorization.removeprefix("Bearer ") not in _credentials:
        raise HTTPException(status_code=401, detail="credential_invalid")
    return {"status": "READ_ONLY", "authority": "Aegis", "live_orders": False}


def _credential(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="credential_required")
    value = authorization.removeprefix("Bearer ")
    if value not in _credentials:
        raise HTTPException(status_code=401, detail="credential_invalid")
    return value


@app.get("/companion/aegis-status")
def aegis_status(authorization: str | None = Header(default=None)):
    _credential(authorization)
    path = Path(r"C:\AegisControl\aegis_health.json")
    try:
        health = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=503, detail=f"health_unavailable:{type(exc).__name__}")
    return {
        "status": "READ_ONLY",
        "overall": health.get("overall"),
        "mode": health.get("mode"),
        "live_order_authority": health.get("liveOrderAuthority", False),
        "repairs_made": health.get("repairsMade", 0),
        "canonical_runtime": health.get("canonicalRuntime"),
        "source": str(path),
        "freshness": path.stat().st_mtime,
    }
