# FAR decision study — S4R3 write-set widening and Stage B successor

Round: `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset`
Project: `PIPD-LS-SP-20261008` · Repo `shw097-team/PIPD-LS-SP`
Prepared by: the bounded EXECUTE-lane writer (`codex`), workorder
`WO-TS-req-s4r3far-decision-study-001` (`REQ-S4R3FAR-DECISION-STUDY-001`)
Base head at admission: `b32192f566026401d239985029906a80e37a734d`
Status: maker-side decision study. Not an acceptance. Changes no flag.

This study cites the packet (`far-study/packet_execute.md`, `prompt_execute.md`) by section and
finding tag (F1–F8, D1–D5, §1–§5). It does not restate them. Facts not supplied by the packet or by
the artifacts it names are written `NOT_SUPPLIED`.

---

## A. Status

Of the round's claims, three are **verified by this project's own pipelines** and reproducible from
committed receipts: the F006 wheel-registry repair (F006 ships the contract registry, with the
hosted winner line `mode=INSTALLED` in `evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt`), the
declared-stage/base write-set logic (both stages clean, `evidence/12_GATES/writeset_gate_local_final.txt`),
and the receipt pack binding commands to exit codes (`evidence/12_GATES/RECEIPT_PACK_C1_C2.json`,
18 steps). The write-set allowlist widening is **verified as a defect against an admitted
obligation**: the mechanical set-diff (`evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt`) and the
finding (`evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md`) show stage-b ALLOWED +2
(`docs/USER_GUIDE.md`, `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/`) against
`REQ-S4R3X-GATE-FALSIFIABILITY-002` ("The allowlists must not be widened…"), and the workflow comment
"This change widens NEITHER allowlist" is false as written (F1). A separate checker lane was served
eight times (attempts 7–14) and produced **advisory-only verdicts, none a pass**; after eight runs the
strongest per claim is C2 CONFIRMED (a10), C4 CONFIRMED (a14), C1 PARTIALLY_CONFIRMED (a11, a12), C3
PARTIALLY_CONFIRMED (a13) (F2). Three of those verdicts were polluted by the round's own bundles and
are corrected in the named files (F3); the C1 shortfall is a co-location gap around an artifact that
already exists and was accepted once (F4). Everything touching the two candidate heads, the flags, the
external evidence and the release decision is **owner-gated**: no acceptance row has been run, no
external-evidence item is closed by this round, and `NO_MERGE`, `NO_PUBLIC_RELEASE`,
`S4_FULL_PASS NOT_GRANTED` all still hold (F6, F8).

---

## B. Decision table (D1–D5)

Owner names are the `owner` values recorded at admission
(`admission/s4r3x_admission.json`, `far-study/far_admission.json`). "Clause restored" cites the
admitted requirement or the round's own promise that the decision discharges.

| Item | Owner | What unblocks it | Cost | Risk | Clause / promise it restores | Artifact that verifies closure |
|---|---|---|---|---|---|---|
| **D1** Adjudicate F1 (correct statement & keep sets / narrow the round-dir entry / register a declared deviation) | CI-OWNER (`REQ-S4R3X-GATE-FALSIFIABILITY-002`) | An owner ruling choosing option 1, 2 or 3 in `FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md` §Remediation | 1 edit (opt 1 or 3); 1 commit + 1 lane run if opt 2 (edits the audited Stage A head) | Opt 1/3: low, no code change; Opt 2: invalidates the audited head, forces a fresh verification round | `REQ-S4R3X-GATE-FALSIFIABILITY-002` "The allowlists must not be widened and the frozen-path refusal must still refuse" | Opt 1/3: an amended `public-plugin-verify.yml` comment plus re-cut C3 wording; Opt 2: narrowed allowlist entry + a new lane verdict |
| **D2** Lift the self-imposed dispatch pause, and whether to land two mechanical guards first | EXTERNAL-VERIFY-LANE (`REQ-S4R3X-VERIFY-005`) | Owner decision; guards are engineering (see §C) | Guard edits: 2 small script edits; resume: 1 lane run | Low; guards reduce the F3 pollution class but the qualification is bounded (see `ACCEPTANCE_RECORD_STAGEB.md` CORRECTION 2) | The round's own head/label discipline and the "claimer must have a receipt" rule it adopted after F3 | `scripts/run_ao_lane_dryaudit*.py` with the two guards + a negative test refusing a receipt-less claim |
| **D3** Land the C1 co-location bundle (F4 artifact + the doctor receipt in one bundle) | PKG07-OWNER (`REQ-S4R3X-F006-WHEEL-REGISTRY-001`) | Bundling the already-existing artifacts; then 1 lane run | 1 edit + 1 lane run | Low; F4 shows the content already exists and was accepted once | The C1 promise that a numeric family count equals a real, enumerated registry | `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md` + the doctor receipt (exit status + command binding) + the sdist-to-wheel receipt in one bundle; a lane verdict C1 CONFIRMED |
| **D4** Re-cut C3 with the corrected baseline diff and honest wording | CI-OWNER (`REQ-S4R3X-GATE-FALSIFIABILITY-002`) | Producing the re-cut bundle from the corrected diff; 1 lane run | 1 edit (wording) + 1 bundle + 1 lane run | Low; the corrected artifacts already exist (F1 locators) | `REQ-S4R3X-GATE-FALSIFIABILITY-002`; the C3 claim previously put to the checker | A C3 bundle carrying `C3_ALLOWLIST_BASELINE_DIFF.txt` + the Stage B workflow copy + a full (not distilled) run receipt; a lane verdict C3 CONFIRMED |
| **D5** Owner inputs outstanding | Human Owner / Release Owner / Host Owners (see §D5 owners) | Owner-supplied inputs and actions | Owner time; NOT_SUPPLIED in round units | Owner-dependent; blocks any release-readiness claim | Blueprint Appendix B `required_external_evidence` (12 items) and `OWNER_INPUT_REQUIRED.json` | `OWNER_ACTION_REQUEST.md` §A–§C checklist, discharged line by line |

D5 breaks down, with owners drawn from `OWNER_ACTION_REQUEST.md`:

| D5 item | Owner | Closure artifact |
|---|---|---|
| F003 publisher identity | Human Publisher (A3) | `plugin.release.json → publisher{name,identity,identity_sha256}` filled by a named human |
| Brand assets | Owner (A4) | `packaging/public-plugin/assets/` real icons with pinned sha256 |
| Vendor validator / A2 pin | Vendor/Build Owner (A2) | `plugin.json → official_schema_sha256` pinned to the byte copy |
| Portal submission | Human Publisher (C12) | Portal publish + public URL + user-side readback |
| Four-host UAT (Hermes native skill, Codex desktop, Codex CLI native skill, Claude Code) | UAT/Host Owner (C5–C10) | Per-host UAT transcripts (currently `NOT_EXECUTED`) |
| `.hgk` archive policy (~62 MB) | Owner | A written policy + its application |
| PR #4 (superseded) close-or-keep | Repo Owner | PR #4 set closed or kept with a stated reason |
| Final merge/release decision | Release Owner / Human Publisher | A signed release decision; `NO_MERGE`/`NO_PUBLIC_RELEASE` lifted only by the owner |

---

## C. Ranked remedy plan (engineering items only: D4, D2, D3, and the F1 options that need engineering)

Cheapest-first. Costs use the round's own units: **an edit**, **a commit**, **a lane run** (one
`VERIFY_SECURITY` dispatch, ~30–110 s per served attempt). "F1 option 2" is the only F1 option that
needs a head edit; "F1 option 1" is the statement-correction edit. F1 option 3 is a governance act,
not engineering, so it is omitted here.

1. **D4 — re-cut C3 (corrected diff + honest wording).**
   Action: adopt the already-produced `evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt` as the C3
   baseline, and replace the round's "allowlists were NOT widened" C3 wording with the enumerated +2
   additions and their justification; assemble one C3 bundle carrying the Stage B workflow copy and a
   full run receipt.
   Cost: 1 edit + 1 bundle + 1 lane run.
   Risk: low — the corrected artifacts exist (F1 locators); the only live risk is re-introducing a
   distilled receipt, which a13 already named as insufficient.
   Receipt: a lane verdict C3 CONFIRMED on the re-cut bundle.

2. **D2 — land the two mechanical guards, then decide on resuming dispatches.**
   Action: (a) a pre-dispatch check that `blocks_kept` covers the claim under test, so a bundle that
   drops the block it claims (the attempt-8 defect, F3) cannot be sent; (b) a rule that any claim put
   to a checker must have a receipt in the round.
   Cost: 2 small edits to `scripts/run_ao_lane_*.py`; +1 lane run to exercise the negative.
   Risk: low, but bounded — a passing guard proves the bundle is well-formed, not that the lane is
   sound (`ACCEPTANCE_RECORD_STAGEB.md` CORRECTION 2: sensitivity is bounded). The guard must not be
   represented as catching the original failure.
   Receipt: the guard's own negative test showing a receipt-less claim is refused, committed under the
   round's `scripts/` + `evidence/12_GATES/`.

3. **D3 — land the C1 co-location bundle.**
   Action: place `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md` (the accepted a11 artifact, F4)
   together with a doctor receipt that carries its own exit status and command binding, and the
   sdist-to-wheel receipt, into one bundle; dispatch once.
   Cost: 1 edit + 1 lane run.
   Risk: low — a11 already accepted the family-identity portion; a12 simply did not carry it (F4).
   Receipt: a lane verdict C1 CONFIRMED, or the bundle itself as a committed artifact a reviewer can
   re-run.

4. **F1 option 1 — correct the statement, keep the sets.**
   Action: amend the `public-plugin-verify.yml` inline comment and the round's C3 wording to enumerate
   the two stage-b additions and stop asserting "neither allowlist was widened"; keep the allowlist and
   denial sets unchanged.
   Cost: 1 edit (+ a commit if the amended comment is committed).
   Risk: the corrected text must state that the frozen-path denial, not the allowlist, carries the
   stage-b guarantee (F1); the finding describes this option as "no candidate head changes" even though
   the comment is committed content — the owner should confirm whether it invalidates the audited head.
   Receipt: the amended comment plus a re-cut C3 bundle whose wording matches the diff.

5. **F1 option 2 — narrow the round-directory entry.**
   Action: replace `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` in the stage-b
   allowlist with the specific evidence paths the gate must tolerate, so the gate does not permit
   arbitrary writes under its own receipts directory.
   Cost: 1 commit (edits the audited Stage A head) + 1 fresh lane run for re-verification.
   Risk: highest of the five — the packet states this edits the audited Stage A head and needs a fresh
   verification round; the previously accepted heads are invalidated.
   Receipt: a narrowed allowlist entry + a new lane verdict on the re-cut head.

Recommended order: **4 → 1 → 2 → 3 → 5**. Option 4 restores the honesty of the C3 statement at the
lowest cost; D4 and the guards are cheap, reversible edits; D3 is a bundling exercise over existing
content; option 2 is the only remedy that invalidates the audited head and is therefore last.

---

## D. External handoff

### D.1 May be handed to an external acceptance officer now

Every path is under `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` unless noted.
Each carries one falsifying check an officer can run themselves.

| Artifact | Falsifying command / check |
|---|---|
| `evidence/12_GATES/C3_ALLOWLIST_BASELINE_DIFF.txt` | Re-run the two `git show` commands quoted at the top of the file against the frozen subject `e71fee6d…` and the current heads, re-parse each `ALLOWED='…'`/`DENIED='…'` assignment, and re-diff. A staging that removes the +2 entries would falsify the finding. |
| `evidence/12_GATES/FINDING_ALLOWLIST_WIDENED_VS_CLAIM.md` | Check the quoted claim against the workflow text in the current heads (`grep -n "widens NEITHER allowlist" .github/workflows/public-plugin-verify.yml`). |
| `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md` | Run `python scripts/report_family_identity.py --tree <worktree>` and expect `verdict: PASS`; then drop one family from an installed registry and re-run — expect `FAIL` (exit 1). |
| `evidence/12_GATES/RECEIPT_PACK_C1_C2.json` | For each of the 18 steps, re-run its `argv` in its recorded `cwd` and compare the observed `rc` to `expected_rc`. |
| `evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt` | `git merge-base <stage A head> <stage B head>` must equal the Stage A head; the file's stated result must reproduce. |
| `evidence/12_GATES/C4_STAGE_B_REFUSAL_TESTS_SOURCE.py` and `C4_REFUSAL_TESTS_RUN.log` | Diff the extracted test bodies against `tests/test_public_plugin_packaging.py` at the Stage B head; re-run the two named tests and confirm the typed refusals. |
| `evidence/12_GATES/SUBJECTS.json` | `git -C <worktree> rev-parse HEAD` and `git ls-remote origin` for the branches, `main` and the tag; compare to the recorded heads. |
| `evidence/12_GATES/writeset_gate_local_final.txt` | Re-run `scripts/run_writeset_gate_locally.py` for both stages and expect exit 0 with the planted-violation refusals. |
| `evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A7.md` … `_A12_A13_A14.md` | Read each as **advisory only**; check the recorded `served_arm`, `ok`, nonce-present and per-claim verdict. None is a pass (F2). |
| `evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt` | Match each quoted hosted-run line to the named run ids; the F006 wheel-gate winner line must read `mode=INSTALLED`. |
| `scripts/run_writeset_gate_locally.py`, `scripts/report_family_identity.py`, `scripts/read_ci_for_sha.py`, `scripts/fetch_job_log.py` | Run each; they are the round's re-derivation tools and must run from the committed tree. |

### D.2 May NOT be handed over yet

| Withheld | Reason |
|---|---|
| The two candidate heads as an **acceptance subject** | No acceptance row is run; every lane verdict is advisory and none is a pass (F2, F6). |
| The final C1 claim bundle | Co-location gap: the family-identity artifact exists and was accepted once but the doctor/sdist receipts were not carried in the same bundle (F4, D3). |
| The final C3 claim bundle | It rests on wording this round now knows to be false ("allowlists were NOT widened"); re-cut required (F1, D4). |
| A workorder result of PARTIAL | The workorder result entrypoint accepts only PASS/FAIL, so a PARTIAL verdict cannot be recorded truthfully (F6). |
| The 12 external-evidence items | All owner/host gates; the round moved none of them (F1, F8, D5; count source in §E). |
| Any merge/tag/release/archive | `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED` still hold; none was performed (F8). |

---

## E. Marginal-value read

The governing blueprint's Appendix B `required_external_evidence` list carries **12 items**
— `REAL_VENDOR_SCHEMA`, `SKILLS_REF`, `REAL_CANDIDATE_BUILD`, `SECURITY_SCAN`, `PLUS_UAT`, `FREE_UAT`,
`HERMES_UAT`, `CODEX_DESKTOP_UAT`, `CODEX_CLI_UAT`, `CLAUDE_CODE_UAT`, `INDEPENDENT_CHECK`,
`HUMAN_PORTAL_PUBLISH` — recorded at **0/12** in `OWNER_ACTION_REQUEST.md` §C and restated in
`verify/far/FAR_S4POST_DEVIATION_AND_REMEDIES_20261013.md` §2. (Source of the count: those two files,
which both enumerate the same 12 names against the blueprint Appendix B.)

Across the rounds under study, **0 of 12 are fully moved**; **1 of 12 (`REAL_VENDOR_SCHEMA`) advanced to
an evidence-level partial closure** — the official schema was downloaded (HTTP 200, 1,805 bytes,
sha256 `0a4aad95…`, byte-identical to `packaging/public-plugin/vendor-plugin.schema.json`) per
`verify/r3/C1_VENDOR_SCHEMA_PROVENANCE.json`, with only the owner digest pin (A2) outstanding
(`OWNER_ACTION_REQUEST.md` §12). This S4R3 round moved **none** of the 12: every one is an owner/host
gate (F1, F8, D5).

Deciding sentence: the next action is the owner's D1 ruling on F1, because the audit trail currently
contains a committed claim ("the allowlists were NOT widened") that the round's own mechanical diff
falsifies, and no further verification-lane dispatch can close an owner gate.

---

## F. DO-NOT list

Lifted from constraints actually stated in the packet and the governing documents it cites:

- **Do not widen either allowlist further** — the admitted obligation forbids it (F1,
  `REQ-S4R3X-GATE-FALSIFIABILITY-002`); any future addition is a new deviation needing an owner ruling.
- **Do not relax the oracle, threshold, validator, guard, exit code or denominator to buy a PASS** —
  forbidden mutation in the R3 PROMPT §3; affirmed unweakened in `ROUND_RESULT_S4R3X.md` §2.
- **Do not merge, tag, release or archive** — `NO_MERGE`, `NO_PUBLIC_RELEASE`, `S4_FULL_PASS NOT_GRANTED`
  all still hold; none was performed (F8).
- **Do not present an advisory lane verdict as an acceptance** — every verdict this round is advisory
  and none is a pass (F2); a dispatched check never yields an OracleReceipt.
- **Do not widen the checker** — no `--allow-sandbox-escalation`, no substitute arm (F2 read-only, no
  escalation; resume procedure forbids both).
- **Do not record a PARTIAL verdict as a workorder result** — the entrypoint accepts only PASS/FAIL, so
  a partial cannot be recorded truthfully (F6).
- **Do not claim either allowlist addition was made to buy a green run** — expressly not claimed
  (F1 NAV); the defect is the assertion, not a proven motive.
- **Do not build new machinery to verify machinery without justifying it against doing nothing** —
  the packet's §4 over-engineering constraint; a candidate remedy must beat the no-build alternative.
- **Do not push `main`, force-push history, or move the frozen refs** — forbidden mutations in the R3
  PROMPT §3; `main` and `v0.1.1-preview.3` are untouched (SUBJECTS.json).

---

## Deliverable provenance

- Written to `.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/EXECUTE_STUDY_DRAFT.md`.
- Grounded only in the packet's F1–F8 / D1–D5 / §1–§5 and the artifacts those sections name.
- No acceptance is granted. No flag changed.

HGK_LANE_NONCE_OK
