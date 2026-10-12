# Bounded writer — Stage B lane B1: packaging tests + tool fixes (SHORT RUN)

Allowed writes: `tests/test_public_plugin_packaging.py` (new), and fixes only inside
`tools/freeze_public_plugin_source.py` and `tools/build_public_plugin.py`. Nothing else.

Read your two tools, then write `tests/test_public_plugin_packaging.py` (stdlib only, fixtures in a
temp dir, no network, must not touch the real repo). It must assert: fake PNG refused (valid magic,
invalid body) and non-PNG refused; unknown plugin manifest property refused; invalid SKILL
frontmatter refused; null/short/mismatched source commit refused (40-hex); symlinked release dir
refused AND the sentinel behind it untouched; changed source set refused; a ninth skill refused;
non-regular/symlinked source file refused; dirty worktree refused; two builds byte-identical
(member set, order, mode, mtime); derivation without an owner record refused; with an owner record
accepted AND the SKILL.md body byte-identical; output overlapping the repo refused; writing into
`dist/` refused; and the owner-input refusal is a NON-ZERO exit with a typed reason (the owner
inputs are deliberately absent: `derivations.json` is empty and no image asset exists).

Fix the TOOLS where they do not satisfy this - never weaken an assertion to match the code.

Finish by pasting verbatim: `python -m unittest tests.test_public_plugin_packaging` summary, then
`python -m unittest discover -s tests -t .` summary. No commit, no push, do not touch `dist/`.
