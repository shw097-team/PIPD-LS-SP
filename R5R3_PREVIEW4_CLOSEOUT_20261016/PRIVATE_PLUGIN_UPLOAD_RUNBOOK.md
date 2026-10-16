# Private GPT-Plugin ZIP upload runbook (generalised from the successful R5Y round)

Purpose: make the private-host plugin import a repeatable, evidenced procedure instead of a one-off.
Scope: the ChatGPT "Add plugin / skills" surface used by the R5Y round. Windows host, Chrome, UIA path.

## Preconditions (verify BEFORE showing any window)

1. Candidate file exists locally and its SHA-256 is recorded. Never upload a file whose digest has not been
   compared against the digest of the intended bytes.
2. The candidate is a single-root ZIP whose root carries `plugin.json` and whose member set matches the
   declared contract (for this project: 8 `SKILL.md` files, no `mcp`/`hooks`/`apps` sections).
3. `zipfile.testzip()` returns clean (CRC check) and the archive has no path-escape members.
4. The account/session is the intended one. Record the account surface you observed, not the one you assumed.
5. Consent for this upload is on record. Each upload is one consented action; a dismissed or timed-out
   consent prompt is a REFUSAL, never a retry trigger.

## Procedure

| # | Step | Evidence to capture |
|---|---|---|
| 1 | Resolve the ChatGPT tab in the live browser session | tab id + title observed at action time |
| 2 | Open the Add-plugin/skills menu from the proven path | menu node path (as recorded by the R5Y scan) |
| 3 | Choose the local-file upload branch | branch label observed |
| 4 | Populate the native file dialog with the absolute path (file dialogs take a value, not keystrokes) | pre-upload digest of the staged file |
| 5 | Submit with the explicit commit control | timestamp, account role, plan shown |
| 6 | Read the surface's own outcome text verbatim | success text, or the refusal string exactly as shown |
| 7 | If a listing/call surface exists, invoke the installed skills and record the call result | call result per skill, or the absence of the surface |
| 8 | Record what did NOT happen (no retry, no bypass, no second submit) | the count of attempts you actually made |
| 9 | Write `PRIVATE_PLUGIN_INSTALL.json` with every step above | this runbook's step ids, digests, verbatim strings |

## Outcome classification

- `INSTALLED_AND_CALLABLE` — the surface lists the skills and a call succeeds. Strongest available evidence.
- `ACCEPTED_NOT_CALLABLE` — the package was accepted but no call surface exists to exercise it. Record the
  ceiling: acceptance observed, runtime use unproven.
- `REFUSED` — record the surface's verbatim text. A refusal with no error code leaves the cause open: attach
  the offline discrimination below instead of guessing.
- `NOT_ATTEMPTED_CONSENT_WITHHELD` — a legitimate, reportable outcome. Do not re-attempt in the same turn.

## Discrimination order when a package is REFUSED

Upload in this order and stop at the first success — each step is one consented action:

1. the target package (the one whose import is in question);
2. the last package the host is known to have ACCEPTED (proves whether the account/platform currently
   accepts anything at all);
3. any prepared structural variants (different manifest projection, minimal member set).

Interpretation: (2) refused ⇒ account/platform side, and no manifest edit will help; (2) accepted while
(1) refused ⇒ the difference between the two packages is the cause and must be enumerated member-by-member.

## What this runbook does NOT do

It does not bypass consent, does not retry a refused submit, does not modify the hosting account, and does
not present an upload as an acceptance of anything else in the round.
