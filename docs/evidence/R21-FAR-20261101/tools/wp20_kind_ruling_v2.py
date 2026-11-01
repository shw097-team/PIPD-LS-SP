"""Kind-surface ruling v2: same 8 kinds, denominator from root_help, dispositions that cannot overclaim.

What changed and why:
  * denominator: 68 commands parsed from root_help.txt (the old "69 verbs" set omitted browser, codex-runtime,
    migrate, profile and included 5 non-commands).
  * disposition vocabulary: the old set said "NO_SURFACE" for three kinds while only having scanned help prose.
    Here a kind can only be labelled NO_VERB_EVIDENCE_IN_HELP -- i.e. "no command help mentions it" -- which is
    a statement about the help surface, not about the host. AGENT_OS gets OS_SERVICE_INSTALLER_FOUND because
    `gateway install` really is an OS service installer (AO N4), and that is recorded as evidence, not as a PASS.
  * every row carries verb + rc + help sha + the verbatim line, so a receiver can re-derive it.
"""
import hashlib
import json
import pathlib
import re
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
WP20 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
PROBE = WP20 / "kind_surface_probe" / "KIND_SURFACE_PROBE_V2.json"
HELPDIR = WP20 / "stdout" / "_kind_v2"

KINDS = {
    "AGENT_SKILL": {"terms": ["skill"], "install_terms": ["install", "add", "sync"]},
    "PROFILE": {"terms": ["profile"], "install_terms": ["create", "clone"]},
    "PLUGIN": {"terms": ["plugin"], "install_terms": ["install", "add"]},
    "CLI_TOOL": {"terms": ["tool"], "install_terms": ["install", "add"]},
    "SIMPLE_AGENT": {"terms": ["agent"], "install_terms": ["install", "add"]},
    "AGENT_OS": {"terms": ["operating system", "systemd", "launchd", "service"], "install_terms": ["install"]},
    "AI_SYSTEM": {"terms": ["model", "provider", "inference"], "install_terms": ["install", "pull", "download"]},
    "GENIE/GENIE.md": {"terms": ["genie"], "install_terms": ["install"]},
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    probe = json.loads(PROBE.read_text(encoding="utf-8"))
    rows = probe["verbs"]
    kinds = {}
    for kind, spec in KINDS.items():
        evidence = []
        for r in rows:
            text = (HELPDIR / f"{r['verb']}_help.txt").read_text(encoding="utf-8", errors="replace")
            low = text.lower()
            if not any(t in low for t in spec["terms"]):
                continue
            if not any(t in low for t in spec["install_terms"]):
                continue
            line = next((ln.strip() for ln in text.splitlines()
                         if any(t in ln.lower() for t in spec["install_terms"])
                         and any(t in ln.lower() for t in spec["terms"])), None)
            if line is None:
                line = next((ln.strip() for ln in text.splitlines()
                             if any(t in ln.lower() for t in spec["install_terms"])), "")
            evidence.append({"verb": r["verb"], "rc": r["rc"], "help_sha256": r["help_sha"],
                             "help_file": r["help_file"], "line": line[:180]})
        if kind == "AGENT_OS":
            disp = "OS_SERVICE_INSTALLER_FOUND" if any(e["verb"] == "gateway" for e in evidence) else "NO_VERB_EVIDENCE_IN_HELP"
        elif kind == "SIMPLE_AGENT":
            disp = "UNCLASSIFIED"
        elif evidence:
            disp = "MEASURED_VERB_EVIDENCE"
        else:
            disp = "NO_VERB_EVIDENCE_IN_HELP"
        kinds[kind] = {"disposition": disp, "evidence": evidence[:6], "evidence_count": len(evidence)}

    doc = {
        "schema": "FHS.R21.WP20.KIND_RULING/2",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "supersedes": "wp20/KIND_SURFACE_RULING.json (which used a hand-written 69-verb list)",
        "ao_return": "wp20/AO_0361E484_RETURN.md",
        "denominator": {"source": "root_help.txt parsed", "verbs": probe["denominator"]["verbs"],
                        "probe": "wp20/kind_surface_probe/KIND_SURFACE_PROBE_V2.json",
                        "probe_sha256": sha(PROBE.read_bytes())},
        "kinds": kinds,
        "summary": {k: v["disposition"] for k, v in kinds.items()},
        "withdrawn": [
            "the 69-verb denominator",
            "AGENT_OS / AI_SYSTEM / GENIE NO_SURFACE ('no surface' is not measurable from help text)",
            "SIMPLE_AGENT classification"],
        "claim_ceiling": ("author-side help-surface scan only. MEASURED_VERB_EVIDENCE means a command's own help "
                          "mentions the kind and an install-like verb; it does not mean the install works, nor that "
                          "a runtime loads. NO_VERB_EVIDENCE_IN_HELP says nothing about the host beyond its help."),
    }
    out = WP20 / "KIND_SURFACE_RULING_V2.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"summary": doc["summary"], "sha256": sha(out.read_bytes())[:16],
                      "verbs": doc["denominator"]["verbs"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
