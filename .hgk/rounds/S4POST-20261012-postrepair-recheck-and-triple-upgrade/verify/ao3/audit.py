from pathlib import Path
import json, os, subprocess, sys, tempfile
SUBJECT = Path.cwd()
ROUND = Path(".hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade")
OUT = SUBJECT / ROUND / "verify/ao3"
RESULTS = {}
def run(name, command, cwd=SUBJECT, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    header = f"COMMAND: {subprocess.list2cmdline(command)}\nCWD: {cwd}\nEXIT_CODE: {result.returncode}\nRAW OUTPUT:\n"
    (OUT / (name + ".txt")).write_bytes(header.encode() + result.stdout)
    RESULTS[name] = {"command":command,"cwd":str(cwd),"exit":result.returncode}
    print(name, result.returncode, flush=True)
    return result
head = run("head", ["git","rev-parse","HEAD"]).stdout.decode().strip()
run("tree", ["git","rev-parse","HEAD^{tree}"])
run("delivery-status-before", ["git","status","--porcelain"])
run("local-branch", ["git","branch","--show-current"])
run("closure-paths", ["git","log","--reverse","--format=commit %H%nparents %P%nsubject %s","--name-status","07681745a436a7d82e85a0aa494d8165acad92a0.."+head])
run("ancestor", ["git","merge-base","--is-ancestor","07681745a436a7d82e85a0aa494d8165acad92a0",head])
scratch = Path(tempfile.mkdtemp(prefix="pipd-ao3-"))
candidate = scratch / "candidate"
(OUT / "snapshot-path.txt").write_text(str(candidate))
run("clone", ["git","clone","--no-hardlinks","--no-checkout",str(SUBJECT),str(candidate)], scratch)
run("detach", ["git","checkout","--detach",head], candidate)
run("snapshot-status", ["git","status","--porcelain"], candidate)
environment = os.environ.copy()
for key in list(environment):
    if key.startswith("GIT_CONFIG_") or key in ("GIT_ASKPASS","SSH_ASKPASS"):
        environment.pop(key)
environment.update({"GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":os.devnull,"GIT_TERMINAL_PROMPT":"0","GIT_ASKPASS":"","SSH_ASKPASS":""})
run("anonymous-remote", ["git","-c","credential.helper=","-c","core.askPass=","-c","http.extraHeader=","ls-remote","https://github.com/shw097-team/PIPD-LS-SP.git","refs/heads/feat/s4post-triple-upgrade-20261012-r2"],scratch,environment)
run("committed-ao2-paths", ["git","ls-tree","-r","--name-only",head,str(ROUND / "verify/ao2")])
for label in ("model-logs","closure-records"):
    selected = [path for path in sorted((candidate / ROUND / "stage-b").glob("*")) if path.is_file() and ((label == "model-logs" and path.name.startswith(("B1_","B2_","B3_","MODEL_DECLARED_","probe_"))) or (label == "closure-records" and any(word in path.name.lower() for word in ("closure","handover","ao2","hygiene"))))]
    run(label, [sys.executable,"-c", 'from pathlib import Path; import sys; [(print("FILE:",p),print(Path(p).read_text(encoding="utf-8",errors="replace"))) for p in sys.argv[1:]]'] + [str(path) for path in selected], candidate)
run("interpreter", [sys.executable,"-c",'import sys,os,platform; print(sys.executable); print(sys.version); print(platform.platform()); print(os.getcwd()); print("O_NOFOLLOW",hasattr(os,"O_NOFOLLOW")); print("O_NONBLOCK",hasattr(os,"O_NONBLOCK"))'],candidate)
workflow = (candidate / ".github/workflows/public-plugin-verify.yml").read_text()
guard = workflow.split("          set -euo pipefail",1)[1].split("\n      - name:",1)[0]
guard = "set -euo pipefail" + "\n".join(line[10:] if line.startswith("          ") else line for line in guard.splitlines()) + "\n"
guard_path = OUT / "guard-extracted.sh"
guard_path.write_text(guard,encoding="utf-8",newline="\n")
guard_environment = os.environ.copy()
guard_environment.update({"PR_BASE_SHA":"","STACKED_BASE_SHA":"52542c395a0f91dc2ba4bd6123acd4cdecd780dc"})
run("guard-current-head", ["C:/Program Files/Git/bin/bash.exe",str(guard_path)],candidate,guard_environment)
run("focused", [sys.executable,"-m","unittest","-v","tests.test_public_plugin_packaging","tests.test_web_fallback","tests.test_s4ext_release_provenance"],candidate)
run("full", [sys.executable,"-m","unittest","discover","-s","tests","-v"],candidate)
(OUT / "command-results.json").write_text(json.dumps(RESULTS,indent=2))
