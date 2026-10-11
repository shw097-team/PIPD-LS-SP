set -e                             # stop at the first failing step; no step fails silently
# 1. Fetch the published wheel and the checksum list, from the immutable tag.
BASE=https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2
curl -fsSLO "$BASE/pipd_ls_sp-0.1.0-py3-none-any.whl"
curl -fsSLO "$BASE/SHA256SUMS"

# 2. Verify the bytes. Check exactly what step 1 downloaded: SHA256SUMS lists three assets, but
#    only the wheel is present here, so select its line. This is the ONLY integrity check offered:
#    there is no install-time or startup cryptographic readback, and no release signature.
#    Published wheel digest: d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f
grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -
#    expect: pipd_ls_sp-0.1.0-py3-none-any.whl: OK
#    Alternative, only after fetching EVERY asset SHA256SUMS lists, the whole file checks clean:
#      curl -fsSLO "$BASE/pipd-ls-sp-v0.1.0-preview.2-source.zip"
#      curl -fsSLO "$BASE/PREVIEW_NOTES_v0.1.0-preview.2.md"
#      sha256sum -c SHA256SUMS       # expect three ": OK" lines (wheel, source zip, notes)

# 3. Install into a virtual environment.
python -m venv .venv
. .venv/bin/activate 2>/dev/null || . .venv/Scripts/activate   # POSIX: .venv/bin/ ; Windows: .venv/Scripts/
python -m pip install ./pipd_ls_sp-0.1.0-py3-none-any.whl

# 4. Check the install, then use it.
pipd doctor                        # expect: {"verdict": "PASS", ...}
pipd --help                        # 13 commands

# 5. Start a project. Both of these lines were executed against the published wheel.
pipd --root ./myproject init      # -> exit 0; creates docs/ schemas/ src/ tests/ dist/
pipd doctor                       # -> {"verdict": "PASS", ...}, and it names the schema source it resolved
