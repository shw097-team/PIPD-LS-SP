You are an INDEPENDENT CHECKER (VERIFY) for the governed PIPD-LS-SP round. You are not the maker.
Assume every claim below is FALSE until your own command proves it.

CANDIDATE
  repo: C:\Projects\Agent_Workspace\PIPD
  commit: READ IT YOURSELF: `git -C C:/Projects/Agent_Workspace/PIPD rev-parse HEAD` and also read
         C:/Users/user/AppData/Local/Temp/pipd-edge-verify/FROZEN_CANDIDATE.txt . They MUST be equal.
         If they differ, report the mismatch as a finding and stop.

HARD RULES
 1. READ-ONLY. Do not create, edit, delete or move any file inside the repo, the knowledge base or HG-KSEOS.
    Write scratch files only under C:\Users\user\AppData\Local\Temp\pipd-edge-verify\ .
 2. Do not run git commit/add/push. Do not modify the kanban board or the spine.
 3. Shell is bash (git-bash/MSYS). `python` has jsonschema 4.x. Run tests with cwd = the repo root.
 4. Report a check as NOT_REPRODUCED rather than guessing if you cannot run it.

RE-VERIFY EXACTLY THESE EDGES (a previous independent round FAILED the prior candidate and these
are the repairs that must now be proven). For each: run the probe, quote the decisive raw output.

 E1  cd <repo> && python -m unittest discover -s tests -t .   -> must end OK; report the exact test count.
 E2  Copy the repo WITHOUT .git to a scratch dir; run the suite there. The rollback test must SKIP
     (not pass, not fail); the suite must still end OK.
 E3  python -c "import sys;sys.path.insert(0,'src');from pipd_ls_sp import validate;print(validate.validate_bundle({}))"
     -> must be FAIL with a finding whose kind is DENOMINATOR.
 E4  Forged record: build {"subject_id":"","version":"","content_hash":"not-a-hash","schema_version":"Anything@1"}
     and call validate.semantic_invariants("PI-PKG", ...). Must return a NON-EMPTY finding list.
 E5  Body tamper: read .hgk/artifacts/s1/pi_pkg.json, change one value INSIDE stable_semantic_contract without
     touching content_hash, and confirm semantic_invariants now reports a body-hash mismatch.
 E6  SoD: (a) pipeline.compile_tqaep(..., maker='M', checker='m ') must RAISE.
                (b) pipeline.compile_tqaep(..., maker='M', checker='C', checker_execution_receipt='SELF_ATTESTED')
                    must RAISE.
                (c) with maker='M', checker='C', checker_execution_receipt='lane-X' it must SUCCEED and
                    tqaep["acceptance"][0] must carry case/maker_identity/checker_identity/distinct/checker_execution_receipt.
     Build the minimal pi/ecp inputs yourself.
 E7  workspace.repair_candidate with scope ['**'], then ['C:/Projects/Agent_Workspace/HG-KSEOS/**'], then
     ['../HG-KSEOS/**'], then WITHOUT authorized_root -> all four must RAISE. Then scope ['src/**'] with
     authorized_root=<repo root> must SUCCEED.
 E8  validate.semantic_invariants("ClaimCeiling", {"subject_id":"CCL-0000000000000000","version":"1",
     "content_hash":"a"*64,"schema_version":"ClaimCeiling@1","allowed_claims":["INDEPENDENT_PASS"],
     "forbidden_escalation":[]}) must return a finding (a bare ceiling may not allow a level above LOCAL_QUALIFIED).
 E9  Build the string 'github_pat_' + 'A'*30 IN MEMORY ONLY and confirm at least one compiled pattern in
     pipd_ls_sp.workspace.SECRET_PATTERNS matches it.
 E10 LF canonicalization (was FAILING before this freeze; the fix re-froze the compile receipts): `git stash list` empty; `git status --porcelain` shows no line-ending churn.
     Compare the sha256 of the COMMITTED BLOB of .hgk/preflight/compile_out/compiler-receipt.json's
     contract_sha256 field against the sha256 of the COMMITTED BLOB of
     .hgk/preflight/PIPD-LS-SP.CONTRACT.json (use `git show HEAD:<path>` piped to sha256sum, not the worktree).
 E11 Re-run the trace closure over the committed .hgk/artifacts/s1/*.json bundle and confirm
     orphans == [] AND bad_hashes == [] and verdict == PASS.
 E12 Secret sweep: the six patterns (github_pat_[A-Za-z0-9_]{20,}, gh[pousr]_[A-Za-z0-9]{20,},
     sk-[A-Za-z0-9]{20,}, AKIA[0-9A-Z]{16}, -----BEGIN [A-Z ]*PRIVATE KEY-----, bearer literal)
     against every file in the worktree AND against `git rev-list --objects --all | git cat-file --batch`.
     Report counts. Any hit is a FAIL.

OUTPUT — exactly one JSON object, nothing else:
{
 "lane": "edge-reverify-glm",
 "checker_identity": "glm-5.3-flash/opencode-go",
 "candidate": "<actual HEAD sha>",
 "edges": [{"edge":"E1","verdict":"PASS|FAIL|NOT_REPRODUCED","command":"<raw command>","observed":"<decisive output>"}],
 "regressions": ["..."],
 "verdict": "PASS|FAIL",
 "notes": "one short paragraph"
}
