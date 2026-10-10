# INDEPENDENT CHECKER BRIEF — R5P narrow closure (attempt 3) — PIPD-LS-SP

Attempt 2 returned `PARTIAL`: `C1/C4/C6/C7/C8 PASS`, `C2 FAIL = EVIDENCE_GAP`. Two of your own notes
became repairs. This pass closes exactly those two, **nothing else**, and must stay small.

## Subject (new, frozen)

| role | value |
|---|---|
| baseline | `r5-s4-packreader` @ `0f06eec96386b7349db8b41ac6cf9c7455d326f1` |
| **subject under review now** | **`9caef8ec36017b4c3ca55b9a672da1fa625fff07`** (tree `910f94127ee6367a6f5adff995321b353f4a6f10`) |
| previous subject (attempt 2) | `812af79422c087f0ef5a07188fbec061df6b47e0` |
| only change since attempt 2 | `ACCEPTANCE.md` — a banner naming the R5P subject (closes your C6 note) |
| wheel | sha256 `bb070a6f525382edc521bcf7fe127579e1e329024113ab4fe2881eeeea7b0a76` (unchanged; the wheel packages `src/` only) |

Mounts: `/w` = pristine export of `9caef8ec…` (read-only, no `.git`), `/round` = round evidence
(read-only), `/briefs` (read-only), `/ao` = your only writable place.

## What to do (three things)

1. **C2 close/re-fail on the bound receipt.** `/round/evidence/host_fullsuite_repair_bound.txt` is a
   re-emitted host run that now carries, in the file itself: the exact command line, cwd, `rev-parse
   HEAD`, `rev-parse HEAD^{tree}`, interpreter version, start/finish timestamps and an explicit
   `# exit_code: 0` line after `Ran 311 tests ... OK (skipped=6)`, with the named SKIP lines present.
   Verify the pairing by hashing the file yourself and reading it; state whether C2 can now close as
   `PASS` (evidence sufficient) or still `EVIDENCE_GAP`, and say precisely what is still missing if so.
   Note honestly: in that worktree `git status` shows two non-product entries
   (`.hgk/artifacts/s1/TECHNOLOGY_ADMISSIONS.json` modified and `.hgk/artifacts/tqaep_design_tmp/`
   untracked) written by the suite's own tests; judge whether that changes your verdict.
2. **C8 re-bind for the new subject.** Run `/round/ops/bound_digest.py /w` and compare with
   `/round/evidence/DIGEST_BINDING.json`. The bound digest moved because `ACCEPTANCE.md` changed —
   confirm the new value and that the rejected narrower definition is still labelled rejected.
3. **C6 re-read.** `/w/README.md` line ~39 and `/w/ACCEPTANCE.md` banner: can a first-screen reader
   tell which branch/subject is under review, what the licence grants, and where acceptance lives?

Do **not** re-litigate C1, C4, C5, C7 — they are settled on the previous subject and unchanged here.

## Deliverable

`AO_VERDICT_V3.json` in `/ao` with, for each of C2/C6/C8: `verdict`, `evidence` (raw paths), `note`;
plus `subject_commit`/`subject_tree`, `overall`, `classification`, `independent_of_maker`,
`human_ratification: PENDING`, `claim_ceiling: CANDIDATE_ONLY`. Log in 繁體中文. Every claim needs a
command, an exit code and a raw file. Do not promote any claim level.
