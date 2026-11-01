"""WP-FHS-13 C5: one ABI fixture, one covering grant, one receipt that carries C2-C5 together.

Sequence (order matters for C5):
  1. build a FRESH fixture (occupant v1) - no reuse of the 00:19 tree that is already v2;
  2. issue the grant NOW, naming both the entry and the candidate with their preimage sha256;
  3. only then run hotswap.py >= with --grant and the issuer's own verifier;
  4. run a refusal control on a second fresh fixture using the stale PROBE-WP13-A1 grant.
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
RUN = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp13"
ISSUER = ROOT / "HG-KSEOS" / "scripts" / "issue_grant.py"
HOTSWAP = ROOT / "PIPD" / "tools" / "hotswap.py"

V1 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v1"\ndef build():\n    return Impl()\n'
V2 = 'class Impl:\n    def identity(self):\n        return "cap-attest-v2"\ndef build():\n    return Impl()\n'


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def new_fixture(tag: str) -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    d = RUN / f"fixture-{tag}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    occ = d / "occupant.py"
    occ.write_text(V1, encoding="utf-8", newline="\n")
    cand = d / "candidate.py"
    cand.write_text(V2, encoding="utf-8", newline="\n")
    return d, occ, cand


def run(cmd, **kw):
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180, **kw)
    return {"cmd": [str(c) for c in cmd], "rc": r.returncode, "ms": round((time.time() - t0) * 1000, 1),
            "stdout": (r.stdout or "")[-1500:], "stderr": (r.stderr or "")[-800:]}


out: dict = {"schema": "FHS.R21.WP13.C5_RUN/1",
             "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

# ---- 1. fresh fixture + covering grant -------------------------------------
d1, occ1, cand1 = new_fixture("covering")
ws = {"writeset": [{"path": str(occ1), "preimage": sha(occ1)},
                   {"path": str(cand1), "preimage": sha(cand1)}]}
ws_path = RUN / "writeset_covering.json"
ws_path.write_text(json.dumps(ws, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

grant1 = RUN / "grant_covering.json"
nonce = f"WP13-R21-{int(time.time())}"
issue = run([sys.executable, ISSUER, "issue", "--principal", "owner", "--operation", "install_occupant",
             "--writeset", ws_path, "--ttl", "900", "--epoch", "40",
             "--scope", "WP-FHS-13 C5: install occupant through the ABI consumer under a covering writeset",
             "--nonce", nonce, "--subject", "WP-FHS-13",
             "--candidate-sha", sha(cand1), "--out", grant1])
out["issue_grant"] = issue
out["grant_issued_at_unix"] = int(time.time())
if not grant1.exists():
    print(json.dumps({"stage": "issue_grant_failed", "result": issue}, ensure_ascii=False, indent=1))
    sys.exit(2)

# ---- 2. the effect, under that grant ---------------------------------------
receipt1 = RUN / "HOTSWAP_ABI_GRANT_BOUND.json"
swap = run([sys.executable, HOTSWAP, "--root", d1, "--entry", occ1.name, "--candidate", cand1,
            "--expect-old", "cap-attest-v1", "--expect-new", "cap-attest-v2",
            "--need", "cap.attest", "--method", "identity",
            "--grant", grant1, "--grant-verifier", ISSUER, "--out", receipt1])
out["hotswap_covering"] = swap

# ---- 3. refusal control with the stale grant -------------------------------
d2, occ2, cand2 = new_fixture("stale")
receipt2 = RUN / "HOTSWAP_REFUSED_STALE_GRANT.json"
stale = ROOT / "HG-KSEOS" / "var" / "issuer-probe" / "grant.json"
refuse = run([sys.executable, HOTSWAP, "--root", d2, "--entry", occ2.name, "--candidate", cand2,
              "--expect-old", "cap-attest-v1", "--expect-new", "cap-attest-v2",
              "--need", "cap.attest", "--method", "identity",
              "--grant", stale, "--grant-verifier", ISSUER, "--out", receipt2])
out["hotswap_stale_grant"] = refuse
out["artifacts"] = {"grant": str(grant1), "grant_sha256": sha(grant1),
                    "receipt_covering": str(receipt1),
                    "receipt_stale": str(receipt2),
                    "fixture_covering": str(d1), "fixture_stale": str(d2)}

for name, p in (("covering", receipt1), ("stale", receipt2)):
    if p.exists():
        r = json.loads(p.read_text(encoding="utf-8"))
        out[name] = {"ok": r.get("ok"), "steps": r.get("steps"),
                     "before": r.get("before"), "pos": r.get("pos"), "neg": r.get("neg"),
                     "control": r.get("control"), "code": r.get("code"), "why": r.get("why"),
                     "grant": {k: r.get("grant", {}).get(k) for k in
                               ("nonce", "issued_before_effect", "covers_entry", "covers_candidate",
                                "candidate_sha_matches", "issuer_verifier_exit", "problems")}}

(RUN / "C5_RUN.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                 encoding="utf-8", newline="\n")
print(json.dumps({"issue_rc": issue["rc"], "swap_rc": swap["rc"], "stale_rc": refuse["rc"],
                  "covering": out.get("covering"), "stale": out.get("stale")},
                 ensure_ascii=False, indent=1))
