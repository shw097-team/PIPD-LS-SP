# LANE SMOKE PROBE (read-only, no writes)

You are a read-only probe of the admitted EXECUTE lane. Do exactly this and nothing else:

1. Run: `ls /w/src/pipd_ls_sp/`
2. Run: `head -3 /w/src/pipd_ls_sp/cli.py`
3. Report the string `LANE_SMOKE_OK` plus the two outputs as plain text.

Do not create, modify or delete any file. Do not run any test suite.
