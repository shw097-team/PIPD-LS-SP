# Independent Acceptance Officer — VERIFY / SECURITY, Round 5

Date: 2026-10-12 (Asia/Taipei). Subject: `S4POST-20261012-postrepair-recheck-and-triple-upgrade`.

**ADJUDICATION A: STILL_NOT_CLOSED.** The delivered worktree was dirty before any officer evidence was created. The untracked path was the launcher's AO5 manifest, not this officer's report.

**ADJUDICATION B: enforcement is real on the specifically repaired branches, but still fails open.** The round-4 D1 missing-input/main-log-copy, D2 detected-dirt, D3 ordinary output-placement and F containment probes now return the expected statuses. That does not establish universal fail-closed enforcement. Independently demonstrated counterexamples include suppressed receipt-copy failure, failed Git cleanliness queries treated as clean, preflight committing an already staged outside-round file, and zero-attempt qualification advertised as passed. The gate also qualifies and launches EXECUTE through different invocation routes by default.

The ceiling is **local stub control-flow verification on this host and subject**, with explicit host configuration adjustments below. No model was launched. A stub proves control flow and proves nothing about a model.

## Subject and delivered-state evidence

I recorded HEAD, tree and porcelain status in the first tool call, before creating any file or directory. That call was grouped PowerShell: its tool exit was 0; individual native exits were not recorded. I do not claim otherwise. Subsequent individually exit-coded subprocess observations corroborate the same identity and pre-existing dirt, while also listing my permitted evidence directory.


Evidence: `first-observation.txt`

```text
COMMAND: git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; git status --porcelain; Get-Location
TOOL_EXIT_CODE: 0 (grouped PowerShell; individual native exits not separately captured)
RAW OUTPUT:
c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d
d8fe6480f5107bcb01a045783c36b2cd536662c3
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest

Path
----
C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt

```

Evidence: `delivery-head.txt`

```text
COMMAND: git rev-parse HEAD
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d

STDERR:

```

Evidence: `delivery-tree.txt`

```text
COMMAND: git rev-parse HEAD^{tree}
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
d8fe6480f5107bcb01a045783c36b2cd536662c3

STDERR:

```

Evidence: `delivery-status.txt`

```text
COMMAND: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao5/

STDERR:

```

HEAD is `c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d`; tree is `d8fe6480f5107bcb01a045783c36b2cd536662c3`. The pre-existing untracked path is:

`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest`.

This falsifies a clean handover for this engagement. I cannot attribute its creator or disprove an earlier temporarily clean instant. A manifest written after preflight is consistent with the launcher source below; that is an inference, not authentication of the historical invocation.


Verbatim source excerpt from `stage-b/run_lane.sh` (full read: `required-source-read.txt`, EXIT_CODE=0):

```text
printf 'LANE=%s\nMODEL=%s\nPROVIDER=%s\nEFFORT=%s\nSTAMP=%s\nWT=%s\nROUTE_STYLE=%s\n' \
  "$LANE" "$MODEL" "$PROV" "$EFF" "$STAMP" "$WT" "${ROUTE_STYLE:-openai}" > "$S/${LANE}_${STAMP}.manifest"
```

## History and method

I read both earlier verdicts and all five required launcher/harness documents, plus the lane-set gate, assignment and owner record. Full contents and a successful read exit are retained in `required-source-read.txt`. The prior verdicts are historical context, not my evidence of current behavior. I did not re-adjudicate product-code closure or accept their path-set analysis as a fresh result.

All attacks ran in an external system-temp clone checked out at the recorded commit. Before each independent launcher scenario, I reset that clone to the subject and removed only its untracked fixtures. Each reset/clean command and exit is retained. Launcher-created commits occurred only in these external clones; the delivery was never staged, committed, pushed, tagged or merged. Inside the repository, my entire write set is this round's `verify/ao5/`.


Evidence: `clone.txt`

```text
COMMAND: git -c safe.directory=C:/Projects/Agent_Workspace/PIPD/.git/worktrees/s4post-b-wt clone --no-hardlinks --no-checkout C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d
EXIT_CODE: 0
STDOUT:

STDERR:
Cloning into 'C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2'...
done.

```

Evidence: `checkout.txt`

```text
COMMAND: git checkout --detach c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:

STDERR:
HEAD is now at c93a41f chore(s4post-b): commit harness artifacts before the AO5 lane handover

```

Evidence: `clone-tree.txt`

```text
COMMAND: git rev-parse HEAD^{tree}
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
d8fe6480f5107bcb01a045783c36b2cd536662c3

STDERR:

```

Evidence: `clone-clean.txt`

```text
COMMAND: git status --porcelain
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:

STDERR:

```

Evidence: `stub-source.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys
for x in sys.argv[1:]:
 print(\"FILE: \"+x);print(pathlib.Path(x).read_text())" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\stub.sh C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qual.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\stub.sh

#!/usr/bin/env bash

printf 'CHILD_LAUNCHED\n' >> "$MARKER"

printf 'STUB argv=%s\n' "$*"

if [ "${MAKE_DIRT:-0}" = 1 ]; then printf dirt > "$LANE_WT/AO5_POST_DIRT"; fi

if [ "${DELETE_LOG:-0}" = 1 ]; then rm -f "$TMPDIR"/hgk-lanes/*.log; fi

exit "${CHILD_EXIT:-0}"



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qual.sh

#!/usr/bin/env bash

printf "QUAL_LAUNCHED\n" >> "$QMARKER"

printf "Q1_OK\nQ2_OK\nQUAL argv=%s\n" "$*"

exit 0




STDERR:

```

The retained external fixtures live under the path in `temp-location.txt`; the final harness-script clone roots additionally appear in their command/case logs. `audit.py`, `adapt.py`, `supplement.py`, `additional.py` and `results.json` preserve commands and fixture construction. These drivers are evidence, not candidate modifications. The listed commands in the logs use Windows argument notation; use the driver's subprocess argument arrays or the Bash recipes below to reproduce them.

### Host adjustments and unsuccessful attempts

The first clone attempt returned 128 for Git dubious ownership. I retried with a command-scoped `safe.directory` exception for the delivery's worktree metadata, without changing global Git configuration. The original refusal is retained in `host-initial/clone-initial-failure.txt`.

Initial native-path launcher attempts could not create the round-relative output directory and returned 3 before a child; those results do not prove the postflight branch. The environment initially disabled MSYS argument conversion. I removed `MSYS_NO_PATHCONV` and `MSYS2_ARG_CONV_EXCL` from the probe subprocess environment and used `/tmp/...` paths for Bash filesystem operations. No launcher code was changed. These are the conditions for the successful branch probes; the unadjusted host remains a portability limitation.


Evidence: `environment-contract.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import os,sys;print(\"INITIAL_MSYS_NO_PATHCONV=\"+os.environ.get(\"MSYS_NO_PATHCONV\",\"<unset>\"));print(\"INITIAL_MSYS2_ARG_CONV_EXCL=\"+os.environ.get(\"MSYS2_ARG_CONV_EXCL\",\"<unset>\"));print(\"TEMP=\"+os.environ[\"TEMP\"]);print(\"PYTHON=\"+sys.executable)"
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
INITIAL_MSYS_NO_PATHCONV=1

INITIAL_MSYS2_ARG_CONV_EXCL=*

TEMP=C:\Users\user\AppData\Local\Temp

PYTHON=C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe


STDERR:

```

Evidence: `host-initial/post.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_POST brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate
EXIT_CODE: 3
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
REFUSED_AO5_POST_DONE

STDERR:
mkdir: cannot create directory ‘C:/Users/user’: Permission denied
REFUSED[3] cannot create round-relative output dir: verify/ao5-probe

```

Both requested test scripts initially returned 9 / `CLONE_FAILED` before assertions. A separately captured clone command exposed filename-length failure. The final runs used fresh shorter system-temp directories and inherited `core.longpaths=true` through process-local `GIT_CONFIG_*` settings. This did not modify a repository or global configuration. Earlier failures remain evidence; the final counts below are actual assertion counts, not estimates.


Evidence: `path-diagnostic.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" -c "git clone --no-hardlinks \"$1\" \"$2\"; c=$?; echo CLONE_EXIT=$c; exit \"$c\"" ao5 C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2 /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/path-diagnostic-clone
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d
EXIT_CODE: 128
STDOUT:
CLONE_EXIT=128

STDERR:
fatal: could not create leading directories of '/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/path-diagnostic-clone': Permission denied

```

## Required attacks and bounded results

| Attack | Actual launcher exit | Observation ceiling |
| --- | ---: | --- |
| Untracked root dirt | 2 | Stub marker absent, no child or lane log |
| Missing brief | 3 | Stub marker absent, no child or lane log |
| Stub writes root dirt after launch | 5 | Detected dirt rejects completion |
| Ordinary `verify/ao5-probe` output | 0 | Round-relative directory exists; no root directory added |
| TMPDIR inside clone | 3 | No child; resolved log directory refused |
| Stub child returns 7 | 7 | Child nonzero propagated |
| Stub unlinks its opened log | 4 | Main log cannot be copied; metadata-only message |

Exit 0 on a status/inventory command means that observation completed, not that its observed state is acceptable. The root-dirt test is separate from the staged-input bypass below. An in-round dirty file is intentionally committed by preflight, so this is not a promise that every dirty input is refused.


Evidence: `dirty.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_DIRTY brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 2
STDOUT:
REFUSED_AO5_DIRTY_DONE

STDERR:
REFUSED[2] worktree not clean before handover: 1 path(s); refusing to launch AO5_DIRTY

```

Evidence: `dirty-inventory.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); r=sys.argv[3]; n=sys.argv[4]; print(json.dumps({\"child_marker\":(b/(n+\"-child.marker\")).read_text() if (b/(n+\"-child.marker\")).exists() else None,\"external_logs\":[str(x) for x in (b/(n+\"-logs\")).rglob(\"*\") if x.is_file()],\"root_output_exists\":(c/\"verify/ao5-probe\").exists(),\"round_output_exists\":(c/r/\"verify/ao5-probe\").exists(),\"lane_exit_files\":[str(x) for x in (c/r/\"stage-b\").glob(\"AO5_\"+n.upper()+\"_*.exit\")]},indent=2))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2 C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade dirty
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
{

  "child_marker": null,

  "external_logs": [],

  "root_output_exists": false,

  "round_output_exists": false,

  "lane_exit_files": []

}


STDERR:

```

Evidence: `missing.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_MISSING AO5_DOES_NOT_EXIST.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 3
STDOUT:
REFUSED_AO5_MISSING_DONE

STDERR:
REFUSED[3] brief not found: stage-b/AO5_DOES_NOT_EXIST.md

```

Evidence: `missing-inventory.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); r=sys.argv[3]; n=sys.argv[4]; print(json.dumps({\"child_marker\":(b/(n+\"-child.marker\")).read_text() if (b/(n+\"-child.marker\")).exists() else None,\"external_logs\":[str(x) for x in (b/(n+\"-logs\")).rglob(\"*\") if x.is_file()],\"root_output_exists\":(c/\"verify/ao5-probe\").exists(),\"round_output_exists\":(c/r/\"verify/ao5-probe\").exists(),\"lane_exit_files\":[str(x) for x in (c/r/\"stage-b\").glob(\"AO5_\"+n.upper()+\"_*.exit\")]},indent=2))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2 C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade missing
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
{

  "child_marker": null,

  "external_logs": [],

  "root_output_exists": false,

  "round_output_exists": false,

  "lane_exit_files": []

}


STDERR:

```

Evidence: `post.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_POST brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 5
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_POST_LANE=20261012T131023Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_POST exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/post-logs/hgk-lanes/AO5_POST_20261012T131023Z.log
POSTFLIGHT:dirty=1 HEAD=6ed9e96
AO5_POST_LANE_DONE

STDERR:

```

Evidence: `post-status.txt`

```text
COMMAND: git status --porcelain
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
?? AO5_POST_DIRT

STDERR:

```

Evidence: `output.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_OUTPUT brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_OUTPUT_LANE=20261012T131024Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_OUTPUT exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/output-logs/hgk-lanes/AO5_OUTPUT_20261012T131024Z.log
POSTFLIGHT:dirty=0 HEAD=b06dcd5
AO5_OUTPUT_LANE_DONE

STDERR:

```

Evidence: `output-inventory.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); r=sys.argv[3]; n=sys.argv[4]; print(json.dumps({\"child_marker\":(b/(n+\"-child.marker\")).read_text() if (b/(n+\"-child.marker\")).exists() else None,\"external_logs\":[str(x) for x in (b/(n+\"-logs\")).rglob(\"*\") if x.is_file()],\"root_output_exists\":(c/\"verify/ao5-probe\").exists(),\"round_output_exists\":(c/r/\"verify/ao5-probe\").exists(),\"lane_exit_files\":[str(x) for x in (c/r/\"stage-b\").glob(\"AO5_\"+n.upper()+\"_*.exit\")]},indent=2))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2 C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade output
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
{

  "child_marker": "CHILD_LAUNCHED\n",

  "external_logs": [

    "C:\\Users\\user\\AppData\\Local\\Temp\\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\\output-logs\\hgk-lanes\\AO5_OUTPUT_20261012T131024Z.log",

    "C:\\Users\\user\\AppData\\Local\\Temp\\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\\output-logs\\hgk-lanes\\AO5_OUTPUT_20261012T131024Z.log.exit"

  ],

  "root_output_exists": false,

  "round_output_exists": true,

  "lane_exit_files": [

    "C:\\Users\\user\\AppData\\Local\\Temp\\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\\candidate2\\.hgk\\rounds\\S4POST-20261012-postrepair-recheck-and-triple-upgrade\\stage-b\\AO5_OUTPUT_20261012T131024Z.exit"

  ]

}


STDERR:

```

Evidence: `output2-root-before.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]);print(json.dumps(sorted(p.name for p in c.iterdir() if p.is_dir())))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
[".agents", ".git", ".github", ".hermes", ".hgk", "dist", "docs", "examples", "fixtures", "openspec", "packaging", "schemas", "skills", "src", "tests", "tools"]


STDERR:

```

Evidence: `output2-root-after.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]);print(json.dumps(sorted(p.name for p in c.iterdir() if p.is_dir())))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
[".agents", ".git", ".github", ".hermes", ".hgk", "dist", "docs", "examples", "fixtures", "openspec", "packaging", "schemas", "skills", "src", "tests", "tools"]


STDERR:

```

Evidence: `inside.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_INSIDE brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 3
STDOUT:
REFUSED_AO5_INSIDE_DONE

STDERR:
REFUSED[3] lane log dir resolves inside the worktree: /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/tmp-inside/hgk-lanes

```

Evidence: `inside-inventory.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,json,sys; c=pathlib.Path(sys.argv[1]); b=pathlib.Path(sys.argv[2]); r=sys.argv[3]; n=sys.argv[4]; print(json.dumps({\"child_marker\":(b/(n+\"-child.marker\")).read_text() if (b/(n+\"-child.marker\")).exists() else None,\"external_logs\":[str(x) for x in (b/(n+\"-logs\")).rglob(\"*\") if x.is_file()],\"root_output_exists\":(c/\"verify/ao5-probe\").exists(),\"round_output_exists\":(c/r/\"verify/ao5-probe\").exists(),\"lane_exit_files\":[str(x) for x in (c/r/\"stage-b\").glob(\"AO5_\"+n.upper()+\"_*.exit\")]},indent=2))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2 C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade inside
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
{

  "child_marker": null,

  "external_logs": [],

  "root_output_exists": false,

  "round_output_exists": false,

  "lane_exit_files": []

}


STDERR:

```

Evidence: `child7.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_CHILD7 brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 7
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_CHILD7_LANE=20261012T131025Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_CHILD7 exit=7 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/child7-logs/hgk-lanes/AO5_CHILD7_20261012T131025Z.log
POSTFLIGHT:dirty=0 HEAD=8ef4330
AO5_CHILD7_LANE_DONE

STDERR:

```

Evidence: `copyfail.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_COPYFAIL brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 4
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_COPYFAIL_LANE=20261012T131027Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_COPYFAIL exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/copyfail-logs/hgk-lanes/AO5_COPYFAIL_20261012T131027Z.log
POSTFLIGHT:dirty=0 HEAD=3772eb7
AO5_COPYFAIL_LANE_DONE

STDERR:
POSTFLIGHT_LOG_COPY_FAILED log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/copyfail-logs/hgk-lanes/AO5_COPYFAIL_20261012T131027Z.log

```

Evidence: `copyfail-message.txt`

```text
COMMAND: git log -1 --format=%B
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
evidence(s4post-b): AO5_COPYFAIL lane METADATA ONLY 20261012T131027Z - no lane log was copied into the tree (child exit 0); do not read this as a completed lane


STDERR:

```

The output2 root-directory snapshots bracket a second isolated successful invocation (`output2.txt`, exit 0). They are equal. Thus the ordinary argument does not add a root directory on this probe. No symlink/junction escape or race is inferred to have passed. The inside-log test creates an empty `tmp-inside/hgk-lanes` directory before refusal; it validates before child/log-file creation, not before all directory creation.

## Residual fail-open findings

### R1 — failed exit-receipt copy still returns 0

This is the smallest direct remaining launcher failure reproducer. I exported a `cp` function which delegates main-log copying unchanged, records a failure marker outside the clone, and returns 23 only for the `.exit` receipt copy. The candidate script was unchanged. This is deterministic fault injection, not a claim that a natural disk failure occurred.

```bash
# Fresh clean external clone at the subject; stub and log/marker paths outside it.
cp() {
  case "$1" in
    *.exit) printf 'EXIT_COPY_RETURN=23
' >> "$FAILMARKER"; return 23 ;;
    *) command cp "$@" ;;
  esac
}
export -f cp
bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_RECEIPT2 brief_nt.md verify/ao5-probe
# Captured wrapper EXIT_CODE=0; receipt copy return=23; receipt absent.
```

`LANE_WT`, `TMPDIR`, `CODEX_BIN`, `MARKER` and `FAILMARKER` are set by `supplement.py`. The receipt is absent, but the launcher reports a done lane with exit 0 and commits the manifest and main log. The main-log-copy repair works; the adjacent exit-copy error remains explicitly discarded.


Verbatim source excerpt from `stage-b/run_lane.sh` (full read: `required-source-read.txt`, EXIT_CODE=0):

```text
    cp "$LOGEXIT" "$S/${LANE}_${STAMP}.exit" 2>/dev/null || true
```

Evidence: `receipt2.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" -c "cp() { case \"$1\" in *.exit) printf \"EXIT_COPY_RETURN=23\n\" >> \"$FAILMARKER\"; return 23;; *) command cp \"$@\";; esac; }; export -f cp; bash \"$@\"" ao5 C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_RECEIPT2 brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_RECEIPT2_LANE=20261012T131222Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_RECEIPT2 exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/receipt2-logs/hgk-lanes/AO5_RECEIPT2_20261012T131222Z.log
POSTFLIGHT:dirty=0 HEAD=6df5761
AO5_RECEIPT2_LANE_DONE

STDERR:

```

Evidence: `receipt2-readback.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys
b=pathlib.Path(sys.argv[1]);s=pathlib.Path(sys.argv[2]);print((b/\"receipt2-failure.marker\").read_text());print(\"child_marker=\"+(b/\"receipt2-child.marker\").read_text());print(\"receipts=\"+repr([str(p) for p in s.glob(\"AO5_RECEIPT2_*.exit\")]))" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\stage-b
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
EXIT_COPY_RETURN=23



child_marker=CHILD_LAUNCHED



receipts=[]


STDERR:

```

Evidence: `receipt2-history.txt`

```text
COMMAND: git log -1 --format=%B --name-status
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
evidence(s4post-b): AO5_RECEIPT2 lane output 20261012T131222Z (lane log copied in from outside the worktree; child exit 0)


A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_RECEIPT2_20261012T131222Z.log
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_RECEIPT2_20261012T131222Z.manifest

STDERR:

```

### R2 — Git status failure is treated as a clean worktree

I exported a Git function that delegates every command except `status`; for that command it records an external marker and returns 128. Both cleanliness queries fail; the launcher launches the stub and returns 0 while printing `PREFLIGHT_CLEAN` and `POSTFLIGHT:dirty=0`. This fault injection proves failed cleanliness queries are unchecked. It does not demonstrate corrupt repository state in the delivery.

Small reproducer, with the same clean external clone/stub environment:

```bash
git() {
  if [ "$1" = status ]; then
    printf 'GIT_STATUS_RETURN=128
' >> "$FAILMARKER"
    return 128
  fi
  command git "$@"
}
export -f git
bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_STATUSFAIL brief_nt.md verify/ao5-probe
# Captured wrapper EXIT_CODE=0; both git-status returns=128.
```

Counting a failed command's empty stdout via `wc -l` yields zero; without checking the query status, the script cannot distinguish clean from unobservable. The relevant source is quoted below.


Verbatim source excerpt from `stage-b/run_lane.sh` (full read: `required-source-read.txt`, EXIT_CODE=0):

```text
DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
[ "$DIRTY" -eq 0 ] || die 2 "worktree not clean before handover: $DIRTY path(s); refusing to launch ${LANE}"
```

Evidence: `statusfail.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" -c "git() { if [ \"$1\" = status ]; then printf \"GIT_STATUS_RETURN=128\n\" >> \"$FAILMARKER\"; return 128; fi; command git \"$@\"; }; export -f git; bash \"$@\"" ao5 C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_STATUSFAIL brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=c93a41f
AO5_STATUSFAIL_LANE=20261012T131322Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_STATUSFAIL exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/statusfail-logs/hgk-lanes/AO5_STATUSFAIL_20261012T131322Z.log
POSTFLIGHT:dirty=0 HEAD=b126b15
AO5_STATUSFAIL_LANE_DONE

STDERR:

```

Evidence: `statusfail-readback.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys;b=pathlib.Path(sys.argv[1]);print((b/\"statusfail-failure.marker\").read_text());print((b/\"statusfail-child.marker\").read_text())" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
GIT_STATUS_RETURN=128

GIT_STATUS_RETURN=128



CHILD_LAUNCHED




STDERR:

```

### R3 — an already staged outside-round file is committed and admitted

In the external clone I created `AO5_OUTSIDE_STAGED` at the root and staged it. Preflight's path-limited `git add` does not restrict the existing index; its `git commit` commits the whole index. It committed that outside-round file under the harness-artifact title, then launched the stub and returned 0. This is a genuine input-state bypass with ordinary Git, not a command override. The staged input was not refused with exit 2.

Small reproducer in a clean external clone:

```bash
printf fixture > "$clone/AO5_OUTSIDE_STAGED"
git -C "$clone" add AO5_OUTSIDE_STAGED
LANE_WT="$clone" TMPDIR="$outside_temp" CODEX_BIN="$stub" MARKER="$marker"   bash "$clone/$RELROUND/stage-b/run_lane.sh" AO5_STAGED brief_nt.md verify/ao5-probe
# Captured launcher EXIT_CODE=0; preflight commit contains AO5_OUTSIDE_STAGED.
```

The launcher is permitted to commit harness artifacts in its own round. This probe shows its existing-index boundary exceeds that scope; cleanliness after an unauthorized scope sweep is not input refusal.


Evidence: `staged-before.txt`

```text
COMMAND: git status --porcelain
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
A  AO5_OUTSIDE_STAGED

STDERR:

```

Evidence: `staged.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lane.sh AO5_STAGED brief_nt.md verify/ao5-probe
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
PREFLIGHT_CLEAN HEAD=7faa424
AO5_STAGED_LANE=20261012T131029Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
AO5_STAGED exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/staged-logs/hgk-lanes/AO5_STAGED_20261012T131029Z.log
POSTFLIGHT:dirty=0 HEAD=3b1b399
AO5_STAGED_LANE_DONE

STDERR:

```

Evidence: `staged-history.txt`

```text
COMMAND: git log "--format=commit %H%nsubject %s" --name-status c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d..HEAD
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
commit 3b1b3998e903cca6010d01bf5cd0dd44fc843a6c
subject evidence(s4post-b): AO5_STAGED lane output 20261012T131029Z (lane log copied in from outside the worktree; child exit 0)

A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_STAGED_20261012T131029Z.exit
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_STAGED_20261012T131029Z.log
A	.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_STAGED_20261012T131029Z.manifest
commit 7faa424a0e04a4ea5c0a6d25c851068ba536754c
subject chore(s4post-b): commit harness artifacts before the AO5_STAGED lane handover

A	AO5_OUTSIDE_STAGED

STDERR:

```

### R4 — zero attempts are called successful qualification

With `GATE_QUALIFY_RUNS=0`, no qualification stub is invoked. The lane stub runs, the gate prints `QUALIFICATION_PASSED ... consecutive_runs=0`, then `LANE_SET_OK`, and returns 0. This is input validation failure, distinct from the explicitly named `GATE_SKIP_QUALIFY=1` testing switch. The default of 3 exists, but a configurable count is not validated as a positive integer.

Smallest gate reproducer with the same external stub environment:

```bash
GATE_QUALIFY_RUNS=0 bash "$clone/$RELROUND/stage-b/run_lanes_gated.sh" VERIFY brief_nt.md
# Captured gate EXIT_CODE=0; qualification marker absent; child marker present.
```


Evidence: `qzero.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh VERIFY brief_nt.md
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
ASSIGNMENT role=VERIFY model=gpt-6.1-sol provider=openai effort=medium
QUALIFICATION_ROUTE style=openai model=gpt-6.1-sol effort=medium
QUALIFICATION_PASSED model=gpt-6.1-sol effort=medium (consecutive_runs=0, two tool round trips each)
PREFLIGHT_CLEAN HEAD=c93a41f
BRIEF_NT__LANE=20261012T131030Z MODEL=gpt-6.1-sol provider=openai reasoning=medium (declared)
BRIEF_NT_ exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/qzero-logs/hgk-lanes/BRIEF_NT__20261012T131030Z.log
POSTFLIGHT:dirty=0 HEAD=03dfe0d
BRIEF_NT__LANE_DONE
CHILD lane=BRIEF_NT_ index=0 exit=0
LANE_SET_OK lanes=1 model=gpt-6.1-sol effort=medium

STDERR:

```

Evidence: `qzero-markers.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys
for x in sys.argv[1:]:
 p=pathlib.Path(x); print(str(p)+\" exists=\"+str(p.exists())); print(p.read_text() if p.exists() else \"\")" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qzero-child.marker C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qzero-qual.marker
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qzero-child.marker exists=True

CHILD_LAUNCHED



C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\qzero-qual.marker exists=False




STDERR:

```

### R5 — default EXECUTE qualification and writer routes disagree

With no `ROUTE_STYLE` override, the gate reads EXECUTE's catalog route and sends the qualification stub `-c model=<slug>`, base URL and catalog. It does not pass that role route to `run_lane.sh`, whose default is openai. The writer stub receives `-m <slug> -c model_provider="opencode-go"`, and its manifest would declare the default openai route. The gate still reports success because the stub accepts both argument forms. This proves a control-flow/configuration mismatch; it does not reproduce a real provider failure or authenticate any endpoint.

Small reproducer: unset `ROUTE_STYLE`; invoke `run_lanes_gated.sh EXECUTE brief_nt.md` with separate qualification and writer argv-recording stubs. Both are supplied by the driver. The raw transcript contains earlier native-path attempts as well as the final `candidate2` attempts; only the latter are used for this finding.


Evidence: `route.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/run_lanes_gated.sh EXECUTE brief_nt.md
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
ASSIGNMENT role=EXECUTE model=opencode-go/deepseek-v4.1-flash provider=opencode-go effort=high
QUALIFICATION_ROUTE style=catalog model=opencode-go/deepseek-v4.1-flash effort=high
  qualification attempt 1/3 PASS
  qualification attempt 2/3 PASS
  qualification attempt 3/3 PASS
QUALIFICATION_PASSED model=opencode-go/deepseek-v4.1-flash effort=high (consecutive_runs=3, two tool round trips each)
PREFLIGHT_CLEAN HEAD=c93a41f
BRIEF_NT__LANE=20261012T131032Z MODEL=opencode-go/deepseek-v4.1-flash provider=opencode-go reasoning=high (declared)
BRIEF_NT_ exit=0 log=/tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/route-logs/hgk-lanes/BRIEF_NT__20261012T131032Z.log
POSTFLIGHT:dirty=0 HEAD=0f9cb53
BRIEF_NT__LANE_DONE
CHILD lane=BRIEF_NT_ index=0 exit=0
LANE_SET_OK lanes=1 model=opencode-go/deepseek-v4.1-flash effort=high

STDERR:

```

Evidence: `route-logs.txt`

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys
for x in pathlib.Path(sys.argv[1]).rglob(\"*.log\"):
 print(\"FILE: \"+str(x));print(x.read_text())" C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\BRIEF_NT__20261012T131032Z.log

STUB argv=-m opencode-go/deepseek-v4.1-flash -c model_provider="opencode-go" -c model_reasoning_effort="high" exec --cd /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2 --sandbox workspace-write --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T130815Z-43181-EXECUTE-r1-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate --sandbox read-only --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T130815Z-43181-EXECUTE-r2-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate --sandbox read-only --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T130815Z-43181-EXECUTE-r3-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate --sandbox read-only --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T131031Z-43690-EXECUTE-r1-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2 --sandbox read-only --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T131032Z-43690-EXECUTE-r2-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2 --sandbox read-only --skip-git-repo-check -



FILE: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\route-logs\hgk-lanes\qual-20261012T131032Z-43690-EXECUTE-r3-opencode-go_deepseek-v4.1-flash.log

Q1_OK

Q2_OK

QUAL argv=-c model=opencode-go/deepseek-v4.1-flash -c model_reasoning_effort="high" -c openai_base_url=http://127.0.0.1:10102/v1 -c model_catalog_json=C:/Users/user/.codex/desktop-model-catalog.json exec --cd /tmp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2 --sandbox read-only --skip-git-repo-check -




STDERR:

```

## Requested harness scripts: actual counts

Only the two explicitly requested harness scripts ran. The product test suite did not run. Both scripts use their own external clones and stubs.

- `run_harness_negative_tests.sh`: **EXIT_CODE=0; pass=15, fail=0**.
- `run_gate_negative_tests.sh`: **EXIT_CODE=0; pass=19, fail=0**.

These are individual assertion counts across T1–T6 and G1–G7, not counts of product tests or proof of complete coverage. Initial setup attempts returned 9 and never reached a result count. All outputs and per-case logs are retained.


Evidence: `harness-tests-final.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/harness/run_harness_negative_tests.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
### T1 dirty preflight is refused (v1 passed this; regression guard)
PASS T1_DIRTY_REFUSED (exit=2)
PASS T1_says_refused
### T2 missing brief: D1a - refuse BEFORE launch, never fail open
PASS T2_MISSING_BRIEF_REFUSED (exit=3)
PASS T2_no_lane_log_written
PASS T2_child_never_launched
### T3 successful run: log really copied in, commit says so, no stray root dir (D3)
PASS T3_STUB_SUCCESS (exit=0)
PASS T3_log_copied_in
PASS T3_commit_states_copy
PASS D3_no_output_dir_at_repo_root
PASS D3_output_dir_is_round_relative
### T4 postflight dirt is REJECTED, not merely printed (D2)
PASS T4_POSTFLIGHT_DIRT_REJECTED (exit=5)
PASS T4_dirt_was_detected
### T5 a non-zero child is propagated, never advertised as success
PASS T5_CHILD_EXIT_PROPAGATED (exit=7)
PASS T5_lane_reports_done
### T6 TMPDIR resolving inside the worktree is refused (F)
PASS T6_TMPDIR_INSIDE_REFUSED (exit=3)

RESULT pass=15 fail=0

STDERR:

```

Evidence: `gate-tests-final.txt`

```text
COMMAND: "C:/Program Files/Git/usr/bin/bash.exe" C:/Users/user/AppData/Local/Temp/pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d/candidate2/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/harness/run_gate_negative_tests.sh
CWD: C:\Users\user\AppData\Local\Temp\pipd-ao5-a6dcec68484d4ed6bd0021cdc7fbfa3d\candidate2
EXIT_CODE: 0
STDOUT:
### G1 a deviating model with NO owner record is refused, zero writers
PASS G1_DEVIATION_REFUSED (exit=6)
PASS G1_names_the_decision
PASS G1_started_no_writer
PASS G1_no_writer_ran
### G2 the SAME deviating model, now named in the owner record, is admitted
PASS G2_AUTHORISED_DEVIATION_RUNS (exit=0)
PASS G2_records_the_deviation
PASS G2_lane_set_ok
### G3 a model that cannot survive qualification is refused before any writer
PASS G3_QUALIFICATION_REFUSED (exit=7)
PASS G3_names_qualification
PASS G3_started_no_writer
### G4 children exiting 0,1,0 must aggregate to a failed lane set
PASS G4_LANE_SET_FAILED (exit=8)
PASS G4_says_nonzero
PASS G4_counts_the_failure
### G5 a child that loses its run receipt is a failure even if it exited 0
PASS G5_MISSING_RECEIPT_FAILS (exit=8)
PASS G5_names_missing_receipt
### G6 an unknown role is refused
PASS G6_UNKNOWN_ROLE_REFUSED (exit=3)
### G7 the assignment model with a working qualification passes end to end
PASS G7_HAPPY_PATH (exit=0)
PASS G7_qualification_passed
PASS G7_no_deviation_notice

RESULT pass=19 fail=0

STDERR:

```

Coverage ceiling: T2 tests missing input, and T5 tests child failure; neither exercises an otherwise successful lane's failed main-log copy. My `copyfail` probe covers that separately. Neither tests the suppressed receipt-copy error or Git-status failure. T2's built-in no-child check searches wrapper output, whereas the stub normally writes to the redirected log; my independent external marker supplies a stronger no-child observation. Gate G5 deletes the main log, causing the child wrapper to return 4 and its receipt to be absent; it cannot isolate the gate's receipt check independently of child failure. The wildcard receipt lookup can match older receipts, as the code and maker's H6 note acknowledge; I did not execute a stale-receipt mutant.


Verbatim source excerpt from `stage-b/run_lanes_gated.sh` (full read: `required-source-read.txt`, EXIT_CODE=0):

```text
  if ! ls "$S/${LANE}"_*.exit >/dev/null 2>&1; then echo "CHILD_RECEIPT_MISSING lane=$LANE"; MISSING=1; fi
```

## NOT_EXECUTED and NOT_SUPPORTED maker claims

This section is intentionally separate. An archived assertion is not accepted as an independently reproduced fact.

| Maker document / claim | Independent disposition and evidence needed |
| --- | --- |
| H1: clean handover fixed by committing artifacts and logging externally | **NOT_SUPPORTED as CLOSED.** Initial manifest dirt contradicts this engagement's clean-handover claim. Require a fresh officer's pre-write clean status and an audited sequence that does not create an in-tree manifest before the child observes delivery. Bounded external logging/preflight behavior is supported by the probes. Historical authorship/timing and the earlier evidence-only closure path sets were not re-audited here. |
| H2: repaired D1/D2/D3/F and test coverage | Supported only for the exact branches measured above. **NOT_SUPPORTED as universal fail-closed enforcement** by R1–R4. The table's T2/T5 evidence does not cover failed main-log copy, and ordinary output placement is not a physical containment proof. Require negative cases for receipt-copy/status failures, existing outside-round index entries, and path aliases. |
| H3: the old `pwd -W ... || pwd` emitted two forms and caused the prior check failure | **NOT_SUPPORTED as independently reproduced historical cause.** Current physical/lowercase check refuses the direct inside path. Require the original host command/exit/stdout and a controlled regression run to establish the old resolver behavior; no such regression was executed here. Symlink/junction/alias containment remains untested. |
| H4: same-second qualification collision and irrecoverably lost first log | **NOT_SUPPORTED independently.** Names now contain role/model/pid/run number in observed logs; collision/destruction/recoverability were not tested. Require original collision trace and inventory/backups; an irretrievably lost transcript cannot be reconstructed as evidence. |
| H5: historical misconfigured route caused provider-not-found; corrected route used identically by gate and writers | Historical provider/model outcomes are **NOT_SUPPORTED as independent executions**. The current identical-route assertion is **contradicted** by R5. Require propagating the role route and comparing qualification/child argv, then authorized real endpoint runs for provider behavior. |
| H5 resolution: assigned lane passed attempt 1, failed attempt 2 with original 400; checker passed 3/3 | **NOT_SUPPORTED by my execution.** Require authenticated original raw attempt logs tied to exact CLI/config/subject and, for a fresh behavioral claim, separately authorized real-model repetitions. I did not invoke either model. |
| H6: earlier helper exited 127; reused receipt made a prior assertion vacuous | **NOT_SUPPORTED as recreated history.** Current scripts visibly use `env` and distinct G5 brief names and pass their assertions. Require prior revision/repro logs to establish historical bug behavior. Their green results do not settle all receipt freshness cases. |
| QUALIFICATION_FINDINGS rates: 3/6 high, 2/6 none, 6/6 backup, 1/1 checker | **NOT_SUPPORTED as my measured rates.** I neither reran models nor independently recounted/authenticated those source transcripts. Need preserved complete logs, per-attempt exits/configs, counting method and provenance; fresh rates require separate permitted repetitions. |
| QUALIFICATION_FINDINGS: both shell calls succeeded, second 547 ms, later 400, 479 tokens | **NOT_SUPPORTED independently.** Need the full cited raw transcript and request/response linkage; no request trace was collected here. |
| QUALIFICATION_FINDINGS: every one of 18 logs has one 426; websocket exonerated / HTTP fallback routine | **NOT_SUPPORTED independently.** Need full log census plus transport trace. Even co-occurrence in passing logs would bound a correlation conclusion, not prove universal transport causality. |
| QUALIFICATION_FINDINGS: model differentiates failure; changing effort does not rescue it / effort is not cause | **NOT_SUPPORTED as a causal conclusion.** Need controlled repetitions and adapter/upstream traces isolating axes. Small sample counts alone do not exclude interaction or effort-dependent behavior. |
| QUALIFICATION_FINDINGS: three consecutive passes reduce false admission probability, each added pass lowers it | **NOT_SUPPORTED quantitatively or causally.** Need a justified dependence model and representative data. My default stub run executes three calls; R4 shows the positive-count requirement can be bypassed. |
| QUALIFICATION_FINDINGS: real-lane EXECUTE refusal at 2/3 and VERIFY admission at 3/3 | **NOT_SUPPORTED as this officer's execution.** Need intact `REAL_QUALIFICATION_3CONSEC.txt` and referenced raw logs with provenance or separately authorized replay. Stubs do not establish real model behavior. |
| Assignment described as immutable; owner record described as authorization | **NOT_SUPPORTED as authenticated immutable policy or owner identity.** I read local policy inputs and exercised parsing only. Need independent policy integrity and genuine owner provenance. The maker's own unauthenticated upstream-model and untested mechanistic-lead limits remain limits here. |

**NOT_EXECUTED:** real Codex/model/API/relay calls; genuine two-tool model round trips; model identity authentication; upstream request/adapter tracing; recreation of historical model failures/rates/collision/tool-helper bugs; product test suite; build/package/plugin correctness review; release acceptance; vendor validator; portal/account/host UAT; public publication; remote readback; push/tag/merge; live races or stress tests; symlink/junction/drive-alias escapes; actual disk/permission failure as opposed to deterministic copy/status injection; stale-receipt attack; seal revalidation; re-audit of prior closure commit path sets or every prior-round claim. No production source edits or delivery Git mutations were performed. No claims outside this handover/enforcement question are granted acceptance.

The documents themselves say intermittency mechanism and upstream identity are unexplained, and the preservation-list lead remains untested. I did not test those hypotheses or promote them to findings. Existing logs, local field strings, owner-shaped text and model self-report are not authentication.

## Verdict limits and delivery preservation

I cannot authenticate any model identity. A clean Git status is not code correctness; it omits ignored files and empty directories and is only an instant observation. Passing tests are not release acceptance. Fault injection proves error-path control flow under stated seams, not the frequency of real infrastructure failures. Stub qualification markers do not prove actual tool round trips. This verdict grants no release, merge, publication, product-security or host-qualification approval.

Delivery HEAD/tree stayed at the recorded subject. Individually captured index and tracked-diff commands remained empty. Final status still shows the initial manifest plus my allowed `verify/ao5/`. I did not remove the maker's dirt to manufacture closure.


Evidence: `final-delivery-head.txt`

```text
COMMAND: git rev-parse HEAD
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d

STDERR:

```

Evidence: `final-delivery-tree.txt`

```text
COMMAND: git rev-parse HEAD^{tree}
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
d8fe6480f5107bcb01a045783c36b2cd536662c3

STDERR:

```

Evidence: `final-delivery-index.txt`

```text
COMMAND: git diff --cached --name-status
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:

STDERR:

```

Evidence: `final-delivery-tracked.txt`

```text
COMMAND: git diff --name-status
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:

STDERR:

```

Evidence: `final-delivery-status.txt`

```text
COMMAND: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao5/

STDERR:

```

**Final adjudication:** A = **STILL_NOT_CLOSED** for the actual handover. B = **bounded repairs demonstrated, universal enforcement rejected**: launcher statuses 0 over receipt-copy return 23 and Git-status returns 128 are explicit remaining fail-open paths; the zero-attempt gate also returns 0 without qualification. The maker's all-fixed assertion must not be accepted at a higher ceiling than these observations.

## Verbatim maker-document readback

The unsupported-claim inventory above refers to these original assertions; they are quoted as claims, not accepted as facts.

```text
COMMAND: C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import pathlib,sys
for x in sys.argv[1:]:
 print(\"FILE: \"+x);print(pathlib.Path(x).read_text(encoding=\"utf-8\"))" C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\harness\HARNESS_DEFECT_LOG.md C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\harness\QUALIFICATION_FINDINGS.md
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
FILE: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\harness\HARNESS_DEFECT_LOG.md
# Harness defect log - round S4POST-20261012

Every defect below was found by running something, not by reading the code. Two of them were found by
the independent officer; two by using the new tools for real; one is a **false positive I produced and
then had to retract**. Kept because a harness that reports its own errors is the only kind worth
trusting, and because the retraction is the most instructive entry here.

## H1 - the handover was dirty by construction (found by the round-3 officer, verdict NOT_CLOSED)

- **Symptom**: every officer was handed a worktree carrying the harness's own brief, runner and lane log.
- **Cause**: the harness wrote its artifacts into the very worktree it then handed to the officer.
- **Fix**: `run_lane.sh` commits harness artifacts first, refuses to launch against a dirty worktree, and
  writes the lane log outside the worktree.
- **Evidence**: the officer independently confirmed the substantive closure (every path in the closure
  commits is under `.hgk/rounds/`, no code path changed) and rejected only the cleanliness promise.

## H2 - the launcher failed open three ways (found by the round-4 officer, verdict PARTIAL)

| ID | Demonstrated defect | Fix | Test |
|---|---|---|---|
| D1 | a missing brief and a failed log copy were masked; the wrapper exited 0 while its own child had failed, and still committed a message claiming the log had been copied in | validate the brief before launch; check the copy; state in the commit message whether a log was really copied; propagate the child status | T2, T5 |
| D2 | postflight detected dirt, printed `POSTFLIGHT:dirty=1`, and still exited 0 | detected dirt is a failure (exit 5) | T4 |
| D3 | `mkdir -p "$WT/$OUTSUB"` created the officer output directory at the **repository root**, outside the round's write set, so the round-relative fallback never ran | round-relative only, and `..`/absolute paths refused | T3 |

It also recorded that `TMPDIR` was never validated against the worktree; now refused (T6).

## H3 - the containment check could not fire (found while testing H2's fix)

- **Symptom**: T6 failed; a log directory inside the worktree was accepted.
- **Cause**: `pwd -W 2>/dev/null || pwd` printed **both** forms on this host - the `-W` form on stdout and
  then, because that form still returned nonzero, the plain form as well. The captured value carried two
  lines, so the `"$WTRES"/*` prefix test could never match.
- **Fix**: one normalising resolver (`cd ... && pwd -P`, lowercased) for both sides, with an explicit
  refusal when either side cannot be resolved.
- **Test**: T6 now passes and would fail again if the resolver regressed.

## H4 - the qualification log overwrote itself (found while using the gate)

- **Symptom**: two qualifications in the same wall-clock second wrote the same path; the second destroyed
  the first one's evidence, which is exactly the evidence I needed.
- **Fix**: the name carries role, sanitised model and pid.
- **Consequence**: the first EXECUTE qualification's raw log is **lost**, and it was not recoverable from
  anywhere else. It is not reconstructed or paraphrased anywhere in this round.

## H5 - the false positive, and the retraction (the important one)

- **What I did**: built the admission gate with the invocation `-m <model> -c model_provider="opencode-go"`.
- **What happened**: `Error: Model provider 'opencode-go' not found`. The gate reported
  `QUALIFICATION_FAILED` and refused, so it looked like the gate had reproduced the original lane failure.
- **What I claimed on that basis**: that the gate independently reproduced the assigned lane's failure,
  and that the assigned model cannot survive a two-tool round trip.
- **Why that claim was wrong**: `opencode-go/...` is a **model catalog slug**, not a provider id. The
  invocation the writers actually used is `-c model=<slug>` together with `openai_base_url` and
  `model_catalog_json`, with no `model_provider`. My gate therefore tested **my own misconfiguration**.
  The refusal was not evidence about the model at all.
- **Correction**: the route is now declared per role in `ROUND_ASSIGNMENT.json`, and both the gate and the
  launcher build the invocation from it, so the qualification and the writers use the identical route.
- **Result after the correction**: the assigned model
  (`opencode-go/deepseek-v4.1-flash`, effort `high`, catalog route) **PASSES** the two-tool round trip -
  `QUALIFICATION_PASSED`, `EXECUTE_QUALIFY_EXIT=0`, transcript at
  `verify/harness/qualification_logs/`.
- **The lesson, stated plainly**: a gate that fails closed on its own misconfiguration is worse than no
  gate, because it manufactures authoritative-looking refusals. Fail-closed protects against a bad lane;
  it does not protect against a bad test. Any refusal must name the exact configuration it refused, and a
  refusal that the operator cannot reproduce by hand is a harness bug until proven otherwise.

### H5 resolution

After the route was corrected the gate was run again requiring three consecutive passes. The assigned
lane passed attempt 1 and was rejected at attempt 2 with the original 400; the checker lane passed 3 of 3.
So the gate refuses the assigned lane, for a reason it measured rather than one it misconfigured - and
Correction 1 in `ACCEPTANCE_RECORD_STAGEB.md` over-corrected in the other direction and is itself
superseded by Correction 2. See `QUALIFICATION_FINDINGS.md`.

## H6 - two test-harness bugs of my own (cosmetic, recorded for completeness)

- the gate test helper built its command with a bare `"$@"` expansion of `NAME=VALUE` assignments, so every
  case exited 127; `env` is required.
- the receipt-isolation case re-used brief names from an earlier case, whose committed receipt made the
  assertion vacuous; it now uses unique brief names.

FILE: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt\.hgk\rounds\S4POST-20261012-postrepair-recheck-and-triple-upgrade\verify\harness\QUALIFICATION_FINDINGS.md
# Qualification findings: what actually breaks, and how often

Measured with the corrected route (`-c model=<slug>` plus `openai_base_url` and
`model_catalog_json`, no `model_provider`), the identical no-write qualification brief, and the identical
CLI. Raw transcripts: `C:\Users\user\AppData\Local\Temp\qual-repeat\`. Raw run text:
`QUALIFICATION_FLAKINESS.txt`, `QUALIFICATION_MATRIX.txt`.

## The rates

| Configuration | Passes | Two-tool round trips attempted |
|---|---|---|
| assigned model `opencode-go/deepseek-v4.1-flash` at effort `high` | 3 | 6 |
| assigned model `opencode-go/deepseek-v4.1-flash` at effort `none` | 2 | 6 |
| backup model `opencode-go/deepseek-v4-flash` at effort `high` | 6 | 6 |
| checker model `gpt-6.1-sol` at effort `medium`, openai route | 1 | 1 |

Six attempts per configuration is a small sample. These are counts, not reliabilities; do not read
"3 of 6" as "50% reliable".

## What the failure is, exactly

The assigned model's failing runs are **not** a failure to use tools. In
`r_opencode-go_deepseek-v4.1-flash_high_1.log` both shell calls succeeded (the second in 547 ms) and the
rejection then landed on the **next** request:

```
Provider error 400: Upstream request failed: [invalid_request_error]
The `reasoning_content` in the thinking mode must be passed back to the API.
```

`tokens used 479`. So the trigger is not transcript size, not the first turn, and not tool use as such.
It is the continuation request **after a second tool result**, in thinking mode.

## The websocket 426 is exonerated by the same data

Every one of the 18 repeat logs contains exactly one
`ERROR codex_api::endpoint::responses_websocket: failed to connect to websocket: HTTP error: 426 Upgrade
Required`, including **all** the passing runs, including the 6/6 clean backup column. The local relay
refuses the websocket and the client falls back to HTTP; that is routine here, and it is not the failure.
This is direct positive evidence for the FAR study's refutation of the 426 hypothesis.

## Axis separation

- **Model axis**: at the same effort (`high`) and the same route, the assigned model passed 3 of 6 and the
  backup model passed 6 of 6. The model is the differentiating factor in this sample.
- **Effort axis**: the assigned model failed at both `high` (3 of 6) and `none` (2 of 6). Changing the
  effort does not rescue it, so the operator's original mixed change (model **and** effort) was not
  required to escape the failure. This is the control the FAR study recorded as NOT_SEPARABLE; it is now
  separable, and the effort axis is not the cause.

## Consequence for the gate, and the repair

A single qualification is a sample of an intermittent fault, so one pass proves very little: the failure
appeared on roughly half of attempts. `run_lanes_gated.sh` now requires **`GATE_QUALIFY_RUNS`
consecutive passes (default 3)** and aborts the lane set on the first failed attempt. With the measured
per-attempt failure rate, one run would have admitted the lane on about half of attempts; three
consecutive passes make that far less likely, and each additional required pass lowers it further.

The honest limit: this raises the cost of a false admission, it does not eliminate it, and the required
count should be raised where a false admission is expensive. The gate is a filter, not a proof.

## What is still not explained

- **Why it is intermittent.** Nothing here identifies whether the adapter drops `reasoning_content` under a
  race, a retry, or a specific interleaving. The upstream message is a requirement statement, not a cause.
- **What the upstream model actually was.** Still unauthenticated. A flaky lane is not evidence of a
  substituted model, and a healthy lane is not evidence of the assigned one.
- The mechanistic lead from the FAR study - the slug being absent from the relay and registry
  reasoning-content preservation lists - remains untested, and is now the most specific thing to test,
  because a list-driven gate would explain an intermittent, model-specific, size-independent failure.

## The gate demonstrated on the real lanes

One invocation of the gate, requiring 3 consecutive passes, against both roles at the same moment:

```
EXECUTE  model=opencode-go/deepseek-v4.1-flash effort=high
  qualification attempt 1/3 PASS
QUALIFICATION_FAILED ... attempt=2/3 exit=1
GATE_REFUSED_NO_WRITERS_STARTED          EXECUTE_QUALIFY_EXIT=7

VERIFY   model=gpt-6.1-sol effort=medium
  qualification attempt 1/3 PASS
  qualification attempt 2/3 PASS
  qualification attempt 3/3 PASS
QUALIFICATION_PASSED (consecutive_runs=3, two tool round trips each)   VERIFY_QUALIFY_EXIT=0
```

This is the point of the gate: the intermittency shows up **inside** a single gate invocation - attempt 1
clean, attempt 2 rejected - and the flaky lane is refused before any writer starts, while the sound lane is
admitted. Record: `REAL_QUALIFICATION_3CONSEC.txt`.


STDERR:

```

## Post-report delivery readback

These observations were collected after report creation.

```text
COMMAND: git rev-parse HEAD
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
c93a41fb07ced91519bdb17e9cb1536bb1a5ac1d

STDERR:

```

```text
COMMAND: git rev-parse HEAD^{tree}
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
d8fe6480f5107bcb01a045783c36b2cd536662c3

STDERR:

```

```text
COMMAND: git status --porcelain
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b/AO5_20261012T130513Z.manifest
?? .hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao5/

STDERR:

```

```text
COMMAND: git diff --cached --name-status
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:

STDERR:

```

```text
COMMAND: git diff --name-status
CWD: C:\Projects\Agent_Workspace\PIPD\worktrees\s4post-b-wt
EXIT_CODE: 0
STDOUT:

STDERR:

```

