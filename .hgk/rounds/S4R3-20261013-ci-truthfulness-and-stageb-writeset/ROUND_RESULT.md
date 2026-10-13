# PIPD_S4_R3_EXECUTION_RESULT

Round: `S4R3-20261013-ci-truthfulness-and-stageb-writeset`
Source order: `PIPD-S4-R3-HERMES-HGK-THIN-COMMAND/1` (report `PIPD-S4-EXT-ACCEPT-R3-20261013`, sha256 `6a579d36…`)
Host: Hermes orchestration plane, HG-KSEOS as the only control plane. Date: 2026-10-13, Asia/Taipei.

**Flags: `NO_MERGE` · `NO_PUBLIC_RELEASE` · `S4_FULL_PASS = NOT_GRANTED`.**

---

## 1. Compiler verdicts (C0–C9 contracts, two separate change sequences)

Two contracts were authored and compiled with the local native compiler
(`construction-acceptance-prompt-compiler/scripts/prompt_contract_compiler.py`) before any product
write. Both passed all four gates; the receipts are in the round's scratch output and their hashes
are reproduced here.

| change sequence | class | lint | activation | acceptance | compile | contract sha256 |
|---|---|---|---|---|---|---|
| `S4R3-STAGE-A-CORE-REPAIR` | `NARROW_REPAIR` | PASS (0 errors) | PASS | PASS | `PROMPT_COMPILE_PASS` | `926e5d5d6e68e2e22501587c8c64d443e14f3b63a7cc28565741e2454a359269` |
| `S4R3-STAGE-B-DISTRIBUTION` | `UPGRADE` | PASS (0 errors) | PASS | PASS | `PROMPT_COMPILE_PASS` | `5cb0a618f7eea8f3134607ae8986d7fb3624d37d1b3f21b451029612366b3289` |

The first iteration of contract A was rejected by the compiler with 49 errors (lifecycle-state
vocabulary and prompt-length ceiling). That rejection is kept as evidence that the gate is real and
was not bypassed; the repaired iteration is the one above. **Deviation, disclosed:** the contracts
were written by the same actor that then executed the work — this is a PLAN-side contract, not an
independent acceptance input.

## 2. HGK admission

Project `PIPD-LS-SP-20261008` (already `EXECUTING`). Seven obligations admitted through the typed
`SharedSpine` / `ProjectLifecycleController` API — 7 requirements `FROZEN`, 7 taskspecs `ADMITTED`,
7 workorders `CREATED`, 7 acceptances bound with oracles and `verdict=NOT_RUN`, 0 errors. Receipt:
`admission/s4r3_admission.json`.

- `REQ-S4R3-STAGE-A-CORE-REPAIR-001` (P0, CI-OWNER) · `…-002` (P0, TQAEP-OWNER)
- `REQ-S4R3-STAGE-B-DISTRIBUTION-001` (P0, PKG07-OWNER) · `…-002` (P1, DX-OWNER)
- `REQ-S4R3-ADMIT-003` · `REQ-S4R3-VERIFY-004` · `REQ-S4R3-CLOSURE-005`

**Ordering deviation, disclosed:** the contracts were compiled and the first candidate edits were
authored in the worktree *before* `admit_requirement` ran. Admission preceded the commit, the push
and every publication act, but not the first uncommitted draft.

## 3. Frozen subject and candidates

| item | value |
|---|---|
| frozen base | `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` (tree `2875287352529ee92277d7dc4f37cd12ffc977c7`) |
| remote `main` at freeze | `224591431a164ab72a9423cd180e417e8a762403` — unchanged by this round |
| Stage A candidate | `517d7a5d3f00935e1589908f456dfacea8fd8a74` |
| Stage A branch tip (candidate + evidence) | `25f4dfed53281617a1dd734663c474aa8b7f7299` |
| Stage B candidate | `8481f29913159ed91ac6dff5ab3d691ea3614355` |
| Stage B declared base | `517d7a5d3f00935e1589908f456dfacea8fd8a74` |
| Stage B branch tip (candidate + evidence) | `d561f52e91b0a0efd63443e21bb5e49bfa509d96` |
| draft PR (Stage A) | https://github.com/shw097-team/PIPD-LS-SP/pull/3 — draft, open, not merged, base `main` |
| draft PR (Stage B, stacked) | https://github.com/shw097-team/PIPD-LS-SP/pull/4 — draft, open, not merged, base = Stage A branch, **7 changed files** |

Push readback: `evidence/09_OWNER_RELEASE/PUSH_READBACK.txt` (remote refs re-read anonymously after
the push; `main` and tag `v0.1.1-preview.3` untouched). No force push, no tag, no release.

## 4. Finding ledger and R2 atom ledger

`evidence/02_LEDGER/R3_FINDING_LEDGER.json` — dispositions of the source report's findings:

| finding | class | disposition | what the ceiling is |
|---|---|---|---|
| `S4R3-F001` | P0 confirmed defect | **CLOSED in scope** | source repair + local Linux/Windows receipts + hosted `ci` on the candidate; not an S4 acceptance |
| `S4R3-F002` | P0 confirmed defect | **CLOSED in scope** | repaired gate green on the hosted run of the Stage B branch; the pre-repair gate's red run is explained, not hidden |
| `S4R3-F003` | P1 evidence gap | **OPEN_TT_OWNER** | human publisher identity, brand assets, vendor validator, portal acts — owner-only |
| `S4R3-F004` | P1 evidence gap | **CLOSED in scope** | artefact present + links clean, verified locally; external newcomer journeys NOT_EXECUTED |
| `S4R3-F005` | hygiene observation | **PARTIAL** | this round added no large binary and deleted no historical receipt; the 62 MB `.hgk` mass needs an owner archival policy |

`evidence/02_LEDGER/R2_ATOM_LEDGER.json` — 118 atoms from the R2 blueprint, every declared family
complete (`F` 14/14, `RP-P` 8/8, `A` 42/42, `TR` 40/40, `UPG-G` 10/10, `UPG-P` 4/4), produced by a
separate PLAN-lane subagent:

| disposition | count |
|---|---|
| `OPEN_TT` | 104 |
| `VERIFIED` | 13 |
| `NOT_APPLICABLE_WITH_REASON` | 1 |

No atom was flipped to PASS on the strength of a file existing.

## 5. Real exit codes and denominators

| environment | suite | result | exit |
|---|---|---|---|
| frozen base `e71fee6e`, hosted Linux | full | `Ran 572` — **`FAILED (failures=11, skipped=6)`** under a job reported *success* | masked (the defect) |
| frozen base `e71fee6e`, hosted Linux | focused | `Ran 108` — **`FAILED (failures=2)`** under the same green job | masked |
| frozen base `e71fee6e`, local Windows 3.11 | full | `Ran 572 tests in 175.143s / OK (skipped=4)` | 0 |
| Stage A, hosted Linux (`ci` run 38349126601) | full + focused + wheel | **success**, all steps executed | 0 |
| Stage B, hosted Linux (`ci` run 38349130157) | full | `Ran 572 tests / OK (skipped=6)` | 0 |
| Stage B, hosted Linux | focused | `Ran 108 tests / OK` | 0 |
| Stage A, local Windows 3.11 | full / focused | `Ran 572 / OK (skipped=4)` · `Ran 108 / OK` | 0 / 0 |
| Stage A, local WSL Ubuntu 24.04 / Python 3.12 | full / focused | `Ran 572 / OK (skipped=10)` · `Ran 108 / OK (skipped=1)` | 0 / 0 |
| Stage A, local Linux CLI smoke | 13 scoped verbs | 13/13, `nonzero_exit: 0` | 0 |

Failure accounting: **13 declared failures at the frozen subject — 13 accounted for, 0 unexplained**,
mapped to 7 named root causes with a repair and a paired control each
(`evidence/02_LEDGER/R3_FAILURE_ROOT_CAUSE_MAP.json`).

Paired fault injection (`evidence/03_CI_TEST/ci_fault_injection.txt`), one deliberately failing test
planted:

```
control_old_direct_rc=1    # the suite really was red
control_old_pipeline_rc=0  # what the shipped step shape returned -> 0 = FALSE GREEN, reproduced
control_new_pipeline_rc=1  # what the repaired step shape returns -> non-zero = true red
```

## 6. Independent verification

The mandated CODEX CLI checker lane (`openai-codex / gpt-6.1-sol`, OpenAI OAuth) **could not be
launched on this host**: no `codex` binary exists (`Program Files/OpenAI/Codex` absent, no
`codex*.exe` anywhere on the machine), while HG-KSEOS `config/lane-routing-registry.yaml` records the
VERIFY/SECURITY lane's *default* arm A as `opencode-go / z-ai/glm-5.3-flash` with the codex arm as the
non-default alternate. The verify lane therefore ran on the registry's default arm:
a one-shot, fresh Hermes session with `-m glm-5.3-flash --provider opencode-go`, a different actor and
a different model from the maker lane. The verdict is at
`evidence/10_INDEPENDENT_VERIFY/AO_VERDICT_S4R3.json` and is a **backup-arm verdict, not the
gpt-6.1-sol verdict the order named**.

**Two defects it found in the repair, both now fixed rather than reported as known-issues:**

1. *Residual masking in the wheel step.* The `Build the wheel and exercise it in a clean venv` step
   pipes `pipd doctor` and `pipd --help` through `tee` and carried no `set -euo pipefail`, so a failing
   installed-wheel command was still masked — the same class as F001, in the one step the first repair
   pass missed. Repaired on the Stage A branch; all six pipeline-carrying steps now carry the guard.
2. *Allowlist regex vs `..` segments.* A path shaped `.hgk/rounds/<round>/../evil.sh` classified as
   inside the round's evidence directory while resolving outside it. No live hole (`git diff
   --name-only` never emits `..` for tracked paths), but now refused explicitly and asserted by a plant
   so it cannot rot. Repaired on the Stage B branch; the local reproduction shows both traversal
   plants refused and the scope still clean.

## 7. Changed paths

- **Stage A (candidate `517d7a5`)** — `.github/workflows/ci.yml`, `.github/workflows/public-plugin-verify.yml`,
  `pyproject.toml`, `src/pipd_ls_sp/workspace.py`, `examples/first-run/run.sh` (mode 100644→100755),
  `examples/first-run/run.ps1`, `tools/cli_smoke.py`, `tests/test_web_fallback.py`, plus the round's
  admission script. Evidence commits `8cbe258`, `25f4dfe` add **only** `.hgk/rounds/S4R3-…/` paths —
  asserted, and checkable with
  `git diff --name-only 517d7a5..25f4dfe | grep -v '^\.hgk/rounds/S4R3-'` (empty).
- **Stage B (candidate `8481f29`)**, vs its declared base, exactly 7 paths:
  `.github/workflows/public-plugin-verify.yml`, `README.md`, `docs/USER_GUIDE.md`,
  `docs/install/PIPD_WEB_FALLBACK.md`, `docs/install/PIPD_WEB_FALLBACK.md.sha256`,
  `docs/install/README.md`, `.hgk/rounds/S4R3-…/scripts/writeset_gate_repro.sh`. **Zero core writes**:
  nothing under `src/`, `schemas/`, `skills/` or `dist/`. Evidence commit `d561f52` adds `.hgk/rounds/S4R3-…/`
  paths only.

## 8. Orchestration surfaces actually used

| surface | what exists on disk |
|---|---|
| **KANBAN** | board `s4r3-20261013` (`kanban.db` under `HERMES_HOME/kanban/boards/`); root card `t_1ebae232` done; worker cards `t_becda8d2` (hgk-coding-factory) and `t_a4ec0310` (hgk-qa) completed **with result and summary text**; verifier `t_6383e558`; synthesizer `t_bcae809b`. Readback: `evidence/11_ORCHESTRATION/KANBAN_READBACK.txt`. |
| **SWARM** | the graph was created from the swarm verb — one root → 2 parallel workers → verifier → synthesizer, i.e. exactly the shape above. **Disclosure:** the cards are the coordination record; the writes themselves were performed in the orchestration role and landed as commits and draft PRs. The event-driven Kanban sink was not used as the execution path, so a reader must not infer "the hgk-coding-factory profile wrote this code" from the card's assignee. |
| **GSTACK** | HG-KSEOS remains the only control plane: admission, workorder and acceptance rows are the shared-spine rows of §2; Hermes Kanban is coordination, not authority. |
| **OPENSPEC** | `openspec validate s4post-triple-upgrade` → *"Change 's4post-triple-upgrade' is valid"*, `openspec list` shows 22/25 tasks. Readback: `evidence/11_ORCHESTRATION/OPENSPEC_READBACK.txt`. |

## 9. TT / CR and resume checkpoint

| id | item | owner | next action |
|---|---|---|---|
| `TT-S4R3-001` | `preview.3` published wheel still carries the Trace false-PASS; the source repair is in the candidate only | release owner | rebuild the wheel from the new candidate and re-run the legal/wrong-type/orphan/wrong-hash suite against the installed package |
| `TT-S4R3-002` | human publisher identity, owner-approved brand assets, official vendor validator, portal scan/review/publish | owner + publisher | owner supplies; then a new immutable release (`S4R3-F003` stays open) |
| `TT-S4R3-003` | four-host UAT (Web GPT-6 Plus/Free, Hermes, Codex Desktop, Codex CLI) | host UAT owner | needs the hosts; today `NOT_EXECUTED`/`NOT_VERIFIED` |
| `TT-S4R3-004` | Stage A's `public-plugin-verify` run is red because the Stage A branch carries the *pre-repair* gate | repo owner | resolves by itself when the Stage B change set lands on a base; no action on the Stage A branch |
| `TT-S4R3-005` | the mandated CODEX CLI checker lane is unavailable on this host | operator | provide the codex CLI, or record the default-arm substitution as the standing verify route |
| `TT-S4R3-006` | `.hgk/` evidence mass (~62 MB) | repo owner | archival policy decision; no executor-side deletion |

Resume checkpoint: everything a later round needs is committed on the two branches and identified by
40-hex commit; the only actions deliberately not taken are merge, tag, release and any portal act.

## 10. Strongest defensible claim

> On the frozen base `e71fee6e`, the `ci` job was reported successful while its own log read
> `FAILED (failures=11, skipped=6)`; that false green is repaired, all 13 failures are traced to 7 root
> causes with paired controls, and the repaired suite runs green on hosted Linux for the Stage A
> candidate (`ci` run 38349126601) and for the Stage B candidate (`Ran 572 / OK`, `Ran 108 / OK`, run
> 38349130157). The Stage B write-set gate now measures the change sequence it actually governs and
> its hosted run is green with its classifier self-tested (`WRITE_SET_CLEAN_AGAINST_517d7a5`, run
> 38349130092). The Web route now ships a real, digest-stamped document and the repository has one
> navigation and one user guide, with 41 local links and anchors clean.

**Everything above that line is source-and-build level.** No host was driven, no vendor validator
ran, no portal act occurred, no release was cut, no S4 acceptance was granted, and the independent
verdict in §6 came from the backup arm rather than the named checker.

**END — candidate not merged, not published, not accepted.**
