HGK_LANE_NONCE_OK

# INDEPENDENT CHECKER BRIEF — FINAL PASS on the amended candidate (S4 R6 / FAR-R17)

## Lane contract

- Lane: `VERIFY_SECURITY`. You are VERIFY_ONLY.
- Work order reference: `WO-TS-CLOSEOUT-04`. You perform no publication, no push, no merge, no tag, no
  release and no repository write of any kind. The remote write authority in this round belongs to the
  orchestrator under the lane POOL/registry policy declared by the owner, not to this dispatch.

## Frozen subject (verify exactly this)

- repository: `C:/Projects/Agent_Workspace/PIPD-S4R6-wt` (a git worktree; branch
  `fix/s4r6-closeout-doc-identity-and-update-route-20261016`)
- commit: `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba`
- tree: `62eef9d8059d307ae373de63519a37551fa14854`
- branch base for the governed write set: `f4021aeff9c016cfb14f17e68a0c570ed4e825c5` (declared by the
  workflow itself as `STAGE_C_BASE_SHA`); product baseline for the diff is
  `d3bd5456afbff21a8c8837994a49f57be3e1b97e` (origin/main at round start)
- previously verified sibling commit: `5defc64f1177a1d6f32502c5479c65cf9a001858` (same two product files,
  already accepted by an earlier VERIFY_SECURITY dispatch; that commit now lives on the branch
  `r6-closeout-evidence-20261016`)

## Boundary discipline (mandatory)

- Do NOT write inside the repository path above. The root is guarded; any change voids this dispatch.
- Put your scratch, downloads and any probe files under `C:/Users/user/AppData/Local/Temp/hgk-r17-checker-final/`
  and keep `TEMP`/`TMP` pointed there for every child process. Set `PYTHONDONTWRITEBYTECODE=1` and pass
  `-p no:cacheprovider` to any unittest run so the guarded root stays byte-identical.
- Before and after your work, run `git -C <repo> status --porcelain` and report both outputs. Both must be
  empty. If a test you run insists on writing inside the repository, do NOT let it: report that test by
  name and exclude it from your acceptance evidence, exactly as you would exclude it from a verdict.
- Use the interpreter at `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe` (it has the
  project's test dependencies importable) for running tests and probes.

## What to verify (C1..C6), and what would falsify each

C1 — Identity and scope. Report `git rev-parse HEAD`, `HEAD^{tree}`, the branch name, and
`git diff --name-only d3bd5456afbff21a8c8837994a49f57be3e1b97e..HEAD`. Expected: exactly
`docs/install/README.md`, `docs/USER_GUIDE.md`, `tests/test_r6_doc_identity_guard.py`,
`.github/workflows/public-plugin-verify.yml`. Report `git diff --name-only HEAD^ HEAD` (expected: only the
workflow file) and `git diff --check` (expected: empty, exit 0).
Falsifier: any changed path outside that set, or any diff that is not what the commit message describes.

C2 — The gate amendment is MINIMAL, NAMED, and SELF-CONSISTENT. Read the `stage-c` arm of
`.github/workflows/public-plugin-verify.yml` and report, verbatim: the `ALLOWED` regex, the `DENIED`
regex, `REFUSED_PLANTS`, `ALLOWED_PLANTS`, and any comment block that names an amendment. Establish:
  (a) the alternation content added to `ALLOWED` is exactly one new path alternative,
      `docs/USER_GUIDE\.md$`, and nothing else — compare it to the `ALLOWED` of `stage-b`, which also
      carries that alternative, and state the difference you find;
  (b) the `stage-a` and `stage-b` arms are untouched by this commit;
  (c) the plant lists agree with the amended `ALLOWED`: every `REFUSED_PLANTS` entry must be refused by the
      amended regex and every `ALLOWED_PLANTS` entry must be accepted by it;
  (d) the round's own evidence directory (`S4_R6_CLOSEOUT_RETURN/**`) is still REFUSED by the arm — i.e.
      the amendment did not accidentally admit the round's receipts.
Falsifier: an addition that is a prefix rather than one path; a plant list that no longer agrees with the
regex; or the evidence directory becoming admissible. If any of those hold, say so plainly — a widened gate
that still passes is a more serious finding than a red check.

C3 — Re-derive the write-set verdict yourself. Do not trust the repository's own script or any helper in
the round's evidence directory. Extract the `ALLOWED`, `DENIED` and `EXCLUDED_PREFIXES` regexes and the
declared base OUT OF THE FILE, then classify `git diff --name-only <declared base>...HEAD` yourself and
report the verdict. Expected: no path outside the declared write set and no frozen-path violation.
Also classify the diff range `f4021ae...d3bd545` (origin/main) to show whether the arm describes main as
well as this branch, and report the number of changed paths in each case.
Falsifier: any path outside the set that the hosted job would print as `UPGRADE_WROTE_OUTSIDE_ALLOWED_SET`.

C4 — The previously verified content is unchanged. Run
`git diff --stat 5defc64f1177a1d6f32502c5479c65cf9a001858 127ec1ca97c71d0437f5b149a6e7d540d0cb3bba -- docs/install/README.md tests/test_r6_doc_identity_guard.py`
and report it. Expected: empty, i.e. the two product files are byte-identical to the ones an earlier
independent dispatch already accepted, so that acceptance transfers to this head by content.
Falsifier: any difference in those two paths.

C5 — Adversarial use of the amendment. Attempt to show that `docs/USER_GUIDE\.md$` inside `^( ... )`
can admit something it should not. Test at least: a nested path (`x/docs/USER_GUIDE.md`), the exact path,
a near-miss (`docs/USER_GUIDE.md.bak`, `docs/USER_GUIDEB.md`), and a case variant
(`docs/user_guide.md`). Report each as accepted or refused by the amended regex, and state whether the
anchoring is what prevents the misses. Report the method you used to evaluate the regex so a reader can
re-run it.
Falsifier: any near-miss or nested path being accepted.

C6 — Behaviour. Run, from the repository root and with the write guards above:
`python -m unittest tests.test_r6_doc_identity_guard -v` and
`python -m unittest tests.test_s4r2m_docs_route tests.test_r5r3_install_route_identity tests.test_s4ext_release_provenance tests.test_r6_doc_identity_guard`
and report the exact `Ran N tests` / `OK` / `FAILED` lines and exit codes. Do NOT attempt the whole
discovery suite: the previous dispatch established that its two errors come from tests that write inside
the guarded root, so under this boundary it cannot be certified green — that bound is known and is not
what this pass is for.
Falsifier: any failure in the two named commands.

## Answer format (required)

Emit, in this order: the lane/model you observe serving this turn; `subject_commit` / `subject_tree`;
`guard_root_status_before` / `guard_root_status_after`; then one block per claim `C1..C6` with
`PASS` / `PARTIAL` / `FAIL` and the raw evidence lines; then `adversarial_findings`; then
`command_receipts` (each raw command with its exit code); then `checker_id` and `verdict`
(`PASS`, `PARTIAL` or `FAIL`); then `claim_ceiling` stating in one sentence exactly what your verdict does
and does not establish. Distinguish NOT_RUN from PASS. Do not round a partial up.

The final line of your reply must be exactly `HGK_LANE_NONCE_OK`.
