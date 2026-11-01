#!/usr/bin/env python3
"""WP-FHS-12 host repair: retire the stale PATH forwarder to a shim that execs its working sibling.

Why this exact repair (measured, not assumed):
  * `D:\\Hermes-Recovery\\live22\\bin\\hermes.cmd` (the entry PATH resolves to) fails 2/2 deterministically:
    rc=1, stdout 0 B, stderr 3249 B ending in `ModuleNotFoundError: No module named 'pm.environments'`,
    and on `--print-runtime-command` in `No module named 'hermes_cli._launchers'`.
  * Its sibling `bin\\hermes` (zipapp, python 3.14.9) and `bin\\hermes.exe` both answer rc=0 with a
    byte-identical 178 B stdout (sha 8b67e84b...), and the product CLI answers the same bytes.
  So the forwarder is a stale hand-written shim pointing at an incomplete tree; the installed launcher is fine.

Contract of this script:
  * refuses unless the preimage sha256 matches the recorded value (no blind overwrite);
  * keeps a byte-identical backup beside the target and records its sha;
  * writes the new shim atomically (temp + replace), with CRLF for cmd.exe;
  * re-reads the target and proves the postimage sha;
  * fresh-load test: runs both `--version` and `--print-runtime-command` through the NEW entry;
  * writes one receipt with preimage/postimage/backup shas, PIDs and raw stdout/stderr shas.

Usage:  apply_wp12.py --check     (measure only, no write)
        apply_wp12.py --apply     (perform the repair)
        apply_wp12.py --rollback  (restore the recorded preimage)
"""
import argparse, hashlib, json, os, pathlib, shutil, subprocess, sys, time

TARGET = pathlib.Path(r"D:\Hermes-Recovery\live22\bin\hermes.cmd")
BACKUP = pathlib.Path(r"D:\Hermes-Recovery\live22\bin\hermes.cmd.wp12-backup")
PREIMAGE_SHA = "UNSET"          # filled by --check on first run, then pinned by the caller
RECEIPTS = pathlib.Path(r"C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp12")
NEW_SHIM = (
    "@echo off\r\n"
    "rem WP-FHS-12 repair: this is the launcher PATH resolves to. It previously pointed at an\r\n"
    "rem incomplete tree (C:\\Users\\user\\AppData\\Local\\hermes\\hermes-agent) with python 3.14.7 and\r\n"
    "rem died with ModuleNotFoundError: pm.environments / hermes_cli._launchers. Exec the installed\r\n"
    "rem sibling launcher instead, so PATH resolution and the entry under test are the same object.\r\n"
    "\"%~dp0hermes.exe\" %*\r\n"
)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(cmd, timeout=60):
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout)
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = "TIMEOUT", b"", b""
    return {"cmd": cmd, "rc": rc, "ms": round((time.time() - t0) * 1000, 1),
            "stdout_sha256": sha256_bytes(out), "stdout_bytes": len(out),
            "stderr_sha256": sha256_bytes(err), "stderr_bytes": len(err),
            "stdout_head": out.decode("utf-8", "replace")[:160],
            "stderr_tail": err.decode("utf-8", "replace").strip().splitlines()[-1][:200] if err.strip() else ""}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    ap.add_argument("--preimage", default=None, help="expected preimage sha256 (required for --apply)")
    a = ap.parse_args()
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    if not TARGET.is_file():
        print(json.dumps({"error": "TARGET_ABSENT", "target": str(TARGET)})); return 2

    pre = TARGET.read_bytes()
    pre_sha = sha256_bytes(pre)
    receipt = {"schema": "FHS.WP12.HOST_REPAIR/1", "target": str(TARGET),
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "preimage_sha256": pre_sha, "preimage_bytes": len(pre),
               "backup": str(BACKUP), "backup_exists": BACKUP.exists()}

    if a.rollback:
        if not BACKUP.is_file():
            print(json.dumps({"error": "NO_BACKUP"})); return 3
        TARGET.write_bytes(BACKUP.read_bytes())
        receipt["action"] = "ROLLBACK"
        receipt["postimage_sha256"] = sha256_bytes(TARGET.read_bytes())
        receipt["restored_to_preimage"] = receipt["postimage_sha256"] == pre_sha
        (RECEIPTS / "WP12_HOST_REPAIR_RECEIPT.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps(receipt, ensure_ascii=False, indent=1)); return 0

    # negative control: the entry as it stands
    receipt["before_runs"] = [run([str(TARGET), "--version"]), run([str(TARGET), "--print-runtime-command"])]

    if a.check:
        receipt["action"] = "CHECK_ONLY"
        receipt["proposed_shim_sha256"] = sha256_bytes(NEW_SHIM.encode())
        print(json.dumps(receipt, ensure_ascii=False, indent=1)); 
        (RECEIPTS / "WP12_HOST_REPAIR_CHECK.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        return 0

    expected = a.preimage or PREIMAGE_SHA
    if expected != pre_sha:
        receipt["action"] = "REFUSED_PREIMAGE_MISMATCH"
        receipt["expected_preimage_sha256"] = expected
        (RECEIPTS / "WP12_HOST_REPAIR_RECEIPT.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps(receipt, ensure_ascii=False, indent=1)); return 4

    if not BACKUP.is_file():
        shutil.copy2(TARGET, BACKUP)
    receipt["backup_sha256"] = sha256_bytes(BACKUP.read_bytes())
    receipt["backup_is_preimage"] = receipt["backup_sha256"] == pre_sha

    tmp = TARGET.with_suffix(".cmd.wp12-tmp")
    tmp.write_bytes(NEW_SHIM.encode("utf-8"))
    os.replace(tmp, TARGET)
    post = TARGET.read_bytes()
    receipt.update({"action": "APPLIED", "postimage_sha256": sha256_bytes(post),
                    "postimage_bytes": len(post)})

    receipt["after_runs"] = [run([str(TARGET), "--version"]), run([str(TARGET), "--print-runtime-command"])]
    receipt["postconditions"] = {
        "version_rc_zero": receipt["after_runs"][0]["rc"] == 0,
        "version_stdout_matches_product": receipt["after_runs"][0]["stdout_sha256"] == "8b67e84be4f9de55",
        "print_runtime_command_rc_zero": receipt["after_runs"][1]["rc"] == 0,
        "negative_control_was_failing": receipt["before_runs"][0]["rc"] not in (0,),
    }
    receipt["all_postconditions"] = all(receipt["postconditions"].values())
    (RECEIPTS / "WP12_HOST_REPAIR_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: receipt[k] for k in ("action", "preimage_sha256", "postimage_sha256",
                                              "postconditions", "all_postconditions")}, ensure_ascii=False, indent=1))
    return 0 if receipt["all_postconditions"] else 5


if __name__ == "__main__":
    sys.exit(main())
