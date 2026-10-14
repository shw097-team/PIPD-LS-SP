#!/usr/bin/env python3
"""Assemble the closure/handover audit bundle deterministically, and REFUSE to emit it if any block is
missing or duplicated.

Why this exists: three successive bundles were assembled by ad-hoc string surgery on the previous prompt,
and that surgery silently dropped BLOCK 8 while the bundle still passed every guard - because a guard can
only check the blocks the spec declares, and the spec had been edited to declare what survived. The
assembly itself therefore has to be checked: every label must appear exactly once, and the character
budget must leave real headroom under the dispatcher's argv ceiling rather than a few dozen characters.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

LABELS = [f"=== BLOCK {i}:" for i in range(1, 9)]
BUDGET = 29000
HEADROOM = 1500


def sh(*a: str) -> str:
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()


def main() -> int:
    b = Path(sys.argv[1])
    a = Path(sys.argv[2])
    rnd = b / ".hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset"
    eg, out = rnd / "evidence/12_GATES", rnd / "far-study/rem3"
    disp = json.loads((eg / "CLOSURE_DISPOSITION.json").read_text(encoding="utf-8"))
    sup = json.loads((eg / "SUPERSESSION_LEDGER.json").read_text(encoding="utf-8"))
    aff = json.loads((eg / "AFFECTED_ONLY_INVALIDATION.json").read_text(encoding="utf-8"))
    hb = json.loads((eg / "RECEIVER_HANDOFF_BUNDLE.json").read_text(encoding="utf-8"))
    blocks: list[tuple[str, str]] = []

    blocks.append((LABELS[0], "the corpus rules this closure obeys, each with its own first-failure code\n" +
                   "\n".join(f"  - {x['rule']}\n      [source: {x['source']}; first failure: {x['first_failure']}]"
                             for x in disp["alignment_premise"]["rules_this_disposition_obeys"])))
    blocks.append((LABELS[1], "closure disposition, one row per pending item\n" + "\n".join(
        f"  {i['id']}: state={i['current_state']} -> next={i['next_legal_state']}\n"
        f"      owner={i['decision_owner']} | first_failure_if_skipped={i['first_failure_if_skipped']}\n"
        f"      falsifier: {i['falsifier'][:130]}" for i in disp["items"])))
    rows = []
    for e in sup["entries"]:
        new = e["new_hash"]
        rows.append(f"  {e['supersession_ref']}\n      old={e['old_hash']}\n      new={new}\n"
                    f"      git rev-list --parents -n 1 {new}  -> "
                    f"{sh('git', '-C', str(b), 'rev-list', '--parents', '-n', '1', new)}\n"
                    f"      git merge-base --is-ancestor {e['old_hash'][:12]} {new[:12]}; echo $?  -> exit "
                    f"{subprocess.run(['git', '-C', str(b), 'merge-base', '--is-ancestor', e['old_hash'], new], capture_output=True).returncode}\n"
                    f"      git rev-parse {e['old_hash'][:12]}^{{commit}}  -> {sh('git', '-C', str(b), 'rev-parse', e['old_hash'])[:12] or 'ABSENT'}")
    blocks.append((LABELS[2], "supersession entries WITH their inputs, so every flag is recomputable\n" + "\n".join(rows)))
    blocks.append((LABELS[3], "affected-only invalidation, complete\n"
                   f"  invariant: {aff['invariant']}\n  graph edge: {aff['graph_edge']}\n"
                   f"  superseded nodes: {[n['head_short'] for n in aff['superseded_nodes']]}\n"
                   f"  current heads: {aff['current_heads']}\n"
                   f"  affected={aff['affected_count']} untouched={aff['untouched_count']}\n"
                   f"  conservative rule: {aff['conservative_rule_applied']}\n"
                   "  ALL affected entries, with the citation that affects each:\n" +
                   "\n".join(f"    {x['artifact'].split('/rounds/')[-1]}  cites {x['cites_superseded']}"
                             for x in aff["affected"]) +
                   "\n  ALL untouched entries, with the citation that spares each:\n" +
                   "\n".join(f"    {x['artifact'].split('/rounds/')[-1]}  cites {x['cites_current']}"
                             for x in aff["untouched"])))
    blocks.append((LABELS[4], "the typed receiver handoff, as carried\n" + json.dumps(
        {k: hb[k] for k in ("schema", "position_in_state_machine", "receiver_state", "admission",
                            "subject_identity", "permissions", "rollback")}, indent=1, ensure_ascii=False)))
    blocks.append((LABELS[5], "declared claim ceiling\n" + json.dumps(disp["claim_ceiling_declared"],
                                                                     indent=1, ensure_ascii=False)))
    receipt = (eg / "REM3_REMEDY_RECEIPT_AT_CURRENT_HEADS.txt").read_text(encoding="utf-8")
    glog = [l for l in (eg / "REM3_GATE_RUN_AT_CURRENT_HEADS.log").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    blocks.append((LABELS[6], "the remedy receipt for ALLOWLIST-WIDENING, SCOPE-ANCHORED to the heads in "
                   "force, and the gate's own run at those same heads\n"
                   "  --- receipt, verbatim ---\n" + "\n".join("  " + l for l in receipt.splitlines()) +
                   "\n  --- the gate run, verbatim incl. its head header ---\n" +
                   "\n".join("  " + l for l in glog)))
    b8 = (eg / "REM3_COMMENT_PATCH_RECEIPT.txt")
    if not b8.exists():
        print(f"REFUSING: {b8.name} is missing; BLOCK 8 would be a claim without its receipt")
        return 1
    blocks.append((LABELS[7], "the patch receipt for FALSE-COMMENT-IN-CANDIDATE\n" +
                   "\n".join("  " + l for l in b8.read_text(encoding="utf-8").splitlines())))

    head = """Bundle v4: this session's CLOSURE and HANDOVER, offered for independent audit (lane VERIFY_SECURITY).

You are an independent checker. Everything you can see is below; you cannot read this machine's files or
run anything here. A claim needing a block you were not given is INCONCLUSIVE - say which block would
settle it. Grade the blocks, not the prose. Answer per claim with exactly one of
CONFIRMED / REFUTED / INCONCLUSIVE, then one sentence citing the block text that decided it. End your
message with this token on its own line: HGK_LANE_NONCE_OK

S1  Every supersession entry satisfies old_hash != new_hash, names a predecessor, and its invariant is
    recomputable from the inputs carried in BLOCK 3 (not from a computed flag).
S2  The affected-only set is consistent with the citations carried: every affected entry cites a
    superseded revision and every untouched entry cites only current heads, both lists complete.
S3  No item advanced past the state its carried evidence supports: ALLOWLIST-WIDENING's receipt is BLOCK 7
    and FALSE-COMMENT-IN-CANDIDATE's receipt is BLOCK 8, and no item is CLOSED anywhere.
S4  The handoff bundle asserts no admission and no PASS and states its own limitations.
S5  Nothing carried claims a P3-P5 state.
"""
    body = "\n\n".join([head] + [f"{lab}\n  {txt}" if "\n" not in txt[:1] else f"{lab}\n{txt}"
                                 for lab, txt in blocks])
    body += ("\n\n=== HOW TO RECOMPUTE ===\n  every claim's recompute command is carried in "
             "bundle_manifest_rem3_v4.json (recompute_commands); BLOCK 3, BLOCK 7 and BLOCK 8 each name "
             "their own command inline.\n")
    # the assembly check the three earlier bundlings lacked
    bad = [lab for lab in LABELS if body.count(lab) != 1]
    if bad:
        print(f"REFUSING: these labels are absent or duplicated in the assembled bundle: {bad}")
        return 1
    if len(body) > BUDGET - HEADROOM:
        print(f"REFUSING: assembled prompt is {len(body)} chars; budget {BUDGET} with {HEADROOM} headroom")
        return 1
    (out / "prompt_rem3_verify_v4.md").write_text(body, encoding="utf-8")
    inventory = {lab: len(txt) for lab, txt in blocks}
    print(json.dumps({"assembled_chars": len(body), "budget": BUDGET, "headroom": BUDGET - len(body),
                      "blocks": inventory, "labels_each_exactly_once": not bad,
                      "all_labels_present": [lab for lab in LABELS if lab in body]},
                     indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
