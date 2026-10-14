# 1 Scope and subject binding

Owner-mandated independent round 2, 2026-10-13, offline, no repair.

HEAD `5351c5fadca5cba14cd0600cead81a62753f0e1a`; tree `3a621e68463e89086d7dda79fa95722db22f686f`. HEAD is detached; local remote-tracking product ref binds this subject. `refs/remotes/origin/main` is `224591431a164ab72a9423cd180e417e8a762403` as required. There is no local `main` ref. Live remote main was not contacted. Previous subject `3233c817cc0a8fcd3f80f49219f219544235d25a` is also the frozen source-ledger commit; it is not this acceptance subject. I did not write or alter candidate bytes. Model/OAuth routing is supplied context, not independently attested.

# 2 Method and raw evidence

Read-only inspection, binary `git cat-file -p HEAD:<full path>` hashing, disk hashing, explicit LF-to-CRLF conversion, tracked-tree byte scan, literal Bash locator commands and literal workflow allowlist step, owner-supply recomputation, exact build, scratch-only icon generation and build, both unittest suites. No network calls, git history changes, commit, branch, push, tag, publish, or tracked edit.

The initial inspection before creating this directory returned empty ordinary status; the first captured pair after officer scaffolding returned `?? .ao-r3b/`. All officer writes are under `.ao-r3b/` except the expressly requested build output temp directory outside the repository. Test temp files and Python caches were redirected under `.ao-r3b/`; an offline Python audit guard rejects socket connection/address lookup/bind attempts. These environment changes are disclosed, not treated as the default suite side-effect test.

Raw evidence: `measurements.json`, `transcript.json`, `historical-spotchecks.json`, `supplement.json`, `publication-section3-verbatim.txt`, `workflow-guard-verbatim.sh`, and per-command `.log` files in this directory. Subprocess byte streams are retained, including CRLF. Initial shell inspection accidentally passed an unquoted PowerShell HEAD^{tree}; that command failed. Correctly quoted rerun obtained the tree above; it was an officer invocation error, not a candidate defect. Two officer patch-transport attempts failed before writing check.py; the successful helper files remain entirely under this directory.

# 3 What is verified

- Claim 1: Verbatim locator commands from root: negative exit 2 / FAIL_LOCATORS_NOT_RERUNNABLE; positive exit 0 / PASS_LOCATORS_IN_TREE. No path-opening error. Python 3.11.9. Network clone/curl and /tmp/r3 cd deliberately not run.
- Claim 2: {"verdict": "PASS_LOCATORS_IN_TREE", "counts": {"RESOLVES_IN_TREE": 1, "EXTERNAL_ONLY": 0, "UNRESOLVABLE": 0, "SHORTHAND_BARE_NAME": 1}}; exit 0. One actual in-tree locator survives; URL produces no offender.
- Claim 4: focused: committed/disk 3666bce6fc04a84e6e7868715349b34048eaa69ce3e677aadc96e3297cbb41d3; CRLF 88d8db8123e744c2699193bd5c8013fbb62c0fd952d425b779c6f9457488eba7. full: committed/disk 46ff948ae879709b87e17d05c4cdbb4dc3400372b9e2ad8d3128d061353aa7a6; CRLF 185a6177ce2296ca11af42e058f9ee661725c465836a65a19be6e8436bb2bc1a. Both labels match; neither blob empty.
- Claim 6: Literal workflow allowlist step: main exit 1, stacked exit 1. Main: 4 frozen paths, 27 outside-allowed paths; stacked: 0 frozen paths, 5 outside-allowed paths (.github/workflows/ci.yml and four removed 160000 gitlinks). Base changes frozen-path outcome, not the overall refusal. Outside-allowed membership/count also varies; only the boolean refusal is unchanged.
- Claim 8: 8 unique derivations for 8 skills. Every independently computed SKILL.md disk digest equals source_sha256 and frozen-ledger files entry; per-skill digests in report and measurements.json.
- Claim 9: Both manifests pin the measured vendor schema sha256 0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883 (1805 bytes). No online authenticity assertion.
- Claim 10: Scratch --generate-icons produces assets/icon-128.png sha256=70bfddc3ebd2d6445f54f1a4258f1f0b0b787ee3a629b47900e47c3aa23a16e8, equal to the non-placeholder pin. Original checkout lacks this file; no candidate file was repaired.
- Claim 12: OWNER_SUPPLIES_DELIVERED.json explicitly says DERIVED from repository owner, not a verified HUMAN. Human attribution, Portal draft/scan/review/Publish, vendor validator, SemVer/tag/assets, and ratification stay owner-only. Disclosure verified, actual account control/authorization not independently verified.
- Claim 13: focused exit 0: Ran 108 tests in 23.795s
OK; full exit 0: Ran 572 tests in 182.747s
OK (skipped=4). Offline socket guard, isolated temp/bytecode paths, specified interpreter and clone PYTHONPATH used.
- Claim 14: Stronger-than-evidence statements explicitly identified: R3_CI_FIRST_RUN.md says stacked allowlist violations zero (measured 5); DOC_RECONCILIATION_ERRATUM.md says one com.ao3 file (current 9), rejects public-plugin-verify.yml (guard actually allows it), and says any base red (only two tested); FAR calls every basis measured despite absent series locator and self-reported route/SID; unconditional build-lift wording requires --generate-icons.

Per-skill actual SHA256 (each equals derivation and ledger):
- `skills/pipd-assurance-tqaep/SKILL.md`: `703d354c5b04caa96c3deded4cd57c3a6ba91603a6419479117e4b83d568f776`
- `skills/pipd-authority-source/SKILL.md`: `89d04cf2e753e539f1d661beaa8e0df348f6ca8db9e423f516656106dcf68e91`
- `skills/pipd-execution-contract/SKILL.md`: `903c0af6ce09929b3c9c9f23abe650989c0a952fa4372dbe9414d076e7648478`
- `skills/pipd-package-project/SKILL.md`: `a5f2a57af6f903adec3cad069d2b1e4c15df42f14a14a8e3940830faae129a67`
- `skills/pipd-pd-bind/SKILL.md`: `613ab403d1163dd1563dc1430b0a247a245b4330d76c33f4d85e65e8223d2f10`
- `skills/pipd-pi-compile/SKILL.md`: `1a8e054f445f4150bdea01e9f302ae471b10896548dd1bbbc5fd13a89db82658`
- `skills/pipd-profile-tailor/SKILL.md`: `611d367d3062bce4f41e0906ed9236d1569205231e9b17625df6e73f190d84fc`
- `skills/pipd-route-intake/SKILL.md`: `72afada18aa79c33bee2d1190b296af153f37734c967f7bbf4574675786acc88`

Historical ADJ1 is correctly bound to receipt subject 389d3973: 107 changed paths, 22 product-side, 0 schemas, 0 src. Current HEAD is 160/22/0/0 against stacked base; the historical total is not relabelled as a current measurement.

# 4 What failed

- Claim 5: current-tree count is NINE, not THREE. All are round-scoped, but some are independently authored checker evidence. Product-side zero is verified separately.
- Claim 7: the cited findings-series file is absent. Nine AO12 findings are locatable; the prior six/three sequence is not established by that missing artifact.
- Claim 11: exact required build returns `REFUSED ICON_MISSING`, exit 2. It is not `REFUSED OWNER_INPUT_REQUIRED`, but it is also not BUILT. The supplies unlock a build with an additional generation flag; they do not make the exact required no-generation command build in this clean checkout. No repair was performed.

There is no ZIP sha256 from the exact command. The scratch-generated ZIP sha256 is `83e5ce5b4b3ac85e1be4842e16132c5450d2ae6074406a210debdc8a05bb4d87` and reproduces the maker receipt, which explicitly includes `--generate-icons`. This distinction is decisive, not a rounding-up opportunity.

# 5 UNCERTAINTY items

- UNCERTAINTY U1: Default fresh-clone three-cache-directory side effect (write-only-under-.ao-r3b restriction).
- UNCERTAINTY U2: Network clone, hosted CI, current PR/release state, online vendor-byte identity, release downloads.
- UNCERTAINTY U3: Verified human publisher, owner account control/authorization/signature, model/provider/SID/on-wire lane identity.
- UNCERTAINTY U4: Missing SELF_ITERATION_AFTER_AO.md and full 6 -> 3 -> 9 findings series.
- UNCERTAINTY U5: Portal/vendor validator, host UAT, production/security certification, release/promotion.
- UNCERTAINTY U6: receipt locator-tool digest form/source is unspecified. Current LF digest is `05f3fe138b9c93d96824a4ad5363949ce52f2f98e3e59a2f8fcf89d5f6066ad7`; historical LF is `70c8c9fd114cb549a0df50404a5bb5b647018610a741541d966a454dcb90521b`, historical CRLF is `1cbc93476fbfb90f9ab708eb780d2d00302c342c77aa6d855e6c0286658ad3e9`. None re-derives the receipt pin.
- UNCERTAINTY U7: differing test skips are environment-dependent; this run measured four, not a proven explanation of historical three versus four.
- UNCERTAINTY U8: the fact that a file is under the round directory is not proof that the maker authored it. Checker provenance is recorded internally, not externally identity-attested.

# 6 DISAGREEMENT items

- DISAGREEMENT D1: claim 5/current FAR THREE files versus measured NINE; product-side ZERO versus measured ZERO. The historical receipt subject had THREE and is not falsified by later additions.
- DISAGREEMENT D2: DOC_RECONCILIATION_ERRATUM.md says ONE versus current NINE (even its historical three-file snapshot differs from one).
- DISAGREEMENT D3: R3_CI_FIRST_RUN.md says stacked allowlist violations ZERO versus measured FIVE. Its earlier stacked table says FOUR outside allowed versus current FIVE; approved ci.yml remains outside the guard.
- DISAGREEMENT D4: unconditional exact build success/exit 0 versus exact measured exit 2/ICON_MISSING; flagged scratch generation is exit 0 and reproduces the recorded ZIP.
- DISAGREEMENT D5: receipt locator-tool recorded `3787c377d81a3e515550c5a202a64b721bbfd08907ecfe5c2bafed5fbe2d7365` versus current measured `05f3fe138b9c93d96824a4ad5363949ce52f2f98e3e59a2f8fcf89d5f6066ad7` (historical forms above also differ).

# 7 Claim-by-claim table (1..14)

| ID | Verdict | Evidence / finding |
|---|---|---|
| 1 | VERIFIED | Verbatim locator commands from root: negative exit 2 / FAIL_LOCATORS_NOT_RERUNNABLE; positive exit 0 / PASS_LOCATORS_IN_TREE. No path-opening error. Python 3.11.9. Network clone/curl and /tmp/r3 cd deliberately not run. |
| 2 | VERIFIED | {"verdict": "PASS_LOCATORS_IN_TREE", "counts": {"RESOLVES_IN_TREE": 1, "EXTERNAL_ONLY": 0, "UNRESOLVABLE": 0, "SHORTHAND_BARE_NAME": 1}}; exit 0. One actual in-tree locator survives; URL produces no offender. |
| 3 | INCONCLUSIVE | Before and after ordinary status: ?? .ao-r3b/ only. No tracked change or new candidate untracked-non-ignored entry. Bytecode redirected under .ao-r3b to obey write boundary; default fresh-clone creation of three cache directories not independently reproduced. |
| 4 | VERIFIED | focused: committed/disk 3666bce6fc04a84e6e7868715349b34048eaa69ce3e677aadc96e3297cbb41d3; CRLF 88d8db8123e744c2699193bd5c8013fbb62c0fd952d425b779c6f9457488eba7. full: committed/disk 46ff948ae879709b87e17d05c4cdbb4dc3400372b9e2ad8d3128d061353aa7a6; CRLF 185a6177ce2296ca11af42e058f9ee661725c465836a65a19be6e8436bb2bc1a. Both labels match; neither blob empty. |
| 5 | FAILED | DISAGREEMENT: current subject has 9 tracked files containing com.ao3, not 3; all under this round, zero product-side hits. Historical receipt subject 389d3973 really had 3; that does not bind the current subject. Additional files include independent-checker artifacts, not solely maker-authored prose. |
| 6 | VERIFIED | Literal workflow allowlist step: main exit 1, stacked exit 1. Main: 4 frozen paths, 27 outside-allowed paths; stacked: 0 frozen paths, 5 outside-allowed paths (.github/workflows/ci.yml and four removed 160000 gitlinks). Base changes frozen-path outcome, not the overall refusal. Outside-allowed membership/count also varies; only the boolean refusal is unchanged. |
| 7 | FAILED | Spot-checked historical ADJ1 (107 total/22 product/0 schemas/0 src), historical ADJ7 (3 versus current 9), negative/positive locator controls, vendor 1805-byte digest, and ADJ5 findings (9 entries). SELF_ITERATION_AFTER_AO.md cited for 6 -> 3 -> 9 is absent; that full series cannot be re-derived. Receipt locator-tool pin 3787c377... does not match current 05f3fe13... or historical LF 70c8c9fd...; hash form/source not specified. |
| 8 | VERIFIED | 8 unique derivations for 8 skills. Every independently computed SKILL.md disk digest equals source_sha256 and frozen-ledger files entry; per-skill digests in report and measurements.json. |
| 9 | VERIFIED | Both manifests pin the measured vendor schema sha256 0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883 (1805 bytes). No online authenticity assertion. |
| 10 | VERIFIED | Scratch --generate-icons produces assets/icon-128.png sha256=70bfddc3ebd2d6445f54f1a4258f1f0b0b787ee3a629b47900e47c3aa23a16e8, equal to the non-placeholder pin. Original checkout lacks this file; no candidate file was repaired. |
| 11 | FAILED | Exact mandated command exits 2: REFUSED ICON_MISSING: pinned icon is absent or not a regular file: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-r3-verify-r2\packaging\public-plugin\assets\icon-128.png Supplemental scratch generation exits 0: BUILT C:\Users\user\AppData\Local\Temp\ao-r3b-build-4l1t6kke\generated\pipd-ls-sp-public-skills.zip sha256=83e5ce5b4b3ac85e1be4842e16132c5450d2ae6074406a210debdc8a05bb4d87 members=56 claim_ceiling=LOCAL_PACKAGER_PASS_ONLY official_portal_verification=NOT_EXECUTED Exact command produced no ZIP/digest; supplemental digest is not rounded up into exact-command success. |
| 12 | VERIFIED | OWNER_SUPPLIES_DELIVERED.json explicitly says DERIVED from repository owner, not a verified HUMAN. Human attribution, Portal draft/scan/review/Publish, vendor validator, SemVer/tag/assets, and ratification stay owner-only. Disclosure verified, actual account control/authorization not independently verified. |
| 13 | VERIFIED | focused exit 0: Ran 108 tests in 23.795s / OK; full exit 0: Ran 572 tests in 182.747s / OK (skipped=4). Offline socket guard, isolated temp/bytecode paths, specified interpreter and clone PYTHONPATH used. |
| 14 | VERIFIED | Stronger-than-evidence statements explicitly identified: R3_CI_FIRST_RUN.md says stacked allowlist violations zero (measured 5); DOC_RECONCILIATION_ERRATUM.md says one com.ao3 file (current 9), rejects public-plugin-verify.yml (guard actually allows it), and says any base red (only two tested); FAR calls every basis measured despite absent series locator and self-reported route/SID; unconditional build-lift wording requires --generate-icons. |

# 8 Reproduction transcript (commands + literal output)

Interpreter: Python 3.11.9. Working directory is the clone root. `$R` assignment and script setup complete with exit 0. Original locator commands, including line continuations, are extracted unchanged; only the local precondition `$R` assignment is prepended. Network clone/curl, external /tmp/r3 navigation, and OpenSpec npm execution are NOT EXECUTED (offline/no path substitution pretending to be verbatim). The two locator calls themselves do run verbatim from root.

```text
git status --porcelain
exit 0
?? .ao-r3b/

```

```text
git status --porcelain --ignored
exit 0
?? .ao-r3b/

```

```text
"C:/Program Files/Git/usr/bin/bash.exe" -c "R=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
python \"$R/verify/tools/check_evidence_locators.py\" --root . --search-dir . \
    \"$R/verify/ao12/EXTERNAL_CHALLENGE_REPORT.md\""
exit 2
{"verdict": "FAIL_LOCATORS_NOT_RERUNNABLE", "counts": {"RESOLVES_IN_TREE": 0, "EXTERNAL_ONLY": 7, "UNRESOLVABLE": 36, "SHORTHAND_BARE_NAME": 54}}
  EXTERNAL_ONLY  C:\Users\user\AppData\Local\Temp\ao12-roo_vkak
  EXTERNAL_ONLY  C:/Users/user/.agents/skills/fabric-external-independent-challenge-reviewer/SKILL.md
  EXTERNAL_ONLY  C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt
  UNRESOLVABLE   C:/Users/user/AppData/Local/Temp/ao12-roo_vkak/CHILD_OS_UNDECIDED_JUNCTION/worktree
  UNRESOLVABLE   C:\Users\user\AppData\Local\Temp\ao12-roo_vkak\challenge.py
  EXTERNAL_ONLY  C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\scripts\\verify_re
  EXTERNAL_ONLY  C:\\Users\\user\\.agents\\skills\\fabric-external-independent-challenge-reviewer\\tests
  EXTERNAL_ONLY  C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepai
  EXTERNAL_ONLY  C:\\Projects\\Agent_Workspace\\PIPD\\worktrees\\s4post-b-wt\\.hgk\\rounds\\S4POST-20261012-postrepai
  UNRESOLVABLE   Users/user/.agents/skills/fabric-external-independent-challenge-reviewer/SKILL.md
  UNRESOLVABLE   stage-b/ROUND_ASSIGNMENT.json
  UNRESOLVABLE   stage-b/OWNER_DECISION_MODEL_DEVIATION.md
  UNRESOLVABLE   evidence/EVIDENCE_RETURN_PACK.json
  UNRESOLVABLE   verify/ao12/FREEZE.json

```

```text
"C:/Program Files/Git/usr/bin/bash.exe" -c "R=.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade
python \"$R/verify/tools/check_evidence_locators.py\" --root . --search-dir . \
    \"$R/OWNER_ACTION_REQUEST.md\" \"$R/HARNESS_FREEZE_AND_AO_LOOP_CAP.md\""
exit 0
{"verdict": "PASS_LOCATORS_IN_TREE", "counts": {"RESOLVES_IN_TREE": 9, "EXTERNAL_ONLY": 0, "UNRESOLVABLE": 0, "SHORTHAND_BARE_NAME": 15}}

```

```text
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/tools/check_evidence_locators.py --root . --search-dir . .ao-r3b/url-control.md
exit 0
{"verdict": "PASS_LOCATORS_IN_TREE", "counts": {"RESOLVES_IN_TREE": 1, "EXTERNAL_ONLY": 0, "UNRESOLVABLE": 0, "SHORTHAND_BARE_NAME": 1}}

```

```text
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe tools/build_public_plugin.py --source-root . --ledger .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/FROZEN_SOURCE_LEDGER.json --source-commit 3233c817cc0a8fcd3f80f49219f219544235d25a --out-dir C:\Users\user\AppData\Local\Temp\ao-r3b-build-4l1t6kke\exact
exit 2
REFUSED ICON_MISSING: pinned icon is absent or not a regular file: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-r3-verify-r2\packaging\public-plugin\assets\icon-128.png

```

```text
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe tools/build_public_plugin.py --source-root . --ledger .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/FROZEN_SOURCE_LEDGER.json --source-commit 3233c817cc0a8fcd3f80f49219f219544235d25a --packaging-root C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-r3-verify-r2\.ao-r3b\packaging-copy --out-dir C:\Users\user\AppData\Local\Temp\ao-r3b-build-4l1t6kke\generated --generate-icons
exit 0
BUILT C:\Users\user\AppData\Local\Temp\ao-r3b-build-4l1t6kke\generated\pipd-ls-sp-public-skills.zip sha256=83e5ce5b4b3ac85e1be4842e16132c5450d2ae6074406a210debdc8a05bb4d87 members=56 claim_ceiling=LOCAL_PACKAGER_PASS_ONLY official_portal_verification=NOT_EXECUTED

```

```text
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest discover -s tests -p test_s4ext_*.py -v
exit 0

----------------------------------------------------------------------
Ran 108 tests in 23.795s

OK
[Full literal output is in focused.log/full.log and transcript.json.]
```

```text
C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -m unittest discover -s tests -t . -v
exit 0

----------------------------------------------------------------------
Ran 572 tests in 182.747s

OK (skipped=4)
[Full literal output is in focused.log/full.log and transcript.json.]
```

```text
git status --porcelain
exit 0
?? .ao-r3b/

```

```text
git status --porcelain --ignored
exit 0
?? .ao-r3b/
!! .ao-r3b/bytecode/
!! .ao-r3b/packaging-copy/assets/icon-128.png

```

```text
git diff --exit-code
exit 0

```

```text
PR_BASE_SHA=224591431a164ab72a9423cd180e417e8a762403 STACKED_BASE_SHA=52542c395a0f91dc2ba4bd6123acd4cdecd780dc bash .ao-r3b/workflow-guard-verbatim.sh
exit 1
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .github/workflows/ci.yml
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/artifacts/tqaep_design_tmp/ecp.json
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/artifacts/tqaep_design_tmp/pi.json
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/execute/candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/pristine-candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/regression-candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/semcheck
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: docs/ERRATUM_2026-10-12_preview3_release_provenance.md
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: docs/RELEASE_TUPLE.json
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: docs/S4_SPEC_DEL_ADJUDICATION.json
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: examples/first-run/run.ps1
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: examples/first-run/run.sh
UPGRADE_WROTE_FROZEN_PATH: schemas/PI-PKG.schema.json
UPGRADE_WROTE_FROZEN_PATH: schemas/TraceLink.schema.json
UPGRADE_WROTE_FROZEN_PATH: src/pipd_ls_sp/profiles.py
UPGRADE_WROTE_FROZEN_PATH: src/pipd_ls_sp/validate.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_publication_projection.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_artifact_reproducibility.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_first_run_portable.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_profile_boundaries.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_release_provenance.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_spec_del_adjudication.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_s4ext_trace_closure.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_technology_admission.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tests/test_tqaep_design_positive.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/admit_technologies.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/build_mount_pack.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/build_s4_spec_del_adjudication.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/history_secret_scan.py
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: tools/verify_evidence_digests.py
WRITE_SET_VIOLATION (base 224591431a164ab72a9423cd180e417e8a762403)
```
Full changed-path stdout: guard-main.log.

```text
PR_BASE_SHA=52542c395a0f91dc2ba4bd6123acd4cdecd780dc STACKED_BASE_SHA=52542c395a0f91dc2ba4bd6123acd4cdecd780dc bash .ao-r3b/workflow-guard-verbatim.sh
exit 1
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .github/workflows/ci.yml
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/execute/candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/pristine-candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/regression-candidate
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: .hgk/rounds/R2-20261009-qualification/product-repair/semcheck
WRITE_SET_VIOLATION (base 52542c395a0f91dc2ba4bd6123acd4cdecd780dc)
```
Full changed-path stdout: guard-stacked.log.

Hash measurements (binary pipes, not PowerShell text roundtrip):
- `git cat-file -p 5351c5fadca5cba14cd0600cead81a62753f0e1a:.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/raw/focused.log`: 18678 bytes; SHA256 3666bce6fc04a84e6e7868715349b34048eaa69ce3e677aadc96e3297cbb41d3; disk 3666bce6fc04a84e6e7868715349b34048eaa69ce3e677aadc96e3297cbb41d3; converted CRLF 88d8db8123e744c2699193bd5c8013fbb62c0fd952d425b779c6f9457488eba7
- `git cat-file -p 5351c5fadca5cba14cd0600cead81a62753f0e1a:.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/raw/full.log`: 95335 bytes; SHA256 46ff948ae879709b87e17d05c4cdbb4dc3400372b9e2ad8d3128d061353aa7a6; disk 46ff948ae879709b87e17d05c4cdbb4dc3400372b9e2ad8d3128d061353aa7a6; converted CRLF 185a6177ce2296ca11af42e058f9ee661725c465836a65a19be6e8436bb2bc1a

Tracked-file scan (git ls-files, read each file as bytes; exempt officer outputs excluded):
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/00_plan/TT_S4POST_REGISTER.tsv`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/ACCEPTANCE_RECORD_STAGEB.md`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/far/FAR_OPEN_ITEMS_ADJUDICATION_20261013.md`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/AO_VERDICT_R3_SUMMARY.md`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/AO_VERIFY_SUBJECT_389D3973_gpt-6.1-sol_medium.log`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/DOC_RECONCILIATION_ERRATUM.md`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/ao_lane/AO_VERDICT.json`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/ao_lane/inspect.py`
- `.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/r3/ao_lane/measurements.json`

Removed gitlink evidence:
```text
:160000 000000 829c17e 0000000 D	.hgk/rounds/R2-20261009-qualification/execute/candidate
:160000 000000 829c17e 0000000 D	.hgk/rounds/R2-20261009-qualification/product-repair/pristine-candidate
:160000 000000 829c17e 0000000 D	.hgk/rounds/R2-20261009-qualification/product-repair/regression-candidate
:160000 000000 829c17e 0000000 D	.hgk/rounds/R2-20261009-qualification/product-repair/semcheck
```

Four-plus FAR spot checks: (1) historical ADJ1 diff gives 107/22/0/0; (2) historical ADJ7 grep gives 3 and present-tree byte scan gives 9; (3) receipt negative locator counts 0/7/36/54 and positive 9/0/0/15 exactly reproduce; (4) C1 vendor file has 1805 bytes and measured 0a4aad95... matching both manifests, but online identity is unverified; (5) AO12 FINDINGS.json has 9 entries, while SELF_ITERATION_AFTER_AO.md is absent; (6) root requirements.lock literally discloses NOT HASH-PINNED and packaging/public-plugin/requirements.lock is absent. The route/SID entry is expressly self-recorded and cannot be re-derived here.

# 9 Non-mutation finding

Captured ordinary before and after: `?? .ao-r3b/` only. Captured ignored before: `?? .ao-r3b/` only. Captured ignored after additionally names `!! .ao-r3b/bytecode/` and `!! .ao-r3b/packaging-copy/assets/icon-128.png`. No ignored src/tests/tools caches appeared because writes there were forbidden and redirected. `git diff --exit-code` exits 0 with empty output; staged changes are absent in porcelain. These are officer-created entries, not candidate mutations. No original packaging icon was generated.

The narrower no-tracked/no-new-untracked-non-ignored-candidate wording is consistent with this run. The default fresh-clone three-cache-directory half is INCONCLUSIVE, not falsely declared verified. It cannot be measured on this clone without violating the explicit write boundary. Scratch build directory outside the repo is the specifically requested output exception, not a candidate edit.

# 10 Scope limits (what this verdict does NOT cover)

This advisory verifies local bytes and executions only. It does not grant owner ratification, promotion, publication, PASS, release, vendor approval, production qualification, a verified human identity, broad security certification, hosted CI re-execution, or live release/PR state. It does not repair anything, independently prove the checker model/provider/OAuth identity, approve governance supersession, or assess all repository vulnerabilities. Local origin/main is a stored ref, not a network freshness guarantee.

# 11 Residual risk

Stale subject-bound records coexist with later prose presented as current; a clean checkout has no pinned icon until generation; guard structure still refuses authorized ci.yml and deleted gitlinks against both tested bases. Good local tests and a reproducible generated ZIP do not discharge owner-only Portal/identity decisions. Locator PASS is limited to the tested documents and existence-based parser; it is not proof of all evidence content or independent authorship. The FAR still overstates the findings-series and route/SID foundations. Existing dependency lock is not artifact-hash-pinned. Icon is generator artwork, not owner brand approval.

# 12 Required owner decisions

- Decide whether the exact no-generation build is a required acceptance contract or whether a documented --generate-icons precondition is intended; do not treat this failed exact invocation as success. No repair is proposed or made by this officer.
- Disposition the current nine-file count and missing/mismatched FAR evidence as CR/TT; do not substitute the three-file historical snapshot for this subject.
- Resolve allowed-set/governance conflict without claiming the existing workflow goes green merely by changing base; declare precise subject/base and approve any future change separately.
- Ratify or reject the integrated candidate and actual A1 approval/publisher identity; verified human attribution, Portal sequence, vendor validator, SemVer/tag/assets remain owner-only.
- Accept or request a separately authorized default-cache side-effect reproduction in a scratch clone if claim 3 must be fully closed. Round-cap policy remains the owner decision.

# 13 Verdict

**FAIL_CHALLENGE**. Required claims 5 and 11 are FAILED; claim 7 also FAILED; claim 3 INCONCLUSIVE. Claims 1, 2, 4, 8, 9, 10, 12, 13 and the scoped claim 6 are verified. Claim 14 is verified as an inspection/reporting obligation: stronger-than-artifact statements are explicitly named, not endorsed. A supplemental successful generated build does not overwrite the exact command refusal.

Advisory evidence to the owner only: grants no release, no pass, no promotion. The checker makes no repairs and leaves the candidate tracked tree unchanged.
