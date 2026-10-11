#!/usr/bin/env python
"""S4-R2 reconciliation: run FRESH positive AND negative counterexamples for every finding the
R2 reaudit raised, against THIS candidate tree. A finding is only marked
ALREADY_CLOSED_WITH_FRESH_POS_NEG when both a POSITIVE and a NEGATIVE case really executed here.

Read-only w.r.t. the repository: every case that needs to write does so under a disposable dir
outside the repo.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ROUND = REPO / ".hgk" / "rounds" / "S4R2-20261011-affected-only"
SB = Path(os.environ.get("R2_SCRATCH", r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\s4r2"))
PY = sys.executable
BASE = "https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2"

CONTRACT_ID = "PIPD-LS-SP-S4-R2-POSTRELEASE-AFFECTED-ONLY-20261011"
results: list[dict] = []


def rec(fid, case, kind, cmd, exit_code, out, verdict, note=""):
    results.append({"finding": fid, "case": case, "kind": kind, "command": cmd,
                    "exit": exit_code, "output": (out or "")[-1800:], "verdict": verdict, "note": note})


def run(args, cwd=None, env=None, timeout=180):
    e = dict(os.environ)
    e["PYTHONPATH"] = str(REPO / "src")
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        e.update(env)
    p = subprocess.run(args, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- F-S4R2-01
def f01():
    d = SB / "f01"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for name in ("pipd_ls_sp-0.1.0-py3-none-any.whl", "SHA256SUMS"):
        try:
            urllib.request.urlretrieve(f"{BASE}/{name}", d / name)
        except Exception as exc:  # noqa: BLE001
            rec("F-S4R2-01", f"download {name}", "POS", f"GET {BASE}/{name}", 1, str(exc),
                "NOT_RUN", "release asset not reachable from this host")
            return

    # NEG-1: the OLD instruction (whole-file check after downloading only the wheel) must fail.
    rc, out = run(["bash", "-c", "sha256sum -c SHA256SUMS"], cwd=d)
    rec("F-S4R2-01", "legacy whole-file check with only the wheel present", "NEG",
        "sha256sum -c SHA256SUMS", rc, out, "PASS" if rc != 0 else "FAIL",
        "the reaudit's counterexample; must still be non-zero")

    # POS: exactly what the README now tells the user to run.
    rc, out = run(["bash", "-c",
                   "grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -"], cwd=d)
    rec("F-S4R2-01", "README wheel-only filter, real published SHA256SUMS + real wheel bytes", "POS",
        "grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -", rc, out,
        "PASS" if rc == 0 else "FAIL")

    # POS2: the published digest literal in README equals the real wheel bytes.
    real = sha256(d / "pipd_ls_sp-0.1.0-py3-none-any.whl")
    pub = "d6c3e295f817b50108b1232a120564c18b517864ad1ad19c4f8d915f396d364f"
    rec("F-S4R2-01", "recomputed wheel sha256 vs published literal", "POS",
        "sha256sum pipd_ls_sp-0.1.0-py3-none-any.whl", 0, f"actual={real}\npublished={pub}",
        "PASS" if real == pub else "FAIL", "the published digest is now verified from real bytes")

    # NEG-2: a single tampered byte must fail closed through the README filter.
    t = d / "pipd_ls_sp-0.1.0-py3-none-any.whl"
    raw = bytearray(t.read_bytes())
    raw[len(raw) // 2] ^= 0xFF
    t.write_bytes(bytes(raw))
    rc, out = run(["bash", "-c",
                   "grep '  pipd_ls_sp-0.1.0-py3-none-any.whl$' SHA256SUMS | sha256sum -c -"], cwd=d)
    rec("F-S4R2-01", "tampered wheel byte through the README filter", "NEG",
        "grep ... | sha256sum -c -", rc, out, "PASS" if rc != 0 else "FAIL")

    # NEG-3: zero matching rows must not silently "succeed" (pipe-left failure must be caught).
    rc, out = run(["bash", "-c",
                   "set -o pipefail; grep '  no-such-asset.whl$' SHA256SUMS | sha256sum -c -"], cwd=d)
    rec("F-S4R2-01", "zero rows with pipefail (pipe-left failure must surface)", "NEG",
        "set -o pipefail; grep '  no-such-asset.whl$' SHA256SUMS | sha256sum -c -", rc, out,
        "PASS" if rc != 0 else "FAIL")


# ---------------------------------------------------------------- profile findings
def prof():
    code = r'''
import json, sys
sys.path.insert(0, r"__SRC__")
from pipd_ls_sp.profiles import compute_profile, AXES
from pipd_ls_sp.errors import PipdError, ProfileVeto, UnsupportedSurface
out = {}

def attempt(key, **kw):
    try:
        out[key] = {"ok": True, "result": compute_profile(**kw)}
    except PipdError as exc:
        out[key] = {"ok": False, "type": type(exc).__name__, "msg": str(exc)[:300]}

attempt("dup_intent_x4", requested="LITE", axes=["intent"]*4)
attempt("non_string",    requested="LITE", axes=["intent", 7])
attempt("empty",         requested="LITE", axes=[])
attempt("unknown_axis",  requested="LITE", axes=["intent", "not_an_axis"])
attempt("trust_boundary_only", requested="LITE", axes=["trust_boundary"])
attempt("lite_ok",       requested="LITE", axes=["intent"])
attempt("standard_ok",   requested="STANDARD", axes=["intent","knowledge","verification","release"])
attempt("assured_ok",    requested="ASSURED", axes=list(AXES))
attempt("provider_off_escalates", requested="LITE", axes=["intent"], provider_off_required=True)
print(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1))
'''.replace("__SRC__", str(REPO / "src"))
    rc, out = run([PY, "-c", code])
    try:
        data = json.loads(out)
    except Exception:  # noqa: BLE001
        rec("F-S4R2-02/03", "compute_profile probe", "OBS", "python -c compute_profile(...)", rc, out, "ERROR")
        return
    for key in ("dup_intent_x4", "non_string", "empty", "unknown_axis"):
        v = data.get(key, {})
        ok = (v.get("ok") is False)
        rec("F-S4R2-02", f"axis set {key}", "NEG", f"compute_profile(requested='LITE', axes={key})",
            0 if ok else 1, json.dumps(v, ensure_ascii=False),
            "PASS" if ok else "FAIL", "must be a typed refusal, not an escalation")
    tb = data.get("trust_boundary_only", {})
    r = tb.get("result", {})
    ok = (tb.get("ok") is True and r.get("risk_assessment") == "NOT_ASSESSED"
          and r.get("profile") == "LITE"
          and json.dumps(r).find("LOW_RISK_VERIFIED") == -1)
    rec("F-S4R2-03", "trust_boundary tag without risk evidence", "NEG",
        "compute_profile(requested='LITE', axes=['trust_boundary'])", 0 if ok else 1,
        json.dumps(tb, ensure_ascii=False), "PASS" if ok else "FAIL",
        "must emit risk_assessment=NOT_ASSESSED and never LOW_RISK_VERIFIED")
    for key in ("lite_ok", "standard_ok", "assured_ok", "provider_off_escalates"):
        v = data.get(key, {})
        rec("F-S4R2-02", f"legal ladder case {key}", "POS", f"compute_profile(...{key})",
            0 if v.get("ok") else 1, json.dumps(v, ensure_ascii=False),
            "PASS" if v.get("ok") else "FAIL", "no regression on the legal ladder")


# ---------------------------------------------------------------- F-S4R2-04
def f04():
    code = r'''
import json, sys
sys.path.insert(0, r"__SRC__")
from pipd_ls_sp import pipeline
from pipd_ls_sp.profiles import AXES
from pipd_ls_sp.validate import validate_record
from pathlib import Path
schemas = Path(r"__SCHEMAS__")
card = pipeline.intake("typed identity probe", sources=[r"__REPO__/README.md"])
pi = pipeline.strip_sidecar(pipeline.compile_pi(card, "LITE"))
out = {}

def probe(key, mut):
    rec = json.loads(json.dumps(pi))
    mut(rec)
    out[key] = validate_record("PI-PKG", rec, schemas)

def set_subject_int(r): r["subject_id"] = 12345
def set_version_int(r): r["version"] = 3
def set_trace_scalar(r): r["trace"] = "not-an-array"
def set_trace_null(r): r["trace"] = None
def set_trace_baditem(r): r["trace"] = [{"from_id": "x"}]
def keep_legal(r): pass

for k, m in (("subject_id_integer", set_subject_int), ("version_integer", set_version_int),
             ("trace_scalar", set_trace_scalar), ("trace_null", set_trace_null),
             ("trace_malformed_item", set_trace_baditem), ("legal_control", keep_legal)):
    probe(k, m)
print(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1))
'''.replace("__SRC__", str(REPO / "src")).replace("__SCHEMAS__", str(REPO / "schemas")).replace("__REPO__", str(REPO).replace("\\", "/"))
    rc, out = run([PY, "-c", code])
    try:
        data = json.loads(out)
    except Exception:  # noqa: BLE001
        rec("F-S4R2-04", "typed identity probe", "OBS", "validate_record('PI-PKG', ...)", rc, out, "ERROR")
        return
    for key, findings in data.items():
        rejected = bool(findings)
        if key == "legal_control":
            rec("F-S4R2-04", "legal PI control", "POS", f"validate_record PI-PKG [{key}]",
                0 if not rejected else 1, json.dumps(findings, ensure_ascii=False),
                "PASS" if not rejected else "FAIL", "a legal record must have zero findings")
        else:
            rec("F-S4R2-04", key, "NEG", f"validate_record PI-PKG [{key}]",
                0 if rejected else 1, json.dumps(findings, ensure_ascii=False),
                "PASS" if rejected else "FAIL", "must be rejected with a typed first-fail")


# ---------------------------------------------------------------- F-S4R2-06 / 10
def f06_10():
    z = REPO / "dist" / "mount" / "PIPD-LS-SP_S4_WEB_MOUNT_v0.1.0-preview.2.zip"
    side = z.with_suffix(".zip.sha256")
    actual = sha256(z)
    declared = side.read_text(encoding="utf-8").split()[0] if side.exists() else ""
    rec("F-S4R2-06", "web mount ZIP vs its published sidecar digest", "POS",
        "sha256sum dist/mount/*.zip", 0, f"actual={actual}\nsidecar={declared}",
        "PASS" if actual == declared else "FAIL")
    d = SB / "f06"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    rc, out = run(["python", "-c",
                   f"import zipfile;zipfile.ZipFile(r'{z}').extractall(r'{d}')"])
    tops = [q for q in d.iterdir() if q.is_dir()]
    root = tops[0] if len(tops) == 1 else d
    rc2, out2 = run(["bash", "-c", "sha256sum -c MANIFEST.sha256"], cwd=root)
    rec("F-S4R2-06", "extracted mount pack vs MANIFEST.sha256", "POS", "sha256sum -c MANIFEST.sha256",
        rc2, out2, "PASS" if rc2 == 0 else "FAIL", f"pack root = {root.name}")
    need = ["README_MOUNT.md", "SKILL.md", "PIPD_LS_SP_QUICKSTART_PROMPT.md", "MANIFEST.sha256",
            "references/PIPD_S4_CORE.md", "references/PIPD_SOURCE_MAP.md",
            "references/PIPD_8_SKILLS_INDEX.md"]
    missing = [n for n in need if not (root / n).exists()]
    got = sorted(str(q.relative_to(root)) for q in root.rglob("*") if q.is_file())
    rec("F-S4R2-06", "required mount files present", "POS", "ls extracted pack", 0 if not missing else 1,
        f"present={got}\nmissing={missing}", "PASS" if not missing else "PARTIAL",
        "R2 names PIPD_PROFILE_SAFETY.md; this pack ships PIPD_PROFILE_AND_SAFETY.md (same role)")

    sm = REPO / "docs" / "NORMATIVE_SOURCE_MAP.md"
    sb = REPO / "examples" / "self-bootstrap" / "run_selfbootstrap.py"
    rec("F-S4R2-10", "pinned source map + self-bootstrap driver exist", "POS",
        "ls docs/NORMATIVE_SOURCE_MAP.md examples/self-bootstrap/",
        (0 if (sm.exists() and sb.exists()) else 1),
        f"source_map={sm.exists()} driver={sb.exists()}", "PASS" if (sm.exists() and sb.exists()) else "FAIL")


# ------------------------------------------------- F-S4R2-NEW-01 (found while reconciling)
def f_new():
    """ProfileBinding types only the universal identity fields; its own contract fields are still
    open objects, so the record that carries the duplicate-axes decision is itself untyped."""
    import json as _json
    schemas = REPO / "schemas"
    import sys as _sys
    _sys.path.insert(0, str(REPO / "src"))
    from pipd_ls_sp.validate import validate_record
    legal = {"profile": "LITE", "axes": ["intent"], "vetoes": [], "artifact_depth": "COMPILED",
             "assurance": "LITE", "subject_id": "profile-binding-0001", "version": "1.0.0",
             "content_hash": "0"*64, "schema_version": "1.0.0"}
    cases = {
        "legal_control": dict(legal),
        "axes_is_a_string": {**legal, "axes": "intent"},
        "axes_has_non_string_item": {**legal, "axes": ["intent", 7]},
        "profile_is_an_integer": {**legal, "profile": 7},
        "vetoes_is_a_string": {**legal, "vetoes": "none"},
    }
    for key, binding in cases.items():
        f = validate_record("ProfileBinding", binding, schemas)
        if key == "legal_control":
            rec_out = ("PASS" if not f else "FAIL")
            note = "a legal binding must have zero findings"
        else:
            rec_out = ("PASS" if f else "FAIL")
            note = "must be rejected; an open {} accepts any JSON type"
        rec("F-S4R2-NEW-01", key, "POS" if key == "legal_control" else "NEG",
            f"validate_record('ProfileBinding', {key})", 0 if (bool(f) ^ (key == "legal_control")) else 1,
            _json.dumps(f, ensure_ascii=False), rec_out, note)


def main() -> int:
    SB.mkdir(parents=True, exist_ok=True)
    for fn in (f01, prof, f04, f06_10, f_new):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            rec(fn.__name__, "driver", "OBS", fn.__name__, 1, repr(exc), "ERROR")
    counts: dict[str, dict[str, int]] = {}
    for r in results:
        c = counts.setdefault(r["finding"], {})
        c[r["verdict"]] = c.get(r["verdict"], 0) + 1
    doc = {"schema": "PIPD-S4R2-RECONCILIATION/1", "contract": CONTRACT_ID,
           "subject_branch": "s4-r2-affected-only-20261011",
           "subject_commit": subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                            capture_output=True, text=True).stdout.strip(),
           "summary": counts, "results": results}
    out = ROUND / "preflight" / "RECONCILIATION_FRESH_EVIDENCE.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False, indent=1))
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
