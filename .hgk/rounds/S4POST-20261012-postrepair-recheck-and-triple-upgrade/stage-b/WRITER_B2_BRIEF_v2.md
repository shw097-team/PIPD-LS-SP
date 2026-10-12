# Bounded writer — Stage B lane B2 (resumed round): web fallback tests + tool fixes

You are a **bounded writer** working in `C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt`
(branch `feat/s4post-triple-upgrade-20261012`). Change ONLY files under "Allowed write set".

## Allowed write set (absolute)
- `tests/test_web_fallback.py`  (new)
- `tools/build_web_fallback.py` (fix only where a test proves it wrong)

Forbidden: everything else - `skills/**`, `src/**`, `schemas/**`, `dist/**`, `.hgk/**`, `README.md`,
`docs/**`, `.github/**`, `packaging/**`, `tests/test_public_plugin_packaging.py`, git history,
commit, push, tag.

## Read first
`tools/build_web_fallback.py`. It is stdlib-only by design. **No new dependency, no network.**

## Deliverable — `tests/test_web_fallback.py`
stdlib `unittest`, temp-directory fixtures, no network, must never touch the real repo tree. Call the
real `build()` function - never a re-implementation.

Cases:
1. exact projection: a frozen mount pack (a small `MANIFEST.sha256` plus its member documents) is
   reproduced into ONE markdown document whose embedded section carries the source bytes verbatim,
   plus the member inventory table and the `DOC_MOUNT_ONLY` ceiling stamp.
2. stale release stamp: a document that names the release but not the pinned commit (or vice versa)
   is REFUSED.
3. over-cap input is REFUSED with no truncation - and assert the destination file does **not** exist
   afterwards (not merely that an exception was raised).
4. a source member whose digest disagrees with the manifest is REFUSED.
5. an unexpected extra file in the mount (absent from the manifest) is REFUSED, and so is a manifest
   entry with no file.
6. an existing destination file is REFUSED (`O_EXCL` semantics) and its bytes are unchanged.
7. a symlinked destination is REFUSED **and the sentinel file behind the symlink is byte-identical
   afterwards**.
8. a manifest that is itself a symlink, or a member that escapes the mount root, is REFUSED.
9. a non-UTF-8 / non-text member type is REFUSED.
10. the refusal path is a **non-zero exit** through the module's CLI `main()` equivalent, and the
    output above the cap is refused rather than trimmed.

## Rules
- If a test exposes a real tool defect, FIX THE TOOL. Never weaken an assertion to match the code.
- Finish by pasting VERBATIM into your final message: the exact command and its summary line for
  `python -m unittest tests.test_web_fallback -v`, then for
  `python -m unittest discover -s tests -t .` (paste only its final `Ran N tests ... OK/FAILED` line).
