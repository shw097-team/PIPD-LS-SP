"""RUNTIME_PATH_LAB v3 — every check computed from a file or a live hash, none asserted.

v2 is kept for audit but is marked superseded here: two of its checks were hardcoded literals
(negative_control_failing_named, no_path_or_registry_edit), which the independent AO caught as
WP12-RS-09, so those axes could never fail. v3 recomputes each one, and where a claim cannot be
computed it is recorded as null with an explicit not_proven entry instead of a hopeful true.
"""
import hashlib
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
W = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp12"
WP12 = ROOT / "HG-KSEOS" / "ops" / "session-20261031" / "FHS-ALLPASS-20261031" / "WP-FHS-12"
TARGET = pathlib.Path(r"D:\Hermes-Recovery\live22\bin\hermes.cmd")
BACKUP = pathlib.Path(r"D:\Hermes-Recovery\live22\bin\hermes.cmd.wp12-backup")

SHIM = (
    "@echo off\r\n"
    "rem WP-FHS-12 repair: this is the launcher PATH resolves to. It previously pointed at an\r\n"
    "rem incomplete tree (C:\\Users\\user\\AppData\\Local\\hermes\\hermes-agent) with python 3.14.7 and\r\n"
    "rem died with ModuleNotFoundError: pm.environments / hermes_cli._launchers. Exec the installed\r\n"
    "rem sibling launcher instead, so PATH resolution and the entry under test are the same object.\r\n"
    "\"%~dp0hermes.exe\" %*\r\n"
)


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


check = load(W / "WP12_HOST_REPAIR_CHECK.json")
receipt = load(W / "WP12_HOST_REPAIR_RECEIPT.v2.json")
matrix = load(W / "ENTRY_EQUIVALENCE_MATRIX.json")
v1_lab = load(WP12 / "RUNTIME_PATH_LAB.json")

before_stdout_zero = all(r["stdout_bytes"] == 0 for r in check["before_runs"])
before_rc_one = all(r["rc"] == 1 for r in check["before_runs"])
named_error = [r["stderr_tail"] for r in check["before_runs"]]
named_pm = any("pm.environments" in t for t in named_error)
named_launchers = any("_launchers" in t for t in named_error)

checks = {
    "preimage_negative_control_named": named_pm,
    "preimage_second_failure_named": named_launchers,
    "preimage_rc_one_and_empty_stdout": bool(before_rc_one and before_stdout_zero),
    "postimage_recomputed_from_source_matches_disk": None,  # set below by recomputation
    "backup_equals_preimage_live": sha(BACKUP) == receipt["preimage_sha256"],
    "postimage_sha_matches_receipt_live": sha(TARGET) == receipt["postimage_sha256"],
    "path_entry_equals_entry_under_test": matrix["summary"]["P_equals_X_everywhere"],
    "extless_equals_exe": matrix["summary"]["X_equals_E_everywhere"],
    "four_entries_identical_in_clean_env": all(v["A_equals_X"] for v in matrix["checks"].values()),
    "four_entries_identical_only_when_HERMES_HOME_pinned": matrix["summary"]["A_equals_X_somewhere_only"],
    "version_bytes_are_git_conditional": matrix["summary"]["version_suffix_is_git_conditional"],
    "v1_controls_were_mislabelled": (
        str(v1_lab["c_recovery_negative"]["entry"]).lower().endswith("hermes.cmd")
        and str(v1_lab["d_injected_control"]["stdout"]).find("not connected to any AI provider") >= 0
    ),
}
# computed, not literal: rebuild the shim bytes independently and compare with the file on disk
checks["postimage_recomputed_from_source_matches_disk"] = (
    hashlib.sha256(SHIM.encode("utf-8")).hexdigest() == sha(TARGET))

lab = {
    "schema": "HGK-WP12-RUNTIME-PATH-LAB/3",
    "supersedes": ["RUNTIME_PATH_LAB.json (v1)", "RUNTIME_PATH_LAB.v2.json (two hardcoded checks)"],
    "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "independent_resit": {
        "by": "deleg_70888a64 (separate read-only AO subagent, distinct principal)",
        "verdict": "PARTIAL",
        "high_findings_absorbed": ["WP12-RS-06 status sha not an identity oracle / not identical in a clean env",
                                   "WP12-RS-07 product venv entry pins HERMES_HOME, so 'four identical' is env-conditional",
                                   "WP12-RS-08 --version gains a 22-byte suffix when git is on PATH"],
        "medium_absorbed": ["WP12-RS-09 two v2 checks were hardcoded True", "WP12-RS-11 v1 lab ran in a contaminated PATH"],
        "reproduced_by_ao": ["WP12-RS-01/02 (preimage fails 3/3 with the named import errors)",
                             "WP12-RS-03 (postimage recomputed byte-identical)",
                             "WP12-RS-04 (permit signature valid over the canonical body)",
                             "WP12-RS-10 (v1 controls mislabelled)",
                             "WP12-RS-12 (PATH entry == entry under test in a user-PATH shell)"],
    },
    "verdict": "PASS_AT_NARROWED_CEILING",
    "claim_ceiling": "PATH_ENTRY_EQUIVALENCE_VERSION_AND_DISPATCH + HOST_INSTALL_OF_ONE_FORWARDER",
    "checks": checks,
    "checks_note": "every entry above is computed from ENTRY_EQUIVALENCE_MATRIX.json, the repair receipts, or a live sha256 of the target/backup; none is a literal",
    "not_proven": [
        "no PATH or registry value was edited: registry values carry no mtime and no pre-change export exists",
        "no collateral change outside D:\\Hermes-Recovery\\live22 and the hermes-agent tree (no whole-host baseline)",
        "signing-key provenance/enrolment (the signature verifies over the recorded key; who holds the private key was not examined)",
        "cmd.exe quoting behaviour of %* for arguments needing redirection/quoting (only 4 probes exercised)",
        "any functional model turn through the repaired entry (read-only lane, no provider call)",
    ],
    "narrowed_claims": {
        "survives": [
            "the PATH entry (D:\\Hermes-Recovery\\live22\\bin\\hermes.cmd) and the entry under test are the same object: byte-identical stdout and rc on --version, status and --print-runtime-command in all 12 env combinations measured",
            "the stale forwarder's failure is deterministic and named, reproducible from the retained backup (AO reproduced 3/3 from a scratch copy)",
            "the single-file write was permitted, is reversible (byte-identical backup) and its postimage is recomputed byte-identical from the source shim",
        ],
        "retired": [
            "'all four entries are byte-identical' - false in a clean env (A serves status 741 B vs 658 B) because the product venv forwarder pins HERMES_HOME",
            "'status ... 741 B same sha' - status output tracks live gateway/job state and is not a durable identity oracle",
        ],
    },
    "matrix_file": "var/FHS-R21-FAR-TT-20261101/wp12/ENTRY_EQUIVALENCE_MATRIX.json",
    "next": "WP-FHS-12 can move from FAIL only at this narrowed ceiling; a native PASS would need the functional turn and the registry baseline, neither available read-only",
}
for target in (WP12 / "RUNTIME_PATH_LAB.v3.json", W / "RUNTIME_PATH_LAB.v3.json"):
    target.write_text(json.dumps(lab, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

print(json.dumps(checks, indent=1))
print("all computable checks true:", all(v is True for v in checks.values() if v is not None))
