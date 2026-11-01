"""Kind-surface ruling v2.1 -- tightened after v2 matched on any help text containing both a kind term and an
install-like word, which produced junk rows (kanban as PROFILE evidence, acp as AI_SYSTEM evidence).

Rule now: a kind's evidence may only come from the verb that owns that kind (profile for PROFILE, plugins for
PLUGIN, ...). Mentions elsewhere are kept as `mentions` and never counted as evidence. Dispositions:
  MEASURED_INSTALL_VERB        the owning verb's help carries an install/create/add verb
  MEASURED_SURFACE_NO_INSTALL  the owning verb exists but its help carries no install-like verb
  OS_SERVICE_INSTALLER_FOUND   gateway install is an OS service installer (AO N4) -- evidence, not a PASS
  UNCLASSIFIED                 the host surface for this kind is doc files, not a command surface
  NO_VERB_EVIDENCE_IN_HELP     no command owns this kind; says nothing about the host beyond its help
"""
import hashlib
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
WP20 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
PROBE = WP20 / "kind_surface_probe" / "KIND_SURFACE_PROBE_V2.json"
HELPDIR = WP20 / "stdout" / "_kind_v2"

OWNER = {
    "AGENT_SKILL": ["skills", "bundles"],
    "PROFILE": ["profile"],
    "PLUGIN": ["plugins"],
    "CLI_TOOL": ["tools", "lsp", "mcp", "computer-use"],
    "SIMPLE_AGENT": [],
    "AGENT_OS": ["gateway", "update"],
    "AI_SYSTEM": ["model", "moa", "proxy", "fallback"],
    "GENIE/GENIE.md": [],
}
INSTALL_TERMS_BY_KIND = {"AI_SYSTEM": ["install", "download", "pull"],
                       "PROFILE": ["create"],
                       "*": ["install", "create", "setup", "download"]}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    probe = json.loads(PROBE.read_text(encoding="utf-8"))
    by_verb = {r["verb"]: r for r in probe["verbs"]}
    kinds = {}
    for kind, owners in OWNER.items():
        evidence, present = [], []
        for v in owners:
            if v not in by_verb:
                continue
            r = by_verb[v]
            text = (HELPDIR / f"{v}_help.txt").read_text(encoding="utf-8", errors="replace")
            present.append({"verb": v, "rc": r["rc"], "help_sha256": r["help_sha"]})
            for ln in text.splitlines():
                low = ln.lower()
                terms = INSTALL_TERMS_BY_KIND.get(kind, INSTALL_TERMS_BY_KIND["*"])
                hit = [t for t in terms if t in low]
                if hit:
                    evidence.append({"verb": v, "rc": r["rc"], "help_sha256": r["help_sha"],
                                     "line": ln.strip()[:180], "matched": hit})
                    break
        if kind == "AGENT_OS" and any(e["verb"] == "gateway" for e in evidence):
            disp = "OS_SERVICE_INSTALLER_FOUND"
        elif not owners:
            disp = "UNCLASSIFIED" if kind == "SIMPLE_AGENT" else "NO_VERB_EVIDENCE_IN_HELP"
        elif evidence:
            disp = "MEASURED_INSTALL_VERB"
        elif present:
            disp = "MEASURED_SURFACE_NO_INSTALL"
        else:
            disp = "NO_VERB_EVIDENCE_IN_HELP"
        kinds[kind] = {"disposition": disp, "owning_verbs_present": present, "evidence": evidence[:4]}

    doc = {
        "schema": "FHS.R21.WP20.KIND_RULING/2.1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "supersedes": ["wp20/KIND_SURFACE_RULING.json (hand-written 69-verb list)",
                       "KIND_SURFACE_RULING_V2.json (v2 matched any help text, not the owning verb)"],
        "ao_return": "wp20/AO_0361E484_RETURN.md",
        "denominator": {"source": "root_help.txt parsed", "verbs": probe["denominator"]["verbs"],
                        "probe": "wp20/kind_surface_probe/KIND_SURFACE_PROBE_V2.json",
                        "probe_sha256": sha(PROBE.read_bytes()),
                        "anomaly": "verb 'hermes' returned rc=2 (root help lists itself)"},
        "kinds": kinds,
        "summary": {k: v["disposition"] for k, v in kinds.items()},
        "withdrawn": [
            "the 69-verb denominator",
            "AGENT_OS / AI_SYSTEM / GENIE 'NO_SURFACE' (not measurable from help text)",
            "SIMPLE_AGENT classification",
            "v2's loose evidence rows (kanban->PROFILE, acp->AI_SYSTEM)"],
        "claim_ceiling": ("author-side help-surface scan. MEASURED_INSTALL_VERB means the owning command's help "
                          "advertises an install-like verb -- not that installing works. OS_SERVICE_INSTALLER_FOUND "
                          "means an OS service installer is advertised, not that an agent OS runtime exists."),
    }
    out = WP20 / "KIND_SURFACE_RULING_V2_1.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"summary": doc["summary"], "sha256": sha(out.read_bytes())[:16]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
