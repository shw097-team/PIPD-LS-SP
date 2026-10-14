#!/usr/bin/env python3
"""Dispatch one governed lane turn for the FAR study, from a prompt FILE.

Why a file: the dispatcher takes the prompt as a command-line argument, so a multi-kilobyte packet
inline in a shell heredoc is both quoting-fragile and capped; reading the packet from disk keeps the
prompt whole and the invocation readable.

Records, per attempt: lane, required arm, the prompt digest, the served arm, the usage receipt
verdict, the nonce carrier check, and the raw stdout/stderr paths. Never infers success from the exit
code alone - a writer lane on Windows can return a clean receipt with nothing written, so the caller
must verify the side effect separately.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

HGK = pathlib.Path("C:/Projects/Agent_Workspace/HG-KSEOS")
DISPATCH = HGK / "scripts/hgk-lane-dispatch.py"
PY = "C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe"
NONCE = "HGK_LANE_NONCE_OK"


def rank_for_arm(arm: str, lane: str | None = None) -> str:
    """Resolve the pool rank carrying `arm`, scoped to `lane`.

    Scoping matters: the same arm sits at different ranks in different lanes (glm-5.3-flash is PLAN
    rank 4 and VERIFY_SECURITY rank 3), so an unscoped search returns the wrong rank and the dispatcher
    refuses with ERR_LANE_REQUIRED_ARM_ABSENT for an arm that is present.

    Fail-closed on purpose: if the arm is not in the pool this returns a rank that cannot match, so the
    dispatcher refuses with its own code instead of the run silently falling through to another arm.
    """
    pool = HGK / "config/lane-route-slots.candidate.json"
    try:
        d = json.loads(pool.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return "0"
    for lane_obj in d.get("lanes", []):
        if lane and lane_obj.get("lane") != lane:
            continue
        for e in lane_obj.get("ordered_pool", []) or []:
            if f"{e.get('provider')}/{e.get('model')}" == arm:
                return str(e.get("rank", "0"))
    return "0"


def head(p: pathlib.Path) -> str:
    return subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def main() -> int:
    lane, prompt_file, cwd, arm, attempt, outdir = sys.argv[1:7]
    timeout = sys.argv[7] if len(sys.argv) > 7 else "1500"
    # The rank is an INPUT, not a constant. `--require-arm` is matched against the pool AFTER
    # `--force-rank` filters it, so hard-coding rank 1 for a checker whose arm sits at rank 3 makes the
    # dispatcher refuse with ERR_LANE_REQUIRED_ARM_ABSENT - which reads like "the arm is gone" and is
    # not. Derive it from the default pool instead of trusting a literal.
    rank = sys.argv[8] if len(sys.argv) > 8 else rank_for_arm(arm, lane)
    pf = pathlib.Path(prompt_file)
    prompt = pf.read_text(encoding="utf-8")
    if len(prompt) > 29000:
        print(json.dumps({"refused": "ERR_PROMPT_TOO_LONG_FOR_ARGV", "chars": len(prompt)}))
        return 2
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    argv = [PY, str(DISPATCH), "--lane", lane, "--prompt", prompt, "--cwd", cwd,
            "--force-rank", rank, "--require-arm", arm, "--nonce", NONCE,
            "--round", "S4R3FAR-20261013-decision-and-handover", "--attempt", attempt,
            "--timeout", timeout, "--attempt-log-dir", str(out / "attempts")]
    proc = subprocess.run(argv, capture_output=True, text=False)
    so, se = out / f"stdout_{lane}_a{attempt}.txt", out / f"stderr_{lane}_a{attempt}.txt"
    so.write_bytes(proc.stdout)
    se.write_bytes(proc.stderr)
    inv = {"lane": lane, "required_arm": arm, "attempt": attempt, "cwd": cwd,
           "force_rank": rank,
           "prompt_file": str(pf), "prompt_chars": len(prompt),
           "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
           "cwd_head": head(pathlib.Path(cwd)), "exit": proc.returncode,
           "stdout_path": str(so), "stderr_path": str(se)}
    try:
        d = json.loads(proc.stdout.decode("utf-8", "replace"))
        a = (d.get("attempts") or [{}])[0]
        inv.update({"ok": d.get("ok"), "code": d.get("code"), "served_arm": d.get("served_arm"),
                    "used_rank": d.get("used_rank"), "used_seconds": d.get("used_seconds"),
                    "usage_receipt_ok": d.get("usage_receipt_ok"),
                    "sandbox": d.get("sandbox"), "escalated": d.get("sandbox_escalation_authorised"),
                    "nonce_present": a.get("nonce_present"), "attempt_stdout_path": a.get("stdout_path"),
                    "attempt_stdout_sha256": a.get("stdout_sha256"),
                    "claim_ceiling": d.get("claim_ceiling")})
    except Exception as exc:  # noqa: BLE001
        inv["parse_error"] = f"{type(exc).__name__}: {exc}"
        inv["stdout_head"] = proc.stdout.decode("utf-8", "replace")[:600]
    (out / f"invocation_{lane}_a{attempt}.json").write_text(
        json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in inv.items()
                      if k in ("lane", "attempt", "ok", "code", "served_arm", "used_rank",
                               "used_seconds", "usage_receipt_ok", "nonce_present", "sandbox",
                               "escalated", "attempt_stdout_sha256", "prompt_chars")},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
