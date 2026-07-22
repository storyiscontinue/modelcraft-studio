param(
    [switch]$SelfTest,
    [switch]$Test
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe = Join-Path $root "OfflineModelingAgent.exe"
if (Test-Path -LiteralPath $exe) {
    if ($Test) { throw "Source tests are not included in the clean portable release" }
    if ($SelfTest) { & $exe --self-test } else { & $exe }
    exit $LASTEXITCODE
}
$env:PYTHONPATH = Join-Path $root "src"
Push-Location $root
try {
    if ($Test) { python -m unittest discover -s tests -v }
    elseif ($SelfTest) { python -m offline_modeling_agent --self-test }
    else { python -m offline_modeling_agent }
} finally { Pop-Location }
exit $LASTEXITCODE