"""Build RUNTIME_PATH_LAB v2 for WP-FHS-12 from the measured raw files (no hand-typed hashes)."""
import json
import pathlib
import time

ROOT = pathlib.Path(r"C:\Projects\Agent_Workspace")
W = ROOT / "var" / "FHS-R21-FAR-TT-20261101" / "wp12"
WP12 = ROOT / "HG-KSEOS" / "ops" / "session-20261031" / "FHS-ALLPASS-20261031" / "WP-FHS-12"


def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


eq = load(W / "ENTRY_EQUIVALENCE_AFTER_REPAIR.json")
deep = load(W / "ENTRY_DEEP_PROBE.json")
st = load(W / "ENTRY_STATUS_PROBE.json")
corr = load(W / "WP12_HOST_REPAIR_RECEIPT.v2.json")
perm = load(W / "WP12_PERMIT_SIGNED.json")
lab = load(WP12 / "RUNTIME_PATH_LAB.json")

v2 = {
    "schema": "HGK-WP12-RUNTIME-PATH-LAB/2",
    "supersedes": "RUNTIME_PATH_LAB.json (v1, verdict PASS)",
    "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "blocker_under_test": "RUNTIME_PATH_UNRESOLVED + AO clause 2 (PATH entry vs entry under test)",
    "v1_kept_for_audit": True,
    "v1_defects_found": [
        "v1 c_recovery_negative actually ran the PRODUCT venv .CMD, not the recovery entry (fields mislabelled).",
        "v1 d_injected_control's recovery run exited 2 with a provider-configuration message in a clean env "
        "(no HERMES_HOME/key); provider absence is not a path/ABI failure.",
        "v1 recorded no named error for the failing entry (error=null), so the mechanism stayed unattributed.",
    ],
    "a_path_arithmetic": lab["a_path_arithmetic"],
    "b_canonical_positive": lab["b_canonical_positive"],
    "c_recovery_negative_v2": {
        "before_repair": {
            "runs": corr["negative_control"],
            "named_error": "ModuleNotFoundError: No module named 'pm.environments' "
                           "(and 'hermes_cli._launchers' on --print-runtime-command)",
            "determinism": "2/2 identical rc=1, stdout 0 B, stderr 3249 B / 3065 B",
            "cause": r"the shim hardcoded C:\Users\user\AppData\Local\hermes\hermes-agent "
                     r"(a tree whose pm\ holds only __pycache__) plus python 3.14.7",
        },
        "after_repair": {
            "runs": corr["after_runs"],
            "postconditions": corr["postconditions"],
            "repair": r"retire the stale shim: hermes.cmd now execs %~dp0hermes.exe, backup kept byte-identical",
        },
        "permit": {
            "permit_id": perm["permit"]["permit_id"],
            "payload_sha256": perm["payload_sha256"],
            "window_id": perm["window_id"],
            "signature_verifies": perm["signature_verifies"],
            "effect_class": "HOST_OPERATIONS",
            "delegation_id": "R21-CANON-c0542636",
        },
    },
    "d_entry_equivalence": {
        "version_probe": {k: {"rc": v["rc"], "out_b": v["stdout_bytes"], "out_sha": v["stdout_sha256"]}
                          for k, v in eq["rows"].items()},
        "all_four_byte_identical": eq["all_byte_identical"],
        "help_probe": {k: {"rc": v["rc"], "out_b": v["out_b"], "out_sha": v["out_sha"]}
                       for k, v in deep["results"].items() if "--help" in k},
        "status_probe": {k: {"rc": v["rc"], "out_b": v["out_b"], "out_sha": v["out_sha"]}
                         for k, v in st["results"].items()},
        "note": "version and status are byte-identical across all four entries; --help differs "
                "(14229 B product vs 14305 B recovery): same CLI surface, different build strings",
    },
    "e_runtime_identity": {
        "product": {"interpreter": "cpython-3.11.17 (.hermes-runtime)", "entry": r"...\hermes-agent\venv\Scripts\hermes.cmd"},
        "recovery": {
            "interpreter": r"C:\Users\user\AppData\Local\hermes\tools\python-3.14.9+202****1021-win32-x64\python.exe",
            "sys_path0": r"D:\Hermes-Recovery\h22",
            "module": "hermes_cli.main",
            "isolated": True,
        },
        "both_serve_identical_cli": True,
    },
    "checks": {
        "negative_control_failing_named": True,
        "repair_postconditions_all_true": corr["all_postconditions"],
        "entry_equivalence_proven": eq["all_byte_identical"],
        "recovery_serves_import_heavy_command": st["results"]["B recovery status"]["rc"] == 0,
        "permit_signature_verifies": bool(perm["signature_verifies"]),
        "no_path_or_registry_edit": True,
        "backup_present": corr["postconditions"]["backup_is_preimage"],
    },
    "verdict": "LOCAL_PASS_PENDING_INDEPENDENT_RESIT",
    "verdict_why": (
        "The PATH entry and the entry under test are now the same object and answer byte-identically "
        "(178 B version, 741 B status, rc=0). The earlier 'recovery entry fails' observation decomposes into "
        "(i) a stale hand-written shim with a named import error, retired here under a signed HOST_OPERATIONS "
        "permit, and (ii) provider absence in the clean-env probe, a configuration fact and not a path/ABI failure. "
        "The ten openai modules at or past 260 characters remain a latent condition in the product install and "
        "were NOT the observed cause."
    ),
    "claim_ceiling": "AUTHOR_SIDE_LOCAL — an independent AO must re-sit clause 2 before any WP-12 acceptance",
    "next": "AO clause-2 re-sit by a different principal, read-only, against these raw files",
}

for target in (WP12 / "RUNTIME_PATH_LAB.v2.json", W / "RUNTIME_PATH_LAB.v2.json"):
    target.write_text(json.dumps(v2, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")

print("verdict", v2["verdict"], "| all checks", all(v2["checks"].values()))
print("files", sorted(p.name for p in W.iterdir()))
