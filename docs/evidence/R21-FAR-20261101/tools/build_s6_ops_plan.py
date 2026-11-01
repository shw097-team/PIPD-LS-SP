"""Turn the 14 OPS edges into a per-ID plan: what the body demands, and what actually exists here.

The user rejects family-level blocker inference, so every row gets its own verdict:
  * the body's own ACC/POS, NEG and first_fail lines (verbatim, so the row cannot drift from the source)
  * a bounded search for a real artefact for that domain, with path + sha256 when found
  * a disposition that names exactly what is missing for THAT row

No row is marked executable because a sibling row is.
"""
import hashlib
import json
import os
import pathlib
import re
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
BODY = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric"
                    r"\FHS\FHS-MSC\FHS-MSC_PIPD-LS-PKG"
                    r"\FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1\01_FHS-MSC_PIPD-LS-PKG_BODY")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "ledgers"
LEDGER = OUT / "S6_EDGE_EFFECT_LEDGER.json"

# Evidence this round actually produced (raw pointers), as opposed to names that merely look right.
EXERCISED = {
    "ISSUER_SUBJECT": {"level": "EXERCISED_THIS_ROUND",
                       "artefact": "HG-KSEOS/scripts/issue_grant.py",
                       "raw": "var/FHS-R21-FAR-TT-20261101/wp13/C5_UNDER_ENVELOPE.json",
                       "what": "grant issued with principal=owner, nonce, ttl=1800, subject=WP-FHS-13; owner-envelope "
                               "signature over the verifier payload; issuer verifier rc=0; swap bound that grant"},
    "RECEIVER_ABI": {"level": "EXERCISED_THIS_ROUND",
                     "artefact": "PIPD/src/pipd_ls_sp/abi.py",
                     "raw": "var/FHS-R21-FAR-TT-20261101/patches/tests/RESULTS.json",
                     "what": "T1 proves the ABI version gate rejects a mismatched Need (ERR_ABI_VERSION_MISMATCH) after "
                             "the candidate patch; pre-patch the gate was unreachable"},
    "QUEUE_WO": {"level": "FILE_QUERIED",
                 "artefact": "HG-KSEOS/scripts/work_queue.py",
                 "raw": "HG-KSEOS/var/shared-spine/hg-kseos.db (work_queue, read-only 19 PASS / 3 FAIL)",
                 "what": "the queue the spine actually reads; queried this round, not exercised against this edge"},
}

SEARCH_ROOTS = ["PIPD/src", "PIPD/tools", "HG-KSEOS/scripts", "HG-KSEOS/src"]
SKIP = {"node_modules", ".git", "var", "__pycache__", ".venv", "venv", "homes"}

# domain -> keywords that would have to appear in a real implementation of that effect
DOMAIN_TERMS = {
    "ISSUER_SUBJECT": ["issuer", "principal", "nonce"],
    "QUEUE_WO": ["queue", "workorder", "work_order"],
    "RECEIVER_ABI": ["abi", "receiver"],
    "EFFECT_JOURNAL": ["journal", "effect_log", "receipt"],
    "NATIVE_CONTINUATION": ["continuation", "resume", "checkpoint"],
    "REVOKE_RACE": ["revoke", "race"],
    "NATIVE_SUCCESSOR": ["successor", "handover"],
}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def search(terms, limit=6):
    hits = []
    for r in SEARCH_ROOTS:
        base = ROOT / r
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP]
            if dirpath[len(str(base)):].count(os.sep) > 3:
                dirnames[:] = []
                continue
            for fn in filenames:
                if not fn.endswith((".py", ".json", ".md")):
                    continue
                tokens = set(re.split(r"[^a-z0-9]+", fn.lower()))
                if any(t in tokens for t in terms):
                    p = pathlib.Path(dirpath) / fn
                    try:
                        hits.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                                     "bytes": p.stat().st_size, "sha256": sha(p),
                                     "matched_by": "filename"})
                    except OSError:
                        continue
                    if len(hits) >= limit:
                        return hits
    if hits:
        return hits
    scanned = 0
    for r in SEARCH_ROOTS:
        base = ROOT / r
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP]
            if dirpath[len(str(base)):].count(os.sep) > 2:
                dirnames[:] = []
                continue
            for fn in filenames:
                if not fn.endswith((".py", ".json")) or scanned > 600:
                    continue
                p = pathlib.Path(dirpath) / fn
                try:
                    if p.stat().st_size > 400_000:
                        continue
                    body = p.read_text(encoding="utf-8", errors="replace").lower()
                except OSError:
                    continue
                scanned += 1
                if all(t in body for t in terms):
                    hits.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                                 "bytes": p.stat().st_size, "sha256": sha(p),
                                 "matched_by": "content"})
                    if len(hits) >= limit:
                        return hits
    return hits


def section_fields(lines, start):
    """Collect the body lines for one edge section, keyed by their leading label."""
    out = {}
    for l in lines[start:]:
        t = l.strip()
        if t.startswith("#"):
            break
        m = re.match(r"-\s*([^：:]{1,24})[：:]\s*(.*)", t)
        if m:
            key = m.group(1).strip()
            out.setdefault(key, m.group(2).strip())
    return out


def main():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    lines = (BODY / "10B_B1_PI27_PD31.md").read_text(encoding="utf-8", errors="replace").splitlines()
    line_of = {e["edge"]: e["line"] for e in ledger["edges"]}
    ops = [e for e in ledger["edges"] if e["effect_class"] == "OPS"]

    rows = []
    for e in ops:
        f = section_fields(lines, line_of[e["edge"]])
        terms = DOMAIN_TERMS.get(e["domain"], [e["domain"].lower().split("_")[0]])
        hits = search(terms)
        rows.append({
            "edge": e["edge"], "pd": e["pd"], "atom": e["atom"], "domain": e["domain"], "line": e["line"],
            "acceptance_pos": f.get("ACC/POS") or f.get("ACC"),
            "negative": f.get("NEG"),
            "first_fail": f.get("first_fail"),
            "exit_resume": f.get("exit/resume"),
            "tqaep": e["tqaep"],
            "search_terms": terms,
            "artefacts_found": hits,
            "disposition": ("CANDIDATE_ARTEFACT_BY_NAME" if any(h.get("matched_by") == "filename" for h in hits)
                            else ("COINCIDENCE_ONLY" if hits else "NO_CANDIDATE")),
            "ex_evidence": EXERCISED.get(e["domain"]),
            "unblock": (((f"bind {e['domain']} to {hits[0]['path']} (sha {hits[0]['sha256'][:12]}) and prove POS/NEG "
                          f"with {len(e['tqaep'])} named cases") if any(h.get("matched_by") == "filename" for h in hits)
                         else (f"{e['domain']}: the only files containing all of {terms} are {hits[0]['path']}; that is a "
                               f"word coincidence, not an implementation, so the row stays unbound"))
                        if hits else
                        (f"needs a {e['domain']} host receiver; no file name or body in PIPD/src, PIPD/tools, "
                         f"HG-KSEOS/scripts matches {terms}")),
        })

    doc = {
        "schema": "FHS.R21.S6.OPS_EDGE_PLAN/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "derived_from": {"ledger": "S6_EDGE_EFFECT_LEDGER.json", "body": "10B_B1_PI27_PD31.md#10.1"},
        "row_count": len(rows),
        "dispositions": {d: sum(1 for r in rows if r["disposition"] == d)
                         for d in {r["disposition"] for r in rows}},
        "exercised_rows": sum(1 for r in rows if r.get("ex_evidence")),
        "rows": rows,
        "claim_ceiling": ("per-edge inventory only: no OPS edge has been executed. CANDIDATE_ARTEFACT_BY_NAME means a "
                          "file NAME carries the domain token -- it is a lead, not an implementation. COINCIDENCE_ONLY "
                          "means only body text matched, which is not evidence and must not be cited as one."),
    }
    (OUT / "S6_OPS_EDGE_PLAN.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                              encoding="utf-8", newline="\n")
    with open(OUT / "S6_OPS_EDGE_PLAN.tsv", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("edge\tpd\tdomain\tdisposition\tartefact\tunblock\tanchor\n")
        for r in rows:
            fh.write("\t".join([r["edge"], r["pd"], r["domain"], r["disposition"],
                                r["artefacts_found"][0]["path"] if r["artefacts_found"] else "",
                                r["unblock"].replace("\t", " "),
                                f"10B_B1_PI27_PD31.md#L{r['line']}"] ) + "\n")
    print(json.dumps({"rows": len(rows), "dispositions": doc["dispositions"],
                      "per_row": [(r["edge"], r["domain"], r["disposition"],
                                   r["artefacts_found"][0]["path"] if r["artefacts_found"] else None)
                                  for r in rows]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
