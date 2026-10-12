<#
PIPD-LS-SP first run for Windows — portable, self-locating, no developer paths.

Same chain as run.sh: preconditions -> doctor -> intake -> compile-pi -> bind-pd -> compile-ecp
-> compile-tqaep -> assemble -> validate -> refusal check. Every path is derived from this script's
own location and the scratch workspace lives under $env:TEMP, outside the checkout. Set $env:PYTHON
to override interpreter auto-detection. Exit 0 means every POSITIVE step exited 0 AND the NEGATIVE
step refused with a non-zero code; a missing precondition exits 3.

Run:  powershell -NoProfile -ExecutionPolicy Bypass -File examples\first-run\run.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

function Fail([string]$Message) {
    Write-Error "PRECONDITION_FAIL: $Message"
    exit 3
}

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = (Resolve-Path (Join-Path $Here '..\..')).Path

# ---------------------------------------------------------------- preconditions
$Py = $env:PYTHON
if (-not $Py) {
    foreach ($candidate in @('python3', 'python')) {
        $found = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($found) { $Py = $found.Source; break }
    }
}
if (-not $Py) { Fail 'no python3/python on PATH (set $env:PYTHON=<interpreter>)' }

$probe = & $Py -c "import sys, jsonschema; print(sys.version_info >= (3, 11))" 2>&1
if ($LASTEXITCODE -ne 0 -or ($probe -join '') -notmatch 'True') {
    Fail "Python >= 3.11 with the 'jsonschema' package is required (probe said: $probe)"
}

# Prefer an installed distribution (no PYTHONPATH at all); otherwise use THIS checkout's src/.
$Pipd = Get-Command pipd -ErrorAction SilentlyContinue
if ($Pipd) {
    $Mode = "installed ($($Pipd.Source))"
    $Cli = { param([string[]]$a) & $Pipd.Source @a }
} elseif (Test-Path (Join-Path $Root 'src\pipd_ls_sp\cli.py')) {
    $Mode = "source ($Root\src)"
    $env:PYTHONPATH = (Join-Path $Root 'src')
    $Cli = { param([string[]]$a) & $Py -B -m pipd_ls_sp.cli @a }
} else {
    Fail "no installed 'pipd' and no src\pipd_ls_sp\cli.py under $Root"
}

$Art = Join-Path $env:TEMP ("pipd-first-run-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$Ctx = Join-Path $Art 'ctx'
New-Item -ItemType Directory -Force -Path $Ctx | Out-Null
$Source = Join-Path $Root 'examples\first-run\source.txt'
if (-not (Test-Path $Source)) { Fail "fixture missing: $Source" }

Write-Host "checkout : $Root"
Write-Host "runner   : $Mode"
Write-Host "workspace: $Art"
Write-Host ''

# A step whose non-zero exit is a failure: $LASTEXITCODE is checked immediately, because a native
# command's failure does NOT throw even with $ErrorActionPreference = 'Stop'.
function Step([string]$Label, [scriptblock]$Body) {
    Write-Host "--- $Label"
    & $Body
    if ($LASTEXITCODE -ne 0) { Fail "step '$Label' exited $LASTEXITCODE" }
}

function Invoke-Cli([string[]]$Arguments, [string]$OutFile) {
    if ($OutFile) { & $Cli $Arguments > $OutFile } else { & $Cli $Arguments }
}

Step 'doctor' { Invoke-Cli @('--root', $Art, 'doctor') }
Step 'intake' {
    Invoke-Cli @('--root', $Art, 'init') (Join-Path $Art 'init.json')
    Invoke-Cli @(
        '--root', $Art, 'intake',
        '--goal', 'Compile this example clause source into a validated PI to PD to ECP to TQAEP chain.',
        '--source', $Source,
        '--constraint', 'candidate-only, no release',
        '--non-goal', 'no upstream document bodies copied'
    ) (Join-Path $Art 'intent.card.json')
}
Step 'compile-pi' { Invoke-Cli @('--root', $Art, 'compile-pi', '--intent', (Join-Path $Art 'intent.card.json'), '--profile', 'LITE') (Join-Path $Art 'pi.json') }
Step 'bind-pd' { Invoke-Cli @('--root', $Art, 'bind-pd', '--pi', (Join-Path $Art 'pi.json'), '--repo-root', $Ctx) (Join-Path $Art 'pd.json') }
Step 'compile-ecp' { Invoke-Cli @('--root', $Art, 'compile-ecp', '--pd', (Join-Path $Art 'pd.json'), '--pi', (Join-Path $Art 'pi.json')) (Join-Path $Art 'ecp.json') }
Step 'compile-tqaep' {
    Invoke-Cli @(
        '--root', $Art, 'compile-tqaep',
        '--pi', (Join-Path $Art 'pi.json'), '--ecp', (Join-Path $Art 'ecp.json'),
        '--maker', 'HERMES-MAKER', '--checker', 'GLM-5.3-FLASH-AO-LANE',
        '--checker-receipt', 'deleg_example/lane-C'
    ) (Join-Path $Art 'tqaep.json')
}
Step 'assemble (no CLI verb exists for this; the helper only re-serialises the four records)' {
    & $Py (Join-Path $Here 'assemble_bundle.py') `
        (Join-Path $Art 'pi.json') (Join-Path $Art 'pd.json') `
        (Join-Path $Art 'ecp.json') (Join-Path $Art 'tqaep.json') > (Join-Path $Art 'bundle.json')
}
Step 'validate' { Invoke-Cli @('--root', $Art, 'validate', '--bundle', (Join-Path $Art 'bundle.json')) }

Write-Host '--- negative: a source locator that does not exist must be refused, non-zero, with no artefact'
& $Cli @('--root', $Art, 'intake', '--goal', 'must be refused',
         '--source', (Join-Path $Root 'examples\first-run\missing.txt')) > (Join-Path $Art 'refusal.json')
$RefusalRc = $LASTEXITCODE
Write-Host "refusal exit code: $RefusalRc"
if ($RefusalRc -eq 0) { Fail 'a missing source locator exited 0' }
Get-Content (Join-Path $Art 'refusal.json')

Write-Host ''
Write-Host "FIRST_RUN_OK: every positive step exited 0 and the refusal exited $RefusalRc"
Write-Host "artefacts under: $Art"
exit 0
