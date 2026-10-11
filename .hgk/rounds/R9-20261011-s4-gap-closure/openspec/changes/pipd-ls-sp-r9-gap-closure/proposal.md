# pipd-ls-sp-r9-gap-closure

## Why

Round R8 closed the cross-model verification gap and consolidated `main`, but left a set of items open
that were waiting on **neither** the owner **nor** an external party. An audit split them into
(a) real gaps that were simply not worked, (b) decisions only the owner can take, and (c) things only
an external party can supply. Class (a) is the subject of this change.

## What changes

1. **Scan this project's own source.** The R7 dependency audit skipped `pipd-ls-sp` (it is not on
   PyPI), so "0 known vulnerabilities" never covered our own code. Run a source-level scanner and
   triage every finding. A HIGH was found and fixed **by construction**, and the fix is proven by
   behaviour on a crafted input, not merely by a quiet re-scan.
2. **Audit the SPEC/DEL active gaps individually.** `PARTIAL_CHALLENGE` at 28/10/19 is a count, and
   `EVIDENCED != PASS`. Each active row gets its own disposition, naming the artefact actually opened.
3. **Resolve DEL-018 on `main`.** The merged tree had one product path with no release-evidence
   disposition. The real cause turned out to be a **four-round-stale evidence seal**, not that path;
   re-sealing lets the existing gate answer truthfully instead of the gate being loosened.
4. **Re-run the cross-model check from a CLEAN committed tree**, so its strict clean-worktree gate
   reports on the release rather than on the auditor's own untracked directory.
5. **High-automation credential scheme**, so long unattended runs stop depending on a long-lived
   owner PAT.
6. **Close the round bookkeeping gap** by writing kanban / swarm / openspec artefacts to disk instead
   of asserting a board state that leaves no trace.

## Impact

- `tools/pi_dedup_check.py`, `tools/github_publish.py` — security repairs.
- `.hgk/artifacts/evidence_manifest.{json,seal.json}` and
  `.hgk/ao/pub/PUBLICATION_PROJECTION_MANIFEST.json` — release-evidence re-binding for the default
  branch.
- `README.md` — limitation 4 corrected from `FAIL(1/253)` to `PASS(253/253)`.
- **No tag moves. No release asset changes. No validator is edited. No product path is moved.**
