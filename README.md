# Aegis Companion — Recovered Foundation

This is a clean reconstruction from the preserved Aegis Companion recovery snapshot.

## Safety status
- PAPER / REPLAY / RESEARCH only.
- Frozen scanner semantics are immutable.
- No live broker authority.
- Research-only components cannot place orders or promote logic.
- Unknown broker state blocks paper execution.
- Duplicate commands/events must be harmless.

## Architecture
Aegis desktop/scanner -> authenticated Companion Bridge -> iOS Companion.

The bridge owns mode/capability checks, command validation, correlation, idempotency,
diagnostics, bounded retries, safe repair, and evidence references.

## Start here on Windows
Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

Then run bridge tests:

```powershell
.\.venv\Scripts\python.exe -m pytest bridge\tests -q
```

Start local bridge:

```powershell
.\.venv\Scripts\python.exe -m uvicorn bridge.aegis_companion.main:app --host 127.0.0.1 --port 8787
```

## iOS
The `ios/` tree is a SwiftUI source scaffold and includes `project.yml` for XcodeGen.
Signing, provisioning, device trust, credentials, and Apple permissions remain explicit
user-controlled steps.
