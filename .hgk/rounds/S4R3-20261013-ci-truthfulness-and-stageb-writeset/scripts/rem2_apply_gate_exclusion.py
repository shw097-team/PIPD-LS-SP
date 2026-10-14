#!/usr/bin/env python3
"""Apply the F1 remedy to both branch copies of the write-set gate, deterministically.

Why a transformer instead of hand edits: the two copies must stay byte-identical except for the single
`STAGE:` line, and the remedy touches seven places in each. A script makes the two applications provably
the same, and `--check` prints the diff for review before anything is written.

The remedy (chosen from the measurement in evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json):
  * the round's scaffolding tree is excluded from the governed PRODUCT write set BY DECLARATION and
    printed, instead of being smuggled in as an allowlist entry - the allowlist previously permitted
    writes to the very directory that holds this gate's own receipts;
  * the round-directory entries are therefore REMOVED from both stage arms, and no entry is added;
  * the surviving stage-b addition (docs/USER_GUIDE.md) stays, because the governed diff is measured to
    require it, and the comment now discloses exactly that instead of claiming nothing was widened;
  * the self-test additionally proves the exclusion cannot be reached from a product path.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

WF = ".github/workflows/public-plugin-verify.yml"
ROUND_ALT_A = (r"|\.github/workflows/(ci|public-plugin-verify)\.yml$"
               r"|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/")
ROUND_ALTS_B = r"|\.hgk/rounds/S4POST-20261012|\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/"

OLD_COMMENT = """        # The two stages have deliberately different, non-overlapping write sets. Stage A repairs the
        # pipeline (the CI exit-code truthfulness guard, the packaging build, the first-run examples,
        # the smoke test) and must be able to write src/ and the workflows; Stage B ships the
        # distribution surface and must not go near src/, schemas/ or dist/. This change widens
        # NEITHER allowlist: each stage is enumerated file by file or by its own narrow prefix, the
        # frozen-path denial for skills/, schemas/ and dist/ applies to both, and the classifier's
        # self-test below still proves that planted violations are REFUSED."""

NEW_COMMENT = """        # The two stages have deliberately different, non-overlapping write sets. Stage A repairs the
        # pipeline (the CI exit-code truthfulness guard, the packaging build, the first-run examples,
        # the smoke test) and must be able to write src/ and the workflows; Stage B ships the
        # distribution surface and must not go near src/, schemas/ or dist/. Each stage is enumerated
        # file by file or by its own narrow prefix, and the classifier's self-test below still proves
        # that planted violations are REFUSED.
        #
        # Scope of the DENIED continuity, stated precisely because the earlier wording overstated it:
        # the frozen-path denial is unchanged for the stage-b set, whose DENIED omits nothing. The
        # stage-a arm deliberately ALLOWS src/, so "the denials are unchanged" is a statement about
        # the stage-b set and must not be read as uniform across the two stages.
        #
        # Allowlist disclosure, measured rather than asserted (locator:
        # evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json, at the revision this file carries):
        # against the frozen subject the stage-b set carries exactly ONE addition, `docs/USER_GUIDE.md`,
        # and the governed diff is measured to require it - removing it makes that path UNLISTED and
        # this gate would refuse a path Stage B legitimately ships. This file previously claimed that
        # the change widened NEITHER allowlist; that claim was false and is withdrawn here.
        #
        # The round's own evidence tree is not in either allowlist. `.hgk/**` is excluded from the
        # governed PRODUCT write set by declaration (EXCLUDED_PREFIXES below), printed and counted in
        # this step's output. The earlier arrangement instead listed the round directory inside the
        # allowlist, which had this gate permit writes to the tree holding its own receipts; an
        # exclusion a reviewer can read beats a permission a reviewer has to notice."""

OLD_ESAC_ECHO = """          esac
          echo "=== governed ${STAGE} write set (${BASE}...HEAD) ===\""""

NEW_ESAC_ECHO = """          esac
          # Declared exclusion, not a permission. `.hgk/` is the governance scaffolding tree: this
          # round's admission records, receipts, study and re-derivation tools. It is not product, and
          # it is excluded here so both allowlists enumerate product paths only. Excluded paths are
          # counted and printed below, and the self-test proves no product path can reach this prefix.
          EXCLUDED_PREFIXES='^\\.hgk/'
          echo "=== governed ${STAGE} write set (${BASE}...HEAD) ===\""""

OLD_LOOP_HEAD = """          bad=0
          while IFS= read -r path; do"""

NEW_LOOP_HEAD = """          bad=0
          excluded=0
          excluded_list=""
          while IFS= read -r path; do"""

OLD_LOOP_BODY = """            esac
            if printf '%s' "$path" | grep -Eq "$DENIED"; then"""

NEW_LOOP_BODY = """            esac
            # Exclusion is tested AFTER the traversal refusal so a `/../` path cannot hide inside the
            # excluded prefix: scaffolding paths are skipped here, never silently accepted downstream.
            if printf '%s' "$path" | grep -Eq "$EXCLUDED_PREFIXES"; then
              excluded=$((excluded + 1))
              excluded_list="${excluded_list}${path}"$'\\n'
              continue
            fi
            if printf '%s' "$path" | grep -Eq "$DENIED"; then"""

OLD_POST_LOOP = """          done <<< "${CHANGED}"
          # Self-test of the classifier ITSELF"""

NEW_POST_LOOP = """          done <<< "${CHANGED}"
          echo "EXCLUDED_BY_DECLARATION (${EXCLUDED_PREFIXES}) from the governed PRODUCT write set: ${excluded} path(s)"
          if [ -n "${excluded_list}" ]; then printf '%s' "${excluded_list}" | sed 's/^/  excluded: /'; fi
          # Self-test of the classifier ITSELF"""

OLD_ALLOWED_OK = """          echo "GATE_SELF_TEST_OK: planted ${STAGE} artefacts are all allowed\""""

NEW_ALLOWED_OK = """          # The declared exclusion must be unreachable from every product path; otherwise it would be
          # a blanket escape and the classifier would judge less than it prints.
          for planted in ${ALLOWED_PLANTS} ${REFUSED_PLANTS}; do
            if printf '%s' "$planted" | grep -Eq "$EXCLUDED_PREFIXES"; then
              echo "GATE_SELF_TEST_FAILED: product path ${planted} would have been EXCLUDED" >&2
              exit 1
            fi
          done
          if ! printf '%s' ".hgk/rounds/example-round/evidence/12_GATES/x.json" | grep -Eq "$EXCLUDED_PREFIXES"; then
            echo "GATE_SELF_TEST_FAILED: the declared exclusion does not match the scaffolding tree" >&2
            exit 1
          fi
          echo "GATE_SELF_TEST_OK: the declared exclusion matches scaffolding only and no product path"
          echo "GATE_SELF_TEST_OK: planted ${STAGE} artefacts are all allowed\""""

EDITS = [
    (OLD_COMMENT, NEW_COMMENT, "comment: withdraw the false claim, disclose the measured widening"),
    (ROUND_ALT_A, r"|\.github/workflows/(ci|public-plugin-verify)\.yml$",
     "stage-a ALLOWED: remove the self-referential round-directory entry"),
    (ROUND_ALTS_B, "", "stage-b ALLOWED: remove both round-directory entries"),
    (OLD_ESAC_ECHO, NEW_ESAC_ECHO, "declare EXCLUDED_PREFIXES before the governed diff"),
    (OLD_LOOP_HEAD, NEW_LOOP_HEAD, "count excluded paths"),
    (OLD_LOOP_BODY, NEW_LOOP_BODY, "skip excluded paths, after the traversal refusal"),
    (OLD_POST_LOOP, NEW_POST_LOOP, "print and count the exclusion in the step output"),
    (OLD_ALLOWED_OK, NEW_ALLOWED_OK, "self-test: the exclusion cannot be reached from a product path"),
]


def transform(text: str, apply: bool) -> tuple[str, list[str]]:
    report = []
    for old, new, label in EDITS:
        n = text.count(old)
        if n != 1:
            report.append(f"REFUSED ({n} matches, need exactly 1): {label}")
            continue
        report.append(f"ok: {label}")
        if apply:
            text = text.replace(old, new, 1)
    return text, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a-worktree", required=True)
    ap.add_argument("--b-worktree", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    bad = 0
    outs = {}
    for label, root in (("stage-a copy", args.a_worktree), ("stage-b copy", args.b_worktree)):
        p = pathlib.Path(root) / WF
        text = p.read_text(encoding="utf-8")
        new, report = transform(text, args.apply)
        print(f"--- {label}: {p}")
        for line in report:
            print(f"    {line}")
            if line.startswith("REFUSED"):
                bad = 1
        if args.apply and not bad:
            p.write_text(new, encoding="utf-8")
            print(f"    WROTE {len(new)} chars (was {len(text)})")
        outs[label] = new
    # the invariant that makes the pair reviewable
    a_lines = outs["stage-a copy"].splitlines()
    b_lines = outs["stage-b copy"].splitlines()
    if len(a_lines) == len(b_lines):
        diff = [i for i, (x, y) in enumerate(zip(a_lines, b_lines)) if x != y]
        print(f"\n--- pair invariant (only the STAGE line may differ): {len(diff)} differing line(s)")
        for i in diff:
            print(f"    line {i+1}: A={a_lines[i].strip()!r}")
            print(f"             B={b_lines[i].strip()!r}")
        if len(diff) != 1 or "STAGE:" not in b_lines[diff[0]]:
            bad = 1
    else:
        print("\n--- pair invariant VIOLATED: the copies differ in line count")
        bad = 1
    if args.apply:
        for root in (args.a_worktree, args.b_worktree):
            d = subprocess.run(["git", "-C", root, "diff", "--stat", "--", WF],
                               capture_output=True, text=True).stdout.strip()
            print(f"\n{root}:\n{d}")
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
