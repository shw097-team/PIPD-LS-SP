"""Probe whether this host exposes any install surface for the surface-less kinds.

The WP-20 blocker asked for a binary ruling on "NO_HOST_SURFACE" with the count given as seven; the AO
(deleg_64257a4d) rejected four of my five absences as prose rather than measurement (F4), and the world
already showed SIMPLE_AGENT has a surface (five definitions in ~/.claude/agents, F5). So this probe enumerates
every subcommand the CLI advertises, captures each --help verbatim, and searches for install/deploy verbs.

Nothing here decides the taxonomy. It converts "I looked at --help once" into per-verb command+exit+sha, so the
ruling can be made on evidence instead of on my reading of one screen.
"""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
OUT = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20" / "kind_surface_probe"
HERMES = pathlib.Path(r"D:/Hermes-Recovery/live22/bin/hermes.exe")
HOME = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20" / "home-base"

# terms that would make a kind installable from this host's own CLI
INSTALL_TERMS = ("install", "deploy", "scaffold", "bundle add", "publish")
KIND_TERMS = {"CLI_TOOL": ("tool", "command", "binary", "cli"),
              "AI_SYSTEM": ("system prompt", "system_prompt", "assistant", "agent os"),
              "AGENT_OS": ("agent os", "runtime image", "operating"),
              "GENIE": ("genie",)}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def call(args):
    env = dict(os.environ)
    env["HERMES_HOME"] = str(HOME)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    t0 = time.time()
    try:
        p = subprocess.run([str(HERMES)] + args, capture_output=True, env=env, timeout=120)
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = "TIMEOUT", b"", b""
    return rc, out, err, int((time.time() - t0) * 1000)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rc, out, err, _ = call(["--help"])
    (OUT / "root_help.txt").write_bytes(out)
    text = out.decode("utf-8", "replace")

    # verbs as the CLI itself lists them
    verbs = sorted(set(re.findall(r"^\s{2,}([a-z][a-z0-9_-]{1,20})\s{2,}\S", text, re.M)))
    rows = []
    for v in verbs:
        vrc, vout, verr, ms = call([v, "--help"])
        blob = (vout + verr).decode("utf-8", "replace")
        low = blob.lower()
        (OUT / f"{v}_help.txt").write_bytes(vout or verr)
        hits = [t for t in INSTALL_TERMS if t in low]
        kind_hits = {k: [t for t in ts if t in low] for k, ts in KIND_TERMS.items()}
        kind_hits = {k: h for k, h in kind_hits.items() if h}
        rows.append({"verb": v, "rc": vrc, "ms": ms, "bytes": len(vout or verr),
                     "help_sha": sha(vout or verr), "install_terms": hits,
                     "kind_terms": kind_hits})

    install_verbs = [r["verb"] for r in rows if r["install_terms"]]
    out_doc = {
        "schema": "FHS.R21.WP20.KIND_SURFACE_PROBE/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hermes": str(HERMES),
        "hermes_version_rc": call(["--version"])[0],
        "root_help_sha256": sha(out),
        "root_help_bytes": len(out),
        "verbs_probed": len(rows),
        "verbs": rows,
        "install_capable_verbs": install_verbs,
        "genie_mentions": [r["verb"] for r in rows if "GENIE" in r["kind_terms"]],
        "interpretation": ("no advertised verb carries an install/deploy/scaffold surface for agent-os, ai-system, "
                           "cli-tool or GENIE artefacts" if not install_verbs else
                           "some verbs advertise install/deploy -- inspect before ruling"),
        "caveat": ("a CLI that never advertises an installer cannot prove a negative for kinds that install out of "
                   "band (e.g. a wheel into a venv); this probe bounds the claim to 'not installable through this "
                   "host CLI', which is what the blocker asked"),
    }
    (OUT / "KIND_SURFACE_PROBE.json").write_text(json.dumps(out_doc, ensure_ascii=False, indent=1) + "\n",
                                                 encoding="utf-8", newline="\n")
    print(json.dumps({"verbs": len(rows), "install_verbs": install_verbs,
                      "genie": out_doc["genie_mentions"],
                      "root_help_sha": out_doc["root_help_sha256"][:16]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
