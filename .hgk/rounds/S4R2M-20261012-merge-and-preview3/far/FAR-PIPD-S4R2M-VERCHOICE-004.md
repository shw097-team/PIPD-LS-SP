# FAR-PIPD-S4R2M-VERCHOICE-004 — the distribution version for a future `preview.3`

- **Round:** `S4R2M-20261012-merge-and-preview3`
- **Question type:** adjudication of a decision the governing prompt routes to the owner, prepared so
  the owner decision is a single choice rather than a research task
- **Status:** decision **made and evidenced here**; the *act* of publishing stays owner-gated

## 1. What is actually published today

Measured from the public release list (anonymous read):

```
pipd_ls_sp-0.1.0-py3-none-any.whl        <- both preview.1 and preview.2 use this exact filename
pipd-ls-sp-v0.1.0-preview.1-source.zip
pipd-ls-sp-v0.1.0-preview.2-source.zip
```

So two different sets of bytes were published under the **same distribution version and the same wheel
filename**. Anything built now inherits that ambiguity unless the version moves.

## 2. The ordering question, measured not argued

Run against a real `packaging.version.Version` on this host:

| candidate | relation to the published `0.1.0` |
|---|---|
| `0.1.0a3` | **LESS** |
| `0.1.0b3` | **LESS** |
| `0.1.0rc3` | **LESS** |
| `0.1.0.post1` | GREATER |
| `0.1.1a1` | GREATER |
| `0.1.1a3` | GREATER |
| `0.1.1b3` | GREATER |
| `0.1.1` | GREATER |

An `0.1.0…` pre-release suffix **sorts below** the version already installed, so it could not be
described as a natural upgrade. That closes the option the brief already suspected, with a number
rather than a citation.

## 3. Decision

**Take `0.1.1a3`**, tag `v0.1.1-preview.3`, wheel `pipd_ls_sp-0.1.1a3-py3-none-any.whl`.

Reasoning, in the order that actually decided it:

1. It is strictly greater than `0.1.0`, so `pip install --pre -U` is a real upgrade rather than a
   downgrade dressed as one.
2. The `a3` suffix keeps the artefact honestly labelled a pre-release, which matches the claim ceiling
   this round is allowed to make (`SCOPED_PREVIEW`, not production).
3. It avoids the `0.1.0.post1` trap: a post-release is PEP 440-legal and sorts correctly, but a post
   release is semantically "a re-release of 0.1.0", and these bytes carry changed source and schema.
   Using it would misdescribe the change.
4. It leaves `0.1.1` and `0.1.1b3` available for later previews, so a sequence of betas does not force
   a version-number jump each time.

The version string must become identical in `pyproject.toml`, `tools/build_dist.py`, the wheel
`METADATA`/`dist-info`, the manifest, the README download URL and the tag name; the release gate fails
if any of those disagree.

## 4. What this document does NOT do

It does not bump any version, build any wheel, create any tag, or publish anything. The tree is
untouched. Publishing is inside the standing R5Q grant's *action* but only once the owner selects it —
see `FAR-PIPD-S4R2M-RELGRANT-003.md`, which is where the grant's edge is drawn.

## 5. If the owner selects the release gate

The order is fixed, and each step's output is the next step's precondition:

1. freeze the product commit; assert `main` already carries it;
2. apply the version in all the places in §3; verify they agree;
3. build wheel + mount ZIP from that frozen commit; the ZIP must be generated for the new version, never
   a rename of the preview.2-named candidate;
4. checksum every asset; the manifest lists exactly the assets that will be uploaded;
5. clean-venv install from the built wheel, `pipd doctor` reporting `schema_source=INSTALLED`, 13
   commands, the profile positives and the mutants; upgrade from the pinned `0.1.0`; rollback smoke;
6. only then tag and publish, then read every asset back anonymously and recompute its digest;
7. release notes must disclose `PARTIAL_CHALLENGE`, manual-vs-native web, the `NOT_ASSESSED` risk gap
   and the absent S5 runtime.

Any checksum disagreement at step 4 or 6 is a stop-ship, not a retry.
