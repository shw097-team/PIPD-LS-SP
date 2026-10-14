# Advisory verdict, attempt 11 - the family-IDENTITY bundle (targeted follow-up)

Fifth served run of the mandated lane this round, and the one aimed squarely at the objection it
raised three times. Verbatim below. Ceiling first.

## Ceiling and run facts

- Lane `VERIFY_SECURITY`, served arm **`opencode-go/glm-5.3-flash`** (forced rank, `served_arm ==
  required_arm`), sandbox `read-only`, escalation not authorised, 110.18 s.
  `ok: True`, nonce present `True`.
- Advisory only, never an OracleReceipt, never an acceptance. Overall verdict
  **`PARTIALLY_CONFIRMED`**. `REQ-S4R3X-VERIFY-005` stays open.
- Bundle: 18966 chars, blocks ['FAMILY_IDENTITY_RECEIPT.md (the artefact the lane named)', 'the REAL doctor receipts (attempt 10 supplied a broken log; the checker caught it)', 'what the lane still says it cannot see'] (the family-identity receipt whole,
  the real doctor receipts, and the previous verdict text so the checker could see what it had asked).

## THE OBJECTION IS CLOSED

The lane's own words, from this verdict:

> On the families question, the bundle **does** let us distinguish a correct registry from a silently
> reduced one using the provided wheel-to-tree identity check and per-family names/hashes, though only
> through the trustworthiness of the identity receipt itself.

That is the answer to the objection it raised in attempts 7, 8, 9 and 10 - that "19" was asserted
rather than enumerated, so a silently reduced registry could print 19 and pass. It now has the
enumeration: 19 canonical NAMES in §7.3 order, per-file digests for the INSTALLED wheel against the
tree, and a paired negative in which dropping one family turns the verdict to `FAIL`. It notes the
obvious ceiling honestly - this establishes the identity of one installed wheel surface against one
tree, not that the receipt's own trustworthiness is beyond question.

## The verdict, verbatim

```
C1: PARTIALLY_CONFIRMED - The Family-IDENTITY receipt is head-bound to the current Stage A head, takes the registry from an installed wheel, reports `mode=INSTALLED`, exact family names, per-file hashes and tree-vs-wheel identity, and has a paired negative `FAIL` when a family is removed. But the doctor receipts do not show an explicit exit status or command/invocation binding, and the sdist-to-wheel route is not evidenced in this bundle.

C2: PARTIALLY_CONFIRMED - The lane text says CI invokes a committed verifier with `--expect-families 19` and checkout deny-prefix, and the bundle now supplies a local falsifiable control for family identity, demonstrating a dropped family turns verdict `FAIL`. However, the bundle does not include the CI gate definition, its tool source, the committed negative test, or a negative run of that specific verifier, so the CI-elements of the claim are not established.

C3: INCONCLUSIVE - The write-set gate, declared stage/base handling, allowlist and frozen-path refusal logic are not represented in this bundle beyond earlier lane comments.

C4: INCONCLUSIVE - The Stage A head identity is established within the family receipt, but Stage B re-pin evidence and the two typed error/refusal cases are not included here.

What I could not verify and why:

- I could not fully verify the doctor or sdist routes under C1 because no `doctor` receipt with exit code and no sdist-to-wheel receipt are included.
- I could not fully verify C2 because the received falsifiable negative belongs to the family-identity reporter rather than to the named CI wheel verifier and its own negative case / test trajectory.
- I could not verify C3 or C4 at all because the material for those controls is simply absent from this bundle.
- No label conflict is visible here: everything provided is attributed to the current Stage A head and attached to the same Stage A subject. On the families question, the bundle does let us distinguish a correct registry from a silently reduced one using the provided wheel-to-tree identity check and per-family names/hashes, though only through the trustworthiness of the identity receipt itself. A clean-log artifact proving the doctor exit code and an sdist-to-wheel receipt would establish the unresolved C1 paths.

Residual risks:

- The family identity receipt is a strong positive with a present negative, but it is not a verification-lane receipt.
- The evidence is limited to one installed wheel surface and the current tree, not to doctor or sdist paths.
- Stage B, write-set gating and CI negative behavior remain ungoverned by this bundle.

So overall: the family identity portion is established to the extent the offered receipt can establish it, but the other claims remain open. The bundle is therefore only partially confirming.

VERDICT: PARTIALLY_CONFIRMED
HGK_LANE_NONCE_OK
```

## Executor's reading, stated separately

- **C1 `PARTIALLY_CONFIRMED`**: the family-identity portion is established; what is still missing is a
  `doctor` receipt carrying its own **exit status and command binding** (the checker keeps refusing to
  take a pass on prose), and the sdist-to-wheel route inside the same bundle.
- **C2 `PARTIALLY_CONFIRMED`**: it accepts a local falsifiable control now exists for family identity,
  but the negative belongs to the family-identity reporter rather than to the named CI wheel verifier,
  so the CI element is not established by it. It wants the gate definition, the tool source, and a
  negative run **of that specific verifier**.
- **C3 and C4 remain `INCONCLUSIVE`** because their material is simply absent from this bundle.
- **No label conflict**: everything supplied is attributed to the current Stage A head and to the same
  subject. The attempt-7 false-`REFUTED` failure mode did not recur, which is the head-labelling fix
  holding across a fourth run.
- Its residual-risk list is fair and should be carried forward unchanged: a strong positive with a
  present negative is still not a verification-lane receipt, and the evidence is scoped to one
  installed wheel surface.

## What remains, exactly (the work item for the next bundles)

| claim | missing artefact |
|---|---|
| C1 | a `doctor` receipt with its own exit status and command binding; the sdist-to-wheel receipt, same bundle |
| C2 | the CI gate definition plus the verifier source plus a negative run **of that verifier** |
| C3 | the write-set gate: declared stage/base handling, allowlists, frozen-path refusals |
| C4 | Stage B re-pin evidence and the two typed refusals (manifest name/version vs release bookkeeping; extension namespaces) |

## Binding

- attempt stdout (quoted above): `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-11-20261013T100012Z\attempt-12520-1791885612-3-stdout.txt`
  bytes=3220, sha256=213ab75fc3a39b46e3645172d58cd30e423b2b55a699df08d4672a392cdc331f
- attempt stderr: `C:\Projects\Agent_Workspace\HG-KSEOS\var\S4R3X-20261013-f006-and-stageb-successor\VERIFY_SECURITY\attempt-11-20261013T100012Z\attempt-12520-1791885612-3-stderr.txt` bytes=220, sha256=52343c4c3d5b2322b861483a33cb34902c38c85dfeb33d9227ab579201021511
- lane receipt: `ao_lane_dryaudit/stdout_family_a11.txt`; invocation `ao_lane_dryaudit/invocation_family_a11.json`
- the artefact audited: `evidence/12_GATES/FAMILY_IDENTITY_RECEIPT.md`
- earlier verdicts: `..._A7.md`, `..._A8.md`, `..._A9_A10.md`
