# SESSION CLOSEOUT & HANDOVER — PIPD-LS-SP S4 R6 closeout / FAR R17

- session: `20261016_174319_cc81b9` (Hermes desktop, default profile)
- round: `PIPD-S4-R6-CLOSEOUT-20261016` → `FAR-20261016-017-s4r6-residual-closure`
- governance: HG-KSEOS = control plane ; Fabric = contract surface ; Hermes = governed runner ;
  Codex CLI = tracked writer / independent checker
- written: 2026-10-16 (Asia/Taipei)

---

## 1. Checkpoint (resume from exactly here)

```yaml
checkpoint:
  command_id: PIPD-S4-R6-CLOSEOUT-20261016
  round_root: C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016
  far_root:   C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research/runs/FAR-20261016-017-s4r6-residual-closure
  worktree:   C:/Projects/Agent_Workspace/PIPD-S4R6-wt        # branch fix/s4r6-closeout-doc-identity-and-update-route-20261016
  subjects:
    main:        {commit: d3bd5456afbff21a8c8837994a49f57be3e1b97e, published: false}
    preview4:    {tag: v0.1.1-preview.4, tag_object: 0618d73c725da0d8c3280f99ef369d13741b5197,
                  tag_target: cc6c1930765160697e7e51d6e37735b9220a30db,
                  tree: 7d277a0afaff28b6841836cea3a31ffd0b214d94, assets: 7, unchanged: true}
    candidate:   {commit: 127ec1ca97c71d0437f5b149a6e7d540d0cb3bba,
                  tree: 62eef9d8059d307ae373de63519a37551fa14854, pr: 18}
    evidence:    {branch: r6-closeout-evidence-20261016,
                  commit: 5defc64f1177a1d6f32502c5479c65cf9a001858}   # carries the withdrawn packet
  checkpoints_on_disk:
    - C:/Projects/Agent_Workspace/r6-prefix-tree   # REMOVED after the pre-repair falsification run
  rollback:
    - delete the branch fix/s4r6-closeout-doc-identity-and-update-route-20261016 (owner-gated)
    - delete the branch r6-closeout-evidence-20261016 (owner-gated; it is the only home of the packet)
    - git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt reset --hard d3bd5456afbff21a8c8837994a49f57be3e1b97e
    - NEVER replace a v0.1.1-preview.4 tag or asset in place
  next_legal_action: >
    none blocked. The round is at its terminal state; the next moves are owner decisions O-1..O-6 below.
```

## 2. Terminal state of the round

| Subject | Result |
|---|---|
| Compiler | `PROMPT_COMPILE_PASS` (lint / activation / acceptance / compile, 4/4 exit 0) |
| HGK admission | `ADMISSION_OK`, 5 WorkOrders, board `pipd-s4r6-closeout-20261016` 8/8 done |
| Candidate | commit `127ec1c…` on `fix/s4r6-closeout-doc-identity-and-update-route-20261016`, PR **#18** open, non-draft, mergeable **clean** |
| Hosted CI on the candidate | `verify` **success**, `offline-gate` success x2 |
| Evidence | packet on branch `r6-closeout-evidence-20261016` (the round's receipts are outside the governed product write set) |
| Release | unchanged: `main=d3bd545…`, tag object `0618d73c…`, 7/7 assets, not re-tagged |
| Round end state | `PARTIAL` — bounded change delivered with an independent checker verdict; owner gates remain |
| Stage recommendation | `S4_PREVIEW_MVP_PHASE = TEMP_CLOSED` (engineering recommendation; **not** self-ratified) |

### 2.1 A red gate this round caused, and closed

The first version of PR #18 was red on `verify` while `ci` stayed green. Cause (reproduced locally from the
workflow's own classifier, not inferred): the declared `stage-c` write set refuses the round's evidence
directory and omits `docs/USER_GUIDE.md`, which this round's work order names. Repair: the evidence moved to
its own branch (byte-identical) and the one file was added by a **named** amendment whose planted-path
self-test was updated in the same commit. Both the local classifier and the arm's own self-test then pass
(`R17_RED_GATE_DIAGNOSIS.md` in the packet), and the hosted `verify` re-ran green on the repaired head.

## 3. Owner decisions (one action each; the round did not execute any of these)

| # | Decision | The single action |
|---|---|---|
| O-1 | Merge PR #18 | press Merge (green: `verify` + `offline-gate` success, 4 files, +419/-22, mergeable clean), or ask for changes |
| O-2 | Merge PR #17 | press Merge (verified: 1 file, +14/-0, non-draft, mergeable clean) |
| O-3 | Ratify `TEMP_CLOSED` | sign the stage close |
| O-4 | Private-host same-id UPDATE smoke | on an account whose plugin page offers Update, run the documented route and save the UI observation |
| O-5 | Distribute the 11 post-tag `main` commits | open a new tag + wheel + ZIP + SHA256SUMS; **never** edit `preview.4` |
| O-6 | **The `VERIFY_SECURITY` pool rank-1 collision (policy, not a defect)** | this is BY OWNER ORDER 2026-10-16 (registry `SOD006-C3`, status `OWNER_ORDERED_IN_FORCE`); the round did not touch the registry and instead pinned the checker by identity. If you want the pool itself to separate duties, that is a new owner order; the fenced candidate diff is in `DEFECT_DOSSIER.md` |

## 4. Open tickets carried forward

`TT-R6-DOC-ONEPASS` (candidate delivered), `TT-R6-PRIVATE-UPDATE-SMOKE`, `TT-R6-NEXT-PREVIEW-IF-NEEDED`,
`TT-R6-HOST-SCOPED-UAT`, `TT-R6-HGK-CNV`, `TT-R6-OD-A` (oracle normalisation disagreement),
`TT-R6-OD-B` (served fallback document declares the previous release's provenance — file is a frozen
asset, correctable only by a future release; now also disclosed in the install SSOT),
plus this round's additions:

- `TT-R17-01` — the `VERIFY_SECURITY` pool ranks the writer's model first. Status: **owner-ordered**
  (`SOD006-C3 OWNER_ORDERED_IN_FORCE`), not an unreviewed defect. Needs a new owner order to change.
- `TT-R17-02` — the checker's two prior NOT_RUNs were a sandbox capability limit; **closed this round** by an
  escalated dispatch bounded by a guard root (the network measurements now exist). If ordinary checker
  dispatches should be able to fetch, that is a lane-default policy question, not a per-round workaround.
- `TT-R17-03` — `tests/test_tooling_executes.py:52` and `tests/test_tqaep_design_positive.py:59` write inside
  the repository, so a no-write checker boundary cannot certify the whole suite green. Found by the
  independent checker; both files are unchanged from the base.
- `TT-R17-04` — `UL-01`: the canonical dispatcher still lacks the R10 nonce / per-turn-receipt repairs.

## 5. What a successor round does NOT need to redo

- Do not re-derive the D1 / D2 / ClaimCeiling repairs: they are on `main` and the R6 report closed them.
- Do not re-derive the served ZIP identity: it is measured, and the packet records the recomputation.
- Do not re-read the compiler bundle to decide whether the round can compile: it compiles.
- Do not rebuild the release-identity half of the guard: `tests/test_r5r3_install_route_identity.py`
  already re-derives tag facts from git and binds the served digest to its download paragraph.
- Do not re-derive the red gate: reproduce it with `R17_check_write_set.py` (in the packet), which reads the
  regexes and the declared base out of the workflow so it cannot drift from the gate it reproduces.
- Do not put the packet back on the product branch: the write set must equal the product change.

## 6. Handover hygiene

- The PAT is used only through a non-echoing askpass helper; it appears in no prompt, log, commit, remote
  URL, evidence file or model context of this round.
- The temporary `r6-prefix-tree` worktree used for the pre-repair falsification was removed; the
  surviving scratch directories are `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/r6-verify-*` and are regenerable.
- Every count in the round's artifacts is derived from files or API responses on disk.

## 7. Disclosed side effects of building this branch (and their repair)

Building this evidence branch produced two unintended modifications, both found and repaired before the
final push, and both recorded here because the round must disclose its side effects rather than only its
result.

1. **Blanket LF normalisation.** The packet is hashed after a CRLF->LF normalisation (`git` stores LF, and a
   CRLF working copy breaks a fresh-clone `sha256sum -c`). The first attempt applied that normalisation to
   the **whole worktree** instead of the packet, which rewrote 195 working-copy files and swept 15
   `.hgk/rounds/**` files plus one `openspec/**` file into the commit as unrelated CRLF churn.
   **Repair:** the commit was rebuilt from the index with only this round's paths staged
   (`S4_R6_CLOSEOUT_RETURN/`, `far-r17/`, `EVIDENCE_BRANCH_README.md`); the unrelated paths were restored
   with `git checkout --`. The superseded commit never reached a merged or tagged state.
2. **One binary file caught in the same sweep.** `dist/pipd_ls_sp-0.1.1a3-py3-none-any.whl` was rewritten
   by the same loop. **Repair:** restored, and verified byte-identical to its committed blob
   (`git hash-object` == `git rev-parse HEAD:<path>`, both `5d9f9c62…`).

**Lesson worth carrying, stated as a rule:** normalise line endings **inside the packet directory**, never
across the worktree, and stage explicit paths rather than `git add -A` in a tree you did not create. A
worktree inherited from the repository contains artefacts you are not entitled to rewrite.
