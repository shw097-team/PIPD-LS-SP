#!/usr/bin/env bash
# Stage B split lanes: three SHORT sequential writer runs (the declared model dies on long runs, so
# the work is split to keep each lane well under the turn count that trips the adapter bug).
set -u
BWT=C:/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt
W="$BWT/.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/stage-b"
CB=/c/Users/user/AppData/Local/OpenAI/Codex/bin/2e5e00daee91c61d/codex.exe
M="${SUBST_MODEL:-gpt-5.6-terra}"

mkdir -p "$W"
cd /c/Projects/Agent_Workspace/PIPD/worktrees/s4post-b-wt

cat > "$W/SPLIT_B1_brief.md" <<'EOF'
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
EOF

cat > "$W/SPLIT_B2_brief.md" <<'EOF'
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
EOF

cat > "$W/SPLIT_B3_brief.md" <<'EOF'
# Bounded writer — Stage B lane B3: install docs + verify workflow (SHORT RUN, no tool edits)

Allowed writes: `docs/install/README.md`, `docs/install/PIPD_AGENT_INSTALL_PROMPT.md` (both new),
`.github/workflows/public-plugin-verify.yml` (new), and `README.md` (install entry points only).
Do NOT edit any file under `tools/`, `tests/` or `packaging/`.

`docs/install/README.md` - one install SSOT: the Web route, the Agent route, the Web fallback and
its DOC_MOUNT_ONLY limit, and the explicit statement that no public directory listing exists yet so
the fallback is the current Web route.
`docs/install/PIPD_AGENT_INSTALL_PROMPT.md` - one copy-paste prompt that makes a host detect itself,
show the exact paths and diffs, ask for consent, verify REAL discovery rather than file presence,
and report NOT_VERIFIED when only files were copied.
`.github/workflows/public-plugin-verify.yml` - `permissions: contents: read`, SHA-pinned actions, no
`pull_request_target`, no secrets, no tag or publish step, and a negative step that FAILS CLOSED:
require the suite green first, require an actual test failure after the mutation, and require the
failure motive (not merely a non-zero exit). Validate the YAML parses.
`README.md` - only the two install entry points plus a pointer to `docs/install/`.

Finish by pasting verbatim: the YAML parse result, and the lines you added to README.md.
EOF

for L in B1 B2 B3; do
  echo "=== LANE $L (model=$M) ==="
  timeout 1800 "$CB" -c model="$M" -c openai_base_url='http://127.0.0.1:10102/v1' \
    -c model_catalog_json='C:/Users/user/.codex/desktop-model-catalog.json' \
    exec --skip-git-repo-check -s danger-full-access - < "$W/SPLIT_${L}_brief.md" \
    > "$W/SPLIT_${L}_OUTPUT.log" 2>&1
  echo "  exit=$? log=$(wc -c < "$W/SPLIT_${L}_OUTPUT.log") bytes"
  tail -6 "$W/SPLIT_${L}_OUTPUT.log"
done
echo "=== 交付盤點"
ls tests/test_public_plugin_packaging.py tests/test_web_fallback.py docs/install/ .github/workflows/public-plugin-verify.yml 2>&1 | tail -6
