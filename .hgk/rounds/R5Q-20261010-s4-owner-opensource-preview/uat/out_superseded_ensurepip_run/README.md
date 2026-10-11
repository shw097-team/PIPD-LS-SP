# Superseded UAT run — kept deliberately, NOT evidence of the release

**Do not read this as a result of the published artifact.** It is retained so that a reviewer who
finds a failing matrix in the round's history can see exactly what it was and why it was discarded.

## What it is

The **first** execution of the UAT harness, launched in the background before the harness had the
venv-bootstrap handling described below. It produced `12 FAIL / 1 BLOCKED / 2 INFO / 14 PASS`.

## What actually failed — the host, not the product

Every install-mode failure traces to one root cause:

```
Error: Command '[... uat00_venv\venv\Scripts\python.exe, -m, ensurepip, --upgrade, --default-pip]'
       returned non-zero exit status 1
```

`python -m venv` bootstraps pip through `ensurepip`, and on this host that bootstrap fails in a
background-process context (it succeeds when the same command is run in the foreground — verified
directly). With no pip in the venv, the fallback `pip install --no-index --no-deps` also failed
(`UAT-ENV install path taken: offline_provisioned exit=1`), so nothing was installed and all 12
install-mode cases failed for the trivial reason that the CLI was not on the path.

The source-mode cases in the same run passed 14/14, which is the tell: the product was fine, the
venv was not.

## What replaced it

The harness now detects a pip-less venv, rebuilds it with `--without-pip`, and installs with
`uv pip install --python`, recording the installer path (`uv_pip_online_index`) in the receipt so an
offline or substituted installation can never be mistaken for a normal one.

Superseding runs, both green, are the real evidence:

| Run | Matrix | Wheel bytes |
|---|---|---|
| `uat/out/` | 27 PASS / 2 INFO / 0 FAIL (source + install) | `c450dbef…` (local build) |
| `uat/out2/` | 14 PASS / 1 INFO / 0 FAIL (install) | `c450dbef…` (**downloaded from the published release**) |

## Ordering (why this is not a clobber)

The superseded run finished at 23:21:45 and wrote to `uat/out/`. The corrected run then removed and
rewrote `uat/out/` at 23:30:14. The committed `uat/out/UAT_MATRIX.json` hashes to
`6e101c1cb56f4972b0154f49a80fd6bc506afa38f0b414c71fbd541451ac7fae` on disk and at HEAD — the covered
evidence was never overwritten by this run.

## Residual disclosure

This is an environment defect on the host, not a product finding, and it is **not** in the release's
Known Limitations beyond the general statement that the clean-install path used `uv` rather than
`pip` for the venv bootstrap (recorded in the UAT receipts and in the final report).
