ROLE: independent checker. Your sandbox denies local file reads and process execution, so
everything needed is inline. Judge only the inline blocks; if a block needed for a sub-claim is absent,
answer INCONCLUSIVE and name it.

SINGLE SUB-CLAIM UNDER TEST: C3e - "each write-set refusal receipt comes from the same revision the
allowlist diff compares".

Why you are being asked again: in two earlier valid turns you answered INCONCLUSIVE for C3e, on the
grounds that (i) the receipts' HEAD was not printed, and (ii) the diff compares Stage B at one revision
while the receipts come from a later head. Blocks 2 and 3 were produced to close exactly those two
objections, and they MEASURE the question instead of asserting it.

=== BLOCK 1: C3_ALLOWLIST_BASELINE_DIFF.txt (full) - the diff, its two compared revisions, and the
+2/-0 entry-level result ===
# Baseline diff of the write-set gate's ALLOWED/DENIED sets (frozen R3 subject vs current heads)

How this was produced, mechanically and repeatably, with no manual editing:

    git -C <stage A worktree> show e71fee6dd3aa73724baec4e8d9cc72127fbe36ed:.github/workflows/public-plugin-verify.yml   # frozen base
    git -C <stage A worktree> show HEAD:.github/workflows/public-plugin-verify.yml        # current Stage A head
    git -C <stage B worktree> show ba27309b50d8623ed9d3ad9b33fe7a4ffb8a9ede:.github/workflows/public-plugin-verify.yml     # current Stage B head
    # every ALLOWED='...' / DENIED='...' assignment parsed, entries split on '|', then set-diffed

A FIRST ATTEMPT AT THIS ARTEFACT WAS WRONG AND WAS DISCARDED. Its extractor terminated on the wrong
token and captured 224 lines from the base against 348 from the head, which is not an allowlist; a
"diff" built from it would have been meaningless. The extraction above parses the assignments
themselves, so the counts below are entry counts, not line counts.

## What the frozen base carried

ONE allowlist and ONE denial set (the single-stage era, before the STAGE switch existed):

  ALLOWED (12 entries): ['README\\.md$', '\\.github/workflows/public-plugin-verify\\.yml$', '\\.hgk/rounds/S4POST-20261012', 'docs/adr/', 'docs/install/', 'openspec/changes/s4post-triple-upgrade/', 'packaging/public-plugin/', 'tests/test_public_plugin_packaging\\.py$', 'tests/test_web_fallback\\.py$', 'tools/build_public_plugin\\.py$', 'tools/build_web_fallback\\.py$', 'tools/freeze_public_plugin_source\\.py$']
  DENIED           : ['dist/', 'schemas/', 'skills/', 'src/']

Note `src/` is in the frozen base's DENIED set.

## What the current Stage A head carries

TWO allowlists and TWO denial sets, selected by `STAGE` (the current Stage A head declares
`STAGE: stage-a`; the Stage B head declares `STAGE: stage-b`).

  stage-a ALLOWED (13 entries): ['MANIFEST\\.in$', '\\.github/workflows/ci', '\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'examples/first-run/run\\.sh', 'ps1$', 'public-plugin-verify\\.yml$', 'pyproject\\.toml$', 'setup\\.py$', 'src/pipd_ls_sp/workspace\\.py$', 'tests/test_standard_wheel_schemas\\.py$', 'tests/test_web_fallback\\.py$', 'tools/cli_smoke\\.py$', 'tools/verify_installed_wheel_registry\\.py$']
  stage-a DENIED           : ['dist/', 'schemas/', 'skills/']

  stage-b ALLOWED (14 entries): ['README\\.md$', '\\.github/workflows/public-plugin-verify\\.yml$', '\\.hgk/rounds/S4POST-20261012', '\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'docs/USER_GUIDE\\.md$', 'docs/adr/', 'docs/install/', 'openspec/changes/s4post-triple-upgrade/', 'packaging/public-plugin/', 'tests/test_public_plugin_packaging\\.py$', 'tests/test_web_fallback\\.py$', 'tools/build_public_plugin\\.py$', 'tools/build_web_fallback\\.py$', 'tools/freeze_public_plugin_source\\.py$']
  stage-b DENIED           : ['dist/', 'schemas/', 'skills/', 'src/']

## The deltas, stated exactly

stage-b vs the frozen base:
  + 2 added: ['\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/', 'docs/USER_GUIDE\\.md$']
  - 0 removed: []

stage-a vs the frozen base (a stage that did not exist in the frozen era, so every entry is new):
  entries not present in the base allowlist: 12
  base entries not present here            : 11

## What this means, without rounding

1. **The claim "the allowlists were NOT widened" is FALSE as written.** The stage-b allowlist gained
   exactly two entries against the frozen base. This contradicts the inline comment in the workflow
   itself ("This change widens NEITHER allowlist") and it contradicts the C3 claim this round put to
   the verification lane in attempts 7-13.
2. **The stage-b frozen-path denial is UNCHANGED**: skills/, src/, schemas/, dist/ all remain denied,
   and it is the denial - not the allowlist - that carries the frozen-path guarantee for stage-b.
3. **stage-a is a new stage whose DENIED set omits `src/`.** For that stage, `src/` files outside the
   single allowed path are still refused, but by the ALLOWLIST rather than by a category denial. That
   is a real change in mechanism for that stage, and it is exactly what repairing the pipeline
   required - it is not presented here as unremarkable.
4. **The more consequential of the two additions is the round directory itself**:
   `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` is inside the governed write set
   of the stage-b gate. The gate therefore permits writes to the directory that holds this round's
   own receipts. Its likely reason is ordinary (the round commits evidence and the gate would
   otherwise fail on it), but its effect is self-referential and it is recorded as such rather than
   justified away.
5. `docs/USER_GUIDE.md` is a doc addition consistent with stage B's distribution surface
   (`docs/install/` and `docs/adr/` were already allowed); it is still a widening.

## Ceiling

This is a mechanical set-diff of two committed revisions. It says what changed in the governed write
set; it does not say whether each change was necessary, and it is not an acceptance.


=== BLOCK 2: HEAD_PROVENANCE_RECEIPT.txt (full) - each local worktree's HEAD captured before and after
its gate run, the gate re-run clean naming the declared base, and each hosted run id mapped to the head
SHA it ran ===
HEAD PROVENANCE RECEIPT - which revision each write-set gate run and each hosted CI run belongs to
generated_utc: 2026-10-13T11:56:35Z

=== local worktrees, HEAD resolved AT THE TIME OF THIS RUN ===
  s4r3a-wt
    path      : C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3a-wt
    branch    : fix/s4r3-stage-a-ci-truthfulness-20261013
    HEAD      : 5310896e706e01a9cdb0123285bccec75086bcb8
    clean     : 0 modified/untracked entries
  s4r3c-wt
    path      : C:/Projects/Agent_Workspace/PIPD/worktrees/s4r3c-wt
    branch    : feat/s4r3-stageb-successor-20261013
    HEAD      : ee5aa3e91ae7a6398493e6e1c76448edee2d59da
    clean     : 37 modified/untracked entries

=== local write-set gate, re-run now, with the HEAD captured in the same invocation ===
  --- s4r3a-wt ---
    HEAD before run: 5310896e706e01a9cdb0123285bccec75086bcb8
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: planted stage-b artefacts are all allowed
WRITE_SET_CLEAN_AGAINST_5310896e706e01a9cdb0123285bccec75086bcb8

2/2 gate runs clean
    gate exit: 0
    HEAD after run : 5310896e706e01a9cdb0123285bccec75086bcb8
  --- s4r3c-wt ---
    HEAD before run: ee5aa3e91ae7a6398493e6e1c76448edee2d59da
GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
GATE_SELF_TEST_OK: planted stage-b artefacts are all allowed
WRITE_SET_CLEAN_AGAINST_5310896e706e01a9cdb0123285bccec75086bcb8

2/2 gate runs clean
    gate exit: 0
    HEAD after run : ee5aa3e91ae7a6398493e6e1c76448edee2d59da

=== hosted CI runs that produced the receipts quoted in this round (run id -> head sha) ===
  ee5aa3e    "sha": "ee5aa3e91ae7a6398493e6e1c76448edee2d59da",
  ee5aa3e      success    verify
  ee5aa3e      success    offline-gate
  ee5aa3e      success    offline-gate
  4bb23e7    "sha": "4bb23e748c0f0ad1f524ce7defbe98d492e58350",
  4bb23e7      success    verify
  4bb23e7      success    offline-gate
  4bb23e7      success    offline-gate
  aeb3c68    "sha": "aeb3c6851c03987d7bba7c139b021f0e6eabb366",
  aeb3c68      success    verify
  aeb3c68      success    offline-gate
  aeb3c68      success    offline-gate
  9d3845a    "sha": "9d3845a9b9e602c33bae74279b1f602bb723a9b0",
  9d3845a      success    offline-gate
  9d3845a      success    verify
  9d3845a      success    offline-gate


=== BLOCK 3: C3_REVISION_BINDING_RECEIPT.txt (full) - the blob identity of the workflow at both
revisions, an empty path diff across the range, the full change list in that range, and the allowlist
sets re-extracted at the current head ===
C3 REVISION BINDING RECEIPT - ties the allowlist diff to the same revision as the refusal receipts
generated_utc: 2026-10-13T12:01:47Z

The a12/a13 checker noted the diff compares Stage B at ba27309 while the receipts come from a later
head. This receipt measures whether that mismatch can change the result, rather than asserting it.

=== blob identity of .github/workflows/public-plugin-verify.yml across the revisions ===
  e71fee6    blob=7f64a4fddb0f263cb7cedc5f4923d3c31b4ceeb3
  ba27309    blob=30a7b1a917fb0851fa48ee1b0ba1e6e4cb3ab474
  9d3845a    blob=30a7b1a917fb0851fa48ee1b0ba1e6e4cb3ab474
  ee5aa3e    blob=30a7b1a917fb0851fa48ee1b0ba1e6e4cb3ab474

  frozen subject e71fee6 is the baseline; the others are Stage B revisions

=== has .github/workflows/public-plugin-verify.yml changed since the diff was cut? ===
  git diff --stat ba27309 ee5aa3e -- .github/workflows/public-plugin-verify.yml
    (empty output above means the file is byte-identical across those two commits)

=== all changes between the diff's revision and the current head ===
  git diff --name-only ba27309 ee5aa3e
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/HANDOVER_PACK_EXTERNAL_ACCEPTANCE.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A12_A13_A14.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C3_REFUSAL_RECEIPT_DISTILLED.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C4_REFUSAL_TESTS_RUN.log
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C4_STAGE_B_REFUSAL_TESTS_SOURCE.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/GUARD_COVERAGE_C1_C3.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/GUARD_RECEIPTS_C1_C3.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/GUARD_SELFTEST_RECEIPT.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/RECEIPT_PACK_C1_C2.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_STEP.yml
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/guards/REAL_RECEIPT.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/CITED_PATH_RESOLUTION.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/E8_DISPATCH_PARAM_ERROR.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/EXECUTE_STUDY_DRAFT.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/PLAN_LEG_DIVERGENCE.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/RETRIEVAL_CHANNEL_FINDING.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/ROUND_RESULT_FAR_DECISION_STUDY.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/VERIFICATION_LANE_CAPABILITY_BOUNDARY.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/bundle_manifest.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/guard_spec.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c1_colocated.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3_recut.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/draft_sha256.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/far_admission.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/invocation_EXECUTE_a2.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/packet_execute.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/prompt_capability.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/prompt_execute.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/prompt_verify.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/retrieval_ledger.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/stderr_EXECUTE_a2.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/stdout_EXECUTE_a2.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/CAPABILITY_PROBE_A6.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/VERDICT_VERIFY_A5.md
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/invocation_VERIFY_SECURITY_a3.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/invocation_VERIFY_SECURITY_a4.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/invocation_VERIFY_SECURITY_a5.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/invocation_VERIFY_SECURITY_a6.json
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stderr_VERIFY_SECURITY_a3.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stderr_VERIFY_SECURITY_a4.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stderr_VERIFY_SECURITY_a5.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stderr_VERIFY_SECURITY_a6.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stdout_VERIFY_SECURITY_a3.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stdout_VERIFY_SECURITY_a4.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stdout_VERIFY_SECURITY_a5.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/stdout_VERIFY_SECURITY_a6.txt
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/bundle_guards.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/far_admission.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/far_run_lane.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/make_receipt_pack.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/read_ci_for_sha.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/run_ao_lane_dryaudit2.py
    .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/scripts/run_ao_lane_split_audit.py

=== the allowlist sets re-extracted AT THE CURRENT HEAD, so the diff and the receipts share one revision ===
  --- e71fee6 ---
    78:          ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012)'
    79:          DENIED='^(skills/|src/|schemas/|dist/)'
  --- ee5aa3e ---
    97:              ALLOWED='^(pyproject\.toml$|setup\.py$|MANIFEST\.in$|src/pipd_ls_sp/workspace\.py$|examples/first-run/run\.(sh|ps1)$|tests/test_web_fallback\.py$|tests/test_standard_wheel_schemas\.py$|tools/cli_smoke\.py$|tools/verify_installed_wheel_registry\.py$|\.github/workflows/(ci|public-plugin-verify)\.yml$|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/)'
    98:              DENIED='^(skills/|schemas/|dist/)'
    118:              ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/USER_GUIDE\.md$|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/)'
    119:              DENIED='^(skills/|src/|schemas/|dist/)'


Adjudicate C3e on these three blocks alone:
  C3e-1  does the diff's Stage B revision and the receipts' head carry identical workflow content
  C3e-2  is any product file changed between them, or only round evidence
  C3e-3  do the sets re-extracted at the current head reproduce the +2 additions and the stage-b DENIED set
  C3e    your verdict, and exactly what remains missing if it is not CONFIRMED

FINAL LINE (required, verbatim, nothing after it): output exactly this token on its own line:
HGK_LANE_NONCE_OK
