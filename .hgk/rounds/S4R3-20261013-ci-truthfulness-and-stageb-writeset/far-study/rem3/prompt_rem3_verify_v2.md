Bundle v2: this session's CLOSURE and HANDOVER, re-offered for independent audit (lane VERIFY_SECURITY).

v2 exists because the v1 audit returned S1/S2/S3 INCONCLUSIVE and all three were defects of THIS bundle:
S1 carried computed booleans instead of the inputs that produce them, S2 truncated the affected list, and
S3 asserted a PATCHED state without carrying the patch receipts. The closure itself is unchanged. Any
figure below can be recomputed from the material in this bundle; the recompute commands are listed at the
end, and a claim whose inputs are missing is a defect of the bundle, not of the closure.

You are an independent checker. Everything you can see is below; you cannot read this machine's files or
run anything here. A claim needing a block you were not given is INCONCLUSIVE - say which block would
settle it. Grade the blocks, not the prose. Answer per claim with exactly one of
CONFIRMED / REFUTED / INCONCLUSIVE, then one sentence citing the block text that decided it. End your
message with this token on its own line: HGK_LANE_NONCE_OK

S1  Every supersession entry satisfies old_hash != new_hash, names a predecessor, and its invariant is
    recomputable FROM THE INPUTS CARRIED IN BLOCK 3.
S2  The affected-only set is consistent with the citations carried: EVERY affected entry cites a
    superseded revision and EVERY untouched entry cites only current heads (both lists complete).
S3  No item advanced past the state its carried evidence supports: the two PATCHED items have their patch
    receipts carried in BLOCK 7, and no item is CLOSED anywhere.
S4  The handoff bundle asserts no admission and no PASS and states its own limitations.
S5  Nothing carried claims a P3-P5 state.


=== BLOCK 1: the corpus rules this closure obeys (each with its own first-failure code) ===
  - TT/finding route is OPEN->ASSIGNED->PATCHED->CHECK_PENDING->CLOSED and no further; CLOSED needs owner AND checker evidence
      [source: PIPD-PKG-06 DOC-05 06-D05-H2-2; first failure: TT_CLOSURE_WITHOUT_CHECKER]
  - external gates need actual target-scoped checker-observed evidence, not expected-evidence placeholders; design gates use author-side receipts
      [source: PIPD-PKG-01 3.2 evidence rule; first failure: FRESH_EVIDENCE]
  - a supersession needs old_id/new_id/old_hash/new_hash/supersession_ref and old_hash != new_hash with a matching predecessor
      [source: PIPD-PKG-09 DOC-01; first failure: SEMANTIC_IDENTITY_DRIFT]
  - invalidation is affected-only (reverse closure), untouched artefacts are NOT invalidated, and where no output delta is provable the conservative branch is taken
      [source: PIPD-PKG-09 DOC-03; first failure: AFFECTED_ONLY_CLOSURE_INCORRECT]
  - P0-P2 can never be promoted to P3-P5 by text; self-promotion or split-brain BLOCKS; the stage gate answers by source hash and version
      [source: PIPD-PKG-10 0.6; first failure: SELF_PROMOTION_OR_SPLIT_BRAIN]
  - candidate != ACK != admitted WorkOrder; only the HGK receiver controls admission; default DENY/HOLD; author-side self-assessment is not a promotion source
      [source: PIPD-PKG-05 0.5 + PIPD-PKG-00 0.1; first failure: ILLEGAL_AUTHORITY_PROMOTION]

=== BLOCK 2: closure disposition, one row per pending item ===
  F1-ALLOWLIST-WIDENING: state=PATCHED -> next=CHECK_PENDING
      owner=owner (accept the remedy) / external acceptance officer | first_failure_if_skipped=TT_CLOSURE_WITHOUT_CHECKER
      falsifier: re-run scripts/measure_allowlist_minimum.py at the head; if any product path is UNLISTED, or a round-directory entry is still in either ALLO
  FALSE-COMMENT-IN-CANDIDATE: state=PATCHED -> next=CHECK_PENDING
      owner=owner / external acceptance officer | first_failure_if_skipped=TT_CLOSURE_WITHOUT_CHECKER
      falsifier: grep the gate file for the withdrawn sentence; if it is still present, this disposition is wrong
  PRIOR-LANE-VERDICTS-AT-SUPERSEDED-HEADS: state=INVALIDATED_AFFECTED_ONLY -> next=re-establish at the current head (not inherit)
      owner=external acceptance officer | first_failure_if_skipped=AFFECTED_ONLY_CLOSURE_INCORRECT
      falsifier: for any artefact listed as untouched, show that it cites a superseded revision; or for any listed as affected, show that its citation is the
  PLAN-LEG-MODEL-DIVERGENCE: state=OPEN -> next=owner ruling: apply the declared routing change, or accept the divergence as declared
      owner=owner only - changing global routing is not a maker action | first_failure_if_skipped=ILLEGAL_AUTHORITY_PROMOTION
      falsifier: re-measure the serving model for a new session; if it reports the mandated arm, the divergence is closed
  NO-TREE-LEVEL-INDEPENDENT-VERIFICATION: state=HOLD -> next=external acceptance officer reads the tree, or the owner opens a read/exec-capable checker lane
      owner=owner / external acceptance officer | first_failure_if_skipped=FOREIGN_OR_STALE_EVIDENCE
      falsifier: hand the tree to a checker with read access and see whether its verdicts change; if they never do, the bundle audits were sufficient
  F003-OWNER-GATE-INPUTS: state=BLOCKED_EXTERNAL -> next=owner supplies the inputs; then the F003 gate can run
      owner=owner / publisher | first_failure_if_skipped=BLOCKED_EXTERNAL
      falsifier: run the F003 gate with the supplied inputs; a red gate means the inputs are not yet sufficient
  FOUR-HOST-UAT: state=NOT_EXECUTED -> next=run on owner-provided hosts
      owner=owner | first_failure_if_skipped=BLOCKED_EXTERNAL
      falsifier: run one host; if the skill loads and its contract holds, the disposition updates for that host only
  CANONICAL-ACCEPTANCE-ROWS: state=AWAITING_EXTERNAL -> next=an external QUALIFICATION_ISSUER signs the qualification receipt
      owner=external qualification issuer / owner | first_failure_if_skipped=QUALIFICATION_WITHOUT_AUTHORITY
      falsifier: read the spine rows; a maker-side write would be visible as an actor that is not an issuer
  PREVIEW3-WHEEL-TRACE-FALSE-PASS: state=OPEN -> next=owner decides: rebuild and republish, or leave the published artefact with this disclosure attached
      owner=owner (publication is an external effect) | first_failure_if_skipped=SOURCE_FREEZE_ANCHOR_STALE
      falsifier: install the published wheel and run the Trace check; a pass under the repaired source would mean the wheel was in fact rebuilt
  HGK-ARCHIVE-POLICY: state=OPEN -> next=owner sets a retention/archive rule
      owner=owner | first_failure_if_skipped=no-silent-loss risk only if deletion were attempted, which it is not
      falsifier: measure the tree size after any archive action and confirm no receipt lost its subject
  PR-DISPOSITIONS: state=OPEN -> next=owner marks the superseded ones and keeps #5 as the reviewable subject
      owner=owner (close/merge are external effects) | first_failure_if_skipped=ILLEGAL_AUTHORITY_PROMOTION if a maker merged
      falsifier: read the PRs back; merged=true by a non-owner actor would falsify this disposition's premise

=== BLOCK 3 (v2): supersession entries WITH THE INPUTS, so the flags are recomputable ===
  fix/s4r3-stage-a-ci-truthfulness-20261013@5310896e706e->759b9f0dc880
      old=5310896e706e01a9cdb0123285bccec75086bcb8
      new=759b9f0dc880b2f960363b2ceaa68446c770061d
      git rev-list --parents -n 1 759b9f0dc880b2f960363b2ceaa68446c770061d   -> 759b9f0dc880b2f960363b2ceaa68446c770061d 5310896e706e01a9cdb0123285bccec75086bcb8
      git merge-base --is-ancestor 5310896e706e 759b9f0dc880; echo $?  -> exit 0
      git rev-parse 5310896e706e^{commit} (presence) -> 5310896e706e
      => recompute: old != new is arithmetic on the two literals; predecessor_matches is the exit code above; presence is the rev-parse above
  feat/s4r3-stageb-successor-20261013@35a68f0c05a2->46ae548311e7
      old=35a68f0c05a26747c2a1553cb86505ac26909b88
      new=46ae548311e7f38d520d4fe98df276d15867939d
      git rev-list --parents -n 1 46ae548311e7f38d520d4fe98df276d15867939d   -> 46ae548311e7f38d520d4fe98df276d15867939d 910823a4d5eff79fcd1d74d3e7fdbcb1d1bd8213
      git merge-base --is-ancestor 35a68f0c05a2 46ae548311e7; echo $?  -> exit 0
      git rev-parse 35a68f0c05a2^{commit} (presence) -> 35a68f0c05a2
      => recompute: old != new is arithmetic on the two literals; predecessor_matches is the exit code above; presence is the rev-parse above
  feat/s4r3-stageb-successor-20261013@46ae548311e7->1f94f8348974
      old=46ae548311e7f38d520d4fe98df276d15867939d
      new=1f94f834897452f52deb74049e8f4efc7dadc4ad
      git rev-list --parents -n 1 1f94f834897452f52deb74049e8f4efc7dadc4ad   -> 1f94f834897452f52deb74049e8f4efc7dadc4ad 46ae548311e7f38d520d4fe98df276d15867939d
      git merge-base --is-ancestor 46ae548311e7 1f94f8348974; echo $?  -> exit 0
      git rev-parse 46ae548311e7^{commit} (presence) -> 46ae548311e7
      => recompute: old != new is arithmetic on the two literals; predecessor_matches is the exit code above; presence is the rev-parse above

=== BLOCK 4 (v2): affected-only invalidation, COMPLETE ===
  invariant: affected == semantic_reverse_closure && untouched_not_invalidated && graph_consistent
  graph edge: artifact -> revision it cites (edge exists when the artifact text names the sha)
  superseded nodes: ['5310896', '35a68f0', '46ae548']
  current heads: {'stage_a': '759b9f0dc880b2f960363b2ceaa68446c770061d', 'stage_b': '1f94f834897452f52deb74049e8f4efc7dadc4ad'}
  affected=35 untouched=5
  conservative rule: no output-delta proof exists for these artifacts, so they are invalidated rather than assumed still-current
  ALL affected entries with the citation that affects each:
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/AFFECTED_ONLY_INVALIDATION.json  cites ['35a68f0', '35a68f0c05a26747c2a1553cb86505ac26909b88', '46ae548', '46ae548311e7f38d520d4fe98df276d15867939d', '5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json  cites ['35a68f0']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/AO_LANE_DRYAUDIT_VERDICT_A7.md  cites ['5310896']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C3_REFUSAL_RECEIPT_DISTILLED.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/C4_REPIN_AND_DECLARED_BASE.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/CI_RUNS_AND_STEP_RECEIPTS.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/HEAD_PROVENANCE_RECEIPT.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/LOCAL_FULL_SUITE_RECEIPTS.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/RECEIPT_PACK_C1_C2.json  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/REM2_NECESSITY_DERIVATION.txt  cites ['46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/REM2_PRODUCT_CHANGE_DIFF.txt  cites ['46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/SUBJECTS.json  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/SUPERSESSION_LEDGER.json  cites ['35a68f0', '35a68f0c05a26747c2a1553cb86505ac26909b88', '46ae548', '46ae548311e7f38d520d4fe98df276d15867939d', '5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/writeset_gate_local_final.txt  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c1_colocated.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c1_v2.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3_recut.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3_v2.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3_v3.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3_v4.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/bundles/prompt_c3e_only.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/packet2_remediation.md  cites ['35a68f0', '35a68f0c05a26747c2a1553cb86505ac26909b88', '5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/packet_execute.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/prompt2_execute.md  cites ['35a68f0', '35a68f0c05a26747c2a1553cb86505ac26909b88', '5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/prompt_execute.md  cites ['5310896', '5310896e706e01a9cdb0123285bccec75086bcb8']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/far2_admission.json  cites ['35a68f0', '35a68f0c05a26747c2a1553cb86505ac26909b88']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/invocation_VERIFY_SECURITY_a21.json  cites ['46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/invocation_VERIFY_SECURITY_a22.json  cites ['46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/prompt_rem2_verify.md  cites ['35a68f0', '46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/prompt_rem2_verify_v2.md  cites ['35a68f0', '46ae548', '46ae548311e7f38d520d4fe98df276d15867939d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem2/verify/VERDICT_REM2_V2_A22.txt  cites ['35a68f0']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/VERDICT_C3_RECUT_A10.md  cites ['5310896']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/verify/VERDICT_C3_RECUT_A8.md  cites ['5310896']
  ALL untouched entries with the citation that spares each:
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/CLOSURE_DISPOSITION.json  cites ['1f94f83', '1f94f834897452f52deb74049e8f4efc7dadc4ad', '759b9f0', '759b9f0dc880b2f960363b2ceaa68446c770061d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/EVIDENCE_ENVELOPE.json  cites ['1f94f83', '1f94f834897452f52deb74049e8f4efc7dadc4ad']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/RECEIVER_HANDOFF_BUNDLE.json  cites ['1f94f83', '1f94f834897452f52deb74049e8f4efc7dadc4ad', '759b9f0', '759b9f0dc880b2f960363b2ceaa68446c770061d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/REM2_GATE_RUN_BOTH_STAGES.log  cites ['759b9f0', '759b9f0dc880b2f960363b2ceaa68446c770061d']
    S4R3-20261013-ci-truthfulness-and-stageb-writeset/far-study/rem3/far3_admission.json  cites ['1f94f83', '1f94f834897452f52deb74049e8f4efc7dadc4ad']

=== BLOCK 5: the typed receiver handoff, as carried ===
{
 "schema": "RECEIVER-HANDOFF-BUNDLE/1",
 "position_in_state_machine": "OFFERED",
 "receiver_state": "AWAITING_EXTERNAL",
 "admission": {
  "admission_receipt": "",
  "admission_receipt_state": "AWAITING_EXTERNAL - only the HGK receiver may produce one; a maker-side value would be a FORGED_ADMISSION",
  "human_token": "",
  "human_token_state": "AWAITING_EXTERNAL",
  "note": "this bundle deliberately carries empty admission fields rather than plausible values"
 },
 "subject_identity": {
  "repo": "https://github.com/shw097-team/PIPD-LS-SP.git",
  "stage_a_branch": "fix/s4r3-stage-a-ci-truthfulness-20261013",
  "stage_a_head": "759b9f0dc880b2f960363b2ceaa68446c770061d",
  "stage_b_branch": "feat/s4r3-stageb-successor-20261013",
  "stage_b_head": "1f94f834897452f52deb74049e8f4efc7dadc4ad",
  "stacked_invariant": "merge-base(stage_a_head, stage_b_head) == stage_a_head",
  "frozen_subject_the_round_examined": "e71fee6dd3aa73724baec4e8d9cc72127fbe36ed",
  "receipt_note": "the receiver must resolve every sha itself; short forms are provided for reading only"
 },
 "permissions": {
  "granted_by_this_bundle": "none",
  "note": "a handoff is not a permission; the receiver grants admission, this bundle only offers"
 },
 "rollback": {
  "refs": [
   {
    "ref": "main",
    "value": "224591431a164ab72a9423cd180e417e8a762403",
    "note": "untouched by this session"
   },
   {
    "ref": "v0.1.1-preview.3",
    "value": "e94cc7f9567acb59de4691ee6166815ac96a9700",
    "note": "untouched; its wheel carries the disclosed Trace defect"
   }
  ],
  "restore_action": "git reset --hard to either frozen ref; both branch heads are additive and no force-push was used on main or the tag"
 }
}

=== BLOCK 6: declared claim ceiling ===
{
 "lattice": "PI_READY != PREDEV_READY != EXECUTION_ADMITTED != OPERATIONAL_ACCEPTED != PRODUCTION_PASS",
 "this_session_state": "VALIDATED_CANDIDATE / OFFERED at stage S4; receiver step NOT reached",
 "never_claimed": [
  "EXECUTION_ADMITTED",
  "OPERATIONAL_ACCEPTED",
  "PRODUCTION_PASS",
  "any acceptance"
 ],
 "flags": {
  "NO_MERGE": true,
  "NO_PUBLIC_RELEASE": true,
  "S4_FULL_PASS": "NOT_GRANTED"
 }
}

=== BLOCK 7 (v2): the remedy receipts, so a PATCHED state has its evidence carried ===
  measurement counts: {"changed": 151, "excluded": 143, "unlisted_product": 0, "denied_product": 0}
  net allowlist change: {"frozen subject": {"added": ["docs/USER_GUIDE\\.md$"], "removed": ["\\.hgk/rounds/S4POST-20261012"]}, "previous head 35a68f0": {"added": [], "removed": ["\\.hgk/rounds/S4POST-20261012", "\\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/"]}}
  --- necessity derivation (verbatim) ---
# Necessity derivation for docs/USER_GUIDE.md in the stage-b allowlist

This is the derivation, not a restatement of it: the same classifier is run twice over the same
governed diff, once with the entry present and once with the entry STRIPPED, and the difference is
printed. A reader can re-run the two lines below and get the same output.

governed base (resolved from STAGE_B_BASE_REF) : 759b9f0dc880b2f960363b2ceaa68446c770061d
head                                          : 46ae548311e7f38d520d4fe98df276d15867939d
declared exclusion in force                   : '^\\.hgk/'
changed paths in the governed diff            : 162

RUN 1 - entry present    : UNLISTED=0 DENIED=0
RUN 2 - entry STRIPPED   : UNLISTED=1 DENIED=0

paths whose verdict changes when the entry is removed (RUN 1 -> RUN 2):
  docs/USER_GUIDE.md   ALLOWED -> UNLISTED

CONCLUSION, mechanical: removing the entry moves exactly the path(s) listed above from ALLOWED
to UNLISTED. Since UNLISTED is what the gate refuses, the entry is load-bearing for this diff.
  --- the gate's own run, verdict lines ---
  ===== stage-a in s4r3a-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
  EXCLUDED_BY_DECLARATION (^\.hgk/) from the governed PRODUCT write set: 23 path(s)
  GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
  GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
  GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
  GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path
  GATE_SELF_TEST_OK: planted stage-a artefacts are all allowed
  WRITE_SET_CLEAN_AGAINST_e71fee6dd3aa73724baec4e8d9cc72127fbe36ed
  ===== stage-b in s4r3c-wt (base env: e71fee6dd3aa/fix/s4r3-stage-a-ci-truthfulness-20261013) -> exit 0 =====
  .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt
  .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_STEP.yml
  EXCLUDED_BY_DECLARATION (^\.hgk/) from the governed PRODUCT write set: 154 path(s)
    excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_LOCAL_AND_CI.txt
    excluded: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/evidence/12_GATES/WRITE_SET_GATE_STEP.yml
  GATE_SELF_TEST_OK: .hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/../evil.sh is refused as a traversal path
  GATE_SELF_TEST_OK: docs/install/../../src/pipd_ls_sp/validate.py is refused as a traversal path
  GATE_SELF_TEST_OK: planted frozen-path violations and unlisted src/** are all refused
  GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path
  GATE_SELF_TEST_OK: planted stage-b artefacts are all allowed
  WRITE_SET_CLEAN_AGAINST_759b9f0dc880b2f960363b2ceaa68446c770061d
  2/2 gate runs clean

=== HOW TO RECOMPUTE EVERYTHING ABOVE ===
  git rev-list --parents -n 1 <new_sha>   # predecessor of each supersession entry (BLOCK 3)
  git merge-base --is-ancestor <old> <new>; echo $?   # 0 means predecessor_matches (BLOCK 3)
  git rev-parse <old>^{commit}   # presence of the superseded object (BLOCK 3)
  scripts/measure_allowlist_minimum.py <worktree>   # regenerates the counts in BLOCK 7
  scripts/closure_close_out.py <b> <a>   # regenerates blocks 3 and 4
  scripts/run_writeset_gate_locally.py   # regenerates the gate verdict lines in BLOCK 7