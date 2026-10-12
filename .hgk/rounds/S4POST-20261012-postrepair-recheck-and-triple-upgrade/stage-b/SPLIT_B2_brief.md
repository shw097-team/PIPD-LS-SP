# Bounded writer — Stage B lane B2: web-fallback tests + tool fixes (SHORT RUN)

Allowed writes: `tests/test_web_fallback.py` (new), and fixes only inside
`tools/build_web_fallback.py`. Nothing else.

Read the tool, then write `tests/test_web_fallback.py` (stdlib only, temp fixtures, no network).
It must assert: exact projection of the frozen mount pack; a document that does not stamp the
release identity is refused; a bad source digest is refused; a manifest/member mismatch is refused;
an unexpected extra file is refused; over-cap input is REFUSED, never truncated (assert the output
is not a shortened document); an existing destination is refused; a symlinked destination is refused
with the sentinel intact; and the document stamps its mount-only ceiling plus the member inventory.

Fix the TOOL where it does not satisfy this - never weaken an assertion to match the code.

Finish by pasting verbatim: `python -m unittest tests.test_web_fallback` summary, then
`python -m unittest discover -s tests -t .` summary. No commit, no push, do not touch `dist/`.
