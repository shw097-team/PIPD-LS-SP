# Independent Acceptance Officer report

Verdict: **FAIL_CHALLENGE**

## Frozen subject

- Commit: `5094939606ba9331ed768743eb5b806ad159e639`
- Tree: `b480182ca3c9c45fffb6d0d04cd81580d5b67c72`
- Wheel SHA-256: `e49d38e519117d67de57153658779eafa139eb0dda5a6d15f486facb44fd00e2`
- Effective counts: PASS 46, FAIL 2, NOT_RUN 4

## Decisive findings

- **FAIL D1 — historical S2 evidence was rewritten/omitted.** `python -B tools/perf_budget.py --check` exited 0 and reported `voting_metrics=["bytes_per_atom"]`, but it did not emit the required original `context_bytes_per_artefact 343547 > 20000` record. It emitted a newly measured `366299 > 20000` advisory FAIL instead. The brief explicitly prohibited replacing the historical literal.
- **FAIL E1 — ancestry is not provable from the publication.** `git merge-base --is-ancestor cd8a06e4... 50949396...` exited 128 with `fatal: Not a valid object name cd8a06e4...`. HEAD and tree themselves matched the frozen tuple.
- Destination safety held for every runnable negative: typed `UNSAFE_DESTINATION`, nonzero exit, and identical full-fixture hashes. Symlink escape was `NOT_RUN` because `os.symlink` returned WinError 1314.
- Wheel identity/equivalence held: 225170 bytes, expected SHA-256, 38 members, 19 schema files, manifest hashes consistent, and packaged Python bytes equal `src/`. Clean offline extraction loaded all 19 schemas from site-packages in a non-repo cwd.
- The two mutated-wheel runtime checks are `NOT_RUN`, not FAIL: each hit the hard three-attempt ceiling because `venv` failed during `ensurepip`, so the prerequisite successful installation was never reached.
- Export held: archive, manifest and SHA256SUMS were independently recomputed; dry-run was byte-for-byte side-effect free; fake-secret export failed typed with zero products.
- Fresh UAT execution produced 25 PASS across source/install modes; source UAT-10 is `NOT_RUN` because lifecycle applies only to install mode. Install mode used the brief-authorized offline zip extraction fallback after ensurepip failure.

## Commands actually run

- `python -B ao_harness.py` (direct A/B/C/D/E adversarial harness)
- `<venv>/Scripts/python.exe -B -m zipfile -e <wheel> <venv>/Lib/site-packages` (4.0.1 fallback)
- `python -B run_uat_fallback.py` (fresh UAT-00..12, source + installed-wheel modes)
- `python -B tools/perf_budget.py --check`
- `git -c safe.directory=<repo> -C <repo> merge-base --is-ancestor cd8a06e4c066a40398a4012b7b39808ac11408a2b 5094939606ba9331ed768743eb5b806ad159e639`

Exact argv, exit codes, stdout/stderr, snapshots, and per-case expectations are in `AO_LOG.ndjson`; full UAT subprocess records are in `uat/RAW_RUNS.jsonl`.

## NOT_RUN

- `A10`
- `B4`
- `B5`
- `UAT-10-source`
