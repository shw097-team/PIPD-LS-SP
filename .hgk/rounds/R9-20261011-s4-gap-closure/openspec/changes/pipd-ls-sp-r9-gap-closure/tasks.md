# tasks — pipd-ls-sp-r9-gap-closure

## 1. Scan our own source

- [x] 1.1 bandit in a clean `uv` venv over `src/` and over `tools/`+`skills/`, measured separately
- [x] 1.2 triage every HIGH/MEDIUM with file:line; assess each honestly rather than restating the rule name
- [x] 1.3 fix the HIGH **by construction** — `extractall` removed, members written by hand
- [x] 1.4 guard the two MEDIUM `urlopen` sites with a scheme allow-list
- [x] 1.5 prove the fix by **behaviour**: crafted traversal / absolute / symlink members refused, benign nested file extracted
- [x] 1.6 prove no regression: end-to-end `pi_dedup_check --check` still reports `baseline_source: HEAD`
- [x] 1.7 re-run the scanner: HIGH 0, MEDIUM 0

## 2. Audit the SPEC/DEL active gaps

- [ ] 2.1 adjudicate each of the 10 active rows individually, naming the artefact actually opened
- [ ] 2.2 recount the denominator from the crosswalk rather than restating prose
- [ ] 2.3 list the rows that could NOT be adjudicated, and why

## 3. DEL-018 on `main`

- [x] 3.1 measure the failure exactly (`253` product paths, `252` covered, 1 uncovered)
- [x] 3.2 find the real cause — a **four-round-stale evidence seal** (`9667783`), not a tool defect and not the missing file
- [x] 3.3 re-seal from the current tree; rebuild the projection; `--check --current` → `PASS` `253/253`
- [x] 3.4 correct README limitation 4 and disclose the release-evidence re-binding

## 4. Cross-model re-run on a clean tree

- [ ] 4.1 run the VERIFY_SECURITY lane (`openai-codex/gpt-6.1-sol`) on a **committed** clean tree
- [ ] 4.2 record its verdict, including the strict clean-worktree gate result, and keep the non-mutation guard

## 5. Credential scheme

- [ ] 5.1 FAR over the credential options, recommending the smallest scheme that survives an unattended run
- [ ] 5.2 implement and verify the automatable parts; enumerate the residual human steps and why each cannot be automated

## 6. Round bookkeeping

- [x] 6.1 verify the R8 board state; record it `UNVERIFIED` and withdraw the unevidenced claim
- [x] 6.2 write kanban / swarm / openspec artefacts to disk so the state is checkable
