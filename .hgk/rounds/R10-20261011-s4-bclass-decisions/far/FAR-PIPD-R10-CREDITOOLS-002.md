# FAR-PIPD-R10-CREDITOOLS-002 — durable home and correct governance route for the credential broker

Round `R10-20261011-s4-bclass-decisions` (`REQ-PIPD-R10-CREDITOOLS-002`, P0, CREDENTIAL-BROKER).
Question: *the R9 credential broker lives in ephemeral agent scratch that is pruned when idle, so it
cannot serve an unattended run. Determine the correct durable home and the correct governance route
for installing it, produce a migration plan and a ready-to-apply candidate, and enumerate exactly the
steps that remain human with the reason each cannot be automated. Any control-plane change it
requires is to be identified as its own admitted round rather than ridden in on a product round. No
secret may appear in any artefact.*

## 1. Facts (measured this round, read-only)

| | |
|---|---|
| Current location | `<scratch>/r9/cred/` — **ephemeral agent scratch**, pruned when idle. This is the entire motivation. |
| Artefacts to move | `cred_broker.py` (8011 B), `cred_preflight.py` (7909 B), `selftest.py` (3838 B), `README.md` (2862 B). |
| What it does (verified from source, not taken on faith) | Mints a GitHub App **installation access token** from an RS256 App JWT signed by shelling to `openssl` (no Python crypto dep); falls back to a fine-grained PAT read from a file. Confines whichever credential it uses to the **git child-process environment** via a URL-scoped `http.https://github.com/.extraheader` (`GIT_CONFIG_KEY_0`/`VALUE_0`) with `GIT_TERMINAL_PROMPT=0`, `GIT_CONFIG_NOSYSTEM=1`, `credential.helper=` reset. Fails **closed** with exit code 2 when no credential is present. |
| Repo target | HG-KSEOS — the sole system governance / normative control plane (AGENTS.md). |
| Non-secret | Both modules are secret-free: the credential is read from an **external** file (`HGK_CRED_FILE`) or minted from an **external** App key (`HGK_APP_KEY`). Nothing in the moved bytes is a secret. |
| Note on the tool-output channel | The agent's `read_file`/`grep` render token-shaped f-strings redacted (e.g. `f"x-access-token:{token..."` and `Authorization: Basic ***`). `od` confirms the **on-disk bytes are intact**. Migration therefore uses a **byte copy** (`cp` + `cmp` + sha256), never reconstruction from displayed text. |

## 2. The governance finding — HG-KSEOS *has* an admission route; the change is a control-plane change

**Finding 1 — this is a control-plane change, not a product-round deliverable.** Editing HG-KSEOS
tooling is a normative control-plane mutation. `FAR-PIPD-R8-DISPATCH-004` §4 fixed this exact
precedent when deciding a dispatcher defect: the correct long-term fix *"edits HG-KSEOS control-plane
tooling. Candidate-only by contract, **needs its own admission, and must not ride along inside a PIPD
round**"* — so option B was *named* rather than executed, to be implemented by "the next round that
owns the tooling". Installing this broker into HG-KSEOS is the same class of change. **R10 therefore
does not install it; R10 records the route and supplies the candidate.**

**Finding 2 — HG-KSEOS does have its own lifecycle projects in the shared spine.** The spine at
`HG-KSEOS/var/shared-spine/hg-kseos.db` (`schema.sql` v3, `projects.product_root` constraint
`= 'HG-KSEOS'`) holds projects for **both** the product and the control plane. Read-only query of the
`projects` / `project_lifecycles` tables returns, among others:

```
HGK-P0                  ACTIVE        (510 requirements; no project_lifecycles row)
HGK-CHU-20261009        EXECUTING     (15 requirements — the control-plane hardening unit)
HGK-PRJ-CLI             PROJECT_CREATED
FAR-LANE-SOD-010-CONVERGE / FAR-LANE-SOD-011-ROUTER-WINDOW / FAR-PLAN-ENFORCEMENT-011 / FAR-LANE-ROUTE-SLOTS-012 / FAR-LANE-HEALTH-REPAIR-013   (control-plane lane rounds)
PIPD-LS-SP-20261008     EXECUTING     (129 requirements — the *product* project this round rides)
```

There is **no single "the HG-KSEOS project id"**; the control plane governs through **several**
lifecycle projects in the one shared spine. The admission mechanism is the typed API, e.g. the R9/R10
admission scripts call `ProjectLifecycleController.admit_requirement(project_id, rid, wording,
owner=…, priority=…)`. **So the control plane has a real admission route for this install.**

**Finding 3 — the minimal admitted change.** `admit_requirement` succeeds only while the target
project is in `EXECUTING / PLAN_READY / WORKORDERS_ADMITTED` (`lifecycle.py:566`). A freshly
`hgk project start`ed project is `PROJECT_CREATED`, which is **not** admissible. Therefore:

- **Route A (minimal, recommended).** Admit **one** requirement `REQ-HGK-CREDBROKER-001` into an
  existing HG-KSEOS control-plane project already in an admissible state — **`HGK-CHU-20261009`**
  (EXECUTING; it already carries the credential obligations `REQ-CHU-R2-04-CREDENTIAL-SCRUB` and
  `REQ-CHU-R2-05-BRIDGE-CONFIG`, and its admission artefact
  `.hgk/checker-upgrade-20261009/admission/admission_late_bound.json` records `project_id:
  HGK-CHU-20261009`). One typed call; it freezes the requirement and auto-creates
  `TS-req-hgk-credbroker-001` + `WO-TS-…` exactly as the R9/R10 admissions did.
- **Route B (own round).** `hgk project start --project-id HGK-CREDBROKER-20261011 --goal …`, advance
  along the main path `PROJECT_CREATED → SOURCE_DISCOVERY → … → PLAN_READY`, then the same single
  `admit_requirement`. Heavier (seven `advance` steps) but gives the install its **own** project id,
  which matches the R8 wording "its own admitted round" most literally.

Both satisfy the rule; **Route A is the minimal admitted change**. The ready-to-run candidate for
either is `admission/hgk_cred_admission.py` (Route A = `--project-id HGK-CHU-20261009`).

**What the install does *not* do:** it does not activate, wire, or enable anything. The requirement's
oracle explicitly forbids any `config/` reference to the installed path (§5 V5). Activation of the
broker into a live lane is a *separate, later* admitted change.

## 3. Recommended home and form

- **Repo:** HG-KSEOS.
- **Home:** `scripts/cred/` — a self-contained subdirectory. Rationale: HG-KSEOS `scripts/` is the
  **operational-run** surface (`hgk-lane-dispatch.py`, `hgk-lane-guard.py`, `start-hgk-*.ps1`), while
  `tools/` is acceptance/harness *library* code invoked by `run_acceptance.py`; the broker is a tool
  that is **run**, and a subdirectory keeps its three modules + manifest as one hash-verifiable unit.
  (`tools/cred/` is an acceptable alternative; the choice is not load-bearing.)
- **Form:** a **standing, non-activated** artefact — files present in git, nothing wired. Mirrors the
  repo's own idiom (`config/project.json` carries `hermes.enabled: false`).
- **Install mode:** byte-preserving copy + `git add` **by the owner** (this task neither copies into
  HG-KSEOS nor runs git there).

## 4. Exact target paths and file contents

Candidate directory (scratch — NOT the target): `<scratch>/r10/cred-candidate/`.

| Candidate file | → target path under `HG-KSEOS/` | sha256 |
|---|---|---|
| `cred_broker.py` | `scripts/cred/cred_broker.py` | `23264973b8612639bfe4e8a76116ff0dc1fa5cee3ee69ed9cfb783e3806b3843` |
| `cred_preflight.py` | `scripts/cred/cred_preflight.py` | `63fa632ffd29645358b9821d1cb30b9e3dbf8b39322ddb9b2be319676c34e5b1` |
| `selftest.py` | `scripts/cred/selftest.py` | `f78be993bbd4e137e8330a6c2f4e032925471323f20f1e38262aae8361eb7196` |
| `verify_offline.py` *(new)* | `scripts/cred/verify_offline.py` | `c15432473ec946c40e8255145561b19a65bfea84bef90564a964237d5b6612ca` |
| `README.md` *(byte-identical to R9)* | `scripts/cred/README.md` | `d235b0dddfa48b4898d270ed864dfa5a14398052160e9d35be124d77b5cebef0` |
| `INSTALL.md` *(new)* | `scripts/cred/INSTALL.md` | `6f0054e8b80cc72a759e4ef562e70bb49a0e6626b9c1b74c41870eb851337b06` |
| `INSTALL_MANIFEST.json` *(new)* | `scripts/cred/INSTALL_MANIFEST.json` | (pins the above; excludes its own digest — self-reference prohibited, AGENTS.md §AO-5) |
| `admission/hgk_cred_admission.py` *(new)* | `.hgk/rounds/HGK-CREDBROKER-20261011/admission/hgk_cred_admission.py` | `e521ae869fc48d56b52a0a94d09d7418dbb078d7b02b533f4788be0cccdbd7ea` |

`cred_broker.py`, `cred_preflight.py`, `selftest.py`, `README.md` are **byte-identical** to the R9
originals (`cmp` clean). `verify_offline.py`, `INSTALL.md`, `INSTALL_MANIFEST.json`,
`admission/hgk_cred_admission.py` are new (network-free verifier; install/governance doc; hash
manifest; control-plane admission candidate). **No file contains a secret.**

## 5. Exact verification commands (install works, and is non-activated)

```bash
# V1 install integrity — every pinned hash matches
python -c "import json,hashlib,pathlib as p;m=json.load(open('scripts/cred/INSTALL_MANIFEST.json'));[print(f['target'], hashlib.sha256((p.Path('.')/f['target']).read_bytes()).hexdigest()==f['sha256']) for f in m['files']]"
#   expect: every line true

# V2 offline security contract (no network, no secret read)
python scripts/cred/verify_offline.py         # expect verdict=PASS_OFFLINE_T5_UNPROVEN, exit 0

# V3 full contract on DUMMY credentials (needs network for T5)
python scripts/cred/selftest.py               # expect 5/5 PASS, exit 0

# V4 fail-closed proof (no credential -> abort before any write)
env HGK_CRED_FILE=/nonexistent python scripts/cred/cred_preflight.py --metadata-only
#   expect verdict=FAIL_CLOSED, exit 2

# V5 NON-ACTIVATION proof — the installed path appears in NO config
git grep -n "scripts/cred" -- config/ scripts/ src/ | grep -v '^scripts/cred/' || echo NON_ACTIVATED_OK
#   expect: NON_ACTIVATED_OK
```

## 6. Residual HUMAN steps — each with WHY it cannot be automated

| # | Human step | Why it cannot be automated (API availability) |
|---|---|---|
| 1 | **Register the GitHub App** | GitHub exposes **no REST/GraphQL endpoint to create an App** — registration is UI-only (`Settings → Developer settings → GitHub Apps → New`). |
| 2 | **Generate and download the App private key (`.pem`)** | The private key is produced **only by GitHub's UI** and returned once; **no API returns it**. |
| 3 | **Install the App on the target repo with `Contents: read & write`** | An **installation is a user consent action**; there is **no API to create your own installation**, and the permission grant is the owner's choice. |
| 4 | **Place the `.pem` on the host outside `.git`; set `HGK_APP_ID`/`HGK_APP_KEY`/`HGK_APP_INSTALLATION_ID`** | File placement is scriptable, but it is **gated by 1–3**, and the agent's binding contract forbids it from reading/writing a secret value or choosing secret-file paths/permissions — that is an owner action. |
| 5 | **Authorize the governance admission (owner signature on the control-plane requirement)** | Admission is a normative control-plane step requiring **Human Authority** (AGENTS.md: no durable free-form mutation; approved drift is a smallest-repair candidate, never an agent self-authorization). Not an API concern — an authority concern. |
| 6 | **Apply the install (copy files into HG-KSEOS, `git add`)** | Deliberately excluded from this task (and from R10): it is a control-plane write. Mechanical once sanctioned, but it must occur **inside the admitted control-plane round**, by the designated writer, not by a product-round agent. |
| 7 | **(Bridge only, until 1–4) Rotate the fine-grained PAT before expiry** | GitHub exposes **no API to read a PAT's own expiry** and **no API to renew/regenerate a PAT** — rotation is a **UI action**. (The org/enterprise "list fine-grained PATs" `token_expires_at` field is callable only by a **GitHub App**, not by the PAT owner about their own token.) The only automatable parts are a recorded expiry date (`HGK_CRED_EXPIRY_FILE`) and a reminder. |
| 8 | **(Only if the owner chooses a deploy key instead)** upload the public half + tick **Allow write access** | Deploy-key upload is a **UI** action (same class as 1–3). |

Everything else — minting, preflight, redaction, git wiring, offline verification — is automated.

## 7. What was ACTUALLY run vs only designed

**Run this round (all local, read-only or dummy-only):**
- Byte copy of the four R9 files → `<scratch>/r10/cred-candidate/`; `cmp` byte-identical; sha256 computed.
- `py_compile` on every candidate `.py` → OK (refutes the tool-output "corruption" and proves intact bytes).
- `cred_preflight.py --metadata-only` with an **absent** file → `verdict=FAIL_CLOSED`, `abort=true`, **exit 2**.
- `cred_preflight.py --metadata-only` with a **dummy** file → `file present, 42 bytes`, `cred_syntax=SKIP` (content **not** read), exit 0.
- `selftest.py` → **5/5 PASS** incl. T5: anonymous `git ls-remote` exit 0, dummy-token exit 128 (header **actually transmitted**), `secret_leaked=false`.
- `verify_offline.py` (new) → `PASS_OFFLINE_T5_UNPROVEN`, exit 0.
- Manifest integrity check → all seven pinned hashes verified `True`.
- Spine **read-only** query (`?mode=ro&immutable=1`): `projects`, `project_lifecycles`, `requirements`.

**Designed only (not run, with reason):**
- The governance admission (`admission/hgk_cred_admission.py`) — it **writes to the canonical spine**, which this task forbids; **syntax-checked only**, never executed.
- `hgk project start` / `advance` for Route B — writes to the spine; not run.
- The install itself (copy into HG-KSEOS) — forbidden this task; the **parent applies it** after review.
- The App **installation-token exchange** (`POST /app/installations/{id}/access_tokens`) — coded, not exercised; needs the owner's real App (steps 1–3).

## 8. Secret handling — confirmation

**No credential VALUE was read, printed, hashed, echoed, or copied.** Proofs: (a) the only
content-reading path used was `--metadata-only`, which by construction reports existence + byte length
and sets `cred_syntax=SKIP` ("content not read"); (b) `selftest.py` / `verify_offline.py` use only the
**dummy** token `github_pat_` + `"A"*30`, and `verify_offline.py` rebinds `cred_preflight.PAT_FILE`
to synthetic paths before any call; (c) no command emitted a token-shaped string; (d) the candidate
files contain no secret (the broker reads the credential from an external file / App key).

## 9. Claim ceiling

`R10_CREDITOOLS_IS_A_MIGRATION_PLAN_WITH_A_VERIFIED_CANDIDATE`. The broker was **not installed, not
activated, and not admitted**; no control-plane or product artefact was written; no remote was
touched. The candidate is the maker's and cannot be accepted by the maker. `HGK-CREDBROKER-001` is a
**proposed** requirement id, not an admitted one. Nothing here grants `G_RELEASE_FULL_PASS`,
`PRODUCTION_VERIFIED`, or any host certification.
