# R5R3-20261016-preview4-closeout — handover checkpoint

**Round:** delta-only verification of the ALREADY-published `PIPD-LS-SP@v0.1.1-preview.4`, plus the bounded
documentation/identity repair it still needed.
**Claim ceiling delivered:** `LOCAL / CANDIDATE_ONLY`; `S4_PREVIEW_MVP_PHASE_TEMP_CLOSED` on the published
preview.4. Nothing merged, no tag created, no release created, no host install claimed.

## Subject (frozen, re-read at the start of every continuation)

| Object | Value |
|---|---|
| frozen subject | `main = dba4b19456777d3b597fdf71480f6423dd974243` (`C:/Projects/wt-r5r3`, detached) |
| compiler base (stage-c) | `f4021aeff9c016cfb14f17e68a0c570ed4e825c5` |
| product branch | `fix/r5r3-preview4-identity-and-route` @ `4cbb22fc9be3c9b91840aacef90da754d3d7414d` |
| pull request | #16, open, **draft**, `mergeable_state=clean`, NOT merged |
| evidence branch | `r5r3-evidence-return-20261016` (head advances with each evidence commit; integrity is bound by `PACK_INDEX.json` + the git object, not by a recorded tip sha) |
| tag under study | `v0.1.1-preview.4` object `0618d73c725da0d8c3280f99ef369d13741b5197` → commit `cc6c1930765160697e7e51d6e37735b9220a30db`, tree `7d277a0afaff28b6841836cea3a31ffd0b214d94` |
| published | 2026-10-14, 7 assets, 6 `SHA256SUMS` entries |

## What this round changed (product branch, 6 files)

`README.md`, `docs/install/README.md`, `docs/RELEASE_TUPLE.json` (new `v0.1.1-preview.4` entry),
`docs/install/ASSET_READBACK_v0.1.1-preview.4.json` (new), `tests/test_r5r3_install_route_identity.py` (new),
`.github/workflows/public-plugin-verify.yml` (one-file named amendment to the stage-c `ALLOWED` arm +
`ALLOWED_PLANTS`).

The defect repaired: `docs/install/README.md` told a reader that the preview.4 identities live in the
`v0.1.1-preview.4` entry of `docs/RELEASE_TUPLE.json` — and that entry did not exist on `main`.

## State of every gate

| Gate | State | Evidence |
|---|---|---|
| CAPC compiler | `PROMPT_COMPILE_PASS`, lint/activation/acceptance/compile all rc=0 | pack `raw/compiler_receipts.json`, `raw/compiler_out/` |
| local full suite | `Ran 624 tests ... OK (skipped=4)`, exit 0 | `raw/full_suite_final.log` |
| focused | `Ran 35 tests ... OK` | `raw/ws_a_acceptance_rerun2.log` |
| hosted CI | `ci` 38849065820 success, `public-plugin-verify` 38849065867 success | red predecessor on `881a2e91` kept as `raw/` evidence |
| mutation control | 4/4 mutations red, tree restored | `raw/mutation_control.json` |
| served assets | 7/7 match the release's own `SHA256SUMS` | `raw/served_assets.json`, `raw/served/assets/` |
| independent checker | `VERIFIED_WITH_FINDINGS` (CODEX CLI `openai-codex/gpt-6.1-sol`, read-only) | pack `CHECKER_VERDICT.json` |
| private host smoke | `NOT_RUN` / `NOT_SUPPORTED_FOR_ACCOUNT` | needs the account owner's entitlement |
| KANBAN board | `r5r3-preview4-closeout-20261016`, all 8 tasks `done` with verdict comments | `<hermes home>/kanban/boards/…` |

## Open items carried forward

1. **TT-R5R3-01** — this host's git ignores `GIT_ASKPASS`: GCM sets `credential.interactive=false`. A
   token-based HTTPS push needs `-c credential.helper= -c credential.interactive=always -c core.askPass=<x.cmd>`
   per invocation (a `.cmd` wrapper; a bare `.py`/`.sh` is not executed).
2. **TT-R5R3-02** — the stage-c arm did not include `docs/RELEASE_TUPLE.json` although the PR path filter and
   the install guide both name it. Amended in PR #16 as a named amendment.
3. **TT-R5R3-03** — GSTACK named-method readback: `HG-KSEOS/config/hermes-codex-lane.json` `codex_sha256`
   differs from the installed executable (HGK tooling projection drift, not a product defect).
4. **Skill hygiene (HGK)** — `hgk-governed-execution/SKILL.md` is ~99.7 KB with 106 files under `references/`;
   it is at the point where no patch that grows it is accepted, so the round added
   `references/product-branch-write-set-gates.md` without a body pointer. It needs a topical split.

## Owner-gated next steps (not performed, not to be claimed)

- merge PR #16 (Repo Owner) — the branch is unmerged and disposable;
- a new immutable release from a merged main SHA, if the Owner wants the tuple/route fix in a release;
- private ChatGPT host smoke from the release ZIP (account owner entitlement);
- `PUBLIC_DIRECTORY`, `S4_FULL_PASS`, `PRODUCTION` remain `NOT_GRANTED`.

## Resume commands

```bash
# subject
git -C C:/Projects/wt-r5r3 rev-parse HEAD
# branch gate, simulated locally (must print GATE_BAD=0)
BASE=f4021aeff9c016cfb14f17e68a0c570ed4e825c5
git -C C:/Projects/wt-r5r3 diff --name-only "$BASE"...HEAD
# evidence pack at the evidence branch
git -C C:/Projects/wt-r5r3-evidence log --oneline -2
# recompute the pack's own index
python C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout/pack_builder.py <out-dir>
```

Round directory: `C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout/`
(round status: `ROUND_STATUS.json`; pack source: `pack_builder.py`; publication: `gh_r5r3_publish.py`,
`push_evidence_branch.py`).
