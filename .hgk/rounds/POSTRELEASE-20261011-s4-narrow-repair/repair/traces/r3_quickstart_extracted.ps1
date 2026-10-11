$ErrorActionPreference = 'Stop'   # stop at the first failing step; no step fails silently
# 1. Fetch the same wheel and checksum list, from the immutable tag.
$Base = "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2"
Invoke-WebRequest -Uri "$Base/pipd_ls_sp-0.1.0-py3-none-any.whl" -OutFile "pipd_ls_sp-0.1.0-py3-none-any.whl"
Invoke-WebRequest -Uri "$Base/SHA256SUMS" -OutFile "SHA256SUMS"

# 2. Verify the wheel against its published digest. SHA256SUMS lists three assets but only the wheel
#    was fetched, so compare the wheel's own hash to the published literal.
$expected = "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
$actual = (Get-FileHash -Algorithm SHA256 -Path "pipd_ls_sp-0.1.0-py3-none-any.whl").Hash.ToLower()
if ($actual -ne $expected) { throw "wheel SHA-256 mismatch: $actual" }
"pipd_ls_sp-0.1.0-py3-none-any.whl: OK"   # expect this line

# 3. Install into a virtual environment.
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "python -m venv failed (exit $LASTEXITCODE)" }
.\.venv\Scripts\Activate.ps1
python -m pip install .\pipd_ls_sp-0.1.0-py3-none-any.whl
if ($LASTEXITCODE -ne 0) { throw "pip install failed (exit $LASTEXITCODE)" }

# 4. Check the install, then use it.
pipd doctor                        # expect: {"verdict": "PASS", ...}
if ($LASTEXITCODE -ne 0) { throw "pipd doctor failed (exit $LASTEXITCODE)" }
pipd --help                        # 13 commands
if ($LASTEXITCODE -ne 0) { throw "pipd --help failed (exit $LASTEXITCODE)" }
pipd --root .\myproject init       # --root is global and must precede the subcommand
if ($LASTEXITCODE -ne 0) { throw "pipd init failed (exit $LASTEXITCODE)" }
