# FAR round 2 — the F1 remedy, decided by measurement and executed

Owner order of 2026-10-13: run FAR on the current state, the open decisions and what can be handed to an
external acceptance officer, recommend the best engineering ruling with an execution plan, and then
execute it. The execution below therefore carries the owner's pre-authorisation; the admission record is
in `far-study/rem2/far2_admission.json`.

## 1. The measurement that decided the remedy

`evidence/12_GATES/ALLOWLIST_MINIMUM_MEASUREMENT.json`, produced by
`scripts/measure_allowlist_minimum.py` at the head named inside it. Method: reproduce the gate's own
governed diff for the stage the branch declares, extract the ALLOWED/DENIED sets and the declared
exclusion from the workflow at that head, classify every changed path, and compute the net allowlist
change against a named revision.

| question | measured answer |
|---|---|
| stage-b governed diff size (Stage A head ... B head) | 151 paths |
| UNLISTED product paths / DENIED product paths | 0 / 0 |
| paths under the round directory | 143 of 151 (`far-study/` 83, `evidence/` 38, `scripts/` 18, round root 3, `admission/` 1) |
| is `docs/USER_GUIDE.md` inside the diff? | yes - so that allowlist entry is **load-bearing**, not gratuitous |
| can the round-directory entry be narrowed? | no: every tested narrowing loses paths (evidence-only loses 105, evidence+far-study loses 22, 12_GATES-only loses 105) |
| net allowlist change versus the frozen subject, after this round's remedy | added: `docs/USER_GUIDE.md$` only; removed: the round-directory entries |

The measurement decides the remedy without a judgement call. Entry 1 must stay (removing it makes a path
Stage B legitimately ships unlisted, and the gate would refuse it). Entry 2 must leave the allowlist: it
is not product, and keeping it means this gate permits writes to the directory that holds its own
receipts. What the measurement does NOT support is any claim that the round-directory entry could simply
be narrowed - that option is dead, and the finding records it as dead rather than leaving it on a list of
options.

## 2. The remedy as executed

Applied by `scripts/rem2_apply_gate_exclusion.py`, which refuses unless each of its eight edits matches
exactly once in each copy and unless the two copies end up differing in exactly one line. Both branch
copies carry their own copy of the gate file, so both were edited, and then the stack was restored.

Entries **removed** from the allowlists (nothing was added anywhere):

| branch copy | `STAGE:` | removed from ALLOWED |
|---|---|---|
| stage-b | `stage-b` | `\.hgk/rounds/S4POST-20261012` |
| stage-b | `stage-b` | `\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` |
| stage-a | `stage-a` | `\.hgk/rounds/S4R3-20261013-ci-truthfulness-and-stageb-writeset/` |

Entries **kept**: `docs/USER_GUIDE.md$` on the stage-b copy, for the reason measured in §1.

Added to the gate (one declaration, in the shell body, in both copies):

```
EXCLUDED_PREFIXES='^\.hgk/'
```

The gate now prints `EXCLUDED_BY_DECLARATION (^\.hgk/) from the governed PRODUCT write set: N path(s)`
and lists each excluded path, so the exclusion is visible in the run log rather than being an implicit
permission inside an allowlist. The exclusion is tested **after** the `..` traversal refusal, so a
traversal path cannot hide inside the excluded prefix. The self-test gained a third obligation: no
planted product path - drawn from both the refused and the allowed plant sets - may match the exclusion
prefix, and a planted path under `.hgk/` must match it.

The withdrawn claim: the file said the change "widens NEITHER allowlist". That was false. It now states
the scope precisely (the DENIED continuity holds for the stage-b set; the stage-a arm deliberately allows
`src/`, so the claim must not be read as uniform), and discloses that the stage-b set carries exactly one
addition measured as required.

## 3. Verification performed, with what each check can falsify

| check | result | what it would falsify |
|---|---|---|
| local gate run, both stages (`run_writeset_gate_locally.py`) | **2/2 clean**, stage-a `WRITE_SET_CLEAN_AGAINST_e71fee6…`, stage-b `WRITE_SET_CLEAN_AGAINST_759b9f0…` | a remedy that leaves the governed write set unlisted, or that breaks the classifier |
| the gate's own self-tests | traversal refused, planted frozen-path violations refused, planted allowed artefacts accepted, exclusion unreachable from product paths | a gate that accepts everything, refuses everything, or quietly widens |
| exclusion accounting | stage-a 23 paths, stage-b 154 paths excluded and listed | an exclusion that silently swallows product paths |
| stacked invariant | `merge-base(A head, B head) == A head` after the edit | an edit that silently detaches the stack |
| pair invariant | the two gate-file copies differ in exactly one line (`STAGE:`) | an edit applied to one branch only |
| hosted CI at both new heads | `public-plugin-verify` and `ci` all **success** (A: 38398212422/38398212337/38398204209; B: 38398216916/38398216898/38398207794) | a local-only green |

Receipts: `REM2_GATE_RUN_BOTH_STAGES.log`, `REM2_PRODUCT_CHANGE_DIFF.txt`,
`ALLOWLIST_MINIMUM_MEASUREMENT.json`, plus the guard outputs `GUARD_COVERAGE_REM2.json`,
`GUARD_RECEIPTS_REM2.json` and `far-study/rem2/blocks_rem2.json`.

## 4. What this changes for an external acceptance officer

Gains: the gate file no longer contains a false statement about its own behaviour; the allowlist no
longer permits writes to the tree holding the gate's receipts; the widening versus the frozen subject is
down to one entry, and that entry carries a measurement showing it is required; the exclusion is printed
where the officer can read it, and the two copies are provably one line apart.

Loses: nothing that had been earned. **No acceptance had been granted on the superseded heads**, so
superseding them costs no accepted result. The earlier lane verdicts (C1 four-of-four, C3 five-of-five
CONFIRMED) were rendered against the superseded revision and are recorded as such - this round re-offers
those claims at the new revision in a fresh bundle rather than carrying them forward.

## 5. Deliberate non-adoptions, so they are not mistaken for oversights

- The bounded writer additionally proposed an `EXCLUDED_REASON` variable. Not adopted: the reason belongs
  in the comment a reviewer reads, and a second machine-readable copy of the same sentence would be a
  second place to keep in sync. Disclosed because the writer recommended it and the executor declined.
- No oracle, threshold, validator, guard, exit code or denominator was relaxed anywhere. The remedy
  removes permissions and adds a check; it loosens nothing.
- No merge, tag, release or archive. `NO_MERGE` / `NO_PUBLIC_RELEASE` / `S4_FULL_PASS NOT_GRANTED` stand.

## 6. Still open, unchanged by this round

F003 owner gate inputs; the four-host UAT (never executed); canonical acceptance rows (still `NOT_RUN`,
zero `evidence_refs`); the published preview.3 wheel whose Trace false-PASS was not rebuilt; the `.hgk/`
archive policy; whether the checker lane should be given read/execute so its verdicts can reach tree-level
truth rather than bundle-level consistency. The last of these is the one that most changes what any
future `CONFIRMED` can mean.
