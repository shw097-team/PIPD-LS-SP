# Bounded writer brief v2 — FAR adjudication implementation (supersedes v1)

You are a **bounded writer**. You may modify ONLY the files listed under "Allowed write set". Anything
else — `skills/**`, `src/**`, `schemas/**`, `dist/**`, `.hgk/artifacts/**`, any release asset, any
other test — is forbidden. If a change outside the set looks necessary, stop and report instead.

**v2 exists because v1's spec was wrong.** v1 said "classify each mismatch against the bases and fail
only on the first unexplained one". An independent measurement pass showed that this alone turns the
tool into a **rubber stamp**: most mismatches *do* match some non-disk basis (the bytes of the sealed
candidate revision), and accepting that basis without a content check would silently pass real
post-seal content edits. The gate below is the corrected one. Do not regress it.

## The gate you must implement (exact)

For each manifest entry with path `p`, recorded digest `r`, and on-disk bytes `d`:

```
normalize_eol(b)  = b.replace(b"\r\n", b"\n")                      # CRLF -> LF
basis_set(p)      = { d,
                      crlf(d), lf(d),
                      blob(p)@HEAD, crlf(blob@HEAD), lf(blob@HEAD),
                      blob(p)@sealed_candidate, crlf(...), lf(...) }
```

- **MATCH_RAW** — `sha256(d) == r`.
- **BENIGN_EOL** — some basis `x` has `sha256(x) == r` **and** `normalize_eol(x) == normalize_eol(d)`.
  Pure checkout/line-ending normalisation: never a failure.
- **UNEXPLAINED_DRIFT** — otherwise. In particular: the path is missing; no basis hashes to `r`; or
  some basis hashes to `r` but `normalize_eol(x) != normalize_eol(d)` — i.e. the content genuinely
  changed after the digest was taken.

The **content-equality clause is mandatory**: accepting `blob@candidate` or `crlf(x)` on a hash match
alone is exactly the false-pass this round exists to prevent. The sealed candidate commit and tree
must be read from the sibling seal when one exists; never hard-code a candidate.

## What you must measure and report (do not trust these numbers, verify them)

An independent pass measured, on this checkout: 1085 entries, 1038 matching the raw disk bytes, 47
mismatching, of which 42 are content drift after EOL normalisation and 5 are EOL-only. **If your
implementation disagrees, report your numbers and your basis breakdown instead of adjusting the code
to hit theirs** — and say plainly which of the two disagrees. The acceptance property that matters is
not the count but this: `--strict` must exit non-zero on this tree whenever the unexplained set is
non-empty, and a rubber stamp that reports zero unexplained here is a FAIL of this task.

## Allowed write set

- `tools/verify_evidence_digests.py` (modify)
- `tests/test_verify_evidence_digests_basis.py` (new)
- `tools/model_eligibility_probe.py` (new)
- `tests/test_model_eligibility_probe.py` (new)
- `docs/FAR_S4POST_ADJUDICATION_2026-10-12.md` (new)

## Requirements

1. `--json` prints exactly `{"checked":N,"match_raw":M,"benign_eol":B,"unexplained":K,"basis_counts":{...}}`.
   Default run: human report, **exit 0**. `--strict`: exit non-zero **iff** `unexplained > 0`.
   Existing flags and the output the current tests read must keep working; `python -m unittest
   tests.test_tooling_executes` and every existing test naming this tool must still pass unchanged.
2. **Ancestry stays report-only** (a prior adjudication rejected making it fatal as a no-op/downgrade).
   Add a test that feeds a non-ancestor candidate head and asserts exit 0 without `--strict` while the
   report still names the non-ancestor value.
3. **`tools/model_eligibility_probe.py`** — two-turn tool-call probe against an OpenAI-compatible
   endpoint (`--base-url`, `--model`), writing a receipt with `declared_model`, `observed_model`,
   `turn1`, `turn2`, `eligible`, `typed_reason`. Exit 0 when both turns pass, 3 with a typed reason for
   the `reasoning_content` second-turn failure class, 2 for transport errors. Never print or store a
   credential.
4. **`tests/test_model_eligibility_probe.py`** — stdlib-only in-process stub server (`http.server`);
   cases: both turns healthy → exit 0, `eligible: true`; second turn HTTP 400 with a `reasoning_content`
   body → exit 3 and the typed reason recorded; connection refused → exit 2. No real network, no sleep
   above 1s, whole module under 20s.
5. **`docs/FAR_S4POST_ADJUDICATION_2026-10-12.md`** — record the four adjudication items and, for each,
   implemented / deliberately not implemented (why) / deferred, including that the ancestry change was
   rejected as a no-op and the in-repo adapter patch was rejected. End with the claim ceiling: candidate
   plus local tests only; no acceptance, release or adaptor-side evidence claimed.

## Rules

- Change no existing test's expectations; if one fails, fix your code, not the test.
- stdlib only, no new dependencies, no network beyond `127.0.0.1`.
- No git history changes, no commit, no push, no tags.
- Finish by running and pasting the raw summary lines of `python -m unittest discover -s tests -t .`
  and `python -m unittest tests.test_verify_evidence_digests_basis tests.test_model_eligibility_probe tests.test_tooling_executes`,
  plus the exact `--json` output and the `--strict` exit code you measured on this tree.
