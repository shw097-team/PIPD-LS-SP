"""Candidate patch for the A2 replay defect, plus the test that proves pre/post.

Measured defect (s6/A2_CASES.json): `cmd_issue` appends to config/issuer/nonce-ledger.jsonl but never consults it,
so the same nonce mints a second grant and verify() calls it GRANT_VALID -- the body's TQ-B1-A2-NEG
("replayed nonce -> PERMIT_SUBJECT_NONCE_REPLAY") is violated by the tool.

The canonical file is HG-KSEOS/scripts/issue_grant.py, so it is NOT edited in place: the patch is generated against
a copy under s6/patch/ and the test runs the copy. Pre-state is the measurement above; post-state is this test.
"""
import hashlib
import json
import difflib
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
S6 = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "s6"
SRC = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
PATCH = S6 / "patch"
PY = sys.executable


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def build_patched_copy():
    PATCH.mkdir(parents=True, exist_ok=True)
    text = SRC.read_text(encoding="utf-8")

    # 1) refuse a spent nonce at issue time
    anchor = '    payload = {\n        "operation": args.operation,'
    if anchor not in text:
        raise SystemExit("anchor for payload not found; refusing to guess")
    new = ('    nonce_candidate = args.nonce or f"G-{key_id()}-{int(time.time())}-{os.urandom(4).hex()}"\n'
           '    if nonce_used(nonce_candidate):\n'
           '        print(json.dumps({"refused": "NONCE_ALREADY_SPENT", "nonce": nonce_candidate}))\n'
           '        return 6\n'
           + anchor)
    text2 = text.replace(anchor, new, 1)
    text2 = text2.replace('        "nonce": args.nonce or f"G-{key_id()}-{now}-{os.urandom(4).hex()}",',
                          '        "nonce": nonce_candidate,', 1)

    # 2) flag a replayed nonce at verify time
    a2 = '    if nonce_used(grant.get("nonce", "")) is False:\n        problems.append("GRANT_NONCE_NOT_LEDGERED")'
    if a2 not in text2:
        raise SystemExit("anchor for nonce check not found; refusing to guess")
    text2 = text2.replace(
        a2,
        a2 + '\n    if nonce_uses(grant.get("nonce", "")) > 1:\n        problems.append("GRANT_NONCE_REPLAYED")', 1)

    # 3) helper counting uses
    anchor3 = "def nonce_used(nonce: str) -> bool:"
    text2 = text2.replace(anchor3,
                          'def nonce_uses(nonce: str) -> int:\n'
                          '    """How many ledger rows carry this nonce (replay detection)."""\n'
                          '    if not nonce or not NONCE_LEDGER.exists():\n'
                          '        return 0\n'
                          '    n = 0\n'
                          '    with NONCE_LEDGER.open(encoding="utf-8") as fh:\n'
                          '        for line in fh:\n'
                          '            try:\n'
                          '                if json.loads(line).get("nonce") == nonce:\n'
                          '                    n += 1\n'
                          '            except json.JSONDecodeError:\n'
                          '                continue\n'
                          '    return n\n\n\n' + anchor3, 1)

    dst = PATCH / "issue_grant.py"
    dst.write_text(text2, encoding="utf-8", newline="\n")
    diff = difflib.unified_diff(text.splitlines(True), text2.splitlines(True),
                                fromfile="a/HG-KSEOS/scripts/issue_grant.py",
                                tofile="b/HG-KSEOS/scripts/issue_grant.py", n=3)
    (PATCH / "issue_grant.nonce.patch").write_text("".join(diff), encoding="utf-8", newline="\n")
    return dst


def run(tool, args):
    p = subprocess.run([PY, str(tool)] + args, capture_output=True, text=True)
    return {"rc": p.returncode, "stdout": p.stdout.strip()[:300],
            "stdout_sha": hashlib.sha256(p.stdout.encode()).hexdigest()}


def main():
    copy = build_patched_copy()
    ws = S6 / "a2_writeset.json"
    stamp = int(time.time())
    nonce = f"A2-POST-{stamp}"
    g1, g2 = S6 / "post_grant_1.json", S6 / "post_grant_2.json"
    for g in (g1, g2):
        g.unlink(missing_ok=True)

    t1 = run(copy, ["issue", "--principal", "owner", "--operation", "install_occupant", "--writeset", str(ws),
                    "--ttl", "600", "--epoch", "40", "--scope", "A2 post-patch probe", "--nonce", nonce,
                    "--subject", "WP-FHS-13", "--out", str(g1)])
    t2 = run(copy, ["issue", "--principal", "owner", "--operation", "install_occupant", "--writeset", str(ws),
                    "--ttl", "600", "--epoch", "40", "--scope", "A2 post-patch probe", "--nonce", nonce,
                    "--subject", "WP-FHS-13", "--out", str(g2)])
    t3 = run(copy, ["verify", "--grant", str(g1)]) if g1.exists() else {"rc": None, "stdout": "no grant"}

    results = {
        "schema": "FHS.R21.S6.A2_PATCH_TEST/1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "canonical_untouched": {"path": "HG-KSEOS/scripts/issue_grant.py", "sha256": sha(SRC),
                                "note": "candidate only; the canonical tool was not edited"},
        "patch": {"file": "s6/patch/issue_grant.nonce.patch", "bytes": (PATCH / "issue_grant.nonce.patch").stat().st_size,
                  "sha256": sha(PATCH / "issue_grant.nonce.patch"),
                  "patched_copy": "s6/patch/issue_grant.py", "patched_copy_sha256": sha(copy)},
        "tests": {
            "T1_first_issue_accepted": {"expect": "rc=0", **t1, "verdict": "PASS" if t1["rc"] == 0 else "FAIL"},
            "T2_replay_refused": {"expect": "rc=6 NONCE_ALREADY_SPENT", **t2,
                                  "verdict": "PASS" if t2["rc"] == 6 and "NONCE_ALREADY_SPENT" in t2["stdout"] else "FAIL"},
            "T3_first_grant_still_valid": {"expect": "rc=0 GRANT_VALID", **t3,
                                           "verdict": "PASS" if t3["rc"] == 0 else "FAIL"},
        },
        "pre_state": {"ref": "s6/A2_CASES.json", "replay": "FAIL_REPLAY_ACCEPTED",
                      "note": "measured before the patch existed"},
        "claim_ceiling": ("candidate patch proven against a copy: replay refused at issue time. Not accepted: the canonical "
                          "HG-KSEOS tool still accepts replays until an owner-authorised change lands."),
    }
    results["summary"] = {k: v["verdict"] for k, v in results["tests"].items()}
    (S6 / "A2_PATCH_TEST.json").write_text(json.dumps(results, ensure_ascii=False, indent=1) + "\n",
                                          encoding="utf-8", newline="\n")
    print(json.dumps(results["summary"], ensure_ascii=False, indent=1))
    print("t2 stdout:", t2["stdout"][:160])
    print("patch bytes:", results["patch"]["bytes"])


if __name__ == "__main__":
    main()
