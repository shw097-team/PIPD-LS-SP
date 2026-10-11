# FAR-PIPD-R9-CREDROT-005 — a credential scheme for long unattended runs that does not rest on the owner's long-lived PAT

Round `R9-20261011-s4-gap-closure` (`REQ-PIPD-R9-CREDROT-005`, P0, CREDENTIAL-BROKER).
Question: *design and implement a HIGH-AUTOMATION, MINIMAL-HUMAN-INTERVENTION credential
scheme for the `shw097-team/PIPD-LS-SP` repo so long unattended agent runs do not depend on a
long-lived owner personal access token; fail closed when no credential is available; never
place a secret in argv/stdout/logs/prompt/evidence/remote URL; and state plainly which
residual step still needs the owner and why it cannot be removed.*

## 1. Facts (measured this round)

| | |
|---|---|
| Target | `https://github.com/shw097-team/PIPD-LS-SP.git` — **public** |
| Read access | **Anonymous.** `git ls-remote <repo>` returns every ref with exit 0 and no credential. Verified this round. |
| Consequence | The credential surface for this repo is **WRITE-ONLY** (push / tag / release). Reads never need a secret. This is the single most important fact and it shrinks the problem. |
| Existing credential | one fine-grained PAT, name `HGK-SWOF-ACCEPTANCE-BRIDGE`, account `shw097`, repo-scoped **admin**. On-disk metadata only: file present, **166 bytes**. Its value was never read. |
| PAT lifespan | configurable, up to 1 year or no expiration; **manual** revocation; **no refresh flow**; GitHub auto-removes a PAT unused for a year. |
| Own-token expiry via API | **none.** GitHub exposes no REST endpoint that reports *this* token's expiry. The org/enterprise "list fine-grained PATs" endpoint (`token_expires_at`) is callable only by a **GitHub App**, not by the PAT owner about their own token. |
| Installation token | `ghs_` prefix, **1-hour** TTL, **automatic** expiry, minted by an RS256 JWT signed with an App private key (`POST /app/installations/{id}/access_tokens`), revocable via `DELETE /installation/token`. |
| `GITHUB_TOKEN` (Actions) | short-lived (**job duration**), automatic expiry; exists only *inside* a workflow run. |
| OIDC id-token | a federated identity for **cloud** providers (AWS/GCP/etc.); it is not a GitHub-to-GitHub write credential. |
| Deploy key | SSH keypair; write access = admin-equivalent on **that one repo**; **no expiry**; upload and "Allow write access" are UI actions; if created via a PAT, deleting the PAT deletes the key (regenerating does not). |
| Host reality | Windows; `openssl 3.5.5` present; **no** `gh`, **no** `jq`, **no** Python `cryptography`/`PyJWT`; `git 2.53`. The run is a **local unattended process**, not a GitHub Actions job. |

## 2. Candidate options

| | Option | Automation / lifespan | Assessment |
|---|---|---|---|
| **A** | **GitHub App + installation access tokens** minted on demand from a stored App private key | Token TTL **1 h, auto-expiring**, minted in-process; **zero human action per run** after a one-time setup | **Recommended.** The short-lived credential is *automatically renewable* with no browser. Residual stored secret = one App private key: repo-scoped (via the installation), rotatable via API, never argv/env-persisted. |
| B | GitHub Actions + `GITHUB_TOKEN` / OIDC | No stored secret | **Inapplicable to this host.** `GITHUB_TOKEN` exists only inside a workflow; OIDC only federates to clouds. The write must originate from the **local** tree, which Actions cannot read. Making it fit means shipping the tree to Actions to be written — a *new* write surface, not fewer secrets. |
| C | Deploy key (write) | **No expiry** | The opposite of the goal. Costs the same one-time UI action as A (upload public half + tick write), and leaves a **permanent** repo-admin-equivalent secret. Its only edge (one-repo blast radius) A already matches with a 1 h secret. |
| D | **Local credential broker + fail-closed preflight** | A *control*, not a source | **Adopted, and orthogonal.** Wraps *any* source: verifies the credential at minute 0 and before each push, and never lets the secret reach argv/env-file/log. It is what makes A safe unattended and what makes the PAT bridge tolerable. |
| E | Fine-grained PAT + expiry preflight + rotation reminder | Long-lived; **UI-only rotation** | **Bridge only.** Smallest to build, retains an account-admin secret that **cannot be renewed by API**. Acceptable strictly until A is set up. |
| F | Machine user / separate automation account SSH key | Long-lived | Adds an account to manage; no lifespan win over C, more to administer. Rejected. |

## 3. Recommendation

**Adopt A wrapped in D.** Use **GitHub App installation access tokens** (1 h TTL), minted
on demand by the **fail-closed local broker** (`cred_broker.py`), which mints a fresh token
immediately before each write. Keep the existing fine-grained PAT **only as a bridge** source
until the one-time App setup is done; the broker already prefers the App when configured and
falls back to the PAT otherwise, so nothing else has to change when the owner completes setup.

Why this is the *smallest* scheme that survives unattended runs:
- Reads are anonymous, so the only thing that must survive is **write** — a much narrower target.
- The App token lives **1 hour** and is regenerated in-process, so "the credential expires" stops
  being an overnight risk: it expires *by design* and is replaced without a human.
- The one long-lived artefact left (the App private key) is **repo-scoped** by its installation,
  **API-rotatable**, and is touched only inside the broker process.

**Honest boundary:** no scheme gives *zero* stored secret on a *local* unattended host. Something
on disk must be able to authenticate. A minimises that something's **scope** (one repo) and
**lifetime of its derived credential** (1 h, auto), and makes the residual key **rotatable**. A
claim of "fully automated, no secret at rest" would be false for this host and is not made.

## 4. Residual steps that still need the human owner — and why each cannot be automated

| # | Human step | Why it cannot be automated |
|---|---|---|
| 1 | **Create the GitHub App** (`Settings → Developer settings → GitHub Apps → New`). | GitHub has **no API to create/register an App**; registration is a UI-only action. |
| 2 | **Generate and download the App private key** (`.pem`). | The private key is produced **only by GitHub's UI**; no endpoint returns it. It is a one-time artefact. |
| 3 | **Install the App on `shw097-team/PIPD-LS-SP`** with `Contents: read & write`. | An **installation is a consent action by a user**; there is no API to create your own installation, and the permissions granted are the owner's choice. |
| 4 | **Place the `.pem` on the host** outside `.git` and set `HGK_APP_ID` / `HGK_APP_KEY` / `HGK_APP_INSTALLATION_ID`. | Local file placement is trivially scriptable, but it is **gated by steps 1–3**, which are human. The three values are non-secret and may live in the broker's environment. |
| 5 | **(Bridge only, until 1–4) Rotate the fine-grained PAT before it expires.** | GitHub exposes **no API to read a PAT's own expiry** and **no API to renew/regenerate a PAT** — rotation is a **UI action**. The only automatable parts are a *recorded expiry date* (`HGK_CRED_EXPIRY_FILE`) and a reminder; the regeneration itself is human. |
| 6 | *(Optional)* set the org/enterprise fine-grained-PAT policy (e.g. allow no-expiry) if the bridge should run long. | Admin **UI** policy action. |
| 7 | *(Only if the owner picks C instead)* upload the deploy-key public half and tick **Allow write access**. | Deploy-key upload is a **UI** action; the keypair itself is generated locally (automatable) but the registration is not. |

Every other link — minting, preflight, redaction, git wiring — is automated in the tooling below.

## 5. Implementation status

**Implemented and verified** (working files under
`…/cache/scratch/r9/cred/`; nothing written elsewhere in the repo):

- `cred_preflight.py` — fail-closed preflight. `--metadata-only` verified against the real file
  (**presence, 166 bytes; content not read**). Syntax + `GET /user` probe path verified with a
  **dummy** token → `401` → `verdict=FAIL_CLOSED`, `abort=true`, **exit 2**. This is the
  minute-0 abort.
- `cred_broker.py` — broker: URL-scoped `http.https://github.com/.extraheader` injected **only**
  into the child env (`GIT_CONFIG_KEY_0`/`VALUE_0`), `GIT_TERMINAL_PROMPT=0`,
  `GIT_CONFIG_NOSYSTEM=1`, `credential.helper=` reset, CLI `-c <extraheader key>` deliberately
  never passed (prior-round silent-unauthenticated-push bug). PAT bridge implemented.
  App JWT (RS256) **implemented and signature-verified** via `openssl` (3-part JWT, `iss`=app_id,
  600 s TTL, `Verified OK`) — no Python crypto dependency.
- `selftest.py` — **5/5 PASS**: fail-closed on absent credential; metadata-only reads no content;
  extraheader is URL-scoped and base64-wrapped with the raw token absent from the value; redaction
  strips token-shaped text; and **the header is actually transmitted over the wire** (dummy-token
  `git ls-remote` is rejected → exit 128 while anonymous is exit 0) with `secret_leaked=false`.

**Designed only** (not executed, with reason):

- The **App installation-token exchange** `POST /app/installations/{id}/access_tokens` is coded but
  not exercised — it needs the owner's real App (steps 1–3). The JWT it depends on is verified.
- The **one-time owner setup** (§4 steps 1–4) is designed, not performed — browser actions.
- **Options B and C** are analysed, not implemented (B is inapplicable; C rejected).
- **No write of any kind** was made against the remote; this round is local-only by instruction.

## 6. Failure mode if the credential silently expires mid-run

- **With the broker (all sources):** preflight runs at **minute 0** and **before every push**. An
  expired/revoked PAT or a revoked App key/installation makes `GET /user` (or the mint) return
  `401` → `cred_api_valid`/mint **FAIL** → the run **aborts before any write**, with a coded reason
  and **no secret in output**. Fail-closed, not fail-open.
- **Expiry between preflight and push:** the push itself returns `401`; the broker sees a non-zero
  exit and reports `FAIL` — it does **not** retry with a stale credential and does **not** fall back
  to an unauthenticated push. Each push is atomic at the ref level, so nothing is half-written.
- **App source specifically:** a 1 h token *may* expire mid-run. Because the broker mints a **fresh
  token immediately before each write** (one cheap API call), a long run either refreshes silently
  or, if the App key/installation was revoked, fails the same closed way.
- **Worst case — the status quo (no preflight):** the failure surfaces only at the first push, after
  the whole long analysis, and a naive setup can **hang on a credential prompt**. The broker sets
  `GIT_TERMINAL_PROMPT=0`, so it never hangs: it returns at minute 0 or at the push, never at minute 90.

## 7. Claim ceiling

`R9_CREDROT_IS_A_DESIGN_WITH_VERIFIED_LOCAL_TOOLING` — the broker and preflight are the maker's, and
the maker cannot accept its own work. The GitHub App is **designed as the target source, not
created**; until the owner completes §4 steps 1–4 the effective source is the existing PAT bridge.
Nothing here grants `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`, `FULL_S0_S4_INDEPENDENT_PASS` or
any host certification, and no remote write was performed.
