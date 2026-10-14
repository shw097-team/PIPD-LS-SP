#!/usr/bin/env python3
"""check_evidence_locators.py - FAR R6: can a third party re-run this bundle's locators?

A finding whose locator resolves only inside the REVIEWER's private temp root, or only inside an
out-of-tree skill/contract copy, is NOT independently re-runnable even when the report itself is
readable (measured: AO10/AO11/AO12 staged evidence under %LOCALAPPDATA%\\Temp\\<lane>-* roots the maker
identity cannot list, and the canonical challenge-review lane lives in ~/.agents/skills/**, outside the repo).

Classification (per locator):
  RESOLVES_IN_TREE  - a real path under --root (or under a --search-dir)
  EXTERNAL_ONLY     - an existing path OUTSIDE --root   [OFFENDER]
  UNRESOLVABLE      - a path-shaped locator with no file behind it anywhere searched [OFFENDER]
  SHORTHAND_BARE_NAME - a bare `name.ext` with no path separator; not a locator, counted only

Usage: check_evidence_locators.py --root <tree> [--search-dir D]... [--json-out F] <file-or-dir>...
Exit: 0 = no offenders; 2 = offenders; 1 = usage error.
"""
import argparse, json, os, re, sys

# path-shaped: MUST contain a separator (so a bare `plugin.json` is a shorthand, not a locator)
ABS = re.compile(r'([A-Za-z]:[\\/][^\s"\'`<>|)*\]]*)')
REL = re.compile(r'([\w.\-]+(?:[\\/][\w.\-]+)+\.(?:py|ipynb|md|json|jsonl|sh|ps1|txt|log|yml|yaml|js|html|css|whl|png|toml|cfg|ini))')
BARE = re.compile(r'([\w.\-]+\.(?:py|md|json|sh|txt|log|yml|yaml))')
SKIP = re.compile(r'^(mailto:|git@)', re.I)
URL = re.compile(r'\bhttps?://[^\s"\'`<>|)\]*]+', re.I)

def iter_text(p):
    if os.path.isdir(p):
        for r, _d, fs in os.walk(p):
            for f in fs:
                if f.endswith(('.md','.json','.txt','.log','.yml','.yaml')):
                    yield os.path.join(r, f)
    else:
        yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--search-dir', action='append', default=[])
    ap.add_argument('--json-out')
    ap.add_argument('inputs', nargs='+')
    a = ap.parse_args()
    root = os.path.realpath(a.root)
    searches = [root] + [os.path.realpath(d) for d in a.search_dir]
    counts = {k:0 for k in ('RESOLVES_IN_TREE','EXTERNAL_ONLY','UNRESOLVABLE','SHORTHAND_BARE_NAME')}
    rows = []
    for src in a.inputs:
        for f in iter_text(src):
            try: txt = open(f, encoding='utf-8', errors='replace').read()
            except OSError: continue
            # A URL is not an in-tree locator. The previous form anchored SKIP at '^', so a URL
            # inside prose (e.g. `https://host/a/b.json`) was never skipped and got fragmented into
            # a relative-token candidate ('s://host/a/b.json'). Mask URLs before tokenising.
            txt = URL.sub(' ', txt)
            seen = set()
            toks = [(m.group(1).strip().rstrip('.,;:'), 'path') for m in ABS.finditer(txt)]
            toks += [(m.group(1).strip().rstrip('.,;:'), 'rel') for m in REL.finditer(txt)]
            bare = {m.group(1).strip().rstrip('.,;:') for m in BARE.finditer(txt)}
            for tok, kind in toks:
                if not tok or tok in seen or SKIP.match(tok) or len(tok) < 5: continue
                seen.add(tok)
                if os.path.isabs(tok):
                    rp = os.path.realpath(tok)
                    cls = ('RESOLVES_IN_TREE' if rp.startswith(root)
                           else ('EXTERNAL_ONLY' if os.path.exists(rp) else 'UNRESOLVABLE'))
                else:
                    cands = [os.path.join(os.path.dirname(f), tok)] + [os.path.join(s, tok) for s in searches]
                    cls = 'RESOLVES_IN_TREE' if any(os.path.exists(c) for c in cands) else 'UNRESOLVABLE'
                counts[cls] += 1
                if cls in ('EXTERNAL_ONLY','UNRESOLVABLE'):
                    rows.append({'file': os.path.relpath(f, root), 'locator': tok, 'class': cls})
            for b in bare:
                if b not in seen and '/' not in b and '\\' not in b:
                    counts['SHORTHAND_BARE_NAME'] += 1
    bad = counts['EXTERNAL_ONLY'] + counts['UNRESOLVABLE']
    verdict = 'PASS_LOCATORS_IN_TREE' if bad == 0 else 'FAIL_LOCATORS_NOT_RERUNNABLE'
    out = {'schema':'HGK-EVIDENCE-LOCATOR-CHECK/1','root':root,'search_dirs':searches,
           'verdict':verdict,'counts':counts,'offenders':rows}
    if a.json_out: open(a.json_out,'w',encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    print(json.dumps({'verdict':verdict,'counts':counts}, ensure_ascii=False))
    for r in rows[:14]: print(f"  {r['class']:14} {r['locator'][:100]}")
    return 2 if bad else 0

if __name__ == '__main__': sys.exit(main())