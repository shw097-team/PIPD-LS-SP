# Tasks

> Status legend: `[x]` = done and re-verified on the frozen candidate by the orchestrator, not merely
> claimed by the writer lane. `[~]` = done as far as the local candidate allows, with the residue named.
> `[ ]` = not done.
>
> The product delta this change describes is **uncommitted** (see `CANDIDATE_TUPLE.json` in the round
> directory): `added 4 / changed 13 / removed 0` on the product paths.

## WO-S4-DEST-001 — safe output destination (`F-R4-S4-01` / `S4-USER-SEC-001`, P0)
- [x] 1.1 `projection.resolve_output_destination(root, out, *, authorized_roots=None, allow_replace=None)` — normalise, then refuse: empty/whitespace, MSYS/POSIX `/c/…`, cwd, home, drive root, source root, source ancestors, source descendants at/above cwd, symlink/junction escape, foreign absolute dirs, preexisting non-empty without `allow_replace`
- [x] 1.2 `UnsafeDestination(ProjectionError)` with `code = "UNSAFE_DESTINATION"`; added to the `project`/`export` failure-code strings in `cli.py`
- [x] 1.3 Staged publish: sibling stage dir → existing strict gates → `os.replace` → kept `.pipd-backup-<token>`; restore on failure; **never** `rmtree` a caller path
- [x] 1.4 Generated-surface marker `.pipd-generated-surface.json`, excluded from the Web/Host/IR denominators
- [x] 1.5 CLI: `project --allow-root` (repeatable) / `--allow-replace`; `PIPD_PROJECT_ALLOWED_ROOTS` + built-in `<root>/dist`; `--out` never silently ignored; `--dry-run` runs the same resolver, reports `destination_safety`, writes nothing
- [x] 1.6 `tests/test_project_destination_safety.py`: every negative typed-refused with exit ≠ 0 and an unchanged before/after canary; positive control writes 5 Web + 3 Host + IR; replay of a second run refuses (non-empty) and `--allow-replace` publishes with a reported backup. Orchestrator-side re-verification: `--out .` → `UNSAFE_DESTINATION` exit 2; second run refused; `--allow-replace` → `replaced=true` + `rollback_pointer`.

## WO-S4-DIST-002 — current wheel + install-safe resources (`F-R4-S4-02` / `S4-USER-DIST-002`, P0)
- [x] 2.1 `registry` resource resolver: `$PIPD_SCHEMAS_DIR` → packaged `importlib.resources` copy → source-tree fallback; typed `ValidationFail` naming every location tried
- [x] 2.2 `tools/build_dist.py`: wheel carries all current modules **and** the 19 schemas + `registry.json` under `pipd_ls_sp/schemas/`; refuses a tree missing any required member; deterministic (byte-identical rebuild — verified: two consecutive builds produced sha256 `e49d38e519117d67de57153658779eafa139eb0dda5a6d15f486facb44fd00e2`)
- [x] 2.3 `WHEEL_MANIFEST.json`: frozen candidate identity, `product_digest`, `member_count` (38)
- [x] 2.4 `pyproject.toml`: package + package-data declaration for `pipd_ls_sp/schemas/*.json`
- [x] 2.5 `tools/portable_install_check.py`: fresh venv, outside-repo cwd, unset `PYTHONPATH`/`PYTHONHOME`, import resolves to site-packages, registry 19/19, mutation negative fails typed — **14/14 PASS**
- [x] 2.6 `tests/test_wheel_distribution.py`: required members present, member SHAs recomputed from the zip equal the source SHAs, 19-family load from the packaged copy, determinism, explicit skip-reason where a real venv is unavailable

## WO-S4-EXPORT-003 — real `export --out` (`F-R4-S4-03` / `S4-USER-EXPORT-003`, P1)
- [x] 3.1 `export` uses the shared resolver; non-dry-run writes archive + manifest + checksums to `--out`
- [x] 3.2 Deterministic member ordering and per-member `rel`/`size`/`sha256`; archive unpack + SHA recompute verified independently (71/71 members matched, archive sha re-derived)
- [x] 3.3 Secret/PII and path-traversal exclusion before publication; staged write; `--dry-run` zero writes; explicit read-only stdout mode
- [x] 3.4 Regression: 13-command CLI surface (`tools/cli_surface_check.py` → 13/13 + 6/6 extras PASS) and the `project` web/host checks stay green
- [~] 3.5 The writer lane for this work order stalled mid-run (provider 429 then a frozen log); it was stopped and the work product independently re-verified on the host, with a 2-line orchestrator fix for the read-only branch that the lane had left red. See `WO3_LANE_INCIDENT.json`.

## WO-S4-UAT-004 — S4 end-user acceptance (`F-R4-S4-04`, P1)
- [x] 4.1 Disposable clean-room harness; UAT-00…12 recorded with environment, frozen subject, argv, stdout/stderr/exit, side-effect snapshots, hashes, checker identity
- [x] 4.2 Three profiles (LITE/STANDARD/ASSURED) per applicable case; no skipped case; no foreign tuple
- [x] 4.3 Two fresh-process replays with equal canonical output hash
- [x] 4.4 Source-import and installed-wheel columns reported separately and not substituted for each other
- [ ] 4.5 The independent non-Maker checker receipt is still outstanding: the checker lane was stopped on the 429 threshold breach and is being retried.

## WO-S2-PERF-005 — performance gate (`F-R4-S2-05`, P1, owner-gated)
- [x] 5.1 Keep the standing `343547 > 20000` FAIL visible; do not adjust the threshold — re-measured this round, still FAIL, `source_of_truth` still `UNPROVENANCED`
- [~] 5.2 Record the four threshold provenance requests against their owner; typed FAIL if unratified — recorded, **not ratified**, so the gate stays FAIL
- [x] 5.3 Preserve semantics (clause/req/trace fidelity) on the small and large corpora

## WO-R4-PUBLISH-006 — publication tuple (`F-R4-PUB-06`, P1)
- [x] 6.1 R5 candidate projection manifest: commit/tree/product digest/wheel digest/local-vs-public readable sets/exclusion reasons (`.hgk/rounds/R5-20261009-s4-user-operability/CANDIDATE_TUPLE.json`)
- [x] 6.2 Historical R3 seal kept as historical; no R5 attestation inherits it
- [x] 6.3 `publication_manifest --check --current` result recorded verbatim — **exit 1, `CURRENT_TREE_UNCOVERED`**: `EVIDENCE_GAP` stands. The local checkout has no remote and does not contain the externally reviewed commit `cd8a06e4c066a40398a4012b7b3908ac11408a2b`, so no publication-bound attestation for that subject is possible from here.

## WO-HGK-ORCH-007 — native path safety (`F-R4-HARNESS-07`, conditional P1)
- [x] 7.1 Route/CWD readback that decides whether S4 actually depends on the HGK/Hermes native command boundary (`.hgk/rounds/R5-20261009-s4-user-operability/route/gstack/route_readback.json`)
- [~] 7.2 S4's own lanes run in an egress-locked image with no git and no credentials, so the historical failure mode (a tokenized URL reaching an unintended `.git/config`) cannot occur there; the product CLI also refuses the MSYS form typed. The HGK/Hermes native command-boundary hardening itself remains an **S5 owner gate** and is not claimed here.

## Cross-cutting
- [x] 8.1 `F-R4-TRACE-08` / `F-R4-GOV-09` / `F-R4-RELEASE-10` dispositions recorded with the existing 42/11/4 baseline preserved
- [x] 8.2 KANBAN board + SWARM graph + GSTACK route readback + this OpenSpec change (`openspec change validate --strict` → valid)
- [x] 8.3 Single evidence master `PIPD-LS-SP_R5_S4_USER_USABILITY_REPAIR_EVIDENCE.md` with its own SHA-256
- [ ] 8.4 Independent non-Maker checker receipt on the same frozen candidate; claim ceiling stays `S4_REPAIR_CANDIDATE_LOCAL_TESTED`
