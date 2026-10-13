ROLE: you are the independent checker for a governed round. Because your sandbox refuses local
file reads and process execution (measured: `git`, `python` and a plain file read all returned
`blocked by policy` on this lane), EVERYTHING needed to judge is reproduced inline below. Judge only
what is inline. If a block needed for a sub-claim is absent, answer INCONCLUSIVE for that sub-claim and
name the missing block - do not infer it from the claim's wording, and do not round a failure up.
A verdict is CONFIRMED only if the inline blocks themselves settle it. End with the token on its own
line.

CLAIM C1 (verbatim, as put to earlier checkers): "The standard build ships the contract registry
(clean install reports mode=INSTALLED with the expected families; doctor exits 0; the sdist-to-wheel
route also holds)."

Sub-claims to adjudicate separately:
  C1a  the built wheel SHIPS the contract registry (not merely that a source tree has it)
  C1b  an installed-wheel check reports mode=INSTALLED with the expected families
  C1c  the doctor receipt carries its own exit code and the command that produced it
  C1d  the sdist-to-wheel route reports the same mode=INSTALLED

=== BLOCK 1: FAMILY_IDENTITY_RECEIPT.md (full) ===
# Family-IDENTITY receipt - the artefact three audits asked for

The mandated verification lane said three times that a numeric family count cannot distinguish a
correct registry from a silently reduced one that preserves the count, and named the artefact that
would settle it: an unredacted output listing the per-family canonical NAMES, plus registry digests
tied to the head, taken from the INSTALLED package rather than the work tree. This is that artefact,
produced by `scripts/report_family_identity.py` and **falsifiable** - the negative control below turns
it red.

## Provenance

- Stage A head bound into this receipt: `5310896e706e01a9cdb0123285bccec75086bcb8`
- wheel built from that tree with the real backend: `pipd_ls_sp-0.1.1a3-py3-none-any.whl` sha256=d2837f37a287d0c9b2b2fdfad30967fa9b363dffe2a1ac106a4d1caac79dd3db
- installed into a fresh venv created with `--system-site-packages` (so the declared `jsonschema>=4.0`
  dependency is satisfied by the host's 4.26.0 rather than silently skipped), installed with
  `--no-index --no-deps`, and run from a neutral working directory so the resolver selects the
  **INSTALLED** surface instead of a workspace-local `schemas/`.
- Registry selection is reported by the product's own `describe_schemas_source()`, so the surface a
  verdict came from is visible rather than assumed.

## Positive run (installed package) - verdict `PASS`

```json
{
  "verdict": "PASS",
  "schemas_source_mode": "INSTALLED",
  "schemas_dir": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\pipd-s4r3-exec\\famvenv\\Lib\\site-packages\\pipd_ls_sp\\schemas",
  "expected_family_count": 19,
  "expected_names_in_order": [
    "ArtifactIdentity",
    "AuthorityBinding",
    "RequirementAtom",
    "ProfileBinding",
    "TechnologyAdmission",
    "PI-PKG",
    "PD-PKG",
    "TraceLink",
    "TaskSpecSeed",
    "ConstructionContract",
    "WorkOrderCandidate",
    "ECP",
    "TQAEP",
    "ExecutionHandoff",
    "EvidenceExpectation",
    "ClaimCeiling",
    "SurfaceProjectionManifest",
    "GENIEProjectionRef",
    "ExecutionBindingRef"
  ],
  "installed_family_count": 19,
  "installed_names_in_order": [
    "ArtifactIdentity",
    "AuthorityBinding",
    "RequirementAtom",
    "ProfileBinding",
    "TechnologyAdmission",
    "PI-PKG",
    "PD-PKG",
    "TraceLink",
    "TaskSpecSeed",
    "ConstructionContract",
    "WorkOrderCandidate",
    "ECP",
    "TQAEP",
    "ExecutionHandoff",
    "EvidenceExpectation",
    "ClaimCeiling",
    "SurfaceProjectionManifest",
    "GENIEProjectionRef",
    "ExecutionBindingRef"
  ],
  "installed_files": [
    "ArtifactIdentity.schema.json",
    "AuthorityBinding.schema.json",
    "ClaimCeiling.schema.json",
    "ConstructionContract.schema.json",
    "ECP.schema.json",
    "EvidenceExpectation.schema.json",
    "ExecutionBindingRef.schema.json",
    "ExecutionHandoff.schema.json",
    "GENIEProjectionRef.schema.json",
    "PD-PKG.schema.json",
    "PI-PKG.schema.json",
    "ProfileBinding.schema.json",
    "RequirementAtom.schema.json",
    "SurfaceProjectionManifest.schema.json",
    "TQAEP.schema.json",
    "TaskSpecSeed.schema.json",
    "TechnologyAdmission.schema.json",
    "TraceLink.schema.json",
    "WorkOrderCandidate.schema.json",
    "registry.json"
  ],
  "installed_per_file_sha256": {
    "ArtifactIdentity.schema.json": "d747387f45e52647edebc7f5487304e6465626998b0597356936a9ffa45920ea",
    "AuthorityBinding.schema.json": "245d33ffb2578a4b00c982f73e768959a00c5d71aa73a44fe94fcae2258470ca",
    "ClaimCeiling.schema.json": "1f02f4fce359cb4fa7615c592601e936ebe9a1afc80b128e9d5c8b6601acec0d",
    "ConstructionContract.schema.json": "d40bc15d09e9694a3a778f8d9e7fd512779b65bfde391a0421ef97f50683c28e",
    "ECP.schema.json": "33688671e6eec18229e3da35a210f0c88799d4e21c5378d0518cd1e4213c7331",
    "EvidenceExpectation.schema.json": "b975375b59ae151b6b5740bb0069a5c8441b3a7e0acc94cf5404fa15ce5068e7",
    "ExecutionBindingRef.schema.json": "3372a5ce1fbbc510372e01e59eec41e13abfd496f0812c39f2a176a02b8c9ae4",
    "ExecutionHandoff.schema.json": "2a96e0d2ce33974beb4d27dd61386cd6b809cc3dd63c6dffebc17d581e641d3a",
    "GENIEProjectionRef.schema.json": "df0b6303bb5f02a489c3b7bbfcb97dabcb05f5834323f24e0b9a3cfe6613d41f",
    "PD-PKG.schema.json": "c6571cc959b1da3d28e74e03c639d80442f62eccc4940ff24e0126499143c445",
    "PI-PKG.schema.json": "ee9b0f8bf7d64fc74b979ddb785f6a739783b45c4deaee81172e9e29a22fce77",
    "ProfileBinding.schema.json": "63798436312fee6a814a1ade64380d3a36646fecea1a0bac07f77a095ee8739d",
    "registry.json": "85100a8e5ba6320f6648d33a14099fb999b2c452a94aff1652854d2550065e9d",
    "RequirementAtom.schema.json": "3394c61dd771ed62a2741ef48e779a7811f7c190101a45d7ebf77eea22ec5541",
    "SurfaceProjectionManifest.schema.json": "acca81b498b787f8279f0981847ed7d13e19ca559c750aa593c99ff9b0c4abc3",
    "TaskSpecSeed.schema.json": "0230171cb7f72dccd5b081d00ce079b6ef9f456bcf614388f4e2acb71140940c",
    "TechnologyAdmission.schema.json": "098be650cce90ed956c9b5224f6907fa7081f57d162819c0cb5c7b3dcec4008e",
    "TQAEP.schema.json": "1e704b3f9942bdbe15cdfc9b1be9baf8880ac39841ef91fd7ddf2084eb0a9fa6",
    "TraceLink.schema.json": "7bd3ab0ff4ed2c3eb8750530dcbabd8a7f0a08b2febe48fbb230cdd21139faaa",
    "WorkOrderCandidate.schema.json": "9cedabd6038862c014641c20714dab086b9b535165c515326b7db9c56b690788"
  },
  "checks": {
    "installed_names_equal_expected_set_and_order": true,
    "installed_count_equal_expected": true,
    "installed_names_are_unique": true,
    "installed_every_family_has_required_fields": true,
    "installed_files_identical_to_tree": true
  },
  "only_in_installed": [],
  "only_in_tree": []
}
```

## Negative control (one family dropped from a copy, selected via `PIPD_SCHEMAS_DIR`) - verdict `FAIL`

```json
{
  "verdict": "FAIL",
  "schemas_source_mode": "OVERRIDE",
  "schemas_dir": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\pipd-s4r3-exec\\famneg\\schemas",
  "expected_family_count": 19,
  "expected_names_in_order": [
    "ArtifactIdentity",
    "AuthorityBinding",
    "RequirementAtom",
    "ProfileBinding",
    "TechnologyAdmission",
    "PI-PKG",
    "PD-PKG",
    "TraceLink",
    "TaskSpecSeed",
    "ConstructionContract",
    "WorkOrderCandidate",
    "ECP",
    "TQAEP",
    "ExecutionHandoff",
    "EvidenceExpectation",
    "ClaimCeiling",
    "SurfaceProjectionManifest",
    "GENIEProjectionRef",
    "ExecutionBindingRef"
  ],
  "installed_family_count": 18,
  "installed_names_in_order": [
    "AuthorityBinding",
    "RequirementAtom",
    "ProfileBinding",
    "TechnologyAdmission",
    "PI-PKG",
    "PD-PKG",
    "TraceLink",
    "TaskSpecSeed",
    "ConstructionContract",
    "WorkOrderCandidate",
    "ECP",
    "TQAEP",
    "ExecutionHandoff",
    "EvidenceExpectation",
    "ClaimCeiling",
    "SurfaceProjectionManifest",
    "GENIEProjectionRef",
    "ExecutionBindingRef"
  ],
  "installed_files": [
    "ArtifactIdentity.schema.json",
    "AuthorityBinding.schema.json",
    "ClaimCeiling.schema.json",
    "ConstructionContract.schema.json",
    "ECP.schema.json",
    "EvidenceExpectation.schema.json",
    "ExecutionBindingRef.schema.json",
    "ExecutionHandoff.schema.json",
    "GENIEProjectionRef.schema.json",
    "PD-PKG.schema.json",
    "PI-PKG.schema.json",
    "ProfileBinding.schema.json",
    "RequirementAtom.schema.json",
    "SurfaceProjectionManifest.schema.json",
    "TQAEP.schema.json",
    "TaskSpecSeed.schema.json",
    "TechnologyAdmission.schema.json",
    "TraceLink.schema.json",
    "WorkOrderCandidate.schema.json",
    "registry.json"
  ],
  "installed_per_file_sha256": {
    "ArtifactIdentity.schema.json": "d747387f45e52647edebc7f5487304e6465626998b0597356936a9ffa45920ea",
    "AuthorityBinding.schema.json": "245d33ffb2578a4b00c982f73e768959a00c5d71aa73a44fe94fcae2258470ca",
    "ClaimCeiling.schema.json": "1f02f4fce359cb4fa7615c592601e936ebe9a1afc80b128e9d5c8b6601acec0d",
    "ConstructionContract.schema.json": "d40bc15d09e9694a3a778f8d9e7fd512779b65bfde391a0421ef97f50683c28e",
    "ECP.schema.json": "33688671e6eec18229e3da35a210f0c88799d4e21c5378d0518cd1e4213c7331",
    "EvidenceExpectation.schema.json": "b975375b59ae151b6b5740bb0069a5c8441b3a7e0acc94cf5404fa15ce5068e7",
    "ExecutionBindingRef.schema.json": "3372a5ce1fbbc510372e01e59eec41e13abfd496f0812c39f2a176a02b8c9ae4",
    "ExecutionHandoff.schema.json": "2a96e0d2ce33974beb4d27dd61386cd6b809cc3dd63c6dffebc17d581e641d3a",
    "GENIEProjectionRef.schema.json": "df0b6303bb5f02a489c3b7bbfcb97dabcb05f5834323f24e0b9a3cfe6613d41f",
    "PD-PKG.schema.json": "c6571cc959b1da3d28e74e03c639d80442f62eccc4940ff24e0126499143c445",
    "PI-PKG.schema.json": "ee9b0f8bf7d64fc74b979ddb785f6a739783b45c4deaee81172e9e29a22fce77",
    "ProfileBinding.schema.json": "63798436312fee6a814a1ade64380d3a36646fecea1a0bac07f77a095ee8739d",
    "registry.json": "08412b561b6804198a627b8f00893436fce2d562fb2cd29ffa050146062334ed",
    "RequirementAtom.schema.json": "3394c61dd771ed62a2741ef48e779a7811f7c190101a45d7ebf77eea22ec5541",
    "SurfaceProjectionManifest.schema.json": "acca81b498b787f8279f0981847ed7d13e19ca559c750aa593c99ff9b0c4abc3",
    "TaskSpecSeed.schema.json": "0230171cb7f72dccd5b081d00ce079b6ef9f456bcf614388f4e2acb71140940c",
    "TechnologyAdmission.schema.json": "098be650cce90ed956c9b5224f6907fa7081f57d162819c0cb5c7b3dcec4008e",
    "TQAEP.schema.json": "1e704b3f9942bdbe15cdfc9b1be9baf8880ac39841ef91fd7ddf2084eb0a9fa6",
    "TraceLink.schema.json": "7bd3ab0ff4ed2c3eb8750530dcbabd8a7f0a08b2febe48fbb230cdd21139faaa",
    "WorkOrderCandidate.schema.json": "9cedabd6038862c014641c20714dab086b9b535165c515326b7db9c56b690788"
  },
  "checks": {
    "installed_names_equal_expected_set_and_order": false,
    "installed_count_equal_expected": false,
    "installed_names_are_unique": true,
    "installed_every_family_has_required_fields": true,
    "installed_files_identical_to_tree": false
  },
  "only_in_installed": [],
  "only_in_tree": []
}
```

The negative control is the point: the same tool, the same expectations, and an altered registry turns
the verdict to `FAIL` on name/order equality, count equality and file identity. A receipt nobody can
falsify is not a receipt.

## The enforcement this receipt exercises, verbatim from the product

```python
def load_registry(schemas_dir: Path | None = None) -> dict[str, Any]:
    d = schemas_dir or _resolve_schemas_dir()
    reg_path = d / "registry.json"
    if not reg_path.is_file():
        raise ValidationFail(f"registry missing: {reg_path}")
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    fams = data.get("families") or []
    if len(fams) != EXPECTED_FAMILIES:
        raise ValidationFail(f"registry family count {len(fams)} != {EXPECTED_FAMILIES}")
    names = [f["contract"] for f in fams]
    if names != SOURCE_ORDER:
        raise ValidationFail("registry family order/name diverges from §7.3 exact set")
    for f in fams:
        if not (d / f"{f['contract']}.schema.json").is_file():
            raise ValidationFail(f"schema file missing for {f['contract']}")
        if not f.get("required_fields"):
            raise ValidationFail(f"{f['contract']} has no required_fields")
    return data
```

Note what this code already does, because it answers the lane's objection directly: `load_registry`
compares the registry's family list against the expected **count** and against the ordered **name
set** (`names != SOURCE_ORDER` -> `ValidationFail`), and then requires a schema file and a non-empty
`required_fields` for every family. A silently reduced registry that preserves the count therefore
still fails closed on the name comparison - which is exactly the distinction the lane said a count
alone could not make.

## Executor's ceiling

This attests the registry surface of one wheel built from the Stage A tree named above, as installed
and read on this host. It is not an acceptance, not a release artefact, and not a verification-lane
verdict.


=== BLOCK 2: F006_RED_GREEN_RECEIPTS.txt (full) ===
S4R3-F006: the standard build did not ship the contract registry.
Every block below is the tail of a file that the named command wrote; nothing was retyped.

[red-before] source: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\pipd-s4r3-exec\red_build.log  sha256=cfc118c90d5304199a8c923d647483043c14778c1f9b7699553042dc463c534d
  produced by: git archive <frozen parent> -> `python -m build --wheel --no-isolation`
               -> wheel member listing -> clean-venv `pipd doctor`
copying build\lib\pipd_ls_sp\cli.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\errors.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\export_bundle.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\pipeline.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\profiles.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\projection.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\registry.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\repo_context.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\requirements.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\util.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\validate.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\workspace.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
copying build\lib\pipd_ls_sp\__init__.py -> build\bdist.win-amd64\wheel\.\pipd_ls_sp
running install_egg_info
Copying src\pipd_ls_sp.egg-info to build\bdist.win-amd64\wheel\.\pipd_ls_sp-0.1.1a3-py3.11.egg-info
running install_scripts
creating build\bdist.win-amd64\wheel\pipd_ls_sp-0.1.1a3.dist-info\WHEEL
creating 'C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\pipd-s4r3-exec\\redout\\.tmp-5xi7y16g\\pipd_ls_sp-0.1.1a3-py3-none-any.whl' and adding 'build\\bdist.win-amd64\\wheel' to it
adding 'pipd_ls_sp/__init__.py'
adding 'pipd_ls_sp/cli.py'
adding 'pipd_ls_sp/errors.py'
adding 'pipd_ls_sp/export_bundle.py'
adding 'pipd_ls_sp/pipeline.py'
adding 'pipd_ls_sp/profiles.py'
adding 'pipd_ls_sp/projection.py'
adding 'pipd_ls_sp/registry.py'
adding 'pipd_ls_sp/repo_context.py'
adding 'pipd_ls_sp/requirements.py'
adding 'pipd_ls_sp/util.py'
adding 'pipd_ls_sp/validate.py'
adding 'pipd_ls_sp/workspace.py'
adding 'pipd_ls_sp-0.1.1a3.dist-info/licenses/LICENSE'
adding 'pipd_ls_sp-0.1.1a3.dist-info/licenses/NOTICE'
adding 'pipd_ls_sp-0.1.1a3.dist-info/METADATA'
adding 'pipd_ls_sp-0.1.1a3.dist-info/WHEEL'
adding 'pipd_ls_sp-0.1.1a3.dist-info/entry_points.txt'
adding 'pipd_ls_sp-0.1.1a3.dist-info/top_level.txt'
adding 'pipd_ls_sp-0.1.1a3.dist-info/RECORD'
removing build\bdist.win-amd64\wheel
Successfully built pipd_ls_sp-0.1.1a3-py3-none-any.whl

[green-after] source: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\pipd-s4r3-exec\f006_gate_tests.log  sha256=c807a717cb90b8d92248e67f797b08378104a64c944d7cd7c77670c54bbf100c
  produced by: `python -m unittest tests.test_standard_wheel_schemas -v`
test_mirror_refuses_a_missing_registry (tests.test_standard_wheel_schemas.MirrorHelperTests.test_mirror_refuses_a_missing_registry) ... ok
test_mirror_refuses_a_registry_naming_an_absent_schema (tests.test_standard_wheel_schemas.MirrorHelperTests.test_mirror_refuses_a_registry_naming_an_absent_schema) ... ok
test_mirror_refuses_an_undeclared_schema_file (tests.test_standard_wheel_schemas.MirrorHelperTests.test_mirror_refuses_an_undeclared_schema_file) ... ok
test_mirror_reproduces_the_registry_byte_for_byte (tests.test_standard_wheel_schemas.MirrorHelperTests.test_mirror_reproduces_the_registry_byte_for_byte) ... ok
test_negative_control_without_the_hook_the_wheel_cannot_resolve_its_registry (tests.test_standard_wheel_schemas.StandardBuildTests.test_negative_control_without_the_hook_the_wheel_cannot_resolve_its_registry)
If the hook is dropped the surface must degrade -- otherwise this module proves nothing. ... ok
test_wheel_ships_the_registry_and_resolves_it_when_installed (tests.test_standard_wheel_schemas.StandardBuildTests.test_wheel_ships_the_registry_and_resolves_it_when_installed) ... ok

----------------------------------------------------------------------
Ran 13 tests in 8.123s

OK

[sdist route] source: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\pipd-s4r3-exec\sdist_to_wheel.json  sha256=12b56318a7bad4d5f75a281a32ee1a28374230b4368d80b3d5a73b6d476c5f07
{
  "sdist_build_rc": 0,
  "sdist": "pipd_ls_sp-0.1.1a3.tar.gz",
  "sdist_schema_members": 20,
  "extracted_root": "pipd_ls_sp-0.1.1a3",
  "wheel_from_sdist_rc": 0,
  "wheel_from_sdist": "pipd_ls_sp-0.1.1a3-py3-none-any.whl",
  "install_rc": 0,
  "doctor_exit_code": 0,
  "doctor_verdict": "PASS",
  "doctor_mode": "INSTALLED",
  "doctor_families": 19
}

A LATER, FAILED RE-ATTEMPT AT THE SAME ROUTE, kept because it consumed round time and because a reader
who finds the empty `sdisttest/ext` directory should not have to guess why. This attempt drove the
extraction with the shell's `tar` instead of the Python path the receipt above used:

  command (abridged): tar -xzf "$SCR/sdisttest/sdist/pipd_ls_sp-0.1.1a3.tar.gz"
  output:
    tar (child): Cannot connect to C: resolve failed
    gzip: stdin: unexpected end of file
    tar: Child returned status 128
    tar: Error is not recoverable: exiting now
  consequence: no wheel was built from the sdist in that attempt, so `sdisttest/ext` is empty and the
  two log paths that attempt referenced were never created.

  reading, stated plainly: MSYS `tar` parses the drive letter in `C:/...` as a REMOTE HOST
  (`host:path`), so it tried to reach a host named `C`. This is a defect in the shell invocation, not
  in the artefact and not in the earlier receipt: the receipt above was produced by
  `verify_sdist_to_wheel.py`, which uses Python's own tarfile/stdlib path handling and needs no
  path translation. The sdist route therefore REMAINS verified by the receipt above; the failed
  re-attempt adds no evidence either way and is recorded only so the empty directory is explained.



=== BLOCK 3: extracted lines from CI_RUNS_AND_STEP_RECEIPTS.txt (the hosted-run lines carrying
mode=INSTALLED and doctor output) ===
      | installed-wheel contract registry: mode=INSTALLED families=19 path=/home/runner/work/_temp/wheelvenv/lib/python3.11/site-packages/pipd_ls_sp/schemas
      | installed-wheel contract registry: mode=INSTALLED families=19 path=/home/runner/work/_temp/wheelvenv/lib/python3.11/site-packages/pipd_ls_sp/schemas
      | installed-wheel contract registry: mode=INSTALLED families=19 path=/home/runner/work/_temp/wheelvenv/lib/python3.11/site-packages/pipd_ls_sp/schemas
      | installed-wheel contract registry: mode=INSTALLED families=19 path=/home/runner/work/_temp/wheelvenv/lib/python3.11/site-packages/pipd_ls_sp/schemas
