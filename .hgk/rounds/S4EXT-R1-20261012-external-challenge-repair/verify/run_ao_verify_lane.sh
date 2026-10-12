#!/usr/bin/env bash
# S4EXT-R1 -- Independent Acceptance Officer / VERIFY + SECURITY lane.
#
# Owner steer: the checker lane runs on the Codex CLI with checker model GPT 6.1 SOL-MEDIUM over
# OpenAI OAuth (auth_mode=chatgpt), inside an ISOLATED CODEX_HOME so the checker cannot inherit the
# maker's session state. The checker is READ-ONLY against the frozen candidate: a non-mutation guard
# records the candidate's `git status --porcelain` and HEAD tree before and after the run.
set -u

MAKER="C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt"
ROUND="$MAKER/.hgk/rounds/S4EXT-R1-20261012-external-challenge-repair"
VDIR="$ROUND/verify"
CAND="C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-verify"
BRANCH="fix/s4-external-challenge-20261012-r1-provenance-trace"
EXPECT_COMMIT="268ad6b10edef215b4f084514b28481e32a121bc"
EXPECT_TREE="$(git -C "$MAKER" rev-parse "refs/heads/$BRANCH^{tree}" 2>/dev/null)"
# The lane was proven with this build: its exec wrapper resolves codex-code-mode-host.exe,
# which sits beside it. The HG-KSEOS runtime build lacks that host binary and every shell
# call in the checker dies with "missing codex-code-mode-host.exe (os error 2)".
CODEX="C:/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe"
# The lane's DECLARED checker model (owner steer) is gpt-6.1-sol / medium over OpenAI OAuth.
# Deviation D-01 (recorded, not silent): on 2026-10-12 the provider answers
#   HTTP 400 invalid_request_error "The 'gpt-6.1-sol' model is not supported when using Codex
#   with a ChatGPT account." for EVERY attempt, including with a freshly authenticated home, so the
# declared model is unserviceable on the mandated OAuth path right now. Per the standing rule
# (refusal -> continue on the sibling in the same lane, do not pause) the checker runs on the
# closest same-family sibling that the account actually serves: gpt-5.6-sol, reasoning medium.
DECLARED_MODEL="gpt-6.1-sol"
CHECKER_MODEL="${CHECKER_MODEL:-gpt-5.6-sol}"
CHECKER_HOME="C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/s4ext/checker-sol"
BRIEF="$VDIR/AO_VERIFY_BRIEF.md"
mkdir -p "$VDIR"

# --- fresh, isolated candidate checkout of exactly what was PUSHED -------------
rm -rf "$CAND"
git clone -q --branch "$BRANCH" --single-branch "$MAKER" "$CAND" 2>"$VDIR/clone.stderr" \
  || git clone -q --branch "$BRANCH" --single-branch "https://github.com/shw097-team/PIPD-LS-SP.git" "$CAND" 2>>"$VDIR/clone.stderr"
echo "CLONE_EXIT=$?" | tee "$VDIR/clone.exit"
git -C "$CAND" rev-parse HEAD        > "$VDIR/SUBJECT_COMMIT.txt"
git -C "$CAND" rev-parse 'HEAD^{tree}' > "$VDIR/SUBJECT_TREE.txt"

# --- non-mutation guard: BEFORE -----------------------------------------------
git -C "$CAND" status --porcelain=v1 > "$VDIR/NONMUTATION_STATUS_before.txt"
if [ "$(cat "$VDIR/SUBJECT_COMMIT.txt")" != "$EXPECT_COMMIT" ]; then
  echo "SUBJECT_MISMATCH expected=$EXPECT_COMMIT actual=$(cat "$VDIR/SUBJECT_COMMIT.txt")" | tee "$VDIR/VERIFY_LANE_EXIT.txt"
  exit 3
fi

cat > "$BRIEF" <<'BRIEF_EOF'
You are the **Independent Acceptance Officer** for one bounded repair round. You are NOT the maker:
you did not write this code, you must not modify it, and you must not accept it on the maker's word.

## Hard rules (violating any of these voids your verdict)

1. **READ-ONLY on the candidate.** Do not create, edit, delete, move or `git add/commit/checkout`
   anything inside the repository you are verifying. `git status --porcelain` must be empty when you
   finish; a non-mutation guard records it before and after.
2. **No network writes.** No `git push`, no tag creation, no releases, no issues, no PRs.
3. **Raw evidence over summaries.** Every verdict line must cite the exact command you ran and its
   real output. If you did not run it, say `NOT_RUN` — never mark it PASS.
4. **Try to falsify, not to confirm.** For each claim below, first attempt the counterexample.
5. Write your machine-readable verdict to
   `C:/Projects/Agent_Workspace/PIPD/worktrees/s4ext-r1-wt/.hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/verify/AO_VERDICT.json`
   (the directory that holds this brief; it is OUTSIDE the candidate checkout). Write NOTHING
   inside the candidate.

## Subject under test

* repository root: the current working directory (a fresh clone of the pushed repair branch)
* branch: `fix/s4-external-challenge-20261012-r1-provenance-trace`
* candidate commit: `268ad6b10edef215b4f084514b28481e32a121bc`
* contract: `PIPD-S4EXT-R1-REPAIR-ROUTEOUT/1`, report id
  `PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1`
* the published (defective) subject for contrast: tag `v0.1.1-preview.3` → commit
  `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`

The maker claims, and you must independently confirm or refute:

| # | claim |
|---|---|
| C1 | all 8 mount-pack documents under `dist/mount/pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.3/` name the tuple's `release_tag_target` as the release identity, and the stale value `8faa64e5…` survives only on lines that explicitly disclose it |
| C2 | the PUBLISHED Web ZIP is byte-identical to its release metadata digest, i.e. the repair did NOT rewrite the published artefact |
| C3 | `validate --bundle` refuses a trace bundle whose endpoints are mis-typed, orphaned, or carry a wrong 64-hex hash, with a non-zero exit — while a legal bundle still validates |
| C4 | the same counterexample PASSES on the released wheel, so the defect classification ("runtime false PASS") is not overstated |
| C5 | the full deterministic test suite is green on this candidate |
| C6 | the 57-row SPEC/DEL adjudication upgrades no status, does not treat `DESIGN_ONLY` rows as implemented, and treats `DEL-008` as not S4-blocking |
| C7 | nothing in the tree claims S4 pass, release or production verification; the claim ceiling stays maker-candidate-only |
| C8 | no secret, token or credential is present in the tree, and the git history scan is clean |

## Method

* `python -m unittest discover -s tests -t .` from the repository root (report the exact `Ran N`/verdict).
* For C3/C4 build the bundles yourself in a scratch dir OUTSIDE the repository (use the system temp
  dir); read `src/pipd_ls_sp/validate.py` and `src/pipd_ls_sp/pipeline.py` to understand the closure
  states, then re-derive the counterexample from first principles rather than trusting the maker's
  scripts. The maker's own probes are in `.hgk/rounds/S4EXT-R1-20261012-external-challenge-repair/raw/`
  and `.../evidence/` — you may read them for cross-checking, but your verdict must come from YOUR run.
* `tools/deny_list_scan.py` and `tools/history_secret_scan.py` for C8.
* `git rev-parse v0.1.1-preview.3^{commit}` and `sha256sum` for C1/C2.
* If something cannot be executed here (no network, missing host), mark it `NOT_RUN` with the reason.

## Output format

1. A short human summary (<= 30 lines): what you ran, what you found, what you could NOT establish.
2. A fenced ```json block containing exactly:

```json
{
  "verdict": "PASS_CHALLENGE | FAIL_CHALLENGE | PARTIAL_CHALLENGE",
  "subject_commit": "...",
  "subject_tree": "...",
  "claims": [{"id": "C1", "verdict": "PASS|FAIL|PARTIAL|NOT_RUN", "command": "...",
              "observed": "...", "counterexample_attempted": "..."}],
  "blocking_findings": [],
  "non_blocking_findings": [],
  "maker_claim_ceiling_respected": true,
  "independent_of_maker": true,
  "candidate_mutated": false,
  "what_this_verdict_is_not": "a release authorization, a tag approval, or a production claim"
}
```

Write the same JSON to that same absolute `AO_VERDICT.json` path. Be specific and adversarial; a polite summary is
worthless. If a maker claim is unsupported, say FAIL and show the command that shows it.
BRIEF_EOF

unset OPENAI_BASE_URL OPENAI_API_KEY
export CODEX_HOME="$CHECKER_HOME"
export PYTHONDONTWRITEBYTECODE=1
export GIT_TERMINAL_PROMPT=0

LOG="$VDIR/AO_VERIFY_${CHECKER_MODEL}.exec-$(date -u +%Y%m%dT%H%M%SZ).log"
{ echo "declared_checker_model=$DECLARED_MODEL (unserviceable: HTTP 400 model-not-supported on ChatGPT auth)";
  echo "actual_checker_model=$CHECKER_MODEL";
  echo "reasoning_effort=medium"; echo "auth_mode=chatgpt (OpenAI OAuth)";
  echo "codex_cli=$("$CODEX" --version 2>/dev/null)";
  echo "deviation_id=D-01"; } > "$VDIR/MODEL_SUBSTITUTION.txt"
# The model is pinned in the isolated CODEX_HOME config.toml: this codex build rejects
# "-m <model> <prompt>" in `exec`, and stdin is the invocation form the lane proved earlier.
timeout 2700 "$CODEX" exec --cd "$CAND" --skip-git-repo-check -s danger-full-access - < "$BRIEF" > "$LOG" 2>&1
echo "VERIFY_LANE_EXIT=$?" | tee "$VDIR/VERIFY_LANE_EXIT.txt"

# --- non-mutation guard: AFTER ------------------------------------------------
git -C "$CAND" status --porcelain=v1 > "$VDIR/NONMUTATION_STATUS_after.txt"
{
  echo "=== NON-MUTATION GUARD (independent checker, read-only candidate) ==="
  echo "candidate      : $CAND"
  echo "expected commit: $EXPECT_COMMIT"
  echo "actual commit  : $(git -C "$CAND" rev-parse HEAD)"
  echo "expected tree  : $EXPECT_TREE"
  echo "actual tree    : $(git -C "$CAND" rev-parse 'HEAD^{tree}')"
  echo "--- status before ---"; cat "$VDIR/NONMUTATION_STATUS_before.txt"
  echo "--- status after  ---"; cat "$VDIR/NONMUTATION_STATUS_after.txt"
  if [ ! -s "$VDIR/NONMUTATION_STATUS_after.txt" ] \
     && [ "$(git -C "$CAND" rev-parse HEAD)" = "$EXPECT_COMMIT" ] \
     && [ "$(git -C "$CAND" rev-parse 'HEAD^{tree}')" = "$EXPECT_TREE" ]; then
    echo "NON_MUTATION_VERDICT=PASS"
  else
    echo "NON_MUTATION_VERDICT=FAIL"
  fi
} | tee "$VDIR/NONMUTATION_GUARD.txt"
