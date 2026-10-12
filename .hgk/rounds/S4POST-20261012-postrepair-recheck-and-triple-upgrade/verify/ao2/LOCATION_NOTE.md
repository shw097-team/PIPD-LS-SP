# Location note - the AO2 evidence set was relocated here, contents unchanged

The round-2 officer wrote its output to `<worktree>/verify/ao2/` at the repository root, because the
brief it was given named that relative path. The repository-root `verify/` prefix is **outside the
Stage-B write-set allowlist** (`^packaging/public-plugin/|tools/...|docs/install/|docs/adr/|
openspec/changes/s4post-triple-upgrade/|.github/workflows/public-plugin-verify.yml$|README.md$|
.hgk/rounds/S4POST-20261012`), so committing it there would itself have been an allowlist violation.

The directory was therefore **moved**, not rewritten, to
`.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao2/`.

Integrity of the move: all 36 files hashed before and after; the sorted sha256 multiset is identical
(36/36), i.e. every byte of the officer's raw evidence is the same. The empty root `verify/` directory
was then removed. No officer-authored byte was edited, and the officer's verdict was not touched.

**Known consequence, disclosed rather than hidden:** absolute path strings inside the officer's own
verdict (and inside its raw logs) still read `.../s4post-b-wt/verify/ao2/...`. Those strings are now
stale by one directory component. This note is the crosswalk; the officer's verdict is left verbatim
so that its authorship is intact.

The brief handed to the officer was the actual defect: it should have named the round-relative path,
or the officer should have been told that root `verify/` is outside the allowlist. Recorded as a
round-level process finding, not a defect of the candidate code.

## Second step: the double nesting was flattened

The officer had created `<root>/verify/ao2/` and written its files into `.../verify/ao2/ao2/`.
After the move that became `{round}/verify/ao2/ao2/`. The inner directory was flattened up one level
so the evidence now sits directly in `{round}/verify/ao2/`, which also matches the `verify/ao2/<file>`
tail the officer's verdict references. Re-hashed across the flatten: the 36 officer files are again
byte-identical (36/36). This directory now holds 37 files: those 36 plus this note.
