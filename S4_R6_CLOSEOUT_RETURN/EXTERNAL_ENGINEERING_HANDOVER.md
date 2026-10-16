# PIPD-LS-SP — external engineering handover

Audience: an engineering team that has never seen this repository. Purpose: understand the branch
model, do not break the governed gates, build and test, find where new work goes, know what is
forbidden. Every factual claim below carries a locator: a fenced command a reader can run, or a
`path:line` reference. A number, path, digest or gate outcome without a locator is a defect in this
document; report it. Where a fact could not be verified it is written `ABSENT` with the place looked.

Traditional-Chinese strings inside code fences are governed identifiers (stage names, ticket IDs,
owner-order prose) and are reproduced verbatim, not translated.

## 1. What this repository is, and what state it is in

PIPD-LS-SP is a governed, contract-first toolkit for the **pre-implementation** stage of a project.
It turns a stated intent into a validated chain of machine-readable artefacts — PI → PD →
ConstructionContract → ECP / TQAEP — each bound to one of **19 canonical JSON Schema families**; it
ships **8 skills** and a **13-command CLI** (`pipd`). *(README.md:1-6)*

```bash
python -c "print(open('README.md',encoding='utf-8').read().splitlines()[:6])"
```

The distribution is `pipd-ls-sp`, version `0.1.1a4`, `requires-python = ">=3.11"`, runtime dependency
`jsonschema>=4.0`. *(pyproject.toml:2-6)*

```bash
python -c "print(open('pyproject.toml',encoding='utf-8').read().splitlines()[:8])"
```

State:

- The **published release is `v0.1.1-preview.4` and is immutable** — 7 assets, not re-tagged.
  *(docs/RELEASE_TUPLE.json:59-81; release_and_plugin_scope.json:2-9)*
- `origin/main` is `d3bd5456afbff21a8c8837994a49f57be3e1b97e`; it carries **11 commits after the
  preview.4 tag** that are NOT released. *(see §2 table)*
- The **candidate** for this round adds the closeout product change at commit
  `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba` on pull request **#18**. It is **not merged, not
  released, and not host-qualified**.
- **Claim ceiling.** Nothing in this repository's current state attests `S4_FULL_PASS`,
  `HOST_QUALIFIED`, `PRODUCTION` or public-plugin-directory publication. All four are
  `NOT_GRANTED` / `OUT_OF_SCOPE`. *(owner_closeout_and_tt.md:44-51; release_and_plugin_scope.json:73-81)*

## 2. Branch model

```bash
git -C <repo> rev-parse origin/main \
  origin/fix/s4r6-closeout-doc-identity-and-update-route-20261016 \
  r6-closeout-evidence-20261016
git -C <repo> rev-parse 'origin/fix/s4r6-closeout-doc-identity-and-update-route-20261016^{tree}'
git -C <repo> rev-list --count cc6c1930765160697e7e51d6e37735b9220a30db..origin/main
```

| role | branch / ref | commit (tip) | tree | what it carries |
|---|---|---|---|---|
| product integration line | `origin/main` | `d3bd5456afbff21a8c8837994a49f57be3e1b97e` | — | frozen subjects; 11 unreleased commits after tag |
| product change (the round's candidate) | `origin/fix/s4r6-closeout-doc-identity-and-update-route-20261016` | `127ec1ca97c71d0437f5b149a6e7d540d0cb3bba` | `62eef9d8059d307ae373de63519a37551fa14854` | the reviewer-facing product diff for PR #18 |
| round evidence | `r6-closeout-evidence-20261016` | `0b50d3edc3c31feff6b674d34e2e3e833aaa7687` | — | this round's receipts/packet (outside the product write set) |

**Why two branches and not one.** The product branch is judged by a *governed product write set* that
positively enumerates the paths a product change may touch. A round's own receipts are deliberately
**outside both allowlists** ("an exclusion a reviewer can read beats a permission a reviewer has to
notice"), so the packet is kept on its own evidence branch, byte-identical, and the product branch
keeps the product change only. *(R17_RED_GATE_DIAGNOSIS.md §3; owner decision O-5/§4 in
owner_closeout_and_tt.md)*

**Where a contributor branches from.** Branch from `origin/main` (the integration line); open a pull
request against `main`. Do not branch from the evidence branch — it exists to hold receipts, not to
carry product work. Do not put a round's evidence tree on the product branch: see §3 for the measured
consequence.

## 3. The governed write-set gate

The gate is `.github/workflows/public-plugin-verify.yml`, job `verify`. It does **not** judge the test
suite (that is `ci.yml`, §5); it judges the **write set** — the set of paths a branch changed.

```bash
git -C <repo> show origin/fix/s4r6-closeout-doc-identity-and-update-route-20261016:.github/workflows/public-plugin-verify.yml | grep -n "STAGE:\|STAGE_C_BASE_SHA:\|ALLOWED='\|DENIED='\|EXCLUDED_PREFIXES"
```

**What it measures.** The declared stage's diff against the declared base,
`git diff --name-only "${BASE}...HEAD"`, classified against a positive allowlist. Paths matching
`DENIED` are reported as frozen; paths matching neither `ALLOWED` nor `DENIED` are reported as
`UPGRADE_WROTE_OUTSIDE_ALLOWED_SET`. The gate fails if there is any frozen or out-of-set path.
*(.github/workflows/public-plugin-verify.yml:201-302; R17_check_write_set.py:76-95)*

**Declared stage.** `STAGE: stage-c`; its declared base is the literal frozen S4-R5 commit
`STAGE_C_BASE_SHA: f4021aeff9c016cfb14f17e68a0c570ed4e825c5` (a merged `main` commit, therefore
immutable). `.hgk/` scaffolding is excluded from the governed product set by declaration
(`EXCLUDED_PREFIXES='^\.hgk/'`). *(product-branch workflow:122,129-131; R17_RED_GATE_DIAGNOSIS.md §2)*

**The exact `ALLOWED` regex for the declared stage (after this round's amendment):**

```
^(src/pipd_ls_sp/|schemas/|tests/|fixtures/|pyproject\.toml$|tools/build_dist\.py$|dist/|README\.md$|docs/install/|docs/USER_GUIDE\.md$|docs/RELEASE_TUPLE\.json$|PREVIEW_NOTES_v0\.1\.1-preview\.4\.md$|\.github/workflows/public-plugin-verify\.yml$)
```

Its `DENIED` companion is `^(skills/|packaging/public-plugin/)`. *(product-branch workflow:191-192;
R17_AMENDMENT.diff)*

**Local reproduction and how to read its verdict.** `R17_check_write_set.py` reads the regexes *and*
the declared base out of the workflow file, so it cannot drift from the gate it reproduces:

```bash
python S4_R6_CLOSEOUT_RETURN/R17_check_write_set.py <repo> [<head>]
```

Exit `0` = the write set is inside the declared arm; exit `1` = a violation (same classification the
hosted job prints); exit `2` = the classifier could not be extracted (fails closed, never blesses).
**Caveat:** the script reads the workflow from the working tree, so to judge a *different* branch you
must point it at that branch's own workflow file. The script is a round artifact: it ships in the
evidence branch (this round's packet), NOT on `main` or the product branch — read it out of the packet
before running it. *(R17_check_write_set.py:1-16,41-95; `git show
r6-closeout-evidence-20261016:S4_R6_CLOSEOUT_RETURN/R17_check_write_set.py`)*

**Planted-path self-test.** The arm ships its own falsification controls and runs them in the same
step: `REFUSED_PLANTS` (four paths that must stay refused), `ALLOWED_PLANTS` (paths that must stay
accepted), and two inline traversal probes (`.hgk/rounds/.../../evil.sh` and
`docs/install/../../src/pipd_ls_sp/validate.py`). A pass prints `GATE_SELF_TEST_OK`; any drift prints
`GATE_SELF_TEST_FAILED`. *(product-branch workflow:193-194,265-297)*

**Amendment rule.** The stage arm may be widened by exactly **one named path alternative, not a
prefix**; the arm's own planted-path self-test must be updated **in the same commit** so the boundary
it *proves* still matches the boundary it *declares*; and the amendment must be **disclosed in the
pull request** that needs it. This round's amendment (`AMENDMENT S4-R6-20261016`) adds the single path
`docs/USER_GUIDE.md` and nothing else — the round's evidence directory is explicitly **not** granted.
*(R17_AMENDMENT.diff; R17_RED_GATE_DIAGNOSIS.md §3)*

**Measured consequence of putting round artifacts on the product branch.** Reproducing the gate against
the pre-repair head reports `changed=43` with `UPGRADE_WROTE_OUTSIDE_ALLOWED_SET` for the 21 packet
paths and `docs/USER_GUIDE.md`, ending `RESULT: FAIL (22 outside, 0 frozen)` — the hosted `verify`
goes red while `ci.yml`/`offline-gate` stays green, producing a false all-clear. *(R17_RED_GATE_DIAGNOSIS.md §2)*
The evidence branch itself, measured this session with the unamended stage-c arm, is
`changed=74 ... RESULT: FAIL (48 outside, 0 frozen)` (exit 1) — proof that a round's receipts must not
ride a product branch. *(command: `python R17_check_write_set.py C:/Projects/Agent_Workspace/PIPD-S4R6-wt HEAD`)*

## 4. The lane model

The governed lane pools live in the control plane (`HG-KSEOS`), not in this repository:
`config/lane-route-slots.candidate.json` (revision 10, `status: CANDIDATE`) and the registry
`config/lane-routing-registry.yaml` (epoch 22). Ordered pools, verbatim from the candidate file:

| lane | rank 1 | rank 2 | rank 3 | rank 4+ |
|---|---|---|---|---|
| PLAN | `opencode-go/glm-5.3-flash` (REACHABLE_VARIANCE_HIGH) | `openai-codex/gpt-6.1-sol` (REACHABLE_BY_PRECEDENT) | `opencode-go/deepseek-v4.1-flash` (DISPATCHABLE) | `opencode-go/mimo-v2.6-pro`, `nvidia/z-ai/glm-5.3-flash`, `nvidia/deepseek-ai/deepseek-v4.1-flash` |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` (DISPATCHABLE) | `openai-codex/gpt-6-luna` (REACHABLE_VIA_HUMAN_HOME_TRANSPORT) | `nvidia/deepseek-ai/deepseek-v4.1-flash` (UNREACHABLE_MEASURED_20261011) | — |
| VERIFY_SECURITY | `opencode-go/deepseek-v4.1-flash` (DISPATCHABLE) | `openai-codex/gpt-6.1-sol` (REACHABLE_VIA_HUMAN_HOME_TRANSPORT) | `opencode-go/glm-5.3-flash` (DISPATCHABLE) | `nvidia/deepseek-ai/deepseek-v4.1-flash` (UNREACHABLE_MEASURED_20261011) |

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS && python -c "import json;d=json.load(open('config/lane-route-slots.candidate.json',encoding='utf-8'));[print(l.get('lane'),[(a.get('rank'),a.get('provider'),a.get('model'),a.get('feasibility')) for a in l.get('ordered_pool',[])]) for l in d['lanes']]"
```

**The rank-1 collision, and why an unpinned dispatch silently loses separation of duties.**
`VERIFY_SECURITY` rank 1 is `opencode-go/deepseek-v4.1-flash` — the *same model identity* as
`EXECUTE` rank 1. The pool's own selection rule is
`"no_session_instruction": "rank 1 (默認/首選) is used"`, and it declares
`"sod": "NOT enforced at this revision (owner D1)"`. So a governed round that simply "dispatches the
VERIFY lane" gets a checker that is the same model identity as its maker — **no model-axis separation
of duties** — unless the arm is pinned. *(DEFECT_DOSSIER.md §Question 2; candidate file
`selection_semantics`)*

**How to pin an arm by identity.** Ask for it explicitly, fail-closed, and acknowledge the human-home
transport the rank-2 arm requires:

```bash
python C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py \
  --lane VERIFY_SECURITY \
  --sandbox danger-full-access \
  --allow-sandbox-escalation \
  --guard-subject C:/Projects/Agent_Workspace/PIPD-S4R6-wt \
  --require-arm openai-codex/gpt-6.1-sol \
  --allow-human-home-transport \
  --round <round-id> \
  --prompt "<checker brief>" \
  --json-out var/<round-id>/verify/checker_receipt.json
```

`--require-arm` fails closed (`ERR_LANE_REQUIRED_ARM_ABSENT` / `ERR_REQUIRED_ARM_NOT_SERVED`) rather
than degrading to another arm; `--allow-human-home-transport` is required because the rank-2 arm is
reachable only through the human home (else `ERR_LANE_HOME_NOT_ISOLATED`); `--sandbox danger-full-access`
with `--allow-sandbox-escalation` seats a real-execution sandbox on a lane that defaults to `read-only`
(`SANDBOX_BY_LANE = {"EXECUTE": "danger-full-access", "VERIFY_SECURITY": "read-only", "PLAN": "read-only"}`);
`--guard-subject <frozen copy>` bounds a writer-grade checker, whose read-only subject is enforced by a
frozen copy plus a post-hoc digest comparison rather than by the sandbox.
*(DEFECT_DOSSIER.md §Question 1(d); scripts/hgk-lane-dispatch.py:90-91)*

**The registry is never edited by the round that measures it.** The rank-1 collision is declared policy,
not an unreviewed defect: the registry records it as `sod_invariants.declared_conflicts[SOD006-C3]` with
`status: OWNER_ORDERED_IN_FORCE` under owner order 2026-10-16 (`declared_by`, round
`ROUND3-LANE-REBIND-AND-CLOSURE-20261016`). A measuring round's correct action is to pin the checker by
identity (above); reordering the pool reverses an owner order and is an owner-only control-plane change.
The candidate reorder is documented as `NOT APPLIED`. *(DEFECT_DOSSIER.md §Question 2; registry
`sod_invariants.declared_conflicts`)*

## 5. Build and test

**Full test suite (the command CI runs):**

```bash
cd C:/Projects/Agent_Workspace/PIPD-S4R6-wt && PYTHONDONTWRITEBYTECODE=1 \
  <venv>/Scripts/python.exe -m unittest discover -s tests -t .
```

CI runs the same discovery with `-v` and pipes the raw log, under `set -euo pipefail` so a red suite is
a red job. *(.github/workflows/ci.yml:47-56)*

Measured results (three different environments; do **not** substitute one for another):

| runner | command | result |
|---|---|---|
| repository recon | `python -m unittest discover -s tests -t .` | `Ran 633 tests in 180.325s` — `OK (skipped=4)`, exit 0 |
| round R17 (final head) | same | `Ran 633 tests in 174.073s` — `OK (skipped=4)`, exit 0 |
| independent checker | different interpreter/boundary | 626 tests (not green — see caveat below) |
| R6 report CI | CI boundary | 624 tests, 6 skipped |

*(REPO_RECON.md §3; R17_MEASUREMENTS.json `denominator_warning`)* The 4 skips ride inside the result
and are not erased. Caveat: the independent checker could not certify the whole suite green because two
pre-existing tests write inside the guarded root — `tests/test_tooling_executes.py:52` and
`tests/test_tqaep_design_positive.py:59`; both are unchanged from the base. *(R17_MEASUREMENTS.json
C4; TT-R17-03)*

**Focused commands:**

```bash
python -m unittest tests.test_r6_doc_identity_guard -v
python -m unittest tests.test_s4r2m_docs_route tests.test_r5r3_install_route_identity \
  tests.test_s4ext_release_provenance tests.test_r6_doc_identity_guard
```

Expected: `Ran 9 tests ... OK` for the guard; `Ran 44 tests ... OK` for the affected set.
*(R17_MEASUREMENTS.json orchestrator_measurements)*

**A wheel** is produced two ways. CI route: build one wheel, install it in a fresh venv, change out of
the source tree, run installed `pipd doctor` / `pipd --help`. Offline route: hand-build a PEP 427 wheel.

```bash
python -m build --wheel --outdir "$RUNNER_TEMP/wheels"
python tools/build_dist.py
```

*(.github/workflows/ci.yml:74-84; tools/build_dist.py:2-14,197-216)*

**The public plugin ZIP** is reproducible from a frozen source commit:

```bash
python tools/freeze_public_plugin_source.py --repo-root . --out ledger.json
python tools/build_public_plugin.py --ledger ledger.json \
  --source-commit 062d84ae3e951d02b2ba6bb732359b18799d2864 \
  --packaging-root packaging/public-plugin --out-dir out --generate-icons
```

This reproduces the **historical R5Y build**: 68,355 bytes, sha256
`2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`, 56 entries, 8 `SKILL.md`. The
bytes a user actually installs are the preview.4 asset: **68,357 bytes**, sha256
`545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75`. `--generate-icons` writes packaging
assets, so that option is **not** read-only. A local packager PASS is not portal approval.
*(README.md:64-79; release_and_plugin_scope.json:11-27)*

**Which CI workflow runs on which paths.**

| workflow | trigger | subject |
|---|---|---|
| `ci.yml` (`offline-gate`) | every `push` and `pull_request`, **no path filter** | the test suite, the wheel build/install, the provenance mutation gate |
| `public-plugin-verify.yml` (`verify`) | path-filtered `pull_request` + manual `workflow_dispatch` | the **governed write set** |

The `verify` path filter includes `src/**`, `schemas/**`, `tests/**`, `fixtures/**`, `pyproject.toml`,
`tools/build_dist.py`, `README.md`, `docs/install/**`, `docs/USER_GUIDE.md`, `docs/RELEASE_TUPLE.json`,
`packaging/public-plugin/**`, `dist/mount/**` and the tooling files above — so a source- or
schema-only repair still runs the write-set gate. The filter is a *trigger* condition, **not** the
write allowlist. *(.github/workflows/ci.yml:7-11; .github/workflows/public-plugin-verify.yml:17-40)*

## 6. Module map and extension points

Package: `src/pipd_ls_sp/` (13 tracked files) — `cli.py` (the 13-command `pipd` CLI), `errors.py`
(typed failure codes), `pipeline.py` (PI→PD→ConstructionContract→ECP/TQAEP), `registry.py` (the
canonical 19/19 machine-contract registry), `validate.py`, `projection.py`, `workspace.py`,
`requirements.py`, `profiles.py`, `repo_context.py`, `export_bundle.py`, `util.py`, `__init__.py`.
*(REPO_RECON.md §2)*

- **A new check / test** → `tests/test_*.py` (51 modules; `tests/__init__.py` makes the tree
  importable). Discovery is `python -m unittest discover -s tests -t .`; a new module is picked up with
  no registration step. *(.github/workflows/ci.yml:54-56; REPO_RECON.md §3)*
- **A new tool** → `tools/*.py` (49 files); the module docstring is the house header. *(REPO_RECON.md §4)*
- **A new skill** → `skills/`. The set is an **exact eight**; a ninth is deliberately refused. The real
  contract is enforced by `tools/skill_pack_check.py` (discover → load → route; refuses
  `MARKER_ONLY_PACK`, `MISSING_SCHEMA`, `DUPLICATE_SKILL_NAME`, `UNEXPECTED_ENTRY`) and exercised by
  `tests/test_skill_contracts.py`. *(tools/skill_pack_check.py:2-18; tests/test_skill_contracts.py:9-41;
  REPO_RECON.md §8)*
- **A new schema** → evolve a family **in place** in `schemas/` (tighten `required`/`properties`,
  keep the `urn:pipd:s0:<Contract>:1` `$id` scheme), preserve the exact 19-family set, then regenerate
  the derived registry and check it: `tools/registry_reconcile.py --write` (regenerate) and
  `--check` (fail on drift). A twentieth family or a removed required field is refused.
  *(docs/S0_CONTRACT_SPEC.md:63-91)*
- **A new documentation page** → `docs/*.md` (22 tracked files). *(REPO_RECON.md §1,§6)*

**House style for a new test file.** Every test module bootstraps `src/` onto `sys.path` itself; do not
rely on alphabetical discovery having done it for you. Sibling example:

```python
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
```

*(tests/test_r6_doc_identity_guard.py:33-36; tests/test_skill_contracts.py:11-12)* This is load-bearing:
a test module that omits the bootstrap has failed with `ModuleNotFoundError` under a direct
`python -m unittest tests.<module>` invocation while discovery still "looked green" because a
lexically-earlier module had already mutated `sys.path`. *(docs/ROUND3_DISCLOSURE.md:80)*

`CONTRIBUTING*`, `AGENTS.md`, and any dedicated "add a check/skill" tutorial in `docs/*.md`: **ABSENT**
in the tracked inventory (searched with `git ls-tree -r HEAD --name-only` and a `docs/`+`README.md`
keyword sweep). *(REPO_RECON.md §8)*

## 7. Open tickets, owner gates and prohibitions

**Open tickets** (each one line):

- `TT-R6-DOC-ONEPASS` — two-document minimal erratum + same-ID UPDATE route; candidate delivered this round.
- `TT-R6-PRIVATE-UPDATE-SMOKE` — one human-account UPDATE + 1 POS + 1 missing-source NACK; needs a human account UI.
- `TT-R6-NEXT-PREVIEW-IF-NEEDED` — distribute post-tag `main` capabilities via a NEW tag/wheel/ZIP/SHA256SUMS.
- `TT-R6-HOST-SCOPED-UAT` — per-claimed-host minimal POS/NEG/nontrigger/security raw evidence.
- `TT-R6-HGK-CNV` — PR #14/#15, CNV spec and Model SoD; routed to the external Project Owner.
- `TT-R6-OD-A` — `KP11-R04 / KP12-R04 / KP16-R04` `MUST NOT` normalization-table ambiguity (`ORACLE_DISAGREEMENT`); needs an upstream Oracle ruling.
- `TT-R6-OD-B` — served preview.4 `PIPD_WEB_FALLBACK.md` header still declares `v0.1.1-preview.3`; a frozen asset, correctable only by a future release, never in place.
- `TT-R17-01` — the `VERIFY_SECURITY` pool ranks the writer's model first; owner-ordered (`SOD006-C3 OWNER_ORDERED_IN_FORCE`), needs a new owner order to change.
- `TT-R17-02` — the checker's prior NOT_RUNs were a sandbox capability limit; **closed** this round by an escalated, guard-bounded dispatch.
- `TT-R17-03` — `tests/test_tooling_executes.py:52` and `tests/test_tqaep_design_positive.py:59` write inside the repository, so a no-write checker boundary cannot certify the whole suite green.
- `TT-R17-04` — `UL-01`: the canonical dispatcher still lacks the R10 nonce / per-turn-receipt repairs.

*(owner_closeout_and_tt.md:53-62; SESSION_CLOSEOUT_AND_HANDOVER.md §4)*

**Owner gates** — one action each, and each is **not an agent's to take** because it needs a human
signature, a human account, or an owner-order control-plane change:

| # | single action | why not an agent's |
|---|---|---|
| O-1 | merge PR #18 (or request changes) | merging is the owner's action |
| O-2 | merge PR #17 | merging is the owner's action |
| O-3 | ratify `S4_PREVIEW_MVP_PHASE = TEMP_CLOSED` | requires the owner's real signature; an agent may not self-ratify a stage close |
| O-4 | run the private-host same-id UPDATE smoke | needs a human account with an Update control; not agent-executable |
| O-5 | distribute the 11 post-tag `main` commits via a NEW tag/wheel/ZIP/SHA256SUMS | must never edit `preview.4`; publication is owner-gated |
| O-6 | flip the `VERIFY_SECURITY` pool rank-1 ordering | reverses an owner order; control-plane ordering is owner-only |

*(SESSION_CLOSEOUT_AND_HANDOVER.md §3; owner_closeout_and_tt.md §2)*

**Standing prohibitions** (do not do these):

- Never edit a published release asset (or its tag) in place — `v0.1.1-preview.4` and its 7 assets are immutable. *(owner_closeout_and_tt.md §4; release_and_plugin_scope.json:2-9)*
- No public directory publication: `PUBLIC_PLUGIN_DIRECTORY = OUT_OF_SCOPE` (owner decision, not a defect). *(owner_closeout_and_tt.md:49; release_and_plugin_scope.json:80)*
- No agent self-ratification of a stage close: `OWNER_FINAL_RATIFICATION = PENDING_ACTUAL_SIGNATURE`. *(owner_closeout_and_tt.md:50)*
- No claim of full-pass / host-qualified / production: `S4_FULL_PASS`, `HOST_QUALIFIED`, `PRODUCTION` are all `NOT_GRANTED`. *(release_and_plugin_scope.json:73-79)*

Rollback pointers: delete the candidate branch or the evidence branch only under owner authorization
(the evidence branch is the only home of the packet); reset the worktree with
`git -C C:/Projects/Agent_Workspace/PIPD-S4R6-wt reset --hard d3bd5456afbff21a8c8837994a49f57be3e1b97e`.
*(SESSION_CLOSEOUT_AND_HANDOVER.md §1; owner_closeout_and_tt.md §4)*
