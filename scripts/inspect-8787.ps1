$ids = 43544,46288
foreach ($id in $ids) {
  try {
    $p = Get-CimInstance Win32_Process -Filter "ProcessId=$id"
    Write-Output "PID=$id"
    Write-Output "NAME=$($p.Name)"
    Write-Output "CMD=$($p.CommandLine)"
  } catch {
    Write-Output "PID=$id ERROR=$($_.Exception.Message)"
  }
}
