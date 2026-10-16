HGK_LANE_NONCE_OK

# VERIFY BRIEF — independent replay under WorkOrder `WO-TS-R18-04`

You are the **checker**. Read-only replay. You did not write any of the bytes you are about to judge.
The maker was a bounded writer on lane EXECUTE (`opencode-go/deepseek-v4.1-flash`). **Your arm is
`opencode-go/deepseek-v4.1-flash` as well** — the same model, by owner order (registry SOD006-C3,
OWNER_ORDERED_IN_FORCE) after the GPT quota constraint. Model-axis independence between writer and
checker is therefore ABSENT and is not claimed; what remains is PROCESS, LANE and EVIDENCE-PATH
independence plus the no-self-acceptance rule. Say so in your verdict rather than implying otherwise.

## Subjects (frozen; do not modify anything)

- Product branch `fix/s4r6-closeout-doc-identity-and-update-route-20261016`, head
  `c17aa761b26033fc0a2a2aa3df5ad0f61f2e5a20`, in the git worktree `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`.
- Evidence branch `r6-closeout-evidence-20261016`, head `338227c78a121db9847dff2574918bdcb2bfbdc2`.
- The round's governing documents and the audit/ruling tables are under
  `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/`.
- A Python interpreter with `jsonschema` for the test runs: use the repository's own invocation; do
  NOT create or modify any file inside the worktree.

## Claims to adjudicate (C1–C6)

**C1.** At `c17aa76`, `docs/install/README.md` no longer contains the dead outgoing link: the string
`](RELEASE_TUPLE.json)` is absent and `](../RELEASE_TUPLE.json)` is present exactly where the page tells
a reader that the release identities live in `docs/RELEASE_TUPLE.json`. Independently: resolve every
relative markdown link in that page against the tree at `c17aa76` using your own code — do not reuse
the repo's test helper — and report every target that does not exist.

**C2.** The new guard check is FALSIFIABLE, not decorative. Read
`tests/test_r6_doc_identity_guard.py` at `c17aa76`, then run its six real-document checks and its five
mutation cases. Then prove the check is load-bearing from git history, not from its author's word: take
the PRE-repair text (`git show 127ec1c:docs/install/README.md`), run the new outgoing-link check against
it, and assert it REPORTS the defect; then run it against the repaired file and assert it reports
nothing. Report both outputs verbatim.

**C3.** The governed write-set gate. In `.github/workflows/public-plugin-verify.yml`, extract the
`stage-c` arm's own `ALLOWED` / `DENIED` regexes and declared base (do not retype them), then classify
`git diff --name-only <declared base>...c17aa76`. Report the path count and every path outside the set.
Also classify the range `<base>...d3bd545` (the unmodified main) as a control. State the verdict of each.

**C4.** The evidence-branch manifest. From the clone you already have, recompute the sha256 of every
path listed in `S4_R6_CLOSEOUT_RETURN/SHA256SUMS` from the committed blobs and report
`N/N byte-identical`. Independently name two packet files whose absence or content mismatch would
matter, and check those specifically.

**C5.** The packet's canonical verdict binding. Read `S4_R6_CLOSEOUT_RETURN/checker_verdict.json` and
report: which `subject_commit` it binds, whether the dispatch history was preserved rather than
rewritten, and whether the recorded verdict text digests can be recomputed from the files the packet
ships. Flag any field that asserts something the shipped files cannot show.

**C6.** Adversarial miss-check on the round's own claims. Take the three most load-bearing claims in
`S4_R6_CLOSEOUT_RETURN/EXTERNAL_ENGINEERING_HANDOVER.md` (pick them yourself, e.g. the branch model, the
write-set gate's allowance, the test command and its expected output) and attempt to FALSIFY each from
the repository. Report each as CONFIRMED / REFUTED / UNVERIFIABLE with the command you ran.

## What NOT to do

- Do not run the whole test suite; the scoped commands above are the contract.
- Do not modify, create or delete any file inside the worktree or the handover directory. Use your own
  scratch space outside both.
- Do not treat a green hosted CI status as your evidence; run the checks yourself.
- Do not accept any claim in this brief as established — it is the maker's framing, and your job is to
  test it.

## Output

A verdict of `PASS` / `PARTIAL` / `FAIL`, then per-claim findings with the exact command and its output,
then a `qualification_limits` list naming everything you could NOT establish and why. State the
same-model-axis limitation explicitly. The final line of your reply must be exactly
`HGK_LANE_NONCE_OK` and nothing may follow it.
