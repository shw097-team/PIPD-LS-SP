# Independent Acceptance Officer — Stage B, Round 3

Date: October 12, 2026 (Asia/Taipei). Two independent adjudications; neither conclusion is used as evidence for the other.

- **VERDICT A: NOT_CLOSED** — the delivered worktree is nonempty even after excluding this officer's own permitted evidence.
- **VERDICT B: ACCEPT_WITH_CONDITIONS** — the reviewed local Stage-B artifacts survive the specified deterministic/collision attacks, but additional probes expose ungated official-manifest identity drift and acceptance of an unreviewed extension. The conditions below bound this acceptance; they are not represented as already satisfied.

## Independently Resolved Subject

Repository: shw097-team/PIPD-LS-SP. Delivery: C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt.

HEAD: **38f413158dc59f78d5c603fc6e82a8c6449c775f**.
Tree: **9ebf378082e29c048195e6fb69740fba351fd89f**.
Remote refs/heads/feat/s4post-triple-upgrade-20261012-r2: **38f413158dc59f78d5c603fc6e82a8c6449c775f**.
The checked-out local branch is feat/s4post-triple-upgrade-20261012, without -r2. Commit equality, not the local branch spelling, identifies this subject.

Exact commands, real exits, and raw readbacks:

```text
COMMAND: git rev-parse HEAD
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
38f413158dc59f78d5c603fc6e82a8c6449c775f
```

```text
COMMAND: git rev-parse HEAD^{tree}
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
9ebf378082e29c048195e6fb69740fba351fd89f
```

```text
COMMAND: git branch --show-current
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
feat/s4post-triple-upgrade-20261012
```

```text
COMMAND: git -c credential.helper= -c core.askPass= -c http.extraHeader= ls-remote https://github.com/shw097-team/PIPD-LS-SP.git refs/heads/feat/s4post-triple-upgrade-20261012-r2
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808
EXIT_CODE: 0
RAW OUTPUT:
38f413158dc59f78d5c603fc6e82a8c6449c775f	refs/heads/feat/s4post-triple-upgrade-20261012-r2
```

Remote readback ran outside any repository with GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=nul, GIT_TERMINAL_PROMPT=0, empty GIT_ASKPASS/SSH_ASKPASS, and inherited GIT_CONFIG_* removed. The command additionally empties credential.helper, core.askPass and http.extraHeader. These environment settings are implemented in audit.py; no credential or authenticated GitHub connector was used.

An external snapshot was made with git clone --no-hardlinks --no-checkout, followed by git checkout --detach at the independently read HEAD. No test suite ran against the dirty delivery. Snapshot commands and initial clean status:

```text
COMMAND: git clone --no-hardlinks --no-checkout C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808
EXIT_CODE: 0
RAW OUTPUT:
Cloning into 'C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate'...
done.
```

```text
COMMAND: git checkout --detach 38f413158dc59f78d5c603fc6e82a8c6449c775f
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 0
RAW OUTPUT:
HEAD is now at 38f4131 evidence(s4post-b): record the round-2 independent acceptance outcome
```

```text
COMMAND: git status --porcelain
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 0
RAW OUTPUT:
```

The snapshot and all attack fixtures are under the system temporary directory, as explicitly required. Repository writes are confined to this report's ao3 directory; no candidate commit, branch, index, tracked file, remote or publication was changed. Snapshot-end-identity.txt and delivery-end-identity.txt both re-read the same HEAD/tree after testing. The temporary snapshot is retained to make the reproducers usable.

Evidence paths in this document are relative to **.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/** unless an absolute path is shown. Each substantive command log records COMMAND, CWD, EXIT_CODE and RAW OUTPUT. audit.py, probes.py, evidence.py, supplement.py, counts.py and repro_identity.py retain the exact methods. Early PowerShell exploration logs are supplementary, not relied on to establish per-command exits; the later subprocess logs supply those exits.

## ADJUDICATION A

### Verdict: NOT_CLOSED

Smallest reproducer: **git status --porcelain** in the delivered worktree. Its exit 0 means the query succeeded, not that its nonempty output is clean. Ignoring every path under this officer's verify/ao3/ still leaves the stage-b launcher, brief and lane artifacts below.

The first terminal observation, before evidence-directory creation, already showed AO3_20261012T115506Z.log, FAR_BRIEF_MODEL_DEVIATION.md, VERIFIER_AO3_BRIEF.md and run_ao3_lane.sh untracked. The auditable subprocess observation below also found FAR lane artifacts. There is no attribution of their creation to the candidate code or maker. Concurrent orchestration may have created them after an earlier clean readback; these observations do **not** establish that the worktree was never temporarily clean. They do falsify the clean delivery presented for this engagement.

```text
COMMAND: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO3_20261012T115506Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T115535Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_BRIEF_MODEL_DEVIATION.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO3_BRIEF.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao3_lane.sh
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_far_lane.sh
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/
```

Final observation:

```text
COMMAND: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO3_20261012T115506Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T115535Z.exit
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_20261012T115535Z.log
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/FAR_BRIEF_MODEL_DEVIATION.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO3_BRIEF.md
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao3_lane.sh
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_far_lane.sh
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/
```

Tracked and index drift queries both exit 0 with empty raw output: delivery-tracked-diff.txt and delivery-index-diff.txt. This is a delivered-state hygiene finding, not tracked-code drift.

### Closing commits and complete path sets

The round-2 verdict stored in verify/ao2 identifies subject 07681745a436a7d82e85a0aa494d8165acad92a0. I resolved its existence/history with Git rather than accepting that text as an identity authority. Two commits follow it, in linear parent order. **Every path in both commits is under .hgk/rounds/**; no code-path change was found. A path outside that prefix would have invalidated the evidence-only closure claim; none is present.

Complete command output (not an abbreviated path list):

```text
COMMAND: git log --reverse "--format=commit %H%nparents %P%nsubject %s" --name-status 07681745a436a7d82e85a0aa494d8165acad92a0..38f413158dc59f78d5c603fc6e82a8c6449c775f
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
commit 4807c111b6077fbe8f82d9edf1abc62a797f079d
parents 07681745a436a7d82e85a0aa494d8165acad92a0
subject chore(s4post-b): close the round-2 AO-02 handover-hygiene finding

A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/AO2_HANDOVER_CLOSURE.md
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/evidence/09_RELEASE/PUSH_CREDENTIAL_INCIDENT.md
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO2_20261012T112125Z.exit
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO2_20261012T112125Z.log
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/VERIFIER_AO2_BRIEF.md
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_ao2_lane.sh
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/AO_VERDICT_STAGEB_R2.md
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_anonymous_remote_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_final_identity_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/A_identity.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_artifact.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_control.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_mapping.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_receipt.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_sidecar.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_current_tool_raw.py
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_artifact.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_control.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_mapping.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_receipt.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre-fix_sidecar.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/B_pre_fix_extraction.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_candidate.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_dist.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_docs.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_guard_exact.sh
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_missing.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_restore.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_unresolved.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/C_workflow_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_committed_evidence.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_final_status.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/D_integrity_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_copy_and_denominators.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_focused_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/E_full_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/F_claims_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/F_return_pack_raw.json
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/LOCATION_NOTE.md
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/audit_driver_raw.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/results.json
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/run_audit.py
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/scratch_path.txt
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/uat/hermes/HOST_UAT_HERMES.md
commit 38f413158dc59f78d5c603fc6e82a8c6449c775f
parents 4807c111b6077fbe8f82d9edf1abc62a797f079d
subject evidence(s4post-b): record the round-2 independent acceptance outcome

A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/AO2_RESULT.md
```

An independent git diff --exit-code from that subject to HEAD excluding .hgk/rounds/** also returns 0; see code-unchanged-since-r2.txt. The ancestor check returns 0:

```text
COMMAND: git merge-base --is-ancestor 07681745a436a7d82e85a0aa494d8165acad92a0 38f413158dc59f78d5c603fc6e82a8c6449c775f
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
RAW OUTPUT:
```

This proves preservation of the round-2 subject in this history and the evidence-only delta, not an absence of every possible unrelated rewrite elsewhere. Anonymous remote equality is independently recorded in the header.

### Relocated evidence: count, hashes, authorship boundary

Recomputed count: **37 files total; 36 excluding LOCATION_NOTE.md**. The note is a separate named file and explicitly presents a relocation explanation. It is separable from the 36-file officer set for inventory and hashing; filename/commit inclusion alone does not authenticate human authorship of any file.

All 37 current snapshot file hashes match their bytes in the first closing commit 4807c111b6077fbe8f82d9edf1abc62a797f079d. Full per-file SHA-256 evidence follows:

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "from pathlib import Path; import hashlib,subprocess,sys,json; root=Path(sys.argv[1]); rows=[]; files=sorted(p for p in root.iterdir() if p.is_file()); print(\"COUNT\",len(files)); print(\"OFFICER_COUNT_EXCLUDING_LOCATION_NOTE\",len([p for p in files if p.name!=\"LOCATION_NOTE.md\"])); [(rows.append({\"name\":p.name,\"current_sha256\":hashlib.sha256(p.read_bytes()).hexdigest(),\"first_commit_sha256\":hashlib.sha256(subprocess.check_output([\"git\",\"show\",\"4807c111b6077fbe8f82d9edf1abc62a797f079d:\"+p.as_posix()])).hexdigest()})) for p in files]; print(json.dumps(rows,indent=2)); print(\"CURRENT_EQUALS_FIRST_COMMIT\",all(row[\"current_sha256\"]==row[\"first_commit_sha256\"] for row in rows)); print(\"This compares after-relocation states; no independently retained pre-move bytes are present here.\")" .hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\ao2
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 0
RAW OUTPUT:
COUNT 37
OFFICER_COUNT_EXCLUDING_LOCATION_NOTE 36
[
  {
    "name": "A_anonymous_remote_raw.txt",
    "current_sha256": "fc0a743e6e59bff6029dcce6b879aafc6a76505efc8acb16e43d6bb1fae03066",
    "first_commit_sha256": "fc0a743e6e59bff6029dcce6b879aafc6a76505efc8acb16e43d6bb1fae03066"
  },
  {
    "name": "A_final_identity_raw.txt",
    "current_sha256": "3bd818e1097fd6f59bcf16a7ddbcbc00202a0a8b40ef218f1248b23ce5fabe1b",
    "first_commit_sha256": "3bd818e1097fd6f59bcf16a7ddbcbc00202a0a8b40ef218f1248b23ce5fabe1b"
  },
  {
    "name": "A_identity.txt",
    "current_sha256": "87f1a9e7a235c3296c37e126208dc9645aeb555b383a75436a98c04580c80d59",
    "first_commit_sha256": "87f1a9e7a235c3296c37e126208dc9645aeb555b383a75436a98c04580c80d59"
  },
  {
    "name": "AO_VERDICT_STAGEB_R2.md",
    "current_sha256": "f3451d99a79edfc1e3ba1490dd311da400dada5681ddb0a81c13168f48e36026",
    "first_commit_sha256": "f3451d99a79edfc1e3ba1490dd311da400dada5681ddb0a81c13168f48e36026"
  },
  {
    "name": "audit_driver_raw.txt",
    "current_sha256": "8d57e606a0e6c72c187bb0004be66e14c7c44f72969cbc94de8781b86b49f04e",
    "first_commit_sha256": "8d57e606a0e6c72c187bb0004be66e14c7c44f72969cbc94de8781b86b49f04e"
  },
  {
    "name": "B_current_artifact.txt",
    "current_sha256": "f91eb6ea2b5b83633cdc77ba216a76c2b0dda8d28b1bd3fb0079d5691ae88e6d",
    "first_commit_sha256": "f91eb6ea2b5b83633cdc77ba216a76c2b0dda8d28b1bd3fb0079d5691ae88e6d"
  },
  {
    "name": "B_current_control.txt",
    "current_sha256": "b4ebcc06a4640bec0c359f1107a3e5c9f3efe3aa85fd1967511fe97b39a60b26",
    "first_commit_sha256": "b4ebcc06a4640bec0c359f1107a3e5c9f3efe3aa85fd1967511fe97b39a60b26"
  },
  {
    "name": "B_current_mapping.txt",
    "current_sha256": "f2b201db7963e872af3089932fe8757ab8da3768be013367ce663bfb64cce0ee",
    "first_commit_sha256": "f2b201db7963e872af3089932fe8757ab8da3768be013367ce663bfb64cce0ee"
  },
  {
    "name": "B_current_receipt.txt",
    "current_sha256": "d19fe5edfffd50bef964beab62ab2225870e51fc6739624f0aff4b7f256aaa99",
    "first_commit_sha256": "d19fe5edfffd50bef964beab62ab2225870e51fc6739624f0aff4b7f256aaa99"
  },
  {
    "name": "B_current_sidecar.txt",
    "current_sha256": "8ed947e253eef5f801e62d3385af23ac1d19f9863a5aa09ee151e75a7adf08fd",
    "first_commit_sha256": "8ed947e253eef5f801e62d3385af23ac1d19f9863a5aa09ee151e75a7adf08fd"
  },
  {
    "name": "B_current_tool_raw.py",
    "current_sha256": "f8de6b75f7790fa90528d51d45911258ecc92525a15464dd578b1f2d2e0b574f",
    "first_commit_sha256": "f8de6b75f7790fa90528d51d45911258ecc92525a15464dd578b1f2d2e0b574f"
  },
  {
    "name": "B_pre-fix_artifact.txt",
    "current_sha256": "33843e0975677ace6c27825b30ce5eb3434fe7a94469b4540f5acabb0255b4b5",
    "first_commit_sha256": "33843e0975677ace6c27825b30ce5eb3434fe7a94469b4540f5acabb0255b4b5"
  },
  {
    "name": "B_pre-fix_control.txt",
    "current_sha256": "28404ab5f093e367f2da15b29f451bfd27b32f84f0f95b37742176e4df6d2905",
    "first_commit_sha256": "28404ab5f093e367f2da15b29f451bfd27b32f84f0f95b37742176e4df6d2905"
  },
  {
    "name": "B_pre-fix_mapping.txt",
    "current_sha256": "be25d9c3964097a2e64f07d1aacdbeff84a9ddc811d55e7423f93920870dfc71",
    "first_commit_sha256": "be25d9c3964097a2e64f07d1aacdbeff84a9ddc811d55e7423f93920870dfc71"
  },
  {
    "name": "B_pre-fix_receipt.txt",
    "current_sha256": "e7639b6f391543185aefcb8e5572ab53646dac02e91b8c20c6abeca2b4753050",
    "first_commit_sha256": "e7639b6f391543185aefcb8e5572ab53646dac02e91b8c20c6abeca2b4753050"
  },
  {
    "name": "B_pre-fix_sidecar.txt",
    "current_sha256": "effe2f10a7df4d070215295ed216655471d33203bcb155460ac1c106dd82eb80",
    "first_commit_sha256": "effe2f10a7df4d070215295ed216655471d33203bcb155460ac1c106dd82eb80"
  },
  {
    "name": "B_pre_fix_extraction.txt",
    "current_sha256": "375cf3b1b88e23a150d44d849bc4d0f7b6aa2fcd9331ecef12dcb44427508f49",
    "first_commit_sha256": "375cf3b1b88e23a150d44d849bc4d0f7b6aa2fcd9331ecef12dcb44427508f49"
  },
  {
    "name": "C_candidate.txt",
    "current_sha256": "d6a8812a517d835619b4d239ec0124ffd3def3cef563a34ff9ceb7e01a2bdf7a",
    "first_commit_sha256": "d6a8812a517d835619b4d239ec0124ffd3def3cef563a34ff9ceb7e01a2bdf7a"
  },
  {
    "name": "C_dist.txt",
    "current_sha256": "3cd1449017596aeb4bdaa27dba1634b458b1eff6c4d6ed3ddddf3634648fc60f",
    "first_commit_sha256": "3cd1449017596aeb4bdaa27dba1634b458b1eff6c4d6ed3ddddf3634648fc60f"
  },
  {
    "name": "C_docs.txt",
    "current_sha256": "903ec384fb62fbd13b6136d824b5112e5808cb54c631fc04c855b724ca742100",
    "first_commit_sha256": "903ec384fb62fbd13b6136d824b5112e5808cb54c631fc04c855b724ca742100"
  },
  {
    "name": "C_guard_exact.sh",
    "current_sha256": "3dec2f59d4347d80252e411d05bc20a95af912a46b97e73c01c8a38d48e49250",
    "first_commit_sha256": "3dec2f59d4347d80252e411d05bc20a95af912a46b97e73c01c8a38d48e49250"
  },
  {
    "name": "C_missing.txt",
    "current_sha256": "9de9021738189745e5d7b977245c433dfbc7e2b112883341515c3abdeeaef972",
    "first_commit_sha256": "9de9021738189745e5d7b977245c433dfbc7e2b112883341515c3abdeeaef972"
  },
  {
    "name": "C_restore.txt",
    "current_sha256": "0b9a08e123f5906c3831bb55a00c2615a0c8be69e60428b27a9a262a2b644d38",
    "first_commit_sha256": "0b9a08e123f5906c3831bb55a00c2615a0c8be69e60428b27a9a262a2b644d38"
  },
  {
    "name": "C_unresolved.txt",
    "current_sha256": "bcac65854a33135aea6939bc338a35b630c9ae3c822a5508c1bc974090b2f39b",
    "first_commit_sha256": "bcac65854a33135aea6939bc338a35b630c9ae3c822a5508c1bc974090b2f39b"
  },
  {
    "name": "C_workflow_raw.txt",
    "current_sha256": "ed21de9d8a5ad384ffd6fed3fe757480c5c42fbf6fb7f544afbced3524205f29",
    "first_commit_sha256": "ed21de9d8a5ad384ffd6fed3fe757480c5c42fbf6fb7f544afbced3524205f29"
  },
  {
    "name": "D_committed_evidence.txt",
    "current_sha256": "8af2b99d2c613ce27a466a1c0e7a939bde7d02f3a23c25f2805556f0fe221aa1",
    "first_commit_sha256": "8af2b99d2c613ce27a466a1c0e7a939bde7d02f3a23c25f2805556f0fe221aa1"
  },
  {
    "name": "D_final_status.txt",
    "current_sha256": "5aa94c9befcec3df2d8211bdb8003cdfe7717fe700d33af665ca81235cc056ce",
    "first_commit_sha256": "5aa94c9befcec3df2d8211bdb8003cdfe7717fe700d33af665ca81235cc056ce"
  },
  {
    "name": "D_integrity_raw.txt",
    "current_sha256": "74afde4d3eeccd9e8318ef095793f16c0a2de991057a2722feb361686779e52d",
    "first_commit_sha256": "74afde4d3eeccd9e8318ef095793f16c0a2de991057a2722feb361686779e52d"
  },
  {
    "name": "E_copy_and_denominators.txt",
    "current_sha256": "49a3f465f30d408b3d42969ad802d5cc3b74c2b183f9472a91dc321148d87f79",
    "first_commit_sha256": "49a3f465f30d408b3d42969ad802d5cc3b74c2b183f9472a91dc321148d87f79"
  },
  {
    "name": "E_focused_raw.txt",
    "current_sha256": "34a70c81c6707c6006077dd680b5714226b05afa918acdffaf7899339d97bab2",
    "first_commit_sha256": "34a70c81c6707c6006077dd680b5714226b05afa918acdffaf7899339d97bab2"
  },
  {
    "name": "E_full_raw.txt",
    "current_sha256": "eb1b0efdc7f0507e118b3616ccaa88175a37523ff7da4a8f58b58ecf8f28f9d4",
    "first_commit_sha256": "eb1b0efdc7f0507e118b3616ccaa88175a37523ff7da4a8f58b58ecf8f28f9d4"
  },
  {
    "name": "F_claims_raw.txt",
    "current_sha256": "b459395a9ea80c7fbef477b0ac662adc78d6a270b085d72981eb9a2e5e1414c9",
    "first_commit_sha256": "b459395a9ea80c7fbef477b0ac662adc78d6a270b085d72981eb9a2e5e1414c9"
  },
  {
    "name": "F_return_pack_raw.json",
    "current_sha256": "2e5a1d19e80ba8759c07c6d1e4b085d3d3ebf67988f1e269965b0266adcfbbe9",
    "first_commit_sha256": "2e5a1d19e80ba8759c07c6d1e4b085d3d3ebf67988f1e269965b0266adcfbbe9"
  },
  {
    "name": "LOCATION_NOTE.md",
    "current_sha256": "badfe105984d1d3582a276916016b02b64eb21a9c024cdff1b22e22559d3c406",
    "first_commit_sha256": "badfe105984d1d3582a276916016b02b64eb21a9c024cdff1b22e22559d3c406"
  },
  {
    "name": "results.json",
    "current_sha256": "13b32baaf2d88cdac966c904dfe3d88cb200441bb949d9e1367553e193c2538c",
    "first_commit_sha256": "13b32baaf2d88cdac966c904dfe3d88cb200441bb949d9e1367553e193c2538c"
  },
  {
    "name": "run_audit.py",
    "current_sha256": "8235b63e778792bbedc3c93569f1ef51cb8b405374f93aea472b2b3b5e6a0d50",
    "first_commit_sha256": "8235b63e778792bbedc3c93569f1ef51cb8b405374f93aea472b2b3b5e6a0d50"
  },
  {
    "name": "scratch_path.txt",
    "current_sha256": "b448c1a7a1177674c8ba6e640c4974c35bf15beb7ce5ecbf0b2491f7f50b022e",
    "first_commit_sha256": "b448c1a7a1177674c8ba6e640c4974c35bf15beb7ce5ecbf0b2491f7f50b022e"
  }
]
CURRENT_EQUALS_FIRST_COMMIT True
This compares after-relocation states; no independently retained pre-move bytes are present here.
```

**Important limit:** these are two **post-relocation** states. The original root verify/ evidence is not tracked in the round-2 subject (original-root-tracked.txt: exit 0, empty output), and the delivery root verify/ is absent (original-root-status.txt: exit 0). I have no independently retained pre-move byte inventory. Thus the physical operation “moved rather than rewritten” and the maker's claimed before/after 36/36 equality remain **maker-asserted, not independently established**. My hash comparison cannot distinguish a byte-preserving move from rewriting the files before their first commit. LOCATION_NOTE.md and AO2_HANDOVER_CLOSURE.md are recorded verbatim in reviewed-source.txt; neither is promoted into proof of its own assertion.

All presently listed ao2 files are committed at HEAD: committed-ao2-paths.txt, exit 0. The closing path list includes the older lane artifacts and Hermes record; it does not cure the newer untracked handover artifacts reported above. “All remaining round artifacts committed” therefore does not hold for the current delivery.

### Exact write-set guard at current HEAD

I extracted the first workflow run body's set -euo pipefail block from the snapshot's .github/workflows/public-plugin-verify.yml, preserving its executable body, into guard-extracted.sh. I did not replace the guard with a reimplementation. It ran in the external detached snapshot with PR_BASE_SHA empty and STACKED_BASE_SHA=52542c395a0f91dc2ba4bd6123acd4cdecd780dc, the workflow's fixed Stage-A stacked base.

Exact body:

ao3/guard-extracted.sh is reproduced below:
```bash
set -euo pipefail
BASE="${PR_BASE_SHA:-${STACKED_BASE_SHA}}"
if ! git cat-file -e "${BASE}^{commit}" 2>/dev/null; then
  echo "BASE_UNRESOLVED: ${BASE} is not present in this checkout; refusing to guess" >&2
  exit 1
fi
git merge-base --is-ancestor "$BASE" HEAD
CHANGED="$(git diff --name-only "${BASE}...HEAD")"
printf '%s\n' "$CHANGED"
ALLOWED='^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012)'
DENIED='^(skills/|src/|schemas/|dist/)'
bad=0
while IFS= read -r path; do
  [ -n "$path" ] || continue
  if printf '%s' "$path" | grep -Eq "$DENIED"; then
    echo "UPGRADE_WROTE_FROZEN_PATH: $path" >&2
    bad=1
  elif ! printf '%s' "$path" | grep -Eq "$ALLOWED"; then
    echo "UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: $path" >&2
    bad=1
  fi
done <<< "$CHANGED"
if [ "$bad" -ne 0 ]; then
  echo "WRITE_SET_VIOLATION (base ${BASE})" >&2
  exit 1
fi
echo "WRITE_SET_CLEAN_AGAINST_${BASE}"
```

Current-HEAD execution exits **0**. Full changed-path output is in guard-current-head.txt; its terminal line is:

> WRITE_SET_CLEAN_AGAINST_52542c395a0f91dc2ba4bd6123acd4cdecd780dc

The command is the exact Bash invocation recorded in guard-current-head.txt. It is distinct from git status: a committed-diff allowlist does not promise a clean delivered worktree.

### A Claim Disposition

| Claim | Independent disposition | Evidence |
| --- | --- | --- |
| Relocation was a move and preserved pre-move bytes | NOT ESTABLISHED; post-move hashes/count verified only | ao2-hashes.txt; original-root-tracked.txt; original-root-status.txt |
| 36 officer files plus one separate note | Inventory confirmed; authorship is not cryptographically authenticated | ao2-hashes.txt; reviewed-source.txt |
| Remaining artifacts committed / delivery clean | FALSE for this delivery | delivery-status-before.txt; delivery-end-status.txt |
| Closing commits evidence-only | Confirmed for both complete path sets | closure-paths.txt; code-unchanged-since-r2.txt |
| Guard still passes at HEAD | Confirmed, exit 0 against fixed Stage-A base | guard-current-head.txt; guard-extracted.sh |
| Round-2 subject remains ancestor / remote equals HEAD | Confirmed, both Git commands exit 0 | ancestor.txt; anonymous-remote.txt |

## ADJUDICATION B

### Verdict: ACCEPT_WITH_CONDITIONS

This adjudication is based on a fresh detached snapshot, my own input fixtures, actual command exits and source inspection. It does **not** rely on trusting adjudication A or the round-2 officer's green results. The backup-label deviation by itself is not a reason to discard reproducibly correct bytes. However, the tests do not license a universal fail-closed claim: my additional accepted-mutant probes identify an untested boundary.

Acceptance means **the reviewed local Stage-B artifacts survive independent verification within the stated conditions**. It does **not** mean Portal approval, publication, host qualification or S4 acceptance. The delivery still refuses to produce its public plugin using the deliberately incomplete checked-in owner inputs.

#### Conditions

1. **Manifest identity/extension boundary must remain explicit.** Before any final owner-filled candidate is treated as release-ready, independently check that official plugin.json name equals release bookkeeping plugin_id, version equals the release/receipt version, and every extension namespace/value has actually been reviewed. The current builder does not enforce those checks. Preserve the exact reviewed manifest values for this Stage-B acceptance; do not extrapolate it to arbitrary operator-edited manifests. A future claim that the builder itself fail-closes these inputs requires gates plus negative regression tests and independent re-verification. My probes are retained; no repair was made.
2. **Retain the narrowed coverage claim.** Do not represent the full run as all 589 discovered tests passing, or as host/publication qualification. The stale-seal readback, real native symlink case, and 17 publication-projection cases remain unexercised. Re-execute the relevant gates in a suitable isolated environment before making those broader claims; do not create misleading substitute refs or reseal evidence just to erase skips in this review.
3. **Record the model deviation and unresolved attribution.** The declared rerun label is opencode-go/deepseek-v4-flash, not the originally declared opencode-go/deepseek-v4.1-flash. The logs do not authenticate the actual upstream model. Before public release, a reviewer must independently approve the substantive skill/projection decisions and final publisher inputs rather than treating the declared-lane label or synthetic approval fields as provenance/authorization.

These conditions do not require the originally declared model to rerun mechanically reproducible work. They restrict what is accepted and what must be reviewed before a broader release claim.

### Suites, Interpreter, CWD and Denominators

Primary interpreter and platform, verbatim:

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import sys,os,platform; print(sys.executable); print(sys.version); print(platform.platform()); print(os.getcwd()); print(\"O_NOFOLLOW\",hasattr(os,\"O_NOFOLLOW\")); print(\"O_NONBLOCK\",hasattr(os,\"O_NONBLOCK\"))"
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 0
RAW OUTPUT:
C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe
3.11.17 (main, Oct  3 2026, 01:03:09) [MSC v.1944 64 bit (AMD64)]
Windows-10-10.0.26200-SP0
C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
O_NOFOLLOW False
O_NONBLOCK False
```

All suites below run in C:/Users/user/AppData/Local/Temp/pipd-ao3-d2_pq808/candidate, not the delivery.

| Run | Command | Reported run count | Successes | Actual individual test skips | Module skip | Exit |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Focused | python -m unittest -v tests.test_public_plugin_packaging tests.test_web_fallback tests.test_s4ext_release_provenance | 65 | 65 | 0 | 0 | 0 |
| Full | python -m unittest discover -s tests -v | 572 | 567 | 5 | 1 module (17 cases not started) | 0 |
| Supplemental wheel + first-run under system Python | python -m unittest -v tests.test_wheel_distribution tests.test_first_run_examples | 9 | 9 | 0 | 0 | 0 |
| Supplemental doctor under system Python | python -m unittest -v tests.test_doctor_schema_truth | 4 | 4 | 0 | 0 | 0 |

The exact executable paths, CWDs, commands and raw outputs are in focused.txt, full.txt, system-interpreter.txt, system-pip.txt, wheel-system-python.txt and doctor-system-python.txt. Supplemental system interpreter: C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe; system-interpreter.txt records its real version. Those supplementary suites run without skips and cover the three actual tests initially skipped for unavailable pip (two wheel-install cases and one installed-doctor mutation case). They are **not** a second full-suite run.

Independent discovery/counting:

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import unittest,json; loader=unittest.TestLoader(); suite=loader.discover(\"tests\",top_level_dir=\".\"); module=loader.loadTestsFromName(\"tests.test_publication_projection\"); print(json.dumps({\"discovered_test_cases\":suite.countTestCases(),\"publication_module_cases\":module.countTestCases(),\"load_errors\":loader.errors},indent=2))"
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 0
RAW OUTPUT:
{
  "discovered_test_cases": 589,
  "publication_module_cases": 17,
  "load_errors": []
}
```

The full loader discovers **589 cases** with no load errors. The module-level skip prevents **17** of them starting; therefore unittest reports **572 run**, comprising **567 successes + 5 individual skips**. Its “skipped=6” is **5 individual skips plus one setUpModule skip**, not six skipped individual cases and not 566 successes. After the separate system-Python runs, the three pip-blocked cases have actually been exercised successfully; 19 discovered cases remain unexercised (the other two individual cases plus 17 publication cases). test-counts.json and counts-driver-output.txt retain accounting and the exact summary lines.

The genuine skip/unexercised distinctions are:

- test_doctor_schema_truth.test_b4_wheel_mutation_installed_doctor_fails: pip absent from the primary interpreter; later exercised successfully in doctor-system-python.txt.
- test_wheel_distribution's two installed-package cases: pip absent from the primary interpreter; later exercised successfully in wheel-system-python.txt.
- test_evidence_manifest.test_byte_level_hash_readback_matches: the existing seal names f541c3968d8b..., not this HEAD. **Gate unexercised**, not new-HEAD integrity proof. I did not regenerate the candidate's seal.
- test_project_destination_safety.test_symlink_escaping_authorized_root_is_refused: this host cannot create native symlinks. **Native OS behaviour unexercised**.
- tests.test_publication_projection setUpModule: local r5-s4-candidate ref unavailable in the external clone. **All 17 cases unexercised**. No equivalent ref was invented.

The packaging/fallback focused symlink tests can use the documented predicate seam where native links are unavailable; “ok” proves their refusal branch, not real OS link capability. interpreter.txt reports O_NOFOLLOW=False and O_NONBLOCK=False. Windows runs do not exercise optional POSIX flag branches.

### Independent Artifact Attacks

probes.py creates eight independently authored minimal skill sources, an auxiliary binary member per skill, a fresh ledger, synthetic approval records and an icon in system temp. It does **not** import candidate test fixture helpers. The candidate tools themselves are invoked by subprocess. Approvals/publisher fields are explicitly synthetic and are not human authorization. The known schema/template bytes are copied from the detached candidate; the source/body sentinels and collision fixtures are my own.

Controls: probe-control.txt and probe-rebuild.txt exit 0. ZIP and **all three standalone sidecars** are byte-identical across two output directories, as recorded with individual SHA-256 values in probe-results.json. The independently expected projected SKILL.md bytes and auxiliary binary bytes match all 16 member checks. The synthetic ZIP inventory has 24 members; this does not assert a 24-member count for the real source tree.

AO-01 collision attacks:

| Seed type | Output member | Builder exit | Same inode as outside sentinel | Outside sentinel unchanged | Seed bytes unchanged | Files remaining in output |
| --- | --- | ---: | --- | --- | --- | ---: |
| regular | `pipd-ls-sp-public-skills.zip` | 2 | false | true | true | 1 |
| regular | `pipd-ls-sp-public-skills.zip.sha256` | 2 | false | true | true | 1 |
| regular | `SOURCE_TO_PLUGIN_MAPPING.json` | 2 | false | true | true | 1 |
| regular | `RELEASE_RECEIPT.json` | 2 | false | true | true | 1 |
| hardlink | `pipd-ls-sp-public-skills.zip` | 2 | true | true | true | 1 |
| hardlink | `pipd-ls-sp-public-skills.zip.sha256` | 2 | true | true | true | 1 |
| hardlink | `SOURCE_TO_PLUGIN_MAPPING.json` | 2 | true | true | true | 1 |
| hardlink | `RELEASE_RECEIPT.json` | 2 | true | true | true | 1 |

Each output retains only its original seeded member, with no promoted artifact/partial generated sidecars. All eight attacks refuse with exit **2**: artifact cases give OUTPUT_ARTIFACT_EXISTS; sidecar/mapping/receipt cases give OUTPUT_MEMBER_EXISTS. The hardlink cases are genuine os.link calls and os.path.samefile readbacks, not monkeypatches. **AO-01 survives the tested preexisting-member/hardlink attacks.** This is a measured static preseed guarantee, not a concurrency/race guarantee.

Refusal probes also exercise repository-overlap and dist output destinations, unknown root-manifest properties, vendor schema byte drift, missing derivations, source-byte drift and a ninth skill. Every refusal has the exact CLI invocation and actual exit in its corresponding sibling file. The missing-owner mutation in probes.py changes the release record without its manifest extension: its actual first refusal is RELEASE_EXTENSION_MISMATCH, **not** OWNER_INPUT_MISSING. I do not credit it as a placeholder-gate test. The separate real delivery-template run, with its actual checked-in frozen ledger, directly reaches the owner gate:

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate\tools\build_public_plugin.py --source-root C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate --ledger C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\evidence\08_PLUGIN\FROZEN_SOURCE_LEDGER.json --source-commit 32962532b7b7176eafbd3d353ced63a3056027fb --packaging-root C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate\packaging\public-plugin --out-dir C:\Users\user\AppData\Local\Temp\pipd-ao3-probes-tqb3wf8s\default-refusal
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 2
RAW OUTPUT:
REFUSED OWNER_INPUT_MISSING: no owner derivation record for skill 'pipd-assurance-tqaep' (derivations.json is empty by design; every skill needs an owner-approved record whose source_sha256 matches the frozen ledger)
```

An earlier attempted default-template command used a nonexistent ledger path and exited 2/LEDGER_UNREADABLE; candidate-default-refusal.txt preserves that failed probe rather than hiding it. Only the corrected command above supports the owner-gate observation.

Web fallback: control and rebuild both exit 0 and produce identical SHA-256 **c88ddc49cfe5fb59fe1a713fdde4cfd6a06ed54cc5831885130e053ce990c2af** from the candidate's actual preview.3 mount directory. Existing regular/hardlinked destinations refuse with exit 2, sentinel unchanged; altered member bytes, an unlisted file, path traversal and a one-byte size cap refuse with exit 2. See probe-web-*.txt and probe-results.json. The output is DOC_MOUNT_ONLY, not a host-installed plugin.

AO-03: the exact workflow guard passes the real current committed diff (exit 0), rejects unresolved base (exit 1), and its frozen-path / outside-positive-allowlist branches reject independently selected diff strings (exit 1). Allowed docs/install path returns 0. Unlike round-2 patch mutations, my negative path probes inject **only git diff output** through an exported Bash git function; real commit-existence and merge-base checks still call real Git. This tests exact body classification without changing or committing candidate files, but is not an end-to-end synthetic commit or real Actions runner exercise.

```text
COMMAND: "C:/Program Files/Git/bin/bash.exe" -c "git() { if [ \"$1\" = diff ]; then printf \"%s
\" dist/ao3.txt; else command git \"$@\"; fi; }; export -f git; bash \"$1\"" ao3 C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\ao3\guard-extracted.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 1
RAW OUTPUT:
dist/ao3.txt
UPGRADE_WROTE_FROZEN_PATH: dist/ao3.txt
WRITE_SET_VIOLATION (base 52542c395a0f91dc2ba4bd6123acd4cdecd780dc)
```

```text
COMMAND: "C:/Program Files/Git/bin/bash.exe" -c "git() { if [ \"$1\" = diff ]; then printf \"%s
\" docs/ao3-unallowed.md; else command git \"$@\"; fi; }; export -f git; bash \"$1\"" ao3 C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\ao3\guard-extracted.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 1
RAW OUTPUT:
docs/ao3-unallowed.md
UPGRADE_WROTE_OUTSIDE_ALLOWED_SET: docs/ao3-unallowed.md
WRITE_SET_VIOLATION (base 52542c395a0f91dc2ba4bd6123acd4cdecd780dc)
```

```text
COMMAND: "C:/Program Files/Git/bin/bash.exe" C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\ao3\guard-extracted.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
EXIT_CODE: 1
RAW OUTPUT:
BASE_UNRESOLVED: 0000000000000000000000000000000000000000 is not present in this checkout; refusing to guess
```

**AO-03 survives those measured guard-body attacks.** This says nothing about branch protection or whether GitHub Actions was actually run.

Exact attack evidence index (full commands, CWD and raw output are in each named file):

| Probe | Actual exit | Raw evidence file |
| --- | ---: | --- |
| `probe-control` | 0 | `probe-control.txt` |
| `probe-rebuild` | 0 | `probe-rebuild.txt` |
| `probe-collision-regular-0` | 2 | `probe-collision-regular-0.txt` |
| `probe-collision-regular-1` | 2 | `probe-collision-regular-1.txt` |
| `probe-collision-regular-2` | 2 | `probe-collision-regular-2.txt` |
| `probe-collision-regular-3` | 2 | `probe-collision-regular-3.txt` |
| `probe-collision-hardlink-0` | 2 | `probe-collision-hardlink-0.txt` |
| `probe-collision-hardlink-1` | 2 | `probe-collision-hardlink-1.txt` |
| `probe-collision-hardlink-2` | 2 | `probe-collision-hardlink-2.txt` |
| `probe-collision-hardlink-3` | 2 | `probe-collision-hardlink-3.txt` |
| `probe-output-overlap` | 2 | `probe-output-overlap.txt` |
| `probe-output-dist` | 2 | `probe-output-dist.txt` |
| `probe-refusal-missing-owner` | 2 | `probe-refusal-missing-owner.txt` |
| `probe-refusal-unknown-manifest` | 2 | `probe-refusal-unknown-manifest.txt` |
| `probe-refusal-bad-vendor` | 2 | `probe-refusal-bad-vendor.txt` |
| `probe-refusal-missing-derivation` | 2 | `probe-refusal-missing-derivation.txt` |
| `probe-source-drift` | 2 | `probe-source-drift.txt` |
| `probe-ninth-skill` | 2 | `probe-ninth-skill.txt` |
| `probe-web-control` | 0 | `probe-web-control.txt` |
| `probe-web-rebuild` | 0 | `probe-web-rebuild.txt` |
| `probe-web-hardlink` | 2 | `probe-web-hardlink.txt` |
| `probe-web-preseeded` | 2 | `probe-web-preseeded.txt` |
| `probe-web-size` | 2 | `probe-web-size.txt` |
| `probe-web-drift` | 2 | `probe-web-drift.txt` |
| `probe-web-extra` | 2 | `probe-web-extra.txt` |
| `probe-web-traversal` | 2 | `probe-web-traversal.txt` |
| `probe-guard-frozen` | 1 | `probe-guard-frozen.txt` |
| `probe-guard-outside` | 1 | `probe-guard-outside.txt` |
| `probe-guard-allowed` | 0 | `probe-guard-allowed.txt` |
| `probe-guard-unresolved` | 1 | `probe-guard-unresolved.txt` |

### Additional Code Review and Accepted Mutants

The complete inspected builder, freezer, fallback, workflow, focused tests, install-state table and closure texts are retained in reviewed-source.txt (read command exits 0). The source walks compare the complete selected skill-file set against ledger digests; source frontmatter is projected only with an approval-shaped record; auxiliary bytes are copied. Text hashes and projection operate after the documented LF canonicalization, so this is not an unconditional promise to preserve arbitrary CRLF source bytes verbatim. The vendor schema's bytes are locked; validation is the tool's local supported-keyword subset, **not execution of the vendor's own validator**.

Two tangible findings not caught by the green suite:

1. **Official manifest identity is not bound to bookkeeping identity.** A valid but different official plugin.json name is accepted with exit 0 while the ZIP root and release receipt still identify pipd-ls-sp-public-skills. A version of 999.0.0 is accepted while the receipt/embedded release remain 0.1.1. The builder validates the official root against the vendor-shaped schema and checks that the embedded com.pipd.s4 object equals the release record, but does not compare the official name/version to that record. Evidence: probe-judgement-name.txt, probe-judgement-name-readback.txt, probe-judgement-version.txt, probe-judgement-version-readback.txt, all exit 0. These are accepted contradictory packaging inputs, not just theoretical concerns.
2. **Opaque extension review is not gated.** An additional com.ao3.unreviewed object is accepted and preserved in the ZIP with exit 0: probe-judgement-extension.txt and its readback. The locked vendor schema allows arbitrary object-valued namespaces; the owner derivation checks authorize SKILL.md transformations, not each manifest namespace/value. This proves acceptance of an unreviewed opaque object. It does **not** establish that any actual host would execute it or that anything was published. The delivered template's current namespaces/values were inspected; acceptance here does not license future arbitrary extensions.

Minimal repeatable version-drift reproducer, after this review's retained external fixtures exist:

    python .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3/repro_identity.py

It creates a **new external temp output** on each run and invokes the unchanged delivered builder. Actual output:

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate\tools\build_public_plugin.py --source-root C:\Users\user\AppData\Local\Temp\pipd-ao3-probes-tqb3wf8s\source --ledger C:\Users\user\AppData\Local\Temp\pipd-ao3-probes-tqb3wf8s\ledger.json --source-commit cccccccccccccccccccccccccccccccccccccccc --packaging-root C:\Users\user\AppData\Local\Temp\pipd-ao3-identity-repro-8k_ualus\packaging --out-dir C:\Users\user\AppData\Local\Temp\pipd-ao3-identity-repro-8k_ualus\output
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao3-d2_pq808\candidate
BUILDER_EXIT_CODE: 0
BUILT C:\Users\user\AppData\Local\Temp\pipd-ao3-identity-repro-8k_ualus\output\pipd-ls-sp-public-skills.zip sha256=ef59b6434a6a901dfc93e432adfd88ba2aa51739ff38405d90840d72c03c3c3a members=24 claim_ceiling=LOCAL_PACKAGER_PASS_ONLY official_portal_verification=NOT_EXECUTED


MANIFEST_VERSION: 999.0.0
RECEIPT_VERSION: 0.1.1
IDENTITY_MISMATCH_ACCEPTED: True
```

The reproducer's own command/exit are retained in repro-identity-exit.txt (exit 0). The anomalous exit 0 is the finding, not a successful identity refusal. These findings are why the verdict is **conditional rather than unconditional ACCEPT**. No suggestion that the model deviation caused them is supported.

Further trust-boundary limits found in inspection: the supplied source ledger is the builder's byte/identity authority, not independent proof that Git contains the claimed commit/tree; approval_receipt/approved_by and publisher identity_sha256 are syntactic evidence fields, not a verified human signature or publisher authentication. The fallback checks member bytes against the supplied manifest and presence of release stamps; it does not cryptographically authenticate a human-authorized release just because a self-consistent pack repeats those strings. Supplying a wholly substituted internally consistent ledger/pack is a different trust hypothesis from altering bytes under a fixed trusted ledger/manifest. This report's probes cannot establish authenticity of all supplied authorities.

The promotion code checks final ZIP existence before building and later uses os.replace; sidecars use exclusive creation. The tested preexisting ZIP refusal does **not** establish no-clobber behaviour if another actor creates/replaces the final path between the check and promotion. No race/stress test ran. Ancestor/path-check races, reparse-point behaviour and concurrent cleanup/replacement are likewise outside these measurements. The packaging instructions' output-dir exclusion and refusal checks do not make hostile concurrent filesystems safe by proof.

### Deviation Analysis — Judged Separately

Exact candidate declarations, original exits, lane-header/tail evidence and probes: model-logs.txt (full raw source contents) and model-summary-retry.txt (successful extraction, exit 0). model-summary.txt preserves an initial extraction SyntaxError (exit 1); no fact is inferred from that failed extraction.

- MODEL_DECLARED_20261012T101452Z.txt names **opencode-go/deepseek-v4.1-flash**. Original B1/B2/B3 headers agree on that model label, with CLI provider field **openai**. All three recorded .exit files contain **1**.
- Their lane tails show **Provider error 400 / invalid_request_error**, explicitly: **The reasoning_content in the thinking mode must be passed back to the API.** They already performed some tool activity before failing. The evidence supports a request/history/protocol compatibility failure as reported by the upstream error; it does not establish that the requested model was nonexistent, universally unavailable, or incapable of the task.
- MODEL_DECLARED_20261012T101611Z.txt names **opencode-go/deepseek-v4-flash**; the three attempt3 headers carry that label and their recorded .exit files contain **0**. The later 102527 declaration names the same label. The rerun logs contain artifact/test work, consistent with a rerun contributing to the eventual candidate. Logs alone do not prove every final byte exclusively came from that rerun; there are prior partial work and later repair commits. Recorded historical lane exit files are source evidence, not exits I independently reproduced by invoking those models now.
- Both DeepSeek-labeled probe logs report a local websocket **426 Upgrade Required** at ws://127.0.0.1:10102/v1/responses and then produce PROBE_OK text. They self-report incompatible identities (claude/Anthropic versus gpt-5-codex). The gpt-6.1-sol probe has a metadata-not-found warning and MODEL_SEEN=unknown. These are corroboration of requested labels, transport/metadata messages and generated strings only; **none is trusted upstream model attestation**. A model's own MODEL_SEEN line has no verified authority here.

Mechanical portions insensitive to authorship **after inputs/specifications are fixed**: exact auxiliary-byte copying, LF-normalized digest comparisons, deterministic ZIP metadata/content order, recomputed SHA-256, measured exclusive-member refusals, typed byte-drift refusals, and executing the exact diff-path guard. Those properties were independently exercised, so they do not need trust in the backup-model label.

Judgement-sensitive portions: choosing the eight skills and published body content, the portable-frontmatter allowlist and dropped keys, whether approval-shaped fields are enough, the local schema-validator coverage, permitted opaque extensions, identity-binding omissions, allowlist breadth, size-cap value and its utility in real accounts, install-route semantics, what UAT/gates to defer, and wording that distinguishes build/review/publication. Tests establish selected mechanics, not that those choices are adequate for every user/host. The accepted manifest mutants prove at least one unverified judgement boundary; real account upload limits and host operational interpretation remain untested.

Before public release a reasonable reviewer needs **actual final manifest/bookkeeping identity coherence; reviewed extension semantics; genuine human publisher identity and authorization for the projected skill content; schema/vendor operational validation; real host/account results; and reliable execution provenance if policy depends on a particular model**. The deviation makes upstream-model provenance and review-of-model-dependent judgement harder to establish, especially because self-reports conflict and reruns follow partial writes. Independent artifact checks reduce, but do not remove, those uncertainties. The deviation is recorded rather than transformed into an owner-only veto or an invented verified model identity.

## NOT_EXECUTED

These items were not run by this officer. Existing documents, receipts, workflow files and historical host logs do not substitute for execution in this engagement. The candidate's install-state table and manifest/receipt ceilings are captured in reviewed-source.txt and the readback logs.

| Activity | This engagement | Candidate's own claim ceiling |
| --- | --- | --- |
| Vendor's own plugin-schema validator | **NOT_EXECUTED** | Local subset validation only; vendor validator NOT_EXECUTED; LOCAL_PACKAGER_PASS_ONLY |
| Portal draft creation | **NOT_EXECUTED** | No approval granted; official_portal_verification=NOT_EXECUTED |
| Portal scan | **NOT_EXECUTED** | NOT_EXECUTED, not local-schema-pass equivalence |
| Portal review | **NOT_EXECUTED** | PORTAL_APPROVED not granted |
| Portal approval | **NOT_EXECUTED** | PORTAL_APPROVED not granted |
| Portal publication | **NOT_EXECUTED** | PUBLISHED not granted; no public listing inferred |
| Real GitHub Actions run | **NOT_EXECUTED** | A workflow/local scripts are verification surfaces, not a runner receipt |
| Plus account UAT | **NOT_EXECUTED** | DOC_MOUNT_ONLY/build-level verification is not account UAT |
| Free account UAT | **NOT_EXECUTED** | DOC_MOUNT_ONLY/build-level verification is not account UAT |
| Codex Desktop GUI host UAT | **NOT_EXECUTED** | HOST_QUALIFIED requires actual host-produced effective 8/8 load and positive/negative triggers; not granted here |
| Codex CLI host UAT | **NOT_EXECUTED** | Same host qualification ceiling; invoking local Python from this CLI is not skill-host UAT |
| Claude Code host UAT | **NOT_EXECUTED** | Same host qualification ceiling; not inferred from docs or model self-report |
| Verified human publisher identity | **NOT_EXECUTED** | Checked-in publisher fields are OWNER_INPUT_REQUIRED; synthetic fields are not authenticated people |
| Public plugin build using genuine owner-complete inputs | **NOT_EXECUTED** | Delivery refuses OWNER_INPUT_MISSING; BUILD_PASS for a genuine release not granted |
| Hostile concurrent output races / POSIX optional flags | **NOT_EXECUTED** | No broader no-race/platform qualification inferred from local collision tests |
| Fresh-HEAD evidence-seal readback | **NOT_EXECUTED** | Old seal is not this HEAD's integrity attestation |
| 17 publication-projection test bodies | **NOT_EXECUTED** | Module skipped; no publication subject qualification inferred |
| Native symlink escape test | **NOT_EXECUTED** | Windows privilege/capability limitation; predicate-seam checks are narrower |
| Historical model executions rerun/actual upstream model authentication | **NOT_EXECUTED** | Declared model labels/logs only, no independent upstream identity proof |

## LIMITS OF THIS REPORT

- A passing subclaim is not acceptance of a dirty handover. Conversely, dirty orchestration artifacts do not demonstrate a defect in the detached candidate's committed code.
- A current empty/dirty status observation cannot reconstruct who created files or whether an earlier historical clean instant occurred. The maker's byte-preserving pre-commit move cannot be authenticated from two post-move copies.
- Conditional Stage-B acceptance covers reviewed local artifacts and measured operations only. It grants **no Portal approval, publication, host qualification, verified publisher identity, merge/release permission, production verification or S4 acceptance**.
- Synthetic approval-shaped fixtures demonstrate mechanics, not human authorization. A deterministic ZIP can still contain incorrect/unreviewed judgement. The accepted name/version/extension mutants are explicit evidence against a universal fail-closed claim.
- Text canonicalization is not arbitrary raw-byte preservation. Equal rebuilds here prove same-input determinism on this interpreter/platform, not every compressor/runtime/platform or hostile concurrent filesystem.
- A supplied digest/ledger/receipt is not self-authenticating. The probes distinguish byte drift against fixed authorities, not all coherent substitutions of those authorities.
- Genuine skips and unexercised gates remain visible. A green exit with module skips is not universal suite coverage; supplemental interpreter runs are not a second full run.
- Git ancestry and anonymous tip equality bind this observation to the read-back commit, not future remote state. Final local/snapshot identity rechecks are retained; no remote mutation occurred.
- Evidence is retained in the allowed round-relative ao3 directory; no repository-root verify/ output was created. Temporary snapshots/fixtures are external as specifically instructed. Failed probes/extraction attempts remain recorded and are not laundered into successful checks.

