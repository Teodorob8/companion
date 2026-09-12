$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "Aegis Companion recovered bootstrap"
Write-Host "Root: $Root"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "Python was not found. Install Python 3.11+ and rerun."
}

if (-not (Test-Path ".venv")) {
  python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r ".\bridge\requirements.txt"

New-Item -ItemType Directory -Force -Path ".\evidence" | Out-Null
New-Item -ItemType Directory -Force -Path ".\runtime\cache" | Out-Null
New-Item -ItemType Directory -Force -Path ".\runtime\config" | Out-Null

Write-Host ""
Write-Host "Running safety foundation tests..."
& ".\.venv\Scripts\python.exe" -m pytest ".\bridge\tests" -q

Write-Host ""
Write-Host "Foundation bootstrap complete."
Write-Host "No scanner or broker configuration was changed."
Write-Host "Start bridge:"
Write-Host "  .\.venv\Scripts\python.exe -m uvicorn bridge.aegis_companion.main:app --host 127.0.0.1 --port 8787"
