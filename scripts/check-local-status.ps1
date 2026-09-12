$ErrorActionPreference = 'Stop'
$response = Invoke-RestMethod -Uri 'http://127.0.0.1:8787/aegis/status' -TimeoutSec 5
$response | ConvertTo-Json -Depth 8
