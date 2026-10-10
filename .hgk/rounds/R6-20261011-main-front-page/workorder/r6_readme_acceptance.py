#!/usr/bin/env python3
"""R6 acceptance checks for the rewritten front page (FAR-PIPD-R6-MAIN-FRONT-PAGE-001 AC1-AC7).

Reads README.md as written on this branch and checks each criterion mechanically.
Exit 0 = all AC pass.

Resolution rules for AC5 (why the heuristics are shaped this way):
  * markdown emphasis is stripped before literal matching, so `**not**` matches `not`;
  * a path reference resolves if it is a tracked file, an untracked working-tree file (new
    files not yet committed), a directory anywhere in the tree, or a suffix path under any
    top-level directory;
  * names that live on the *release page* rather than in this repository are exempt, but only
    when the page says so -- that assertion is itself checked;
  * tokens that are not paths at all (ratios like `9/9`, bare extensions like `.sha256`) are
    filtered rather than reported as missing.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

WT = Path(__file__).resolve().parents[4]
README = WT / "README.md"
HIST = WT / "docs" / "FRONT_PAGE_HISTORY.md"

raw = README.read_text(encoding="utf-8")
text = re.sub(r"[*`]", "", raw)          # emphasis/backtick-free copy for literal matching
lines = raw.splitlines()
results = []


def check(ac, ok, detail):
    results.append((ac, bool(ok), detail))


def git(*args) -> list[str]:
    return subprocess.run(["git", *args], cwd=WT, capture_output=True,
                          text=True).stdout.split()


FILES = set(git("ls-files")) | set(git("ls-files", "--others", "--exclude-standard"))
DIRS = {"/".join(f.split("/")[:i]) for f in FILES for i in range(1, len(f.split("/")))}

# names that are release assets, not repo paths
RELEASE_ASSETS = {
    "pipd_ls_sp-0.1.0-py3-none-any.whl",
    "PREVIEW_NOTES_v0.1.0-preview.1.md",
    "SHA256SUMS",
}
# paths that exist on the release branch but not on this one; the page must say so
RELEASE_BRANCH_ONLY = {
    "tests/test_git_object_reader.py",
    "tests/test_doctor_schema_truth.py",
    "tests/test_tqaep_design_positive.py",
    "tools/build_publication_manifest.py",
}
SCOPING_PHRASES = ("On the release branch", "none of which are in this tree")


def resolves(ref: str) -> bool:
    p = ref.rstrip("/")
    if not p:
        return True
    if p in FILES or str(WT / p) and (WT / p).exists() or p in DIRS:
        return True
    return any(f == p or f.endswith("/" + p) or ("/" + p + "/") in f for f in FILES)


# ---- AC1: H1 must not carry the superseded status word; the page must deny being the entry point
h1 = next((l for l in lines if l.startswith("# ")), "")
check("AC1", "review candidate" not in h1.lower(), f"H1 = {h1!r}")
check("AC1b", "Apache-2.0" in text and "not the distribution entry point" in text,
      "names the licensed preview and denies being the entry point")

# ---- AC2: main's own licence state stated; no unreconciled bare non-grant line
check("AC2", "decision: UNSET" in text and "no licence is granted" in text.lower(),
      "main's unlicensed state is stated explicitly")
bare = [l for l in lines if l.strip().lower().startswith("no license is granted")
        and "this branch" not in l.lower()]
check("AC2b", not bare, f"no unreconciled bare 'No license is granted' line (found {len(bare)})")

# ---- AC3: the repo map covers every top-level entry that exists on the branch
top = git("ls-tree", "--name-only", "HEAD")
SELF = {"README.md"}      # the page itself; listing it in its own tree map adds nothing
missing = sorted(e for e in set(top) - SELF if e not in text)
check("AC3", not missing, f"{len(set(top) - SELF)} entries present (README.md exempt: is the page); missing={missing}")

# ---- AC4: every external URL must be the real release target
urls = re.findall(r"https?://[^\s)\]<>`]+", raw)
ok_urls = bool(urls) and all(
    u.startswith("https://github.com/shw097-team/PIPD-LS-SP/releases/tag/v0.1.0-preview.1")
    for u in urls)
check("AC4", ok_urls, f"{len(urls)} external URL(s); all point at the preview tag: {ok_urls}")

# ---- AC5: every in-tree path reference must resolve; release-page names must be declared as such
cands = {m.group(1).strip() for m in re.finditer(r"`([A-Za-z0-9_./-]+)`", raw)}
NOT_A_PATH = re.compile(r"^(\.\w+|\d+/\d+|[a-z]+=.*)$")
refs = {r for r in cands if not NOT_A_PATH.match(r)
        and ("/" in r or r.endswith((".md", ".json", ".toml", ".py", ".yaml", ".whl", ".sha256", ".txt")))}
bad = sorted(r for r in refs - RELEASE_ASSETS - RELEASE_BRANCH_ONLY if not resolves(r))
check("AC5", not bad, f"{len(refs)} path refs checked; unresolvable={bad}")
scoped = all(p in text for p in SCOPING_PHRASES)
check("AC5b", scoped,
      "release-branch-only paths are declared as not being in this tree; "
      f"scoping phrases present={[p for p in SCOPING_PHRASES if p in text]}")
check("AC5c", all(a in text for a in RELEASE_ASSETS),
      "release-page asset names are named in the page (not presented as repo paths)")

# ---- AC6: history moved, not deleted
hist = HIST.read_text(encoding="utf-8") if HIST.exists() else ""
need = ["R3 audit-repair status", "TT-HGK-SANITIZER-UNANCHORED-KEY-PATTERN",
        "QUARANTINE_DISPOSITION_R3.json", "Correction of a wording overclaim",
        "derived, non-authoritative knowledge index", "No license is granted",
        "OD-R3-001", "TEMP_CLOSED"]
missing_h = [n for n in need if n not in hist]
check("AC6", HIST.exists() and not missing_h,
      f"docs/FRONT_PAGE_HISTORY.md present={HIST.exists()}; missing={missing_h}")
check("AC6b", "FRONT_PAGE_HISTORY.md" in raw, "front page points at the moved history")

# ---- AC7: no claim escalation; the unpublished-repair fact is disclosed
esc = [f for f in ("PRODUCTION_VERIFIED is **GRANTED", "FULL_S0_S4_INDEPENDENT_PASS is **GRANTED")
       if f in raw]
check("AC7", not esc, f"no forbidden claim escalations ({esc})")
check("AC7b", "nothing you can download today contains the fix" in text.lower(),
      "discloses that the repair is not published")
check("AC7c", "28 evidenced / 10 active gaps / 19 deferred" in text,
      "carries the PARTIAL_CHALLENGE denominator")

# ---- report
w = max(len(a) for a, _, _ in results)
allok = True
for ac, ok, detail in results:
    allok &= ok
    print(f"[{'PASS' if ok else 'FAIL'}] {ac.ljust(w)}  {detail}")
print()
print(json.dumps({"checks": len(results), "passed": sum(1 for _, o, _ in results if o),
                  "all_pass": allok}, indent=1))
sys.exit(0 if allok else 2)
