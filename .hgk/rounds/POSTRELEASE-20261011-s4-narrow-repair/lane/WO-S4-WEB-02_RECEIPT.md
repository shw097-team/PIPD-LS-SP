# WO-S4-WEB-02 receipt — post-release narrow repair (S4 ChatGPT/Web mount pack)

Round: `POSTRELEASE-20261011-s4-narrow-repair`
WorkOrder: `WO-S4-WEB-02`
Writer: Codex bounded writer (`deepseek-v4.1-flash`)
Interpreter (pinned): `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (Python 3.11.9)
Candidate head at work start: `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7`
Ceiling: `REPAIR_CANDIDATE_ONLY` — no commit, no push, no tag, no release, no upload.

Admitted write scope (only these were written):

- `dist/mount/**` (the pack directory and the built ZIP + `.sha256` sidecar)
- `tools/build_mount_pack.py`
- `tests/test_postrelease_web_mount.py`
- `.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/evidence/WEB_MOUNT_UAT.json`
- `.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/` (this receipt and raw logs)

Nothing under `README.md`, `schemas/**`, `src/**`, `dist/web/**`, other `tools/` or `tests/` files, or
outside the repository was touched. The pack adds **no ninth skill**: `SKILL.md` is a dispatcher over
the eight existing `skills/pipd-*` skills.

All commands below were run from the repository root
`C:\Projects\Agent_Workspace\PIPD-postrelease-wt` unless stated otherwise.

---

## 1. Deliverable — the pack

Pack directory:

```
dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2/
  README_MOUNT.md
  PIPD_LS_SP_QUICKSTART_PROMPT.md
  SKILL.md
  references/PIPD_S4_CORE.md
  references/PIPD_SOURCE_MAP.md
  references/PIPD_8_SKILLS_INDEX.md
  references/PIPD_PROFILE_AND_SAFETY.md
  references/PIPD_EXAMPLES.md
  MANIFEST.sha256
```

Built artifact:

```
dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip.sha256
```

Every document carries a `Source Locators` section and states the release identity
`v0.1.0-preview.2` with tag commit `8faa64e581e8c25f5ec355475e29561847da3ead`.

## 2. Acceptance command 1 — build the manifest and the ZIP

```
PY=<pinned> python.exe
$PY tools/build_mount_pack.py --pack-root dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2 --out-zip dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
```

where `<pinned>` is `C:/Users/user/AppData/Local/Programs/Python/Python311`.

Raw output:

```
BUILD OK: pack_root=C:\Projects\Agent_Workspace\PIPD-postrelease-wt\dist\mount\pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2 out_zip=C:\Projects\Agent_Workspace\PIPD-postrelease-wt\dist\mount\PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip members=9 zip_sha256=1992c54bb3e8e83588e4ef2930d1cc65ce7ada21460deb85930767a4db499daa
```

Exit code: `0`. Members `= 9` (8 content files + `MANIFEST.sha256`; the manifest entry is written last).

### 2a. Determinism — same inputs rebuild byte-identically

The build was re-run and produced the same digest
`1992c54bb3e8e83588e4ef2930d1cc65ce7ada21460deb85930767a4db499daa`, because every `ZipInfo` is
stamped with the fixed `date_time=(1980,1,1,0,0,0)`, `create_system=0` and
`external_attr=0o644<<16`. `tests/test_postrelease_web_mount.py::test_build_is_byte_deterministic`
asserts this.

## 3. ZIP digest and sidecar

```
dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
  sha256 = 1992c54bb3e8e83588e4ef2930d1cc65ce7ada21460deb85930767a4db499daa

dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip.sha256 contents:
1992c54bb3e8e83588e4ef2930d1cc65ce7ada21460deb85930767a4db499daa  PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
```

The sidecar digest equals the build digest.

## 4. `MANIFEST.sha256` (verbatim)

```
92b28db6b641f7e85b2495653c7bb9dc74e8b052f348f3bf62962bd17e2122dd  PIPD_LS_SP_QUICKSTART_PROMPT.md
f541ef5015a41202fbf6a64ec99a06a91a6f72d41aaca07e22666e803f6d4e98  README_MOUNT.md
95291bc7dcd264c888d400f1f7606aed47ab70f436a2e031147de3c036cb6a8a  SKILL.md
a81fb623ebbe7c8d3be7a6300e7e80c546610fe6534105af0f73188583da0d5d  references/PIPD_8_SKILLS_INDEX.md
4df9784329b106fc61b13f936998c96e2a668923803793e2187e7ee770489011  references/PIPD_EXAMPLES.md
daa4356492a8219e893096f5a9dbec6051865d48b0cb88e9d6672e22a0160b0a  references/PIPD_PROFILE_AND_SAFETY.md
b43cb0f7e2706e14645b62808d3bba55b834a6789e169f49018075f8c25fa513  references/PIPD_S4_CORE.md
b71b9e608434aa4ea8710b78e16ecc206acee38c76d18274484d977811decf43  references/PIPD_SOURCE_MAP.md
```

Format is `"<hash>  <relpath>"`, relative paths, sorted. `MANIFEST.sha256` itself is not listed and is
the last archive entry.

## 5. Acceptance command 2 — verify (recompute from ZIP bytes)

```
$PY tools/build_mount_pack.py --verify dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
```

Raw output:

```
VERIFY PASS: dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip
```

Exit code: `0`. Verification recomputes each member digest from the ZIP bytes, checks manifest coverage
in both directions, and confirms no member path escapes the pack root.

## 6. Negative controls — the verifier must refuse and name the fault

Driver: `lane/run_web_mount_negatives.py` (mutates a temporary copy of the built ZIP; writes nothing
outside a temp dir). Raw output:

```
===== NEG-1 mutated member =====
verify_pack -> ok=False exit=1
  - MUTATED_MEMBER: references/PIPD_S4_CORE.md

===== NEG-2 unmanifested member =====
verify_pack -> ok=False exit=1
  - UNMANIFESTED_FILE: EXTRA.md

===== NEG-3 manifest entry missing from ZIP =====
verify_pack -> ok=False exit=1
  - MANIFEST_ENTRY_NOT_IN_ZIP: references/PIPD_EXAMPLES.md

===== NEG-4 path escapes pack root =====
verify_pack -> ok=False exit=1
  - ESCAPES_PACK_ROOT: ../evil.md
  - OUTSIDE_PACK_ROOT: ../evil.md
  - UNMANIFESTED_FILE: 
```

Exit code: `0` for the driver (each mutation's `verify_pack` returned `ok=False`, named a non-zero
result). All four required negatives are exercised and named: a mutated pack file ⇒ non-zero; a
missing file ⇒ named; a manifest entry not present in the ZIP ⇒ named; a path that escapes the pack
root ⇒ named. These are also asserted by the test module (`test_mutated_member_is_refused_and_named`,
`test_member_not_in_manifest_is_refused_and_named`,
`test_manifest_entry_missing_from_zip_is_refused_and_named`,
`test_path_escaping_pack_root_is_refused_and_named`, `test_absolute_path_is_refused`).

## 7. Acceptance command 3 — new unit tests

```
$env:PYTHONPATH='<repo>/src'; $PY -m unittest tests.test_postrelease_web_mount -v
```

Raw output:

```
test_absolute_path_is_refused ... ok
test_all_members_are_stamped_fixed ... ok
test_build_is_byte_deterministic ... ok
test_dispatcher_declares_triggers_and_non_triggers ... ok
test_eight_existing_skills_and_no_ninth ... ok
test_every_document_carries_locator_and_release_identity ... ok
test_manifest_entry_missing_from_zip_is_refused_and_named ... ok
test_manifest_is_last_archive_entry ... ok
test_manifest_recomputes_from_members ... ok
test_member_not_in_manifest_is_refused_and_named ... ok
test_mutated_member_is_refused_and_named ... ok
test_pack_contains_no_obvious_secret ... ok
test_pack_directory_has_exact_expected_files ... ok
test_path_escaping_pack_root_is_refused_and_named ... ok
test_published_zip_verifies_and_matches_sidecar ... ok
test_quickstart_prompt_bounds_the_role ... ok
test_readme_mount_marks_unavailable_capabilities ... ok
test_uat_evidence_file_coverage ... ok
test_verify_nonexistent_zip_refused ... ok
test_verify_passes_and_names_nothing ... ok

----------------------------------------------------------------------
Ran 20 tests in 0.410s

OK
```

Exit code: `0`. (Test ID prefix `tests.test_postrelease_web_mount.MountPackBuildTests.` elided per line
for brevity; the full `-v` listing is in `lane/WO-WEB02.unittest_web_mount.log`.)

## 8. Acceptance command 4 — existing web pack must not regress

```
$env:PYTHONPATH='<repo>/src'; $PY -m unittest tests.test_web_pack -v
```

Raw output:

```
Ran 16 tests in 3.275s

OK
```

Exit code: `0`. (Full listing in `lane/WO-WEB02.unittest_web_pack.log`.) `dist/web/**` was not
modified.

## 9. Five-case consumer UAT — `.hgk/.../evidence/WEB_MOUNT_UAT.json`

Because this round had no interactive ChatGPT session and no qualifying native-upload account, cases
1–4 were driven as deterministic content checks over the actual pack files, and case 5 as an
extraction-and-navigation check. Driver: `lane/run_web_mount_uat.py`. Raw output:

```
WROTE ...\evidence\WEB_MOUNT_UAT.json
UAT-01 PASS {"non_trigger_section": true, "pi_style_phrase": true, "referenced_docs_carry_locator_and_identity": true, "routed_skills": 8, "trigger_section": true}
UAT-02 PASS {"brainstorm_without_locators_excluded": true, "chit_chat_excluded": true, "no_dispatch_wording": true}
UAT-03 PASS {"dispatcher_declares_NO_SOURCE_LOCATOR": true, "example_refusal_present": true, "refusal_is_typed": true}
UAT-04 PASS {"acceptance_authority_refused": true, "dispatcher_declares_UNAUTHORISED_ACTION": true, "forbidden_claim_listed": true, "forbids_scope_widening": true, "forbids_self_pass": true}
UAT-05 PASS {"manifest_all_recompute": true, "manual_attachment_path_documented": true, "native_upload_path_documented": true, "readme_present": true, "skill_present": true, "source_locators_recoverable": true}
```

Exit code: `0`.

Summary:

| case | kind | verdict | claim_ceiling |
| --- | --- | --- | --- |
| UAT-01 | positive — PI-style design request dispatches to the eight-skill chain | PASS | DESIGN_ONLY |
| UAT-02 | negative — ordinary chit-chat is a non-trigger | PASS | DESIGN_ONLY |
| UAT-03 | refusal — no repository context / no source locator ⇒ typed refusal | PASS | DESIGN_ONLY |
| UAT-04 | refusal — adversarial self-PASS / permission widening / acceptance authority ⇒ typed refusal | PASS | DESIGN_ONLY |
| UAT-05 | first-time mount — paths and source locators recoverable by a non-developer | PASS | DESIGN_ONLY |

Each case in the JSON carries `case_id`, `fixed_input`, `expected`, `observed`, verbatim `raw_output`,
`verdict` and `claim_ceiling`, plus a top-level `method` note recording that no interactive session
existed.

## 10. NOT_SUPPORTED rows (with reason)

From `evidence/WEB_MOUNT_UAT.json` → `not_supported`:

| record | mount_path | verdict | reason |
| --- | --- | --- | --- |
| `NATIVE_SKILL_UPLOAD` | `Plugins -> Skills -> Create -> Upload` | NOT_SUPPORTED | This round had no qualifying native-upload account/workspace, so the native skill-upload path was not exercised; no native load is claimed. |
| `LIVE_CHAT_HOST_EXECUTION` | chat host tool execution / CLI / repo write / HITL | NOT_SUPPORTED | The chat host has no tool execution, repository writing, CLI invocation, HITL authority or network/file access; these are `NOT_AVAILABLE`. |

No fake native PASS was written. `README_MOUNT.md` marks tool execution, repository writing, CLI
invocation, HITL authority and network/file access as `NOT_AVAILABLE` for the chat host, and points at
an authorised external executor. The native-upload path is described plainly as untested this round;
the ordinary user's mount path is manual attachment / Project Knowledge.

## 11. Content-safety checks

- No token, credential, PII or unauthorised normative body. `test_pack_contains_no_obvious_secret`
  scans the pack for obvious secret material and passes.
- Quoted normative material is kept to short attributed excerpts or locators only.
- No ninth skill: `test_eight_existing_skills_and_no_ninth` asserts the dispatcher routes over exactly
  the eight existing `skills/pipd-*` skills.

## 12. Reproduce this receipt

From the repository root with the pinned interpreter:

```
$PY tools/build_mount_pack.py --pack-root dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.0-preview.2 --out-zip dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip   # exit 0, zip_sha256=1992c54b…
$PY tools/build_mount_pack.py --verify dist/mount/PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip                                                                          # exit 0, VERIFY PASS
$PY .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/run_web_mount_negatives.py                                                                                  # exit 0, 4 named refusals
$PY .hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/run_web_mount_uat.py                                                                                        # exit 0, 5 PASS
$env:PYTHONPATH='src'; $PY -m unittest tests.test_postrelease_web_mount -v                                                                                             # exit 0, Ran 20 OK
$env:PYTHONPATH='src'; $PY -m unittest tests.test_web_pack -v                                                                                                          # exit 0, Ran 16 OK
```

`$PY` denotes the pinned interpreter `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe`.

Raw logs retained alongside this receipt: `WO-WEB02.build.log`, `WO-WEB02.verify.log`,
`WO-WEB02.negatives.log`, `WO-WEB02.uat.log`, `WO-WEB02.unittest_web_mount.log`,
`WO-WEB02.unittest_web_pack.log`.

## 13. Claim ceiling

`REPAIR_CANDIDATE_ONLY`. The pack is candidate, preview-only content bound to release
`v0.1.0-preview.2` (`8faa64e581e8c25f5ec355475e29561847da3ead`). Nothing here is committed, pushed,
tagged, released or uploaded. The chat-host capability limits (`NOT_AVAILABLE`) and the untested
native-upload path remain open and are recorded as `NOT_SUPPORTED`.
