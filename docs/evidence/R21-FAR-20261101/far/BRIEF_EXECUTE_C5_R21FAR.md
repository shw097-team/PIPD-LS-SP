NONCE: EXECUTE-R21FAR-1793529500

Emit that exact nonce on the first line of your answer.

You are the EXECUTE lane. Do exactly one bounded job, then report.

## Job

Run this command from `C:/Projects/Agent_Workspace` and capture its real output:

```
python var/FHS-R21-FAR-TT-20261101/tools/s5_c5_cases.py
```

Then compute and report the sha256 of `var/FHS-R21-FAR-TT-20261101/s5/C5_CASES.json`.

## Rules

- Do not edit any file. Do not read any file larger than 50 KB. Do not walk `知識庫`.
- Do not change `PIPD/tools/hotswap.py` — the script only uses copies under `var/`.
- If the command exits non-zero, report the exit code and the last 20 lines of stderr, and stop.

## Report format

```
NONCE: <nonce>
exit_code: <n>
summary: <the JSON summary object printed by the script>
c5_json_sha256: <hex>
```

Nothing else.
