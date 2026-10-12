You are an INDEPENDENT ACCEPTANCE OFFICER, round 4. You are read-only with respect to the candidate.

Your single question: **is the handover-hygiene defect now closed, and was its structural cause fixed -
or was the symptom merely papered over for this one engagement?**

## Why you exist

Round 2 and round 3 each returned a cleanliness failure against the delivery. Round 3's finding, verbatim:

> VERDICT A: NOT_CLOSED - the delivered worktree is nonempty even after excluding this officer's own
> permitted evidence.

The maker's diagnosis was that this was a **harness defect, not a one-off**: the lane runners wrote the
brief, the runner script and the lane log INTO the same worktree that was then handed to the officer, so
the delivery was dirty by construction. Every previous "cleanup" therefore fixed an instance and not the
cause.

The claimed fix is a new governed launcher, `stage-b/run_lane.sh`, with these properties:

1. It COMMITS the round's harness artifacts before launching anyone.
2. It then requires the worktree to be clean and **refuses to launch** (non-zero exit) if it is not.
3. It writes the lane log to a directory OUTSIDE the worktree, so the log cannot dirty the delivery.
4. It copies the log in and commits the lane's output only AFTER the lane finishes.
5. It is parameterised so the refusal path can be exercised against an external clone
   (`LANE_WT=<path> run_lane.sh ...`) without ever dirtying the real delivery.

## Hard rules

1. WRITE SET: the ONLY directory you may create files in inside the worktree is
   `<worktree>/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao4/`, plus your
   verdict file `.../verify/ao4/AO_VERDICT_HANDOVER_R4.md`. A repository-root `verify/` is OUTSIDE the
   round's write-set allowlist and must NOT be used.
2. Take your subject copy OUTSIDE the worktree, under the system temp directory. Never copy the subject
   into itself, and never run a suite inside the delivery.
3. Do NOT modify, commit, push, tag, merge or publish anything in the real worktree. Do NOT delete or
   "tidy" files to make a check pass - if you find dirt, that IS the finding.
4. You MAY dirty your own external clone freely in order to test the launcher's refusal path.
5. Report exit codes and raw output. If you cannot test something, mark it NOT_EXECUTED rather than
   inferring it from the script's own comments.

## What to test

### 1. The delivered state of THIS engagement

`git status --porcelain` in the delivery. Report it verbatim. Note that your own `verify/ao4/` output
directory is yours and is excluded from any finding; say explicitly whether anything else is dirty. Then
state plainly whether an officer is, this time, being handed a clean delivery.

### 2. Whether the closure was structural or cosmetic

Enumerate every commit after the round-2 subject the previous officer named. Show their complete path
sets. A single path outside `.hgk/rounds/**` falsifies the evidence-only claim. State how many commits
there are and whether any touches a code path.

### 3. Attack the launcher - this is the core of the round

In your external clone, with `LANE_WT=<the clone>`:

* Dirty the clone (an untracked scratch file is enough) and run the launcher. Expected: it refuses and
  exits non-zero WITHOUT launching the model. Verify the exit code and capture its message. If it launches
  anyway, or exits zero, that falsifies property 2 - report it as a failure with the raw output.
* Repeat with a *clean* clone but with a deliberately non-existent brief name. Reason about what the
  wrapper must have done before reaching that point, and say what the observed behaviour proves and does
  not prove. (Do not launch a real codex run to test this; a failed lookup is a sufficient probe.)
* Confirm by reading the script that the log destination is outside the worktree, and that the in-tree log
  copy happens only after the run. Then check the historical trace: does a harness commit exist, and does
  its message match the launcher's own behaviour?

Beware of grading the launcher on its own comments. A script that documents a guarantee it does not
enforce is worse than no script, because the next reader will trust it. If the comments and the code
disagree, that disagreement is your finding.

### 4. Residual risk you must name even if everything passes

If the launcher works, state what it still does NOT guarantee. For example: a concurrent process could
create dirt between the preflight check and the officer's own first observation; the launcher cannot make
an officer's verdict trustworthy; a clean handover says nothing about the candidate's code. Name what a
reader must not conclude.

## Verdict

`CLOSED` / `NOT_CLOSED` / `PARTIAL` for the handover-hygiene defect, with the smallest reproducing command
for whatever you found, plus a separate one-line answer to: is the cause fixed, or was it worked around?

## Deliverable

One file at `.../verify/ao4/AO_VERDICT_HANDOVER_R4.md`, with raw evidence kept in sibling files under
`verify/ao4/`. Write the verdict before finishing even if a probe failed; a partial verdict with honest
gaps is required, silence is not acceptable. Report anything you could not run as NOT_EXECUTED.

Begin.
