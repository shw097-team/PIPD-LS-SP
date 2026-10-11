# R11 independent verification brief (VERIFY_ONLY)

You are the INDEPENDENT CHECKER for round `R11-20261011-s4-credential-closure-and-fda-integration`.
The maker cannot sign its own verdict; your verdict is the acceptance input.

## Hard rules

1. **VERIFY_ONLY.** Do not write, repair, edit, create or delete ANY file, anywhere. If something is
   wrong, report it - do not fix it. Any write invalidates your own verdict.
2. **RE-DERIVE, do not relay.** For every claim below, run the command yourself and report the raw
   result. Do not read the maker's reports and restate their conclusions. If you cannot re-derive a
   claim, say `UNCERTAIN` and say why.
3. **Assert IMMUTABLE facts only.** A commit's content, a file's hash, a suite's result, a binding
   string. Branch tips may move: REPORT them, do not fail on them.
4. Use the interpreter `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (absolute
   path - a bare `python` on this host may lack dependencies).
5. Pass NATIVE `C:/...` paths to native programs; MSYS `/c/...` paths are NOT translated and will fail
   with "cannot open file".

## Repositories

- control plane: `C:/Projects/Agent_Workspace/HG-KSEOS`
- product round: `C:/Projects/Agent_Workspace/PIPD-r7-release`
- evidence host: `C:/Projects/Agent_Workspace/Fabric`

Expected commits: control plane **`8ab82ec`**, product round **`ae08136`** plus the round artefacts
committed after it, evidence host **`463ca0a`**.

## Claims to verify (each one, by re-running it)

### C1 - the control-plane change is a one-line-class fix to a gate, not a behaviour widening

```
git -C C:/Projects/Agent_Workspace/HG-KSEOS show --stat 8ab82ec
git -C C:/Projects/Agent_Workspace/HG-KSEOS show 8ab82ec -- scripts/cred/cred_preflight.py
```
Assert: the gate now resolves an effective source and requires THAT source's validity; the App is probed
by minting an installation token; a configured-but-unprobed App is REFUSED (not passed). State whether
any code path still fails closed, and name it.

### C2 - the suites pass, and the manifest pins resolve

```
cd C:/Projects/Agent_Workspace/HG-KSEOS
<PY> -B scripts/cred/selftest.py
<PY> -B scripts/cred/verify_offline.py
```
Assert: `selftest` verdict and passed/total; `verify_offline` verdict. Then independently recompute every
sha256 in `scripts/cred/INSTALL_MANIFEST.json` against the file it names and report the mismatch count.
Do NOT trust the suite's own pin check - recompute it yourself.

### C3 - the evidence artefact does not move the sealed binding

```
cd C:/Projects/Agent_Workspace/HG-KSEOS
<PY> -B var/fda/hgk_evidence_preflight.py
```
Assert: the final `PREFLIGHT:` line and its exit code, and the exact `three-way bound:` value printed.
Then confirm by independent inspection that the latest `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE*` file in
`C:/Projects/Agent_Workspace/Fabric/fabric-desktop-automation/evidence/` is the SAME file as before this
round's addition (i.e. the new artefact did not join that series), and that the new artefact does not
contain the literal string `this_file_sha256`.

### C4 - the evidence host commit contains EXACTLY the round's two paths

```
git -C C:/Projects/Agent_Workspace/Fabric show --stat 463ca0a
```
Assert: exactly 2 files, both under `fabric-desktop-automation/evidence/`. Then recompute the sha256 of
`fabric-desktop-automation/evidence/FDA_R11_CREDENTIAL_AUTOMATION_DISCIPLINE_AND_EVIDENCE.md` and compare
it to `evidence_md_sha256` in the sibling sidecar `FDA_R11_EVIDENCE_SIDECAR.json`. Report equal or not.

### C5 - the round's own artefacts exist and say what the round claims

List `C:/Projects/Agent_Workspace/PIPD-r7-release/.hgk/rounds/R11-20261011-s4-credential-closure-and-fda-integration/`
recursively and report every file with its size. Then open and report:
- `admission/r11_admission.json` - the admitted requirement count, the requirement states, and the error list.
- `kanban/BOARD_READBACK.json` - the board slug and the swarm ids.
- `surface/GSTACK_R11_ROUTE_READBACK.json` - the DECLARED plan route vs the MANDATED one, and whether the
  file keeps them separate.
- `far/FAR-PIPD-R11-CREDGATE-001.md` and `far/FAR-PIPD-R11-FDAEVID-002.md` - the claim ceiling line of each.

### C6 - the credentials named in the artefacts are not present in them

Search the whole round directory and the Fabric evidence artefact for token-shaped strings
(`github_pat_`, `ghs_`, `ghp_`, `gho_`, `-----BEGIN`) and for a private-key filename with content. Report
the hit count. A non-zero hit is a FAIL for this round.

### C7 - the write claim, tested by you rather than read from the maker

The maker claims a token minted from an organisation-owned GitHub App installation wrote to
`https://github.com/shw097-team/PIPD-LS-SP.git`. Tests you can run **without any credential**:
```
git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git main
git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git "refs/tags/*"
```
Report the values. Then state plainly: **what can a credential-free read NOT establish about that claim?**
(This is the point of the question - a public repository's read is anonymous, so say so.)

## Required output (JSON, nothing else after it)

```json
{
  "verdict": "PASS | FAIL | UNCERTAIN",
  "checks": [{"id": "C1", "status": "PASS|FAIL|UNCERTAIN", "evidence": "<the raw command result>", "note": "<one line>"}],
  "could_not_verify": ["<each claim you are unable to establish, with the reason>"],
  "disagreements": ["<every place the artefacts contradict each other or the code, or empty>"],
  "immutable_facts_asserted": ["<the digests / bindings you confirmed>"],
  "moved_and_only_reported": ["<branch tips or counts that legitimately changed>"]
}
```

Be adversarial. A checker that agrees with everything has added nothing. If the maker's claim ceiling is
too high, say which part is not supported.
