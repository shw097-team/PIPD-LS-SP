# Independent Acceptance Challenge — Frozen Stage B

Date: 2026-10-12 (Asia/Taipei). The checker did not implement this candidate. No candidate repairs, commits, formatting changes, or release approvals were made. All checker-created files and temporary checkouts are confined to this report's ao directory.

## Subject

- Repository: shw097-team/PIPD-LS-SP.
- Requested remote branch: feat/s4post-triple-upgrade-20261012-r2.
- Measured HEAD: 2a903bd09c7760c494f20ed98b840fae789b24d6.
- Measured HEAD tree: ccb4d4407a27b0d53d13cc5c38f61f8a92fc7485.
- Actual local branch: feat/s4post-triple-upgrade-20261012 (not the requested remote branch name).
- Stacked base: 52542c395a0f91dc2ba4bd6123acd4cdecd780dc. No main-based write-set comparison was substituted.
- Original tree T: C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt.
- AO: T/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao.

Commands below use T and AO as these exact path abbreviations. Full invocations and raw outputs are retained in the adjacent transcript/log files. Get-Content/rg source inspections and temporary-copy setup are recorded in those transcripts as well.

Primary commands:

~~~text
git -C T rev-parse HEAD
git -C T rev-parse HEAD^{tree}
git -C T branch --show-current
git -C T status --porcelain
git -C T diff --name-status 52542c395a0f91dc2ba4bd6123acd4cdecd780dc 2a903bd09c7760c494f20ed98b840fae789b24d6
git -C T diff --name-only 52542c395a0f91dc2ba4bd6123acd4cdecd780dc 2a903bd09c7760c494f20ed98b840fae789b24d6
git -C T diff --exit-code 52542c395a0f91dc2ba4bd6123acd4cdecd780dc 2a903bd09c7760c494f20ed98b840fae789b24d6 -- skills/
git -C T rev-parse 52542c395a0f91dc2ba4bd6123acd4cdecd780dc:skills 2a903bd09c7760c494f20ed98b840fae789b24d6:skills
python -m unittest tests.test_public_plugin_packaging tests.test_web_fallback
python -m unittest discover -s tests -t .
python tools/freeze_public_plugin_source.py --repo-root T --out AO/frozen_check.json
python tools/build_public_plugin.py --source-root T --ledger AO/frozen_check.json --source-commit 2a903bd09c7760c494f20ed98b840fae789b24d6 --out-dir AO/build-output
python AO/probe_f05.py
git ls-remote origin refs/heads/feat/s4post-triple-upgrade-20261012-r2
git diff --exit-code
git diff --cached --exit-code
~~~

The focused unittest command ran in T. Full discovery ran ONLY in AO/candidate-copy, an independent --no-hardlinks clone checked out at the named commit; it did not run in T. The first clone checkout failed with a long filename; a command-local core.longpaths=true retry checked it out successfully. Both attempts and their outputs are preserved. A second clean clone, AO/owner-candidate, was used only for the supplementary owner-gate reproduction; core.longpaths=true was configured in that copy, never in T.

For Python execution, PYTHONDONTWRITEBYTECODE=1 and PYTHONUTF8=1 were set. TEMP, TMP and TMPDIR were redirected to AO/temp. This prevents normal test temporary files and bytecode from being written elsewhere. The full suite contains fixed ROOT/.hgk/artifacts writes, which is why it was not run against the original worktree. No tests were changed.

Initial status BEFORE any AO output existed:

~~~text
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO_20261012T105531Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO_BRIEF.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao_lane.sh
~~~

These three pre-existing untracked files were not removed or edited. Subsequent status additionally lists verify/ao/, the explicitly permitted checker output. Final tracked and staged diffs both exited 0 with no output; HEAD and tree remained unchanged. This is tracked-content integrity, NOT a clean-worktree assertion.

Remote readback exited 0:

~~~text
2a903bd09c7760c494f20ed98b840fae789b24d6 refs/heads/feat/s4post-triple-upgrade-20261012-r2
~~~

## What I reproduced

### A. Skill ledger and identity

Ledger directories = 8; ledger file keys = 48; actual directories = 8; actual files = 48. Directory and file path sets match. The initial PowerShell property-count display expanded to 48 individual ones; a separate count correctly measured 48 (C_preflight_raw.txt). The successful independent all-file canonical hash check measured 0 mismatches and 146511 canonical bytes. Its failed quoting attempt is also retained, not suppressed.

Eight names: pipd-assurance-tqaep, pipd-authority-source, pipd-execution-contract, pipd-package-project, pipd-pd-bind, pipd-pi-compile, pipd-profile-tailor, pipd-route-intake.

Three raw on-disk SHA256 recomputations, each matching its ledger value:

~~~text
skills/pipd-assurance-tqaep/SKILL.md
703d354c5b04caa96c3deded4cd57c3a6ba91603a6419479117e4b83d568f776
skills/pipd-authority-source/SKILL.md
89d04cf2e753e539f1d661beaa8e0df348f6ca8db9e423f516656106dcf68e91
skills/pipd-execution-contract/SKILL.md
903c0af6ce09929b3c9c9f23abe650989c0a952fa4372dbe9414d076e7648478
~~~

Exact hash command: Get-FileHash -LiteralPath <each path above> -Algorithm SHA256. Raw evidence: AB_checks_raw.txt. All-file supplemental check: A_ledger_all_retry_raw.txt. The checked-in ledger identifies earlier commit 32962532b7b7176eafbd3d353ced63a3056027fb and tree 40b9507a97eea29cdc20f55e69cedb34ee8e2302; it is a historical source ledger, not a declaration of the current Stage-B commit/tree. Its skill bytes were independently checked rather than assuming identity metadata matched.

### B. Stacked-base write set

The exact diff commands are listed under Subject; their entire 79-path name-status output is in AB_checks_raw.txt. Independently counted output:

~~~text
diff_exit=0
Changed=79; Outside=0
skills/ changed=0
src/ changed=0
schemas/ changed=0
dist/ changed=0
skills_diff_exit=0
9341a4915cdd3f30da757af9c8c37ffeac363487
9341a4915cdd3f30da757af9c8c37ffeac363487
~~~

Outside paths were counted against this anchored allowlist:

~~~text
^(packaging/|tools/|tests/|docs/install/|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012)
~~~

Zero outside paths and identical skills subtree IDs establish the committed write-set and byte-identity claims for this base/candidate pair. They do not establish the CI guard is equivalent.

### C. Independently observed test counts

| Run | Location | Exit | Total | Failures | Errors | Skips | Derived passing test cases |
|---|---|---:|---:|---:|---:|---:|---:|
| Focused requested modules | Original T | 0 | 44 | 0 | 0 | 0 | 44 |
| Full discovery, first incomplete copy | AO/candidate-copy | 1 | NOT_COLLECTED | N/A | collection abort | N/A | N/A |
| Full discovery, successfully checked-out copy | AO/candidate-copy | 1 | 569 | 4 | 3 | 6 | 556 |
| Full discovery against original T | NOT_EXECUTED | N/A | N/A | N/A | N/A | N/A | N/A |

Observed totals DO NOT differ from 44 and 569 for the completed runs. The full run is NOT an all-pass reproduction; 556 = 569 - 4 - 3 - 6 is an arithmetic derivation, not a maker-provided number. Copy location and Windows path/Git-ancestor effects constrain interpretation.

Focused raw stderr:

~~~text
............................................
----------------------------------------------------------------------
Ran 44 tests in 1.804s

OK
~~~

Full-copy raw conclusion:

~~~text
Ran 569 tests in 104.122s

FAILED (failures=4, errors=3, skipped=6)
~~~

Raw stdout/stderr and exits: C_focused_*.txt, C_full_copy_*.txt, C_full_copy_retry_*.txt; setup transcripts: C_full_preflight_raw.txt and C_full_retry_preflight_raw.txt. No failure logs were replaced by successful retries.

### E. Supplementary owner-gate reproduction

Original-tree reproduction is separately reported as failed below. A clean isolated committed copy, after setting its LOCAL core.longpaths=true, froze with exit 0. Using that freshly produced ledger against that copy and a separate AO/copy-build-output directory exited 2:

~~~text
REFUSED OWNER_INPUT_MISSING: no owner derivation record for skill 'pipd-assurance-tqaep' (derivations.json is empty by design; every skill needs an owner-approved record whose source_sha256 matches the frozen ledger)
~~~

stderr was empty, stdout carried the refusal, and the target directory contained 0 entries. Commands and raw outputs: E_isolated_owner_retry_raw.txt, E_copy_freeze_retry_stdout.txt, E_copy_build_retry_stdout.txt, E_copy_build_retry_stderr.txt. This is a clean-copy owner refusal, NOT successful execution of the requested original-tree freeze. The preceding copy attempt also failed because Git without its longpaths configuration reported four long-path deletions; its raw failure is retained in E_copy_freeze_stdout.txt.

## What I could NOT reproduce

### Clean original worktree / original owner-gate chain

Initial git status already disproved the clean-worktree precondition. The exact original freeze command in Subject exited 2:

~~~text
REFUSED DIRTY_WORKTREE: worktree is not clean:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO_20261012T105531Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO_BRIEF.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao_lane.sh
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao/
~~~

It did not create frozen_check.json. The requested subsequent build exited 2 with empty stderr and the following stdout:

~~~text
REFUSED LEDGER_UNREADABLE: [Errno 2] No such file or directory: 'C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\ao\frozen_check.json'
~~~

AO/build-output remained empty (0 entries). This proves no archive for this attempted chain, but DOES NOT prove owner-gate execution there. The output-directory placement inside T would also trigger OUTPUT_ROOT_OVERLAPS_REPO if a valid ledger were supplied; the observed failure was earlier LEDGER_UNREADABLE. I did not bypass either original-tree gate. Raw: E_refusal_raw.txt and E_freeze_*/E_build_*.txt.

### Original-tree full unittest command

NOT_EXECUTED in T: tests/test_tqaep_design_positive.py:50 creates ROOT/.hgk/artifacts/tqaep_design_tmp; lines 59–60 write pi.json and ecp.json, and line 131 writes empty_pi. Restoring bytes afterward would still violate the prohibition on transient candidate writes. Source inspection is in C_preflight_raw.txt/C_full_preflight_raw.txt. The command was instead attempted in a committed clone under AO. Initial checkout failure (exit 128) was:

~~~text
fatal: cannot create directory at '.hgk/rounds/R11-20261011-s4-credential-closure-and-fda-integration/openspec/changes/pipd-ls-sp-r11-credential-closure': Filename too long
~~~

The subsequent discovery on that incomplete checkout aborted before collecting tests:

~~~text
ImportError: Start directory is not importable: 'tests'
~~~

After successful longpaths checkout, the 569-test run still failed. Exact failing cases:

- tests.test_atomic_requirements.RepoContextBinding.test_non_git_root_degrades_and_discloses: AssertionError: 'git' != 'filesystem'.
- tests.test_atomic_requirements.RepoContextBinding.test_stale_context_is_refused: equal currentness_epoch fingerprints.
- tests.test_atomic_requirements.RepoContextBinding.test_tracked_files_exclude_vcs_internals: AssertionError: 0 != 2.
- tests.test_s4ext_artifact_reproducibility.ArtifactReproducibility.test_t2_scanner_stays_out_of_the_tree: AssertionError: False is not true : the scan artefact was not written to --out.
- tests.test_tooling_executes.TestToolingExecutes.test_cli_smoke_runs: shutil.Error during nested copytree, including Windows missing/long-path errors.
- tests.test_tooling_executes.TestToolingExecutes.test_export_manifest_has_no_vcs_paths: FileNotFoundError [WinError 3] on a long evidence path.
- tests.test_tooling_executes.TestToolingExecutes.test_tracked_file_metric_excludes_vcs_internals: shutil.Error during nested copytree, including WinError 206.

These are measured local-copy failures. The forced deep AO directory, temporary directories nested inside a Git checkout, and Windows long-path handling are confounders; I do not label these seven cases newly introduced Stage-B regressions. The raw tracebacks are unabridged in C_full_copy_retry_stderr.txt.

### G. External and human gates

- Vendor's own manifest validator: NOT_EXECUTED — only the repository's local validator and synthetic tests were run; no vendor validator was invoked.
- OpenAI Portal scan/review: NOT_EXECUTED — no Portal submission, scan receipt, or review was performed.
- Real Host effective-load beyond this machine: NOT_EXECUTED — no external host was installed or exercised.
- codex-desktop GUI: NOT_EXECUTED — no GUI load/install/use acceptance flow was operated.
- Claude Code: NOT_EXECUTED — no Claude Code runtime or integration was launched.
- Windows account UAT: NOT_EXECUTED — unattended unit tests under this process are not a user/account UAT.
- GitHub Actions workflow execution: NOT_EXECUTED — the workflow was inspected locally; a remote run was not started or certified.
- Real filesystem symlink-overwrite attempt: NOT_EXECUTED — os.symlink failed with OSError(22, '用戶端沒有這項特殊權限。'); a real hardlink attack WAS executed instead.

## Findings

### AO-01 — HIGH — An output hardlink permits sentinel overwrite despite F05 closure language

Claim: the coverage matrix calls F05 'symlink overwrote a sentinel' REPAIRED and identifies 'check_output_root + O_EXCL test_05, test_21-path case'.

Exact falsifying command, with TEMP/TMP/TMPDIR=AO/temp and PYTHONDONTWRITEBYTECODE=1:

~~~text
python AO/probe_f05.py
~~~

The harness imports the candidate's existing complete-owner fixture and invokes its REAL Env.build -> build_plugin. No candidate code is patched. It precreates the checksum output as a real hardlink to a sentinel outside the output directory; all attack files remain inside AO/temp. Raw output:

~~~text
symlink: NOT_EXECUTED link creation failed: OSError(22, '用戶端沒有這項特殊權限。')
hardlink: before=b'INDEPENDENT_AO_SENTINEL_DO_NOT_OVERWRITE\n'
hardlink: builder_verdict=BUILT
hardlink: after=b'e77501f25007ceb96d3e107070ad6d223731a07b51c04fcfdfb1b2676df918a6  pipd-ls-sp-public-skills.zip\n'
hardlink: sentinel_untouched=False
probe_exit=0
~~~

Evidence: probe_f05.py and D_f05_probe_raw.txt. tools/build_public_plugin.py:800 writes sidecar bytes non-exclusively; lines 804–805 likewise write mapping/receipt paths. Root/ancestor symlink rejection does not protect pre-existing output members. The measured attack is a HARDLINK, not a successfully created symlink; it establishes an actual unauthorized overwrite in the complete-owner fixture, not that today's owner-missing release configuration can produce a real archive. The local attacker must be able to prepopulate the output directory/link. No TOCTOU exploitation, production attacker access, or vendor-host behavior was measured.

### AO-02 — MEDIUM — Delivered-tree clean precondition is false

Claim: the candidate must be clean. Exact falsifying command: git -C T status --porcelain, run before AO output creation. Raw initial status is under Subject and shows three pre-existing untracked stage-b files. The subsequent freeze refuses DIRTY_WORKTREE, not the owner gate. This is a delivery/environment finding, not a tracked-code mutation. The remote commit itself matches.

### AO-03 — MEDIUM — CI's write-set guard is narrower than the required upgrade allowlist

Claim under challenge: the workflow guard matches the stated upgrade set and protects dist as well as frozen paths. Exact inspection/falsification commands:

~~~text
Get-Content .github/workflows/public-plugin-verify.yml
foreach($path in @('dist/payload.zip','unrelated/changed.txt','docs/elsewhere.md','skills/pipd-route-intake/SKILL.md')) { Write-Output "path=$path rejected_by_workflow_guard=$($path -match '^(skills|src|schemas)/')" }
~~~

Raw evaluation (DF_detail_raw.txt):

~~~text
path=dist/payload.zip rejected_by_workflow_guard=False
path=unrelated/changed.txt rejected_by_workflow_guard=False
path=docs/elsewhere.md rejected_by_workflow_guard=False
path=skills/pipd-route-intake/SKILL.md rejected_by_workflow_guard=True
~~~

The guard only rejects ^(skills|src|schemas)/. It has no positive allowed-path check and no dist exclusion. It derives BASE from PR base or HEAD~1, not from the fixed stacked base. A workflow_dispatch run on this commit defaults to the immediately preceding commit, so it does not necessarily examine the entire stacked Stage-B write set. This is a guard-logic mismatch; I did NOT execute a mutated remote CI run. The independently measured committed diff nevertheless has zero violations.

### D. Historical test coverage assessment (F01–F05)

All methods below belong to PublicPluginPackagingTest in tests/test_public_plugin_packaging.py. Entire source is preserved in C_preflight_raw.txt; targeted excerpts in D_sources_raw.txt and DF_detail_raw.txt. Their executions are included in the 44 passing focused cases.

| Defect | Method(s) | What the test actually does | Scope assessment |
|---|---|---|---|
| F01 fake PNG accepted | test_01_png_signature_with_broken_body_is_refused; test_01_non_png_icon_is_refused | Replaces real fixture icon bytes, supplies matching malicious digest, invokes real builder, checks ICON_INVALID and motive (truncated_chunk/signature), checks no output. | Direct regression inputs, not vacuous. Does not establish every PNG validity rule or Portal scanning. |
| F02 arbitrary manifest accepted | test_02_unknown_manifest_property_is_refused; test_16_unknown_top_level_key_in_the_official_manifest_is_refused; test_16_the_previous_internal_manifest_is_refused_as_the_package_root | Inserts unknown keys / legacy root shape into packaging fixtures and checks exact real-builder schema refusal. | Direct local schema regression, not vacuous. Local validate_subset and byte-pinned schema are NOT execution of the vendor's own validator. |
| F03 invalid SKILL.md accepted | test_03_skill_without_frontmatter_is_refused; test_03_skill_with_wrong_frontmatter_name_is_refused; test_12_complete_owner_record_builds_and_projects_the_body_verbatim | Freezes the malformed source first (preventing a hash-drift proxy), invokes real builder, checks SKILL_FRONTMATTER_INVALID; positive case checks body and kept/dropped keys in a built zip. | Direct missing-frontmatter/name regressions with a real positive build. Not exhaustive vendor skill-format qualification. |
| F04 null source_commit accepted | test_04_source_commit_gates | Calls real builder with None, abc123 and a differing 40-hex value; checks SOURCE_COMMIT_NULL/INVALID/MISMATCH and no zip. | Direct regression at Python API boundary. Does not separately execute a subprocess CLI omitting --source-commit in this method. |
| F05 symlink overwrote sentinel | test_05_symlinked_output_root_is_refused_and_target_untouched | Makes the OUTPUT ROOT a symlink, or substitutes only _path_is_symlink if Windows disallows it; checks OUTPUT_ROOT_SYMLINK, sentinel bytes, and directory members. | Genuine root gate test, but on this machine it exercises a predicate seam, not real filesystem symlink resolution. A proxy for generalized overwrite safety; does not test output-member symlinks/hardlinks or concurrent swaps. AO-01 actually overwrites a sentinel through a hardlink. |

No listed test was found to be vacuous or to assert an unrelated refusal code. F05 is materially narrower than the closure language. Exact additional inspection: rg -n '^    def test_(05|21)' tests/test_public_plugin_packaging.py. The frozen module has test_05 but no test_21; the coverage matrix's test_21-path locator cannot be resolved there. mkstemp's exclusive temporary zip creation does not make the subsequent sidecar/receipt writes exclusive.

### F. CI workflow inspection

- Actual triggers: pull_request with path filters and workflow_dispatch; no push trigger.
- Permissions block: contents: read; checkout specifies persist-credentials: false. No explicit repository-push/tag/publish command or write-token permission was found.
- Literal pull_request_target DOES appear, in the comment on line 9; it is NOT a YAML trigger. Likewise secrets.* appears in that comment, not a secret-consuming expression. A literal 'nowhere in the file' claim would be false; absence of that active trigger is supported by inspection.
- No step explicitly needs a configured secret. This is a source inspection, not proof of every third-party action's implementation or all code executed by pip install/tests.
- Steps CAN and DO write to the runner's checkout: py_compile writes bytecode; pip's editable installation/test suite has writes; the mutation step rewrites a tracked dist/mount README then git checkout restores it; logs and fallback work files are created. Therefore 'no repository write' is defensible only as NO REMOTE GITHUB REPOSITORY MUTATION, not as a read-only local worktree promise.
- Path filters include docs/RELEASE_TUPLE.json and dist/mount/**, which are outside the user-specified upgrade set, while omitting broad tools/tests, docs/adr, OpenSpec and round-evidence paths. 'restricted to the upgrade paths' in the header is not an exact description of this task's allowlist.
- docs/install/README.md:165 calls it a 'read-only gate'; that wording needs the remote-versus-local distinction. The file/docs explicitly deny Portal/publication/host/S4 acceptance; those ceilings are appropriately stated, not independently granted here.
- Guard/base discrepancies and measured regex evidence are in AO-03. Entire workflow and documentation search output: F_workflow_raw.txt.

## Verdict

**FAIL_CHALLENGE**

Scope: the measured local challenge of commit 2a903bd09c7760c494f20ed98b840fae789b24d6 finds an actual complete-owner-fixture output hardlink overwrite and a CI guard mismatch; it also records a dirty delivered tree and a non-passing isolated 569-test run. It DOES NOT authorize release, merge, publish, or S4 full pass, and does not cover vendor/Portal/GUI/other-host/account UAT or an original-tree full-suite execution.

Passing subclaims remain passing: requested commit/remote readback, eight/48 ledger inventory and hashes, stacked-base zero-outside-path diff, unchanged skills subtree, 44 focused tests, and owner refusal/no archive in the clean isolated copy. A FAIL_CHALLENGE is not a claim that every candidate feature failed.

## Makers-vs-checker differences

- Maker totals 44 and 569: measured totals match; 44 is green, while the isolated 569 run exits 1 with 4 failures, 3 errors and 6 skips. Original-tree full-suite execution remains NOT_EXECUTED under the hard write prohibition; local-copy environmental effects prevent a clean regression attribution.
- Clean subject assumption: false before checker outputs existed; three untracked stage-b files were already present.
- Requested local branch identity: local branch lacks -r2; remote -r2 and local HEAD nevertheless resolve to the specified commit.
- Real owner refusal: not reached in the requested original freeze/build chain (dirty tree, then missing ledger). Reproduced only in a separate clean committed copy after copy-local longpath configuration. Refusal text is stdout, not stderr.
- F05 'REPAIRED' coverage: root symlink refusal passes, but generalized sentinel safety does not; real hardlink overwrite measured. Matrix's test_21-path locator is absent from the packaging test module.
- CI 'read-only'/'upgrade paths' wording: no explicit remote write step, but runner checkout writes and the guard/filter set is not the required allowlist. Remote CI execution NOT_EXECUTED.
- All external/human qualification gates remain NOT_EXECUTED. This report grants none of them.

Raw evidence index: A_identity_raw.txt; AB_checks_raw.txt; C_preflight_raw.txt; A_ledger_all_retry_raw.txt; C_focused_stdout.txt/C_focused_stderr.txt/C_focused_exit.txt; C_full_preflight_raw.txt; C_full_copy_stdout.txt/C_full_copy_stderr.txt/C_full_copy_exit.txt; C_full_retry_preflight_raw.txt; C_full_copy_retry_stdout.txt/C_full_copy_retry_stderr.txt/C_full_copy_retry_exit.txt; D_sources_raw.txt; DF_detail_raw.txt; D_f05_probe_raw.txt; E_refusal_raw.txt and E_freeze_*/E_build_*; E_isolated_owner_raw.txt and E_copy_*; E_isolated_owner_retry_raw.txt and E_copy_*_retry_*; F_workflow_raw.txt; final_integrity_raw.txt. These retain failed attempts as well as successful checks. Temporary clones and attack harness live below AO and are not candidate fixes.
