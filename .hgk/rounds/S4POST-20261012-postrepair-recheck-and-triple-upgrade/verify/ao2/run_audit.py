from pathlib import Path
import json, os, shutil, subprocess, sys
subject = Path(__file__).resolve().parents[2]
evidence = subject / "verify/ao2"
scratch = Path((evidence / "scratch_path.txt").read_text().strip())
candidate = scratch / "candidate"
results = {}
def run(command, cwd, log, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with (evidence / log).open("ab") as output:
        output.write(("COMMAND: " + subprocess.list2cmdline([str(item) for item in command]) + "\nCWD: " + str(cwd) + "\n").encode())
        output.write(result.stdout)
        output.write(("\nEXIT_CODE=" + str(result.returncode) + "\n").encode())
    return result
sys.path.insert(0, str(candidate))
from tests import test_public_plugin_packaging as fixture
old_tools = scratch / "pre-fix/tools"
old_tools.mkdir(parents=True)
old_bytes = run(["git", "show", "07681745a436a7d82e85a0aa494d8165acad92a0^:tools/build_public_plugin.py"], candidate, "B_pre_fix_extraction.txt").stdout
(old_tools / "build_public_plugin.py").write_bytes(old_bytes)
shutil.copyfile(candidate / "tools/freeze_public_plugin_source.py", old_tools / "freeze_public_plugin_source.py")
for version, tool in [("current", candidate / "tools/build_public_plugin.py"), ("pre-fix", old_tools / "build_public_plugin.py")]:
    for case, member in [("sidecar", fixture.PLUGIN_ID + ".zip.sha256"), ("artifact", fixture.PLUGIN_ID + ".zip"), ("mapping", "SOURCE_TO_PLUGIN_MAPPING.json"), ("receipt", "RELEASE_RECEIPT.json"), ("control", None)]:
        case_root = scratch / ("probe-" + version + "-" + case)
        case_root.mkdir()
        test_env = fixture.Env(case_root)
        ledger = test_env.freeze()
        test_env.write_packaging(ledger)
        ledger_path = test_env.write_ledger(ledger)
        test_env.out.mkdir()
        sentinel = case_root / "outside-sentinel.bin"
        sentinel_bytes = b"AO2_EXTERNAL_SENTINEL_DO_NOT_OVERWRITE\x00\xff\n"
        sentinel.write_bytes(sentinel_bytes)
        seeded = test_env.out / member if member else None
        if seeded:
            os.link(sentinel, seeded)
        same_inode = os.path.samefile(sentinel, seeded) if seeded else None
        command = [sys.executable, str(tool), "--source-root", str(test_env.source), "--ledger", str(ledger_path), "--source-commit", fixture.COMMIT, "--packaging-root", str(test_env.packaging), "--out-dir", str(test_env.out)]
        completed = run(command, candidate, "B_" + version + "_" + case + ".txt")
        artifact = test_env.out / (fixture.PLUGIN_ID + ".zip")
        record = dict(exit_code=completed.returncode, sentinel_unchanged=sentinel.read_bytes() == sentinel_bytes, sentinel_before_hex=sentinel_bytes.hex(), sentinel_after_hex=sentinel.read_bytes().hex(), seeded_exists=seeded.exists() if seeded else None, hardlink_verified=same_inode, artifact_exists=artifact.exists(), artifact_promoted=artifact.exists() and (case != "artifact" or artifact.read_bytes() != sentinel_bytes), remaining_members=sorted(path.name for path in test_env.out.iterdir()))
        results[version + "-" + case] = record
        with (evidence / ("B_" + version + "_" + case + ".txt")).open("a") as output:
            output.write(json.dumps(record, indent=2) + "\n")
workflow = (candidate / ".github/workflows/public-plugin-verify.yml").read_text()
(evidence / "C_workflow_raw.txt").write_text(workflow)
section = workflow.split("      - name: Prove the upgrade wrote only inside its allowed set\n", 1)[1].split("      - name:", 1)[0]
guard = section.split("        run: |\n", 1)[1]
guard = "\n".join(line[10:] for line in guard.splitlines()) + "\n"
(evidence / "C_guard_exact.sh").write_text(guard)
guard_path = scratch / "guard.sh"
guard_path.write_text(guard, newline="\n")
base = "52542c395a0f91dc2ba4bd6123acd4cdecd780dc"
shell_env = os.environ.copy()
shell_env["PR_BASE_SHA"] = ""
shell_env["STACKED_BASE_SHA"] = base
bash = shutil.which("bash")
for case, relative in [("candidate", None), ("dist", "dist/scratch.txt"), ("docs", "docs/random-note.md")]:
    if relative:
        run(["git", "checkout", "--detach", "07681745a436a7d82e85a0aa494d8165acad92a0"], candidate, "C_" + case + ".txt")
        added = candidate / relative
        added.parent.mkdir(parents=True, exist_ok=True)
        added.write_text("AO2 synthetic disallowed path\n")
        run(["git", "add", "--force", relative], candidate, "C_" + case + ".txt")
        run(["git", "-c", "user.name=AO2 scratch only", "-c", "user.email=ao2@example.invalid", "commit", "-m", "AO2 synthetic " + relative], candidate, "C_" + case + ".txt")
    completed = run([bash, str(guard_path).replace("\\", "/")], candidate, "C_" + case + ".txt", shell_env)
    results["guard-" + case] = completed.returncode
run(["git", "checkout", "--detach", "07681745a436a7d82e85a0aa494d8165acad92a0"], candidate, "C_restore.txt")
for case, value in [("missing", ""), ("unresolved", "0" * 40)]:
    altered_env = shell_env.copy()
    altered_env["STACKED_BASE_SHA"] = value
    completed = run([bash, str(guard_path).replace("\\", "/")], candidate, "C_" + case + ".txt", altered_env)
    results["guard-" + case] = completed.returncode
round_path = ".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/"
for path in [round_path + "verify/ao/AO_VERDICT_STAGEB.md", round_path + "evidence/08_PLUGIN/UPG_GATE_RECEIPT.json"]:
    run(["git", "cat-file", "-e", "HEAD:" + path], subject, "D_committed_evidence.txt")
for path in [round_path + "verify/ao/AO_VERDICT_STAGEB.md", round_path + "evidence/08_PLUGIN/UPG_GATE_RECEIPT.json", round_path + "ROUND_RESULT.md", "packaging/public-plugin/OWNER_INPUT_REQUIRED.json", "docs/install/README.md"]:
    run(["git", "show", "HEAD:" + path], candidate, "F_claims_raw.txt")
for label, command in [("focused", [sys.executable, "-m", "unittest", "tests.test_public_plugin_packaging", "tests.test_web_fallback"]), ("full", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."])]:
    completed = run(command, candidate, "E_" + label + "_raw.txt")
    results["regression-" + label] = completed.returncode
run(["git", "status", "--porcelain"], subject, "D_final_status.txt")
(evidence / "results.json").write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
