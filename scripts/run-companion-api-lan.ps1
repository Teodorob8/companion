[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$BindAddress,
    [int]$Port = 8877,
    [Parameter(Mandatory=$true)][string]$Certificate,
    [Parameter(Mandatory=$true)][string]$Key
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if ($BindAddress -in @('127.0.0.1','::1','localhost')) {
    throw 'Use run-companion-api-local.ps1 for loopback development.'
}
if (!(Test-Path -LiteralPath $Certificate) -or !(Test-Path -LiteralPath $Key)) {
    throw 'Refusing LAN bind: TLS certificate and key must both exist.'
}

$env:PYTHONPATH = $root
$python = (Get-Command py -ErrorAction Stop).Source
Write-Host "Aegis Companion API: HTTPS $BindAddress`:$Port"
Write-Host 'Mode: read-only; explicit TLS-gated LAN runner'
& $python -3 -m uvicorn bridge.aegis_companion.readonly_api:app `
    --app-dir $root --host $BindAddress --port $Port `
    --ssl-certfile $Certificate --ssl-keyfile $Key
