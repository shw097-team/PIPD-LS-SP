# R11 independent verification brief (VERIFY_ONLY, revision 2)

You are the INDEPENDENT CHECKER for round `R11-20261011-s4-credential-closure-and-fda-integration`.
The maker cannot sign its own verdict; your verdict is the acceptance input.

> **Why revision 2 exists.** Revision 1 was itself defective, and it is stated rather than hidden: it
> asserted a claim the maker had not proven; it forbade the temporary writes that two of the suites need,
> so they became uncheckable; it told you to search for secret-shaped literals using those same literals as
> examples - a rule that flags itself; and it never told you to emit the lane nonce, so a turn that did the
> whole job was nonetheless voided at the gate. All four are fixed below. Revision 1 is kept on disk
> unedited as the record of what the checker was first asked to do.

## Hard rules

1. **One permitted write directory.** You may write ONLY under
   `C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/r11/xverify/checker-tmp`
   (create it if needed; this is what lets the suites run). Do **not** write, edit, create or delete
   anything anywhere else - not in any repository, not in the round directory, not in the evidence
   folder. **A write outside that directory voids your own verdict**, even if every check passed.
2. **RE-DERIVE, do not relay.** For every claim, run the command yourself and report the raw result. Do
   not read the maker's reports and restate their conclusions. If you cannot re-derive a claim, say
   `UNCERTAIN` and say why.
3. **Assert IMMUTABLE facts only.** A commit's content, a file's hash, a suite's result, a binding
   string. Branch tips may move: REPORT them, do not fail on them.
4. **Be adversarial.** A checker that agrees with everything has added nothing. If a claim ceiling is too
   high, name the part that is not supported.
5. Use the interpreter `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (absolute path -
   a bare `python` on this host may lack dependencies). Pass NATIVE `C:/...` paths to native programs;
   MSYS `/c/...` paths are NOT translated and will fail with "cannot open file".

## OUTPUT CONTRACT - READ THIS BEFORE YOU ANSWER

Your **final message** must contain the exact token

```
HGK_LANE_NONCE_OK
```

on its own line, and after it the JSON verdict block below and nothing else. The lane gate rejects a turn
whose final message does not carry the nonce: such a turn is recorded VOID and your entire verification is
discarded unread. So: do the work, then emit **the nonce line, then the JSON**.

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

## Repositories

- control plane: `C:/Projects/Agent_Workspace/HG-KSEOS`
- product round: `C:/Projects/Agent_Workspace/PIPD-r7-release`
- evidence host: `C:/Projects/Agent_Workspace/Fabric`

Expected commits: control plane **`8ab82ec`** plus any later commit that corrects the artefacts (report
what you find); product round **`ae08136`** plus the round artefact commit after it; evidence host
**`463ca0a`**.

## Claims to verify (each one, by re-running it)

### C1 - what the gate actually requires

```
git -C C:/Projects/Agent_Workspace/HG-KSEOS show --stat 8ab82ec
git -C C:/Projects/Agent_Workspace/HG-KSEOS show 8ab82ec -- scripts/cred/cred_preflight.py
```

Determine, by **executing the committed source** where you can, not by reading it:

- Does the default path require the validity of the source that will actually be used (i.e. the App, when
  an App is configured), rather than unconditionally the PAT's validity?
- **Enumerate every flag or environment variable that can turn that requirement OFF**, and for each one
  state exactly what verdict `run_preflight()` returns and whether it aborts. `--no-probe` is known to be
  one such flag: reproduce it yourself and report the raw `effective_source`, `app_cred_valid`, `required`,
  `failed_required`, `verdict` and `abort` values.
- Then state plainly whether the artefacts' claims match that behaviour. **An earlier assertion, "a
  configured-but-unprobed App is refused", was FALSE for `--no-probe`; do not take any claim in the FARs
  on trust - check each one against the code.**

### C2 - the suites, which revision 1 made uncheckable

```
cd C:/Projects/Agent_Workspace/HG-KSEOS
<PY> -B scripts/cred/selftest.py
<PY> -B scripts/cred/verify_offline.py
```

Both write temporary files; that is what the permitted directory in Hard rule 1 is for. If a suite still
cannot complete, report the exact error rather than adopting the maker's number.

Assert: the `selftest` verdict and passed/total, and the `verify_offline` verdict. Then **independently
recompute** every sha256 in `scripts/cred/INSTALL_MANIFEST.json` against the file it names - do NOT trust
the suite's own pin check - and report the mismatch count. Also check whether the manifest's declared
expectation for `V3_full_contract_dummy` matches what `selftest.py` actually reports; the maker says the
expectation was stale at `5/5` and now reads `7/7`.

### C3 - the evidence artefact does not move the sealed binding

```
cd C:/Projects/Agent_Workspace/HG-KSEOS
<PY> -B var/fda/hgk_evidence_preflight.py
```

Assert: the final `PREFLIGHT:` line, its exit code, and the exact `three-way bound:` value printed. Then
confirm **by independent inspection** (e.g. `git ls-tree` at the commit's parent and at the commit) that
the latest `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE*` file in
`C:/Projects/Agent_Workspace/Fabric/fabric-desktop-automation/evidence/` is byte-identical across this
round's addition, and that the new artefact does not contain the literal string `this_file_sha256`.

### C4 - the evidence host commit contains EXACTLY the round's two paths

```
git -C C:/Projects/Agent_Workspace/Fabric show --stat 463ca0a
git -C C:/Projects/Agent_Workspace/Fabric diff-tree --no-commit-id --name-status -r 463ca0a
```

Assert: exactly 2 files, both under `fabric-desktop-automation/evidence/`. Then recompute the sha256 of
`fabric-desktop-automation/evidence/FDA_R11_CREDENTIAL_AUTOMATION_DISCIPLINE_AND_EVIDENCE.md` and compare
it to `evidence_md_sha256` in the sibling sidecar `FDA_R11_EVIDENCE_SIDECAR.json`. Report equal or not.

### C5 - the round's own artefacts exist and say what the round claims

List `C:/Projects/Agent_Workspace/PIPD-r7-release/.hgk/rounds/R11-20261011-s4-credential-closure-and-fda-integration/`
recursively and report every file with its size. Then open and report:

- `admission/r11_admission.json` - the admitted requirement count, the requirement states, the error list.
- `kanban/BOARD_READBACK.json` - the board slug and the swarm ids, and whether the recorded statuses match
  the live board.
- `surface/GSTACK_R11_ROUTE_READBACK.json` - the DECLARED plan route vs the MANDATED one, whether the file
  keeps them separate, **and whether it claims any observation it did not make** (`observed_this_round` is
  expected to be `null` - say so if it is, and do not read a declaration as execution).
- `far/FAR-PIPD-R11-CREDGATE-001.md`, `far/FAR-PIPD-R11-FDAEVID-002.md` and (if present)
  `far/FAR-PIPD-R11-LANEDISPATCH-003.md` - the claim ceiling line of each, and every residual each admits.

### C6 - no credential material in the artefacts (revised: the briefs are excluded)

Scan every file under the round directory **and** the Fabric evidence artefact for secret-shaped literals
and for a private-key filename with content. **Exclude `verify-codex/VERIFY_BRIEF_R11.md` and
`verify-codex/VERIFY_BRIEF_R11_REV2.md` from this scan** - revision 1 named the search patterns inside the
brief, so the brief flagged itself and the rule was self-defeating; that was an acceptance-rule failure,
not a leak. Report the hit count excluding those two files. A non-zero hit is a FAIL for this round.

### C7 - the write claim, tested by you rather than read from the maker

The maker claims a token minted from an organisation-owned GitHub App installation wrote to
`https://github.com/shw097-team/PIPD-LS-SP.git`. Tests you can run **without any credential**:

```
git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git main
git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git "refs/tags/*"
```

Report the values. Then state plainly **what a credential-free read can NOT establish about that claim** -
note in particular that this repository is public, so an anonymous read proves nothing about any token.

Remember: nonce line first, then the JSON, and nothing else.
