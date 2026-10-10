# External acceptance entry point — R5 S4 repair round (2026-10-10)

This branch was published so that an **independent verifier** can accept it. Everything here is written
for that reader. **Nothing in this repository is a claim of acceptance** — see the claim ceiling below.

| item | value |
|---|---|
| branch to accept | `r5-s4-packreader` |
| subject commit | the tip of this branch: `git rev-parse HEAD`; pinned authoritatively (commit and tree) in `.hgk/ao/pub/PUBLICATION_SUBJECT_ATTESTATION.json` |
| previous public state (parent) | `7f13b90dc06354a0c6b7bd013f83a8cc244bf93d`; its tree is `git rev-parse 7f13b90^{tree}` |
| round | `R5-20261009-s4-user-operability` |
| scope | exactly one confirmed defect (**D1**) repaired, then independently checked |
| independent verdict | `.hgk/rounds/R5-20261009-s4-user-operability/d1repair/D1_INDEPENDENT_VERDICT_V2.json` |
| the contract that checker executed | `.hgk/rounds/R5-20261009-s4-user-operability/d1repair/CONTRACT-verify-D1.v2.md` |
| superseded first contract (kept deliberately) | `.hgk/rounds/R5-20261009-s4-user-operability/d1repair/CONTRACT-verify-D1.v1.md` |
| writer order | `.hgk/rounds/R5-20261009-s4-user-operability/d1repair/WO-WS-A-codex-writer.md` |
| provenance audit of the defect class | `.hgk/rounds/R5-20261009-s4-user-operability/far/D1_PROVENANCE_AUDIT.md` |
| evidence manifest — every round artifact, delivered or withheld, each with a hash | `.hgk/rounds/R5-20261009-s4-user-operability/EVIDENCE_MANIFEST.json` |

## The defect (D1)

`tools/perf_budget.py` prints a `historical` block, commented as the recorded verdicts of earlier stages.
That block read **no stored value at all**: it re-measured the live corpus and printed the result as if it
were the record. The same field therefore took different values in different checkouts — observed live
readings `343547 / 368432 / 370091 / 372224 / 372935 / 375068` against a committed record of `343547` —
while the adjacent comment claimed the number was *preserved verbatim*. That contradicts the owner ruling
`S2_HISTORICAL_FAIL: PRESERVE` and the committed artifact `.hgk/artifacts/s2/PERF_BUDGET.json`
(`context_bytes_per_artefact = 343547`, verdict `FAIL`). `tests/test_perf_budget.py` could not catch it:
it hard-coded the expected number and asserted only the metric name.

## What changed

1. A `historical` row's `value` is now the **recorded** number, read at run time from the file its
   `origin {file, field}` names, with `recorded: true`. The live reading is **kept separately** in
   `measured_now`, so the drift is visible instead of disguised.
2. A row with no recorded counterpart sets `recorded: false` and states in plain text that its value is a
   live measurement, not a recorded one. No record is fabricated.
3. **No threshold, budget or voting metric changed** — verified byte-identical against the parent.
4. Four regression tests were added; the expectation is read from the recorded file at test time and is
   never hard-coded.

## Subject files, pinned by digest

| file | sha256 |
|---|---|
| `tools/perf_budget.py` | `f90c3d8d6061f55b9807c2e8740998f98124b56fbcb5c42397f459c4368ff015` |
| `tests/test_perf_budget.py` | `6c0d21fa8ce6c0a047539d2333973b88a75eea68c82ce031a96381749791d270` |

## Acceptance criteria — run these yourself, do not trust this file

```bash
git clone --branch r5-s4-packreader https://github.com/shw097-team/PIPD-LS-SP.git pipd-accept
cd pipd-accept

# A1 the digests above match
python -c "import hashlib,pathlib;[print(f,hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest()) for f in ['tools/perf_budget.py','tests/test_perf_budget.py']]"

# A2 the recorded value is invariant, and the live reading is disclosed separately
python tools/perf_budget.py --check
#   historical row must read: value=343547 recorded=true origin={file,field} measured_now=<this checkout's own reading>

# A3 the record really is read from the file it names (perturb a COPY, never the repo)
cp -r . /tmp/pipd-perturb && cd /tmp/pipd-perturb
python - <<'PY'
import json,pathlib
p=pathlib.Path('.hgk/artifacts/s2/BYTES_PER_ATOM_BASELINE.json')
d=json.loads(p.read_text()); d['pi_bytes']=1
p.write_text(json.dumps(d))
PY
python -m unittest tests.test_perf_budget
#   must go RED; a green suite here means the test is inert
cd - && rm -rf /tmp/pipd-perturb

# A4 no regression, and the branch is green where the parent is green
python -m unittest discover -s tests
#   expect: Ran 283 tests ... OK (skipped=4)

# A5 no threshold moved against the parent
git diff 7f13b90 HEAD -- tools/perf_budget.py
#   budgets and voting_metrics must be untouched

# A6 the repository's own spec and projection gates
npx openspec validate --changes --strict
python tools/build_publication_manifest.py --check --commit "$(git rev-parse HEAD)" --tree "$(git rev-parse HEAD^{tree})"
#   expect: violations: []
```

## What was NOT done, and where this could still be wrong

- The independent check was performed by a **different model and a different lane from the maker**
  (`gpt-6.1-sol`, `openai-codex` OAuth, Hermes-native, read-only) against a contract written for it. It
  returned `ALL_PASS`: 9 of 9 properties `RE_DERIVED`, `DISAGREED=0`, `UNCERTAIN=0`. Its first pass over an
  earlier contract returned `FAIL_CHALLENGE`, and that pass's two disagreements were **defects in that
  contract, not in the code**. Both contracts and both verdicts are published side by side so a verifier can
  judge that call rather than take it.
- Seven raw transcripts exceed the evidence threshold and are **withheld with a recorded hash** rather than
  committed; `EVIDENCE_MANIFEST.json` names each one with its size and sha256.
- No deployment, publication or production operation was performed.
- The suite carries pre-existing failures in some environments: run inside a working tree that holds deep
  round artifacts, Windows path limits break two tooling tests. In a clean clone the suite is green. That is
  the parent's property, not this candidate's; `EVIDENCE_MANIFEST.json` records which runs were in which tree.
- The round's own `openspec/specs/` directory is empty, as it is for every other change in this repository —
  changes are kept as validated proposals in `openspec/changes/`, which is the repository's convention, not
  a gap left by this round.

## Claim ceiling for this round

| claim | state |
|---|---|
| `D1_REPAIR_LOCALLY_VERIFIED_BY_INDEPENDENT_CHECKER` | **claimed**, scoped to the published contract and the pinned digests |
| `ARTIFACT_PUBLICLY_CONSUMABLE` | **claimed** — verified by anonymous clone |
| `INDEPENDENT_PASS` | **NOT claimed by the maker** — the maker does not sign its own acceptance |
| `PUBLICATION_APPROVED` | **NOT claimed** |
| `RELEASED` | **NOT claimed** |
| `PRODUCTION_VERIFIED` | **NOT claimed** |

Granting any of those is the external verifier's act, not this round's.
