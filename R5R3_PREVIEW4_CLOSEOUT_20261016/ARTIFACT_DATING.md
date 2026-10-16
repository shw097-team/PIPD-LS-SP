# ARTIFACT DATING — which readback belongs to which round/epoch

Written after an independent checker found that this round's packet contained **two control-plane readbacks
that disagree while both look "live"**. They disagree because they were taken at different registry epochs.
`raw/` holds artefacts from more than one round of this session, so a reader cannot date them from the file
name. This file supplies the missing dating; a dated subdirectory per measurement is the durable fix and is
filed as an owner-ready process item.

| artefact | taken (UTC) | registry epoch | subject | note |
|---|---|---|---|---|
| `raw/gstack_readback.json` | 2026-10-16T03:15:09Z | **19** | GSTACK named-method + drift readback of the previous round | carries 1 `DRIFT_VALUE` row (`/codex_sha256` expected `D13914CE…`, actual `e98c516f…`) and reports `sod_plan_vs_verify` OK |
| `raw/control_plane_probe.json` | 2026-10-16T05:28:12Z | **21** | this round's probe of the live gates | `check_drift` = 0 rows; `check_sod(PLAN, VERIFY_SECURITY)` = `SOD_VIOLATION` |
| `raw/zip_repro/ZIP_REPRO_R5R3.json` | 2026-10-16 (this round) | n/a | release-build reproduction | two builds at `cc6c193` |
| `raw/zip_repro_r5y/` | 2026-10-16 (this round) | n/a | rebuild at `062d84ae` | reproduces the previously accepted package |
| `CHECKER_VERDICT_WS_C.json` (round root, not `raw/`) | previous round | n/a | an earlier independent checker's verdict on the product branch | `REJECTED` — disclosed in `CLAIM_CORRECTIONS_R5R3.md` |

**Reading rule:** a lane-routing fact is mutable state. Quote every readback WITH its epoch, and never compare
two readbacks without checking the epochs first. Where the two above disagree, the epoch-21 measurement is the
current one; the epoch-19 row is evidence of the state the drift ticket was opened against, not of the state
now.
