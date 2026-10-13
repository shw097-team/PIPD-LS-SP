# S4R3 handover summary — results, gaps/TT, decisions needed

Round `S4R3-20261013-ci-truthfulness-and-stageb-writeset`. Written for a reader who has the branch
and nothing else. Every number below is checkable from this file's own tree; where it is not, that is
said so.

## 1. What actually ran, and what is verified

| item | value |
|---|---|
| frozen subject | `e71fee6dd3aa73724baec4e8d9cc72127fbe36ed` (tree `2875287352529ee92277d7dc4f37cd12ffc977c7`) |
| Stage A candidate / branch tip | `517d7a5d3f00935e1589908f456dfacea8fd8a74` / `fix/s4r3-stage-a-ci-truthfulness-20261013` |
| Stage B candidate / declared base | `8481f29913159ed91ac6dff5ab3d691ea3614355` / `517d7a5d…` |
| Stage B branch tip | `feat/s4r3-stage-b-distribution-20261013` |
| `main` and tag `v0.1.1-preview.3` | `224591431a…` / `e94cc7f9…` — untouched; no force push, no tag, no release |
| draft PRs | #3 (base `main`) and #4 (base = the Stage A branch, 7 Stage B paths) — both open, draft, unmerged |

**The defect this round was convened for, and its proof.** At the frozen subject the hosted `ci` job
reported `success` while its own log read `Ran 572 / FAILED (failures=11, skipped=6)` and, in the
focused suite, `Ran 108 / FAILED (failures=2)`. `tee` was returning the pipeline's exit status.
Every pipeline-carrying step now carries `set -euo pipefail`, and the repair is proven by its own
effect rather than by a green badge: removing the last residual mask (the wheel step) turned that step
**red** and exposed `S4R3-F006`. All 13 failures are mapped to 7 root causes with a repair and a paired
control each; `13 declared / 13 accounted / 0 unexplained`.

**Independent instances of the frozen subject, all red, all repaired**

| environment | frozen subject | after repair |
|---|---|---|
| hosted Linux, full + focused | 11 + 2 failures under a *green* job | Stage B: `572 OK (skipped=6)`, `108 OK` |
| local Linux (WSL 24.04), full | `Ran 572 / FAILED (failures=4, skipped=10)` | `Ran 572 / OK (skipped=10)` |
| local Windows 3.11, full + focused | `Ran 572 / OK (skipped=4)` | `Ran 572 / OK (skipped=4)`, `108 OK` |

Paired fault injection, one deliberately failing test planted: old step shape → `rc=0` (false green
reproduced), repaired shape → `rc=1`.

**Deliverables that exist as artefacts, not as intentions:** a committed, digest-stamped
`docs/install/PIPD_WEB_FALLBACK.md` plus its `.sha256`; a single navigation block in `README.md` that
no longer competes with the install SSOT; one `docs/USER_GUIDE.md`; 41 local links and anchors clean;
the Stage B write-set gate measuring its declared base with a self-testing classifier, green on the
hosted runner with all 15 steps executed, including the five the pre-repair gate had skipped.

**Governance surfaces:** 7 obligations admitted through the HGK typed API (0 errors); Kanban board
`s4r3-20261013` with root → 2 workers → verifier → synthesizer, every card completed with result and
summary text; `openspec validate s4post-triple-upgrade` → valid, 22/25 tasks.

**Deviations, recorded rather than smoothed over:** the C0–C9 contracts were authored by the actor
that executed the work (and the compiler rejected the first iteration with 49 errors); admission
preceded the commit and the push but not the first uncommitted draft; the swarm cards are a
coordination record, not evidence that the named profile wrote the code; the mandatory CODEX CLI
checker lane is absent from this host, so verification ran on the lane registry's default arm and is
labelled a **backup-arm verdict** (`TEMP_CLOSED`, 10 findings, 6 falsification attempts, 0 overclaims,
10 NOT_VERIFIED); the checker's own late refinement means one earlier committed copy of its verdict was
an intermediate state and was superseded in-tree.

## 2. Gaps and TT — open, with owner

| id | gap | owner | next action | why not closed here |
|---|---|---|---|---|
| `S4R3-F006` | **The wheel ships no schemas payload.** `pipd doctor` from a scratch cwd against a clean install of the built wheel returns `verdict=FAIL`, `resolved schemas surface (mode=NONE)`, exit 1 | packaging owner + PKG07 build owner | decide how the schemas surface is delivered, repair, re-run the wheel step unmasked | needs a packaging design decision; no oracle was relaxed to hide it |
| `S4R3-F003` | human publisher identity, owner-approved brand assets, official vendor validator, portal scan/review/publish | PKG07 build owner + human publisher | supply assets and identity, then a new immutable release | owner-only acts; no executor can stand in |
| `S4R3-HOST` | four-host UAT (Web GPT-6 Plus/Free, Hermes, Codex Desktop, Codex CLI) | host UAT owner | drive each host; capture discovery, effective load, POS/NEG/EDGE/SEC, uninstall | no host was driven; `NOT_EXECUTED` |
| `TT-S4R3-001` | the published `preview.3` wheel still carries the Trace false-PASS; the source repair is candidate-only | release owner | rebuild the wheel from a new candidate and re-run the legal/wrong-type/orphan/wrong-hash suite against the installed package | a release is HOLD |
| `TT-S4R3-004` | Stage A's `public-plugin-verify` is red — the Stage A branch still carries the **pre-repair** gate, which measures `main...HEAD` | repo owner | no action on this branch; resolves when the Stage B change set lands on a base | category mismatch: it is the Stage B gate running against a Stage A change set |
| `TT-S4R3-005` | the mandatory CODEX CLI checker lane is unavailable on this host | operator | install the codex CLI, or accept the default-arm route as standing | environment, not subject |
| `TT-S4R3-006` | `.hgk/` evidence mass ≈62 MB | repo owner | archival policy (`source-in-repo` + append-only evidence archive + digest/locator handoff) | executing an archival policy is not an executor decision |
| process observation | one WSL process printed `EXIT=0` while the log it tailed reads `FAILED (failures=4)`; the log's mtime and the clone's reflog place that log at the frozen subject | — | none required | that process-level line is not cited by any claim; the committed receipt is the log itself plus its attribution note |

**Deliberately not done, by rule:** no merge, no tag, no release, no portal act, no deletion or rewrite
of historical raw receipts, no test deleted/relaxed/skipped to buy green, no second control plane, no
ninth skill.

## 3. Decisions the user has to make

Each item states the options and what it costs; nothing here can be decided by an executor.

1. **How to deliver the schemas surface with the wheel (`S4R3-F006`).**
   (a) ship `schemas/` as package data inside the installed package so `pipd doctor` resolves it from
   the wheel; (b) keep the schemas external and give `doctor` an explicit resolution path plus a typed
   refusal when absent; (c) declare the wheel source-only and drop the installed-wheel claim from the
   product surface. **Recommended: (a)**, because the install SSOT promises an installable wheel, and
   (a) is the only option that makes `pipd doctor` meaningful in exactly the environment the pipeline
   tests. (b) changes the product's contract; (c) contradicts the README.

2. **PR shape for the two change sets.** (a) keep two sequential PRs, each with its own base and
   allowlist, as the order describes; (b) collapse into one integrated PR with a single ratified
   allowlist after `F006` is fixed. **Recommended: (a)**, because the two write sets have genuinely
   different owners and only (a) keeps `UPG-G01` auditable — but note that as stacked, Stage B does not
   inherit later Stage A fixes, which is why Stage B's green does not cover the wheel.

3. **Whether to accept the backup-arm verifier.** Since the CODEX CLI is absent, the only independent
   verdict available is the lane registry's default arm. (a) accept that as the standing verify route
   and say so in the policy; (b) keep verification blocked until a codex CLI exists; (c) verify on a
   third route you name. **Recommended: (a)**, recorded as a deviation, since a blocked verify lane
   buys nothing, while an unlabelled substitute verdict would be a false claim.

4. **`preview.3` and the next release.** (a) after `F006`, cut a new immutable preview (`.4`) from the
   merged candidate and run the process/publishable checks against it; (b) leave the published wheel as
   is and carry the limitation on the README until the portal work is done. **Recommended: (a)**, since
   the published wheel's Trace false-PASS is currently disclosed but not fixed anywhere a user can get.

5. **`.hgk/` evidence mass (~62 MB, 95% of the tree's blob size).** (a) decide the archival policy now
   and migrate future rounds to `source-in-repo` + append-only archive with digest/locator handoff;
   (b) defer to release prep. **Recommended: (a)**, because every further round adds mass under the
   current policy.

6. **Disposition of the draft PRs.** (a) leave #3/#4 as drafts until `F006` and the owner gates close;
   (b) convert to ready-for-review now; (c) close and re-open against a fresh candidate. **Recommended:
   (a)** — `NO_MERGE` is the current verdict and a ready PR would imply otherwise.

7. **Whether you want a portable host-UAT kit** (per-host prompts, raw-capture templates, rollback
   script, typed-NACK cases) prepared so the four-host work can be executed by whoever has the hosts.
   That is the only remaining route to `S4_FULL_PASS`, and it can be prepared without any host.

## 4. Claim ceiling

**`NO_MERGE` · `NO_PUBLIC_RELEASE` · `S4_FULL_PASS = NOT_GRANTED`; round status `PARTIAL`.**

Strongest defensible claim: on the frozen subject the CI job reported success while its own log read
`FAILED (failures=11, skipped=6)`; the masking is repaired on every step and proven by its own effect —
the last repair turned the wheel step red and exposed a real distribution defect; all 13 failures are
traced to 7 root causes with paired controls and run green after repair on hosted Linux, local Linux and
local Windows; the Stage B write-set gate now measures the range it governs and is green with its
classifier self-tested.

Everything above is source-and-build level. No host was driven, no vendor validator ran, no portal act
occurred, no release was cut, no S4 acceptance was granted, and the independent verdict came from the
backup arm. **A green build receipt from this pipeline does not mean the package works — `F006` is why.**
