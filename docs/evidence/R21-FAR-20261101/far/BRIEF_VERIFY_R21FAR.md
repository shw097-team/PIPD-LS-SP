NONCE: VERIFY-R21FAR-1793528300

Emit that exact nonce on the first line of your answer.

You are the VERIFY lane (VERIFY_SECURITY, fresh context, read-only). You did not write these artefacts and you must not repair them.

## Subject

Read these two files in the current directory (they are small):

- `ResearchSynthesis.md`
- `gaps/GAP_LEDGER.json`

Optionally verify ONE concrete claim against the file it cites, e.g. recompute a sha256 or re-read `sources/WORK_QUEUE_READBACK.json`.

## What to decide

1. Which statements in the synthesis are NOT supported by an artefact that exists here, or overstate what the artefact proves?
2. Which gap rows are misclassified (wrong state, wrong unblock, or a "blocked" item that could be done locally)?
3. Is the "owner key envelope can register a governed test principal for the three SP offices" proposal sound as an engineering path, or does it smuggle in a capability the envelope does not grant? Say why.
4. Anything material that is missing from the gap list.

## Rules

- Do not write files. Do not edit the subject. Report only.
- If you cannot read something, say so — do not guess.
- Your verdict is advisory: it is not an acceptance receipt and it cannot promote anything.

## Report format

```
NONCE: <nonce>
verdict: AGREE | AGREE_WITH_CORRECTIONS | OBJECT
unsupported_claims:
  - <claim> :: <why>
misclassified_gaps:
  - <id> :: <current state> -> <proposed state> :: <why>
envelope_proposal: SOUND | UNSOUND :: <reason>
missing:
  - <item>
notes: <short>
```
