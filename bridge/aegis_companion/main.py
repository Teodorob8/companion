from pathlib import Path
import csv, json
from fastapi import FastAPI, HTTPException
from .models import Command, Capability
from .authority import allowed
from .idempotency import DuplicateSuppressor
from .evidence import write_evidence
from .repair import run_safe_repair
from .snapshot import build_snapshot_meta

app = FastAPI(title="Aegis Companion Bridge", version="0.2.0-readonly")
dupes = DuplicateSuppressor()
evidence_dir = Path("evidence")
BROKER_STATE_KNOWN = False
AEGIS_ROOT = Path(r"C:\Aegis")

def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def _paper_counts(path: Path) -> dict:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    closed = sum(r.get("lifecycle_state") in {"PAPER_CLOSED", "REVIEWED"} for r in rows)
    return {"rows": len(rows), "closed": closed}

@app.get("/health")
def health():
    return {
        "status": "FOUNDATION",
        "bridge": "ready",
        "live_authority": False,
        "broker_state_known": BROKER_STATE_KNOWN,
        "modes": ["PAPER","REPLAY","RESEARCH"],
    }

@app.get("/aegis/status")
def aegis_status():
    try:
        authority_path = AEGIS_ROOT / r"Runtime\Active\AEGIS_RUNTIME_AUTHORITY.json"
        validation_path = AEGIS_ROOT / r"EngineeringLabs\Reports\FULL_SYSTEM_VALIDATION_LATEST.json"
        adf_path = AEGIS_ROOT / r"Data\ADF\paper_eligibility_20260908.json"
        ledger_path = AEGIS_ROOT / r"Data\PaperResearch\paper_validation\paper_trade_ledger.csv"
        authority = _read_json(authority_path)
        validation = _read_json(validation_path)
        adf = _read_json(adf_path)
        paper = _paper_counts(ledger_path)
        snapshot = build_snapshot_meta([authority_path, validation_path, adf_path, ledger_path])
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"authoritative_snapshot_unavailable:{type(exc).__name__}")
    return {
        "status": "READ_ONLY",
        "runtime_status": authority.get("status"),
        "runtime_mode": authority.get("mode"),
        "full_system_validation": validation.get("status"),
        "adf_paper_eligibility": adf.get("status"),
        "paper_ledger": paper,
        "live_authority": False,
        "orders_enabled": False,
        "broker_state_known": BROKER_STATE_KNOWN,
        "frozen_scanner_modified": authority.get("frozen_scanner_modified"),
        "snapshot": snapshot,
    }

@app.post("/command")
def command(cmd: Command):
    if not allowed(cmd.mode, cmd.requested_capability, broker_state_known=BROKER_STATE_KNOWN):
        raise HTTPException(status_code=403, detail="capability_not_authorized")
    if not dupes.first_seen(cmd.idempotency_key):
        return {"status":"duplicate_suppressed","idempotency_key":cmd.idempotency_key}

    if cmd.requested_capability == Capability.SAFE_REPAIR:
        name = str(cmd.args.get("repair",""))
        ctx = dict(cmd.args.get("context",{}))
        try:
            result = run_safe_repair(name, ctx)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        path = write_evidence(evidence_dir, "safe_repair", {
            "command": cmd.model_dump(mode="json"),
            "result": result,
        })
        return {"status":"ok","result":result,"evidence_path":str(path)}

    path = write_evidence(evidence_dir, "command", {
        "command": cmd.model_dump(mode="json"),
        "note": "Foundation bridge does not execute scanner/broker actions.",
    })
    return {"status":"accepted_foundation_only","evidence_path":str(path)}
