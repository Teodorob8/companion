from pathlib import Path
import hashlib, json

root = Path(__file__).resolve().parents[1]
important = [
    "README.md",
    "bridge/aegis_companion/main.py",
    "bridge/aegis_companion/authority.py",
    "bridge/aegis_companion/repair.py",
    "contracts/event-envelope.schema.json",
    "contracts/diagnostic-record.schema.json",
    "ios/project.yml",
]
rows = []
for rel in important:
    p = root / rel
    rows.append({
        "path": rel,
        "exists": p.exists(),
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None,
    })
print(json.dumps(rows, indent=2))
raise SystemExit(0 if all(r["exists"] for r in rows) else 2)
