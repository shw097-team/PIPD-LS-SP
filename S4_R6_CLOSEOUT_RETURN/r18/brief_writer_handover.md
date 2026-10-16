HGK_LANE_NONCE_OK

# EXECUTE BRIEF — bounded writer (S4 R6 / R18 external-engineering handover)

## Lane contract and scope

- Work order: `WO-TS-R18-05` (Package and delivery, project `PIPD-S4R6-R18`). The publication itself is
  performed by the orchestrator under that work order; you write files and nothing else.
- You are a **bounded writer**. You may create or modify ONLY these two paths, both relative to the
  repository root given below:
  - `S4_R6_CLOSEOUT_RETURN/EXTERNAL_ENGINEERING_HANDOVER.md` (create)
  - `S4_R6_CLOSEOUT_RETURN/ROUND_STATE.json` (create)
  Do NOT touch any other file. Do NOT run git commands that change state (no add, commit, checkout,
  branch, push, stash). Do NOT push anything anywhere. Reading git history is fine.
- Repository root (a git worktree, currently on branch `r6-closeout-evidence-20261016`):
  `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`

## Why these two files

The round's product change lives on a different branch and is already green. What is missing is the path
an **external engineering team** takes to continue development. Your job is to write that path down, so
that a reader who has never seen this repository can (a) understand the branch model, (b) not break the
governed gates, (c) build and test, (d) find where new work goes, and (e) know what is forbidden.

## Ground truth you MUST read first

Read these before writing, and derive every fact from them rather than from this brief:

1. `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/r18/REPO_RECON.md`
   — the evidence-located repository reconnaissance (tree layout, package layout, test command and its
   real result, build tooling, the two CI workflows including the write-set classifier and the declared
   `ALLOWED` regex, docs layout, `RELEASE_TUPLE.json` shape, extension points). **This is your primary
   source.** If a fact you need is not in it, verify it yourself with a read-only command and cite the
   command you ran.
2. `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/S4_R6_CLOSEOUT_RETURN/R17_RED_GATE_DIAGNOSIS.md`
   — the write-set gate failure this round's predecessor hit, why the evidence lives on its own branch,
   and the amendment rule including the planted-path self-test requirement.
3. `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/S4_R6_CLOSEOUT_RETURN/R17_MEASUREMENTS.json`
   — the measured numbers (test counts, digests, the checker's verdict (a checker separated by process/lane/evidence path only - the model is identical, see CURRENT_SUBJECTS.md) and its ceiling).
4. `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/far-r17/SESSION_CLOSEOUT_AND_HANDOVER.md`
   — the round's checkpoint: branch tips, open tickets, owner decisions in one-action form, rollback
   pointers, and the disclosed side effects.

## What the handover document must contain (all seven, in this order)

1. **What this repository is and what state it is in**, in a short factual opening: what the plugin is,
   which release is published and immutable, which commit the candidate adds, and the claim ceiling.
2. **Branch model.** Which branch carries the product change, which carries the round's evidence, and
   **why** they are separate (the governed product write set). Give the exact tip SHAs and say what a
   contributor should branch from.
3. **The governed write-set gate.** The declared stage, what it measures
   (`git diff --name-only <declared base>...HEAD` against a positive allowlist), the exact `ALLOWED`
   regex for the declared stage, the local reproduction command and how to read its verdict, the
   planted-path self-test, and the amendment rule (one named path alternative, self-test updated in the
   same commit, disclosed in the pull request). Include the *measured* consequence: what happens if you
   put round artifacts on the product branch.
4. **The lane model.** The ordered candidate pool per role; the fact that the pool's rank 1 for the
   verification role is the writer's own model **by owner order** (so an unpinned dispatch silently
   loses separation of duties); how to pin an arm by identity; and that the registry is never edited by
   the round that measures it.
5. **Build and test.** The exact commands, with their expected output — the full-suite command and its
   measured result, the focused commands, how a wheel and the public plugin ZIP are produced, and which
   CI workflows run on which paths.
6. **Module map and extension points.** Where a new check, a new tool, a new skill and a new
   documentation page go, derived from the recon; plus the repository's own house style for a new test
   file (the `sys.path` bootstrap and anything else a sibling carries) so a newcomer's first test lands
   correctly.
7. **Open tickets, owner gates and prohibitions.** Each open ticket in one line; each owner-gated item
   stated as a single action with the reason it is not an agent's to take; and the standing
   prohibitions (never edit a published release asset in place, no public directory publication, no
   agent self-ratification of a stage close, no claim of full-pass/host-qualified/production).

## Rules for what you write

- **Every factual claim carries a locator**: a fenced command a reader can run, or a `path:line`
  reference. A sentence that asserts a number, a path, a digest or a gate outcome without one is a
  defect — either give it a locator or drop the sentence.
- **Never invent** a path, a command, an output, a version, a digest or a CI result. If something is
  absent, write `ABSENT` and say where you looked. If you cannot verify a claim, omit it.
- **Do not overstate.** This repository's candidate is not merged, not released and not host-qualified.
  Say so where a reader could otherwise infer otherwise.
- Write in **English** for the handover document (its audience is an external engineering team), with
  Traditional-Chinese identifiers left intact where they name a governed artifact.
- Keep it dense and skimmable: headings, short tables, fenced commands. No marketing prose.

## `ROUND_STATE.json` — required shape

A single JSON object (UTF-8, LF endings, 2-space indent) with at least:
`round`, `generated_from` (the locators you derived it from), `subjects` (per branch: `branch`, `commit`,
`tree`, `role`), `immutables` (release tag, tag object, tag target, asset count, and an explicit
`unchanged: true` plus how you checked it), `gates` (each gate name with its observed state and the
locator), `tickets` (array of `{id, what, owner_action}`), `prohibitions` (array of strings),
`claim_ceiling` (one string stating what the state document does and does not attest), and
`self_binding` — since a document cannot carry its own hash, set `self_binding` to the literal string
`git-blob` and add a note that the integrity binding is the git object that carries the file.
Every SHA you put in it must be readable from the repository at the moment you write it; run the
read-only command and copy the value from its output rather than from this brief.

## Output

When finished, print a short report: the two paths, their byte sizes and line counts, and — for the
handover document — a list of every command you embedded (so the orchestrator can have them
independently re-run). State plainly anything you could NOT verify.

The final line of your reply must be exactly `HGK_LANE_NONCE_OK` and nothing may follow it.
