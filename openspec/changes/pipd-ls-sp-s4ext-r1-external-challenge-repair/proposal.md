# S4EXT-R1 — external-challenge narrow repair (release provenance, trace closure, first-run portability)

## Why

The external independent challenge `PIPD-LS-SP-S4-EXTERNAL-CHALLENGE-2026-10-12-R1` returned
`FAIL_CHALLENGE` on the release-provenance gate and `NOT_GRANTED` on S4 as a whole, with two
CONFIRMED_DEFECTs and four EVIDENCE_GAPs:

| id | class | what the challenge proved |
|---|---|---|
| **F001** | CONFIRMED_DEFECT, release provenance | all **8/8** published Web-Mount documents named `8faa64e5…` as the `v0.1.1-preview.3` tag commit; the real tag target is `cbf69756…`. The stale value is the `v0.1.0-preview.2` tag, so it is a wrong release identity, not a stale branch tip. |
| **F002** | CONFIRMED_DEFECT, schema level (grade left open) | `TraceLink`'s endpoint properties were `{}` and `PI-PKG.trace.items` required keys without typing them; `validate.validate_bundle()` never called the already-present `pipeline.trace_closure()`, so a tampered trace body could pass. The challenge could not run the published wheel, so the runtime grade was **owed**. |
| **F003** | EVIDENCE_GAP | `tests/test_postrelease_web_mount.py` pins `preview.2`; nothing pinned the *current* release, so the F001 class of defect could escape again. |
| **G004–G006** | EVIDENCE_GAP | no fresh full runtime on the frozen subject, no four-host consumer proof, no independent recomputation of the published bytes. |
| **O007–O009** | observations | quickstart still used the author's absolute paths; SemVer enforcement and a 12-axis risk engine were both rejected as over-engineering. |

This change is the **minimum** that closes the two defects and the test-gap, without touching the
published tag or any release asset, without a 20th schema family, a 9th skill or a 14th CLI verb.

## What changes

1. **Release identity is a frozen tuple, not a sentence** — `docs/RELEASE_TUPLE.json` separates
   `build_source_commit` from `release_tag_target`, and the 8 pack documents are re-generated from it.
   The published ZIP is **not** rewritten (its digest is unchanged and recorded); the correction ships
   as a new `…-erratum1.zip` plus `docs/ERRATUM_2026-10-12_preview3_release_provenance.md`.
2. **Trace endpoints are typed, and closure is part of validation** — `TraceLink.schema.json` gains
   typed, non-blank, 64-hex endpoint constraints; `PI-PKG.trace.items` carries the **inlined
   equivalent** (no remote `$ref`, so the resolver cannot drift); `validate_bundle()` runs
   `pipeline.trace_closure()` and reports `FULL`/`SCHEMA_ONLY`/`FAILED`, so a partial bundle states
   what it is instead of implying a closed chain.
3. **The current release is pinned by a test** — `tests/test_s4ext_release_provenance.py` re-derives
   the identity from the frozen tuple (never a floating branch) and refuses the stale value; the
   historical `preview.2` regression is kept.
4. **The first-run path is portable** — `examples/first-run/run.sh` / `run.ps1` derive every path from
   their own location, check preconditions, fail closed with `PRECONDITION_FAIL`, and execute
   doctor → intake → compile-pi → bind-pd → compile-ecp → compile-tqaep → assemble → validate plus a
   typed refusal. No author path, no exported `PYTHONPATH` required.
5. **Profile boundaries are covered** — `tests/test_s4ext_profile_boundaries.py` covers the 3/4 and
   6/7 axis thresholds, provider-off + complexity interaction, input immutability, no-auto-approval and
   a **non-string `requested` typed refusal**, which replaces the bare `AttributeError` the report
   predicted.
6. **The 57-row crosswalk is adjudicated without rewriting it** — `tools/build_s4_spec_del_adjudication.py`
   emits `docs/S4_SPEC_DEL_ADJUDICATION.json`: one disposition per non-`EVIDENCED` row, no status
   upgrade, `DEL-008` explicitly not S4-blocking, the 4 `DESIGN_ONLY` rows explicitly not implemented.

## Impact / claim ceiling

* `validate --bundle` on a tampered trace bundle: **exit 0 → exit 1 with CLOSURE findings**.
* Released wheel `pipd_ls_sp-0.1.1a3`: **byte-identical** to the published asset digest (unchanged).
* Claim ceiling stays **MAKER_CANDIDATE_AND_LOCAL_TESTS_ONLY_UNTIL_EXTERNAL_REQUALIFICATION**;
  S4 remains `NOT_GRANTED`, the release gate stays `HOLD`, production is not claimed.
* Known limits: the four-host UAT is recorded as `NOT_RUN` for the three chat/agent hosts, the
  published bytes were not re-downloaded from GitHub in this session, and no independent checker has
  yet requalified the candidate.
