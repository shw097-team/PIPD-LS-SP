"""Re-probe the kind surface with the denominator taken from root_help.txt, not a hand-written list.

AO deleg_0361e484 (N3) showed the "69 verbs" set was not the host's command set: 4 real commands were
never probed (browser, codex-runtime, migrate, profile) and 5 probed entries are not commands at all
(branches, firewall, schemas, server, settings). I re-measured that myself before writing this
(root_help lists 68; the old probe listed 69).

This re-probe: takes verbs from root_help.txt, probes every one with the same binary the first probe used
(D:\\Hermes-Recovery\\live22\\bin\\hermes.exe), keeps rc + byte count + sha for each, records the
non-commands separately, and stores the raw help text under stdout/_kind_v2/.
"""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
WP20 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp20"
PROBE = WP20 / "kind_surface_probe"
OUT = WP20 / "stdout" / "_kind_v2"
OLD = PROBE / "KIND_SURFACE_PROBE.json"
NON_COMMANDS = {"branches", "firewall", "schemas", "server", "settings"}
VERB_RE = re.compile(r"^    ([a-z][a-z0-9-]{2,20})\s{2,}", re.M)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(binary, args, timeout=90):
    t0 = time.time()
    p = subprocess.run([binary, *args], capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return {"rc": p.returncode, "ms": int((time.time() - t0) * 1000),
            "out": p.stdout or "", "err": p.stderr or ""}


def main():
    old = json.loads(OLD.read_text(encoding="utf-8"))
    binary = old["hermes"]
    if not pathlib.Path(binary).exists():
        raise SystemExit(f"probe binary missing: {binary}")
    OUT.mkdir(parents=True, exist_ok=True)

    root = run(binary, ["--help"])
    (OUT / "root_help.txt").write_text(root["out"], encoding="utf-8", newline="\n")
    verbs = sorted(set(VERB_RE.findall(root["out"])))

    rows = []
    for verb in verbs:
        r = run(binary, [verb, "--help"])
        f = OUT / f"{verb}_help.txt"
        f.write_text(r["out"], encoding="utf-8", newline="\n")
        blob = r["out"].encode("utf-8")
        (OUT / f"{verb}_err.txt").write_text(r["err"], encoding="utf-8", newline="\n")
        rows.append({"verb": verb, "rc": r["rc"], "ms": r["ms"], "bytes": len(blob),
                     "help_sha": sha(blob), "help_file": str(f.relative_to(ROOT)).replace("\\", "/"),
                     "is_command": verb not in NON_COMMANDS,
                     "stderr_first": r["err"].strip().splitlines()[:1]})

    old_verbs = [v["verb"] for v in old["verbs"]]
    doc = {
        "schema": "FHS.R21.WP20.KIND_PROBE_V2/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "binary": binary,
        "binary_sha256": sha(pathlib.Path(binary).read_bytes()),
        "root_help": {"rc": root["rc"], "bytes": len(root["out"].encode("utf-8")),
                      "sha256": sha(root["out"].encode("utf-8")),
                      "file": "var/FHS-R21-FAR-TT-20261101/wp20/stdout/_kind_v2/root_help.txt"},
        "denominator": {"from": "root_help.txt (parsed)", "verbs": len(verbs),
                        "non_command_entries_kept_for_evidence": sorted(NON_COMMANDS & set(verbs))},
        "diff_vs_old_probe": {
            "old_probed": len(old_verbs),
            "unprobed_before": [v for v in verbs if v not in old_verbs],
            "probed_but_not_a_command": [v for v in old_verbs if v not in verbs],
        },
        "verbs": rows,
        "claim_ceiling": ("author-side local probe; the denominator now comes from the host's own root help. "
                          "Naming a verb's help text is not evidence that the verb installs or loads anything."),
    }
    out = PROBE / "KIND_SURFACE_PROBE_V2.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"verbs": len(verbs), "root_help_sha": doc["root_help"]["sha256"][:16],
                      "unprobed_before": doc["diff_vs_old_probe"]["unprobed_before"],
                      "probed_not_command": doc["diff_vs_old_probe"]["probed_but_not_a_command"],
                      "probe_sha": sha(out.read_bytes())[:16]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
