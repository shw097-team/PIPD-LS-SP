# FAR-PIPD-R10-CREDITGUIDE-004 - two defects found by EXECUTING the operator guide

Owner asked for a consolidated "GitHub App setup + PAT rotation" operating guide. Writing it was not the
finding. **Running every command in it was.** Two defects surfaced that reading the tool never would have.

## Finding 1 (FIXED) - a verification field that could only ever report `false`

`cred_broker.py`'s `dry-run` computed `header_would_be_supplied` by comparing the header it had just built
against a **redaction placeholder written into the source as if it were the scheme word**:

```python
supplied = env["GIT_CONFIG_KEY_0"] in env and env["GIT_CONFIG_VALUE_0"].startswith("Authorization: *** ")
```

The built value is `Authorization: Basic <base64>`, so the comparison **never** matched and the field
returned `false` unconditionally - while the header was in fact built correctly. Established in-process
with a dummy token: the base64 round-trips to `x-access-token:<dummy>`, and only the *check* was wrong.

**Why this matters more than it looks.** A field that always says "yes" is obviously worthless; a field
that always says "no" reads as *rigour* and is equally worthless. This is the same class as the round-5
failure that the cross-model checker caught in prose: **an assertion is not evidence just because it sounds
cautious.** A redaction placeholder had been pasted into executable code and survived because nobody ran it.

Fix: a semantic check on the construction - key ends with `/.extraheader`, value starts with
`Authorization: Basic ` - which cannot drift from a literal.

**Verified after the fix:** `verify_offline.py` -> `PASS_OFFLINE_T5_UNPROVEN` (exit 0); `dry-run` ->
`header_would_be_supplied: true`, `secret_printed: false`; `INSTALL_MANIFEST.json` pin re-computed for the
edited file, **7/7 pins resolve**.

## Finding 2 (DISCLOSED, NOT CHANGED) - the installed tool hardcodes one host's owner path

`cred_preflight.py:34-35`:

```python
os.environ.get("HGK_CRED_FILE",
    r"C:\Projects\Agent_Workspace\API KEY\Fine-grained personal access tokens.txt")
```

This is why `--metadata-only` returned `OK` / `exit 0` on a shell with **no** `HGK_*` variable set, and why
`dry-run` reported `credential_kind: "pat"`, `credential_length: 93` out of the box: the default silently
resolved to the owner's PAT notes file.

Consequences:

- **Benefit**: the tool works on this host with zero setup.
- **Risk**: the control-plane tool is **silently coupled to one machine's file layout**. On any other host
  it fail-closes - safe, but indistinguishable from "broken" to an operator.
- It also means an operator can believe they have configured a source when they have not.

**Adjudication: disclose, do not change.** Altering default credential resolution is a control-plane
behaviour change and would need its own admission; the env var is and remains the sanctioned mechanism.
The correct response is that the guide now states plainly: **always set `HGK_CRED_FILE` explicitly; never
rely on the built-in default.**

## What the guide-verification pass also corrected

The guide had three statements that were wrong on this host and are now measured, not assumed:

| guide said | measured |
|---|---|
| `--metadata-only` returns `FAIL_CLOSED` (exit 2) when unset | returns `OK` (exit 0) - Finding 2 is why; fail-closed only when pointed at a nonexistent path |
| `dry-run` should show `credential_kind="app"` | today it is `"pat"`, length 93 - **expected**, since the three App variables are not yet set |
| `header_would_be_supplied=true` | was `false` - Finding 1 |

## Residual human steps (unchanged, and still not automatable)

GitHub exposes **no API** for App registration, private-key download, installation consent, or PAT
rotation / expiry read. Those four remain browser-only; the guide walks them step by step.

## Honest limits of this FAR

- Finding 1's fix is verified only to the `dry-run` / offline level. **No end-to-end push was performed
  through the broker** in this pass, so "the broker pushes correctly" is **not** established here.
- The broker remains **installed but NOT activated**: `config/` references it zero times
  (`NON_ACTIVATED_OK`).
- Finding 2 is **not fixed** - it is disclosed.
- The guide is a new file outside the pinned install set; nothing was wired.

**Claim ceiling:** `CREDENTIAL_GUIDE_WRITTEN_AND_EXECUTED__ONE_FALSE_FIELD_FIXED_AND_REPINNED__ONE_HOST_COUPLING_DISCLOSED_NOT_CHANGED`.
