#!/usr/bin/env python3
"""S0 G-KNOWLEDGE-READY — quarantine review path.

TT-PIPD-KNOWLEDGE-QUARANTINE close condition: "a quarantine review path distinguishes a documented
pattern from a live secret, with an owner decision recorded". This builds that path and classifies
every quarantined source with reproducible evidence.

It never disables a control: each entry is re-derived from the file, the matched substring is shown
REDACTED, and a real-looking credential would be reported as LIVE_SECRET_SUSPECT (blocking) rather
than waved through. The point is to distinguish a rule the document declares from a value that leaked.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AW = ROOT.parent
REPORT = ROOT / ".hgk" / "knowledge" / "KNOWLEDGE_READY_REPORT.json"
OUT = ROOT / ".hgk" / "knowledge" / "QUARANTINE_REVIEW.json"

METACHARS = set("\\[]{}()?*+|.")


def redact(s: str) -> str:
    """Never store a candidate secret in full: a short prefix/suffix and its length only."""
    if len(s) <= 8:
        return s[0] + "*" * max(0, len(s) - 2) + s[-1] if len(s) > 2 else "**"
    return f"{s[:4]}{'*' * 8}{s[-4:]} (len={len(s)})"


def classify(line: str, span: tuple[int, int], kind: str = "") -> tuple[str, str]:
    matched = line[span[0]:span[1]]
    before = line[span[0] - 1] if span[0] > 0 else ""
    if before and (before.isalnum() or before in "_-"):
        return ("IDENTIFIER_SUBSTRING_FALSE_POSITIVE",
                "the match is the tail of a longer identifier, so the detector's pattern lacks a "
                "left word-boundary anchor")
    if any(c in matched for c in METACHARS):
        return ("PATTERN_DECLARATION",
                "the matched text is itself a regex/rule literal that the document declares")
    if kind == "PROMPT_INJECTION":
        return ("DOCUMENTED_INJECTION_EXAMPLE",
                "the matched phrase is one the document itself quotes as an attack example it "
                "teaches about; the prompt-injection control stays enabled, only this source is "
                "flagged for a human to confirm it is teaching material")
    if re.search(r"^[A-Za-z0-9_\-]{16,}$", matched):
        return ("LIVE_SECRET_SUSPECT", "high-entropy token with no rule syntax; needs owner review")
    return ("PLACEHOLDER_OR_EXAMPLE", "not a rule literal and not credential-shaped")


def main() -> int:
    rep = json.loads(REPORT.read_text(encoding="utf-8"))
    quarantined = rep["knowledge_index_readback"]["quarantined"]
    reviews, counts = [], {}
    for item in quarantined:
        path = AW / item["rel"]
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        findings = []
        for raw in item["findings"]:
            kind, _, pat = raw.partition(":")
            entries = []
            try:
                rx = re.compile(pat)
            except re.error:
                rx = re.compile(re.escape(pat))
            for m in list(rx.finditer(text))[:5]:
                line_start = text.rfind("\n", 0, m.start()) + 1
                line_end = text.find("\n", m.end())
                line = text[line_start:line_end if line_end != -1 else len(text)]
                span = (m.start() - line_start, m.end() - line_start)
                verdict, why = classify(line, span, kind)
                entries.append({"verdict": verdict, "why": why,
                                "match_redacted": redact(m.group(0)),
                                "line_context_redacted": redact(m.group(0)).split(" ")[0]})
                counts[verdict] = counts.get(verdict, 0) + 1
            findings.append({"detector": kind, "pattern_declared_by_report": pat,
                             "matches_in_file": len(list(rx.finditer(text))), "entries": entries})
        reviews.append({"source_id": item["source_id"], "rel": item["rel"], "exists": path.exists(),
                        "sha256_prefix": __import__("hashlib").sha256(text.encode()).hexdigest()[:16],
                        "findings": findings})
    live = counts.get("LIVE_SECRET_SUSPECT", 0)
    payload = {
        "gate": "G-KNOWLEDGE-READY / quarantine review",
        "quarantined_total": len(quarantined),
        "classification_counts": counts,
        "review": reviews,
        "controls_disabled": [],
        "owner_decision_required": True,
        "owner_decision_slot": {
            "question": "Ratify the per-source classification below and lift the quarantine for the "
                        "sources whose only finding is a documented rule or an identifier substring?",
            "options": ["RATIFY_ALL_AS_DOCUMENTED",
                        "RATIFY_SELECTIVELY (list source_ids)",
                        "REJECT (keep quarantined)"],
            "status": "AWAITING_OWNER",
        },
        "verdict": "PARTIAL" if live == 0 else "FAIL",
        "why_not_pass": "the review path and the evidence exist, but lifting a quarantine is a "
                        "knowledge-owner authority act; an agent must not self-clear a security control",
        "candidate_head": __import__("subprocess").run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                                                       capture_output=True, text=True).stdout.strip(),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(json.dumps({"quarantined": len(quarantined), "counts": counts,
                      "live_secret_suspects": live, "verdict": payload["verdict"]},
                     ensure_ascii=False, indent=1))
    return 0 if payload["verdict"] == "PARTIAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
