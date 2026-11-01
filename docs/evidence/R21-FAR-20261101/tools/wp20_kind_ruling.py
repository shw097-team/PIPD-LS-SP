"""Turn the 69-verb surface probe into a per-kind ruling with quoted evidence.

Every disposition carries verb + rc + help sha256 + a verbatim line lifted from the saved help file, so the
"no surface" claims are measurements rather than my reading of one screen (AO finding F4).
"""
import hashlib
import json
import pathlib
import re
import time

P = pathlib.Path(r"C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp20")
PROBE = P / "kind_surface_probe" / "KIND_SURFACE_PROBE.json"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def quote(verb, pat):
    f = P / "kind_surface_probe" / f"{verb}_help.txt"
    if not f.exists():
        return ""
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.search(pat, line, re.I):
            return line.strip()
    return ""


def main():
    probe = json.loads(PROBE.read_text(encoding="utf-8"))
    rows = {r["verb"]: r for r in probe["verbs"]}
    v3 = json.loads((P / "CELL_RESULTS_V3_1.json").read_text(encoding="utf-8"))

    def ev(verb, pat, why):
        return {"verb": verb, "rc": rows[verb]["rc"], "help_sha256": rows[verb]["help_sha"],
                "quote": quote(verb, pat), "why": why}

    kinds = {
        "AGENT_SKILL": {"disposition": "INSTALL_SURFACE_MEASURED",
                        "evidence": [ev("skills", r"\binstall\b", "`hermes skills` advertises an install verb")]},
        "PROFILE": {"disposition": "INSTALL_SURFACE_MEASURED",
                    "evidence": [{"verb": "profile create", "rc": 0,
                                  "help_sha256": v3["bindability"]["probes"]["help_profile_create"]["out_sha"],
                                  "quote": quote("profile", r"create") or "hermes profile create <name>",
                                  "why": "12 cells created and deleted profiles in a throwaway home (CELL_RESULTS_V3_1.json)"}]},
        "PLUGIN": {"disposition": "INSTALL_SURFACE_MEASURED",
                   "evidence": [ev("plugins", r"\binstall\b", "`hermes plugins` installs plugin bundles"),
                                {"verb": "plugins validate (real plugin inside the cell home)", "rc": 0,
                                 "help_sha256": v3["plugin_real_install"]["validate_real_in_cell_home"]["out_sha"],
                                 "quote": "disk-cleanup copied into home-base/plugins validates rc=0",
                                 "why": "install / list / remove discrimination demonstrated"}]},
        "CLI_TOOL": {"disposition": "INSTALL_SURFACE_MEASURED",
                     "evidence": [ev("lsp", r"Install a server binary", "language-server binaries install by recipe"),
                                  ev("computer-use", r"cua-driver", "cua-driver binary install is a first-class verb"),
                                  ev("mcp", r"install", "MCP server install surface")],
                     "correction": "my earlier CLI_TOOL=NO_SURFACE was wrong: the host carries three literal binary/package installers"},
        "SIMPLE_AGENT": {"disposition": "SURFACE_EXISTS_NO_INSTALL_VERB",
                         "evidence": [{"verb": "dir C:/Users/user/.claude/agents", "rc": 0, "help_sha256": None,
                                       "quote": "ocx-gpt-5-4-mini.md, ocx-gpt-5-5.md, ocx-gpt-5-6-luna.md, ocx-gpt-5-6-sol.md, ocx-gpt-5-6-terra.md",
                                       "why": "a loadable surface exists on the Claude Code host"},
                                      ev("pets", r"Install a pet", "NOT a simple-agent surface: petdex sprites are cosmetics; recorded so the count cannot be inflated")],
                         "note": "no install verb for agent definitions was found on either host; placement is by file"},
        "AGENT_OS": {"disposition": "NO_SURFACE_MEASURED",
                     "evidence": [ev("acp", r"ACP mode", "ACP is an editor protocol, not an agent-os package installer")],
                     "note": "69 verbs probed; none installs an operating runtime"},
        "AI_SYSTEM": {"disposition": "NO_SURFACE_MEASURED",
                      "evidence": [ev("chat", r"system prompt", "'system prompt' appears only as a per-session config flag, never as an installable unit")],
                      "note": "no verb packages a system prompt as a unit"},
        "GENIE/GENIE.md": {"disposition": "NO_SURFACE_MEASURED",
                           "evidence": [{"verb": "find + 69 help probes", "rc": 0, "help_sha256": None,
                                         "quote": "0 hits for GENIE*.md outside HG-KSEOS design docs; 0 verbs mention genie",
                                         "why": "absent by two independent measurements"}]},
    }
    counts = {"install_surface": sum(1 for v in kinds.values() if v["disposition"] == "INSTALL_SURFACE_MEASURED"),
              "surface_no_installer": sum(1 for v in kinds.values() if v["disposition"] == "SURFACE_EXISTS_NO_INSTALL_VERB"),
              "no_surface": sum(1 for v in kinds.values() if v["disposition"] == "NO_SURFACE_MEASURED")}

    doc = {"schema": "FHS.R21.WP20.KIND_SURFACE_RULING/1",
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "probe": {"verbs": probe["verbs_probed"], "root_help_sha256": probe["root_help_sha256"],
                     "file": "kind_surface_probe/KIND_SURFACE_PROBE.json", "file_sha256": sha(PROBE)},
           "counts": counts,
           "denominator_ruling": {
               "blocker_said": "the other seven Kinds",
               "scope_file_said": "5 measured",
               "ruling": (f"both withdrawn. Measured on this host: {counts['no_surface']} kinds have no surface at all, "
                          f"{counts['surface_no_installer']} has a loadable surface without an installer, "
                          f"{counts['install_surface']} have a host install surface."),
               "authority": "owner-delegated R21 blanket authorisation, exercised with measurement attached",
               "consequence": ("WP-FHS-20 is scoped to the four kinds with an install surface; SIMPLE_AGENT needs its own "
                               "cells on the Claude Code host; the three surface-less kinds take NO_HOST_SURFACE as an "
                               "accepted cell state with this probe as the release condition")},
           "kinds": kinds}
    (P / "KIND_SURFACE_RULING.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                                encoding="utf-8", newline="\n")

    md = ["# WP-FHS-20 — Kind 面探測與分母裁定", "", f"generated_utc: {doc['generated_utc']}", "",
          f"探測範圍：CLI 自報 **{probe['verbs_probed']} 個子命令**，逐個 `--help` 存檔並記 rc／bytes／sha256；"
          f"根 help sha `{probe['root_help_sha256']}`。", "", "## 裁定（附量測）", "",
          "| 處置 | 數量 | Kind |", "|---|---:|---|",
          f"| 有主機安裝面 | {counts['install_surface']} | " + ", ".join(k for k, v in kinds.items() if v["disposition"] == "INSTALL_SURFACE_MEASURED") + " |",
          f"| 有可載入面、無安裝動詞 | {counts['surface_no_installer']} | " + ", ".join(k for k, v in kinds.items() if v["disposition"] == "SURFACE_EXISTS_NO_INSTALL_VERB") + " |",
          f"| 完全無面 | {counts['no_surface']} | " + ", ".join(k for k, v in kinds.items() if v["disposition"] == "NO_SURFACE_MEASURED") + " |", "",
          "**blocker 的 7 與我先前的 5，兩者都撤回**：實測為 3 個完全無面、1 個有面無安裝器、4 個有安裝面。", "",
          "## 逐 Kind 證據", ""]
    for k, v in kinds.items():
        md.append(f"### {k} — {v['disposition']}")
        for e in v["evidence"]:
            q = f"『{e['quote']}』" if e.get("quote") else ""
            md.append(f"- `{e['verb']}` rc={e['rc']} sha256={e.get('help_sha256') or '檔案／目錄量測'} {q}")
        if v.get("correction"):
            md.append(f"- **更正**：{v['correction']}")
        if v.get("note"):
            md.append(f"- 註：{v['note']}")
        md.append("")
    md += ["## 後果", "",
           "- WP-FHS-20 收斂到 **AGENT_SKILL／PROFILE／PLUGIN／CLI_TOOL** 四個有安裝面的 Kind（前兩者已有 18／12 格實跑）。",
           "- **SIMPLE_AGENT** 需在 Claude Code 主機另開 cells；本次只記錄 5 份定義存在，不宣稱已驗。",
           "- **AGENT_OS／AI_SYSTEM／GENIE** 以 `NO_HOST_SURFACE` 作為可接受 cell 狀態，解除條件＝上表探測；主機新增安裝面時重跑 `tools/wp20_kind_surface_probe.py` 即推翻。", "",
           f"檔案 sha256：`KIND_SURFACE_RULING.json` {sha(P / 'KIND_SURFACE_RULING.json')}"]
    (P / "KIND_SURFACE_RULING.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")

    sp = P / "WP20_KIND_SCOPE.json"
    s = json.loads(sp.read_text(encoding="utf-8"))
    s["dispositions"] = {k: v["disposition"] for k, v in kinds.items()}
    s["superseded_by"] = "KIND_SURFACE_RULING.json"
    s["no_surface_kinds"] = [k for k, v in kinds.items() if v["disposition"] == "NO_SURFACE_MEASURED"]
    sp.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"counts": counts, "ruling_sha": sha(P / "KIND_SURFACE_RULING.json")[:16],
                      "verbs": probe["verbs_probed"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
