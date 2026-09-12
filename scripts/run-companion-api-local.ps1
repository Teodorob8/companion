[CmdletBinding()]
param([int]$Port = 8877)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $root
$python = (Get-Command py -ErrorAction Stop).Source

Write-Host 'Aegis Companion API (local development only)'
Write-Host "Binding: 127.0.0.1:$Port"
Write-Host 'Mode: read-only; Wi-Fi exposure disabled'

& $python -3 -m uvicorn bridge.aegis_companion.readonly_api:app `
    --app-dir $root --host 127.0.0.1 --port $Port
