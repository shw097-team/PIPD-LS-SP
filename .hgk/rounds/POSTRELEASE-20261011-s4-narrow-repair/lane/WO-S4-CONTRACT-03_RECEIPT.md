# WO-S4-CONTRACT-03 receipt — post-release narrow repair (identity type / trace / profile fail-closed)

Round: `POSTRELEASE-20261011-s4-narrow-repair`
Task: `PIPD-LS-SP-S4-POSTRELEASE-NARROW-REPAIR-20261011`
Capabilities served: `CAP_S4POST_IDENTITY_TYPE`, `CAP_S4POST_PROFILE_FAILCLOSED`, `CAP_S4POST_REGRESSION_EXACT_SETS`
Writer: Codex bounded writer (`deepseek-v4.1-flash`)
Interpreter (pinned): `C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe` (Python 3.11.9, jsonschema 4.26.0)
Candidate head at work start: `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7`
Ceiling: `REPAIR_CANDIDATE_ONLY` — **no commit, no push, no tag, no release**.

Admitted write scope actually written:
`schemas/*.schema.json` (identity typing + `PI-PKG.trace`), `src/pipd_ls_sp/profiles.py`,
`src/pipd_ls_sp/pipeline.py`, `tests/test_postrelease_contract_hardening.py` (new), and this
`lane/` output tree. No other file was written. `README.md`, `.hgk/artifacts/**`,
`openspec/changes/**` and `tests/test_postrelease_quickstart.py` carry **pre-existing / other-WO**
changes that this WorkOrder did not touch.

---

## 0. Defects repaired (raw evidence in the brief's reproduction, now closed)

| ID | Defect | Repair |
|----|--------|--------|
| D1 | universal identity fields were `{}` (accept ANY JSON value); `PI-PKG.trace` was `{}` | typed all 19 families' `subject_id`/`version`/`content_hash`/`schema_version`; `PI-PKG.trace` is now `array` of trace-link objects |
| D2 | `compute_profile` counted raw `axes` (4×`intent` escalated) while `profile_record` emitted `sorted(set(axes))` | malformed axis sets fail closed typed; one normalised list is returned *and* emitted, so basis == record |
| D3 | no risk input; `vetoes` hardcoded `[]`; LITE implied a risk pass | `risk_assessment="NOT_ASSESSED"` when no evidence; never `LOW_RISK_VERIFIED`; carried in `_profile_meta` sidecar |

---

## 1. Schema diff — D1

### 1.1 Canonical identity typing applied to every declaring family

All four fields get exactly the brief's spec wherever they are declared:

```json
"subject_id":     {"type": "string", "minLength": 8, "maxLength": 200},
"version":        {"type": "string", "minLength": 1, "maxLength": 64},
"content_hash":   {"type": "string", "pattern": "^[0-9a-f]{64}$"},
"schema_version": {"type": "string", "minLength": 1, "maxLength": 64}
```

19 files, 4 identity fields each; `supersedes` / `invalidates` left untouched (they remain `{}`),
`required` and `additionalProperties` untouched. Verified mechanically:

```
$ grep -c '^diff --git' lane/SCHEMA_DIFF.patch        -> 19
$ grep -c '^-.*(required|additionalProperties)' ...   -> 0 removed
$ set of removed (-) lines (deduped): subject_id/version/content_hash/schema_version/trace
                                       empty-schema lines + one TechnologyAdmission "type":"string"
  (no `required` line and no `additionalProperties` line is removed or added anywhere)
```

Representative diff (`ArtifactIdentity`, the family the brief quotes):

```diff
   "properties": {
-    "subject_id": {},
-    "version": {},
-    "content_hash": {},
-    "schema_version": {},
+    "subject_id":     {"type": "string", "minLength": 8, "maxLength": 200},
+    "version":        {"type": "string", "minLength": 1, "maxLength": 64},
+    "content_hash":   {"type": "string", "pattern": "^[0-9a-f]{64}$"},
+    "schema_version": {"type": "string", "minLength": 1, "maxLength": 64},
     "supersedes": {},
     "invalidates": {}
   }
```

`TechnologyAdmission.schema.json` was the one outlier: it already typed the four fields but only as
`{"type": "string"}`. It was tightened to the canonical spec (still a *narrowing within the same
`type: string`*, so no legal record is newly refused — see §1.4). Its 1-space indent style was
preserved.

### 1.2 `PI-PKG.trace` — inline object constraint (`urn:pipd:s0:TraceLink:1` `$ref` is NOT resolvable)

`trace` was `{}`; it is now:

```json
"trace": {
  "type": "array",
  "items": {
    "type": "object",
    "required": ["from_type","from_id","from_hash","to_type","to_id","to_hash",
                 "rationale","subject_id","version","content_hash","schema_version"]
  }
}
```

The brief offered a choice: a `$ref` to `urn:pipd:s0:TraceLink:1`, or inline, *decided by a probe*.
The probe result (`lane/REF_PROBE.log`) is deterministic:

```
BARE_VALIDATE_FAIL: _WrappedReferencingError Unresolvable: urn:pipd:s0:TraceLink:1
REF_BUILD: OK                      # the schema BUILDS; it fails at validation time
REF_WITH_REGISTRY: OK              # only resolvable if a referencing.Registry is injected
INSTALLED trace type: array
```

`validate._validator` constructs `Draft202012Validator(schema)` with **no** registry, so a bare
`$ref` would raise `Unresolvable` for every PI record (breaking the positive path), not refuse a
bad trace. Therefore the equivalent object constraint is inlined. `trace` stays REQUIRED.

### 1.3 Full schema diff

Raw, unedited: `lane/SCHEMA_DIFF.patch` (15,620 bytes, 19 files).

### 1.4 No legal existing record is newly refused (breaking-change check, brief step 6)

* The identity typing is a **narrowing of the same JSON type** that a valid record already had to
  satisfy semantically (`validate.semantic_invariants` already required an 8+ char id and a 64-hex
  hash — but only *after* coercion; the schema is now the first fail). A record with a legal id /
  version / hash is unaffected.
* The one real risk was `TechnologyAdmission`, whose 4 fields were typed `string` and whose 22 live
  admission records were checked: `subject_id` len 44, `version` 3–60, `content_hash` = 64 hex. All
  pass the tighter spec. No adversarial float is affected because JSON `1.0` is not an integer
  (`type: integer` is not used here) and the identity values are strings.
* `trace` was never a declared *string* anywhere; the only legal shape the compiler emits is an
  array of links (confirmed by the PI positive test). `PD-PKG` / `ECP` / `TQAEP` never declared
  `trace`, so inlining on `PI-PKG` alone does not widen them (§4).

---

## 2. Source diff — D2 / D3

Raw, unedited: `lane/SOURCE_DIFF.patch` (5,249 bytes, `profiles.py` + `pipeline.py`).
`validate.py` was **not** changed (no diff) — see §3.

### 2.1 `profiles.compute_profile` — fail closed, return one normalised list

```python
if axes is None:
    used = ["intent"]
elif not isinstance(axes, (list, tuple)):
    raise ProfileVeto("axes must be a list of canonical axis names, got %s" % type(axes).__name__)
else:
    used = list(axes)
if not used:
    raise ProfileVeto("axes must be a non-empty list (an empty axis set binds no surface)")
nonstr = [a for a in used if not isinstance(a, str)]
if nonstr:
    raise ProfileVeto("axes must be strings; non-string entries %r refused" % nonstr)
unknown = sorted({a for a in used if a not in AXES})
if unknown:
    raise UnsupportedSurface("unknown axes %s" % unknown)   # kept the existing error type
dupes = sorted({a for a in used if used.count(a) > 1})
if dupes:
    raise ProfileVeto("duplicated axis/axes refused (double-counted complexity): %s" % dupes)
normalised = sorted(set(used))
...
if len(normalised) > cfg["max_axes"]:      # supersedes the old `len(used)`
    ...
return {..., "axes": normalised, "risk_assessment": risk_assessment, "vetoes": [], ...}
```

### 2.2 `pipeline.profile_record` — consume exactly the returned list

```diff
     full = compute_profile(profile_name, axes=axes)
-    rec = _rec("ProfileBinding", "PB", {"p": full["profile"], "a": sorted(axes)},
-               profile=full["profile"], axes=sorted(set(axes)), ...)
+    bound_axes = list(full["axes"])
+    rec = _rec("ProfileBinding", "PB", {"p": full["profile"], "a": bound_axes},
+               profile=full["profile"], axes=bound_axes, ...)
```

`pipeline.compile_pi` still calls `profile_record(name, sorted({a.get("axis") or "intent" ...}))`,
which yields a valid unique sorted list — unchanged and still working (positive tests green).

### 2.3 D3 — the risk statement

`compute_profile` adds `"risk_assessment": "NOT_ASSESSED"` (or `"EVIDENCE_SUPPLIED_UNVERIFIED"` if
risk evidence is explicitly passed). It never emits `LOW_RISK_VERIFIED`, and axis count is never
used as a risk score. `vetoes` stays `[]`.

**`ProfileBinding.schema.json` does NOT declare `risk_assessment`** (verified:
`"risk_assessment" in properties -> False`). Per the brief, adding a property to the contract would
be a breaking change, so the marker is carried in the existing non-record `_profile_meta` sidecar
instead of the record. The compiled PI therefore shows:

```
_profile_meta = {"profile":"LITE","requested_profile":"LITE","escalated":false,
                 "escalation_reason":null,"axes":["intent"],
                 "risk_assessment":"NOT_ASSESSED","vetoes":[],
                 "artifact_depth":"L1_SCHEMA_CONTRACT",
                 "assurance":["deterministic_validator"],"canonical_truth":"single"}
```

`_profile_meta` is in `NON_RECORD_SIDECARS`, so it is stripped before the schema check and does not
change the body hash (verified: the PI still validates to `[]` findings).

**TODO answered honestly:** *no veto evidence exists* — there is no per-axis risk-ceiling or veto
input in this runtime; `vetoes` remains `[]` and no veto was manufactured to look complete.

---

## 3. First-fail ordering and pointer (brief step 3)

`validate.validate_bundle` runs `validate_record` (SCHEMA) for a contract **before**
`semantic_invariants` (SEMANTIC), appending SCHEMA findings first — so a wrongly-typed identity/trace
is the first finding, tagged `kind:"SCHEMA"`. Pointer formatting was already adequate and was left
unchanged (`validate.py` has no diff): a type error names the contract and JSON pointer, e.g.
`ArtifactIdentity/subject_id: 12345678 is not of type 'string'`. No pointer improvement was needed.

---

## 4. Named acceptance commands — raw output and exit codes

All run from the repo root with the pinned interpreter; `src` is bootstrapped by each test module.

### A. Focused 3-module run

```
PYTHONPATH=<repo>/src <interpreter> -m unittest tests.test_s0_contracts tests.test_ce_repair_regression tests.test_tqaep_design_positive -v
```

Raw tail (`lane/ACC1_focused3.log`):

```
Ran 27 tests in 3.634s

OK
```

Exit code `0`.

### B. New hardening module

```
PYTHONPATH=<repo>/src <interpreter> -m unittest tests.test_postrelease_contract_hardening -v
```

Raw tail (`lane/ACC2_hardening.log`):

```
Ran 28 tests in 1.273s

OK
```

Exit code `0`. (28 = the D1×9 + PI-trace×6 + undeclared-trace×1 + body-edit×1 + axes×6 +
risk×4 + positive×1 cases.)

### C. Whole-suite discovery

```
PYTHONPATH=<repo>/src <interpreter> -m unittest discover -s tests -t . -v
```

Raw tail (`lane/ACC3_discover.log`):

```
Ran 357 tests in 110.019s

OK (skipped=3)
```

Exit code `0`. Baseline before this WorkOrder was `Ran 329 tests ... OK (skipped=3)`
(`evidence/BASELINE_FULL_SUITE.log`); 329 + 28 new = 357, and the 3 skips are pre-existing/environment
gates, unchanged.

### D. Required negatives — exact first-fail captured

Identity (`lane/NEG_identity.log`, each `kind=SCHEMA`, `contract=ArtifactIdentity`, escape shown raw):

```
subject_id=12345678  -> detail=ArtifactIdentity/subject_id: 12345678 is not of type 'string'
subject_id=null      -> detail=ArtifactIdentity/subject_id: None is not of type 'string'
version=1            -> detail=ArtifactIdentity/version: 1 is not of type 'string'
version=null         -> detail=ArtifactIdentity/version: None is not of type 'string'
content_hash='XYZ'   -> detail=ArtifactIdentity/content_hash: 'XYZ' does not match '^[0-9a-f]{64}$'
content_hash=123     -> detail=ArtifactIdentity/content_hash: 123 is not of type 'string'
```

PI `trace` (`lane/NEG_trace_profile.log`):

```
trace='not-an-array' -> detail=PI-PKG/trace: 'not-an-array' is not of type 'array'
trace=None           -> detail=PI-PKG/trace: None is not of type 'array'
trace={}             -> detail=PI-PKG/trace: {} is not of type 'array'
trace=123            -> detail=PI-PKG/trace: 123 is not of type 'array'
trace=MISSING        -> detail=PI-PKG/: 'trace' is a required property
```

Undeclared `trace` on PD/ECP/TQAEP + body-edit (`lane/NEG_undeclared_body.log`):

```
undeclared trace on PD-PKG -> PD-PKG/: Additional properties are not allowed ('trace' was unexpected)
undeclared trace on ECP    -> ECP/: Additional properties are not allowed ('trace' was unexpected)
undeclared trace on TQAEP  -> TQAEP/: Additional properties are not allowed ('trace' was unexpected)
PD body edit w/o rehash   -> PD-PKG: content_hash does not match the record body (body edited without re-issuing identity)
```

Profile axes (`lane/NEG_trace_profile.log`):

```
["intent","intent"] -> ProfileVeto: duplicated axis/axes refused (double-counted complexity): ['intent']
[1,2]               -> ProfileVeto: axes must be strings; non-string entries [1, 2] refused
[]                  -> ProfileVeto: axes must be a non-empty list (an empty axis set binds no surface)
"intent" (non-list) -> ProfileVeto: axes must be a list of canonical axis names, got str
["nope"]            -> UnsupportedSurface: unknown axes ['nope']
```

Positive: a legal PI/PD/ECP/TQAEP bundle validates (`verdict=PASS`, `checked=4`, `findings=[]`) and
the CE-1/CE-2 regressions pass (command A). Covered by `PositiveBundleTests` + module A.

---

## 5. Exact-set check — 19 families / 8 skills / 13 CLI (unchanged)

| Set | Command | Raw result | Exit |
|-----|---------|-----------|------|
| 19 families | `<interp> tools/registry_reconcile.py --check` (`lane/EXACT_registry.log`) | `registry_reconcile: OK 19/19 families field-exact (registry.json == schemas, single-sourced)` | 0 |
| 8 skills | `<interp> tools/skill_pack_check.py --all` (`lane/EXACT_skills.log`) | `"state":"PASS","discovered":8,"loaded":8,"routed":8,"cases_run":56,"cases_passed":56,"first_failing_invariant":"NONE"` | 0 |
| 13 CLI | `<interp> tools/cli_surface_check.py` (`lane/EXACT_cli.log`) | `"passed":"13/13","exact_set":"PASS","verdict":"PASS"` | 0 |

`schemas/*.schema.json` glob count = `19`; `registry.json` `families` length = `19`.
`tests.test_s0_contracts` (module A) independently asserts the 19-family registry and
`additionalProperties:false`.

---

## 6. D3 confirmations (sidecar, not record)

* `ProfileBinding.schema.json` property set: `risk_assessment` **absent** (`False`).
* Compiled PI: `PI-PKG.stable_semantic_contract.profile_binding` has **no** `risk_assessment` key;
  `PI-PKG._profile_meta.risk_assessment == "NOT_ASSESSED"`.
* `"LOW_RISK_VERIFIED"` does not appear anywhere in a compiled bundle (string scan of
  `json.dumps(bundle)`).

---

## 7. NOT_RUN / out-of-scope items and reasons

| Item | Status | Reason |
|------|--------|--------|
| Commit / push / tag / release | NOT_RUN | Candidate-only terminal state; explicitly forbidden. |
| README quickstart, web mount ZIP, self-bootstrap example, source map, docs | NOT_RUN | Those are sibling WOs (S4-UX-01 already landed; S4-WEB-02 / S4-SELFBOOT-04 / source-map are separate lanes) and outside this WorkOrder's admitted write scope. |
| `$ref` to `urn:pipd:s0:TraceLink:1` | NOT_RUN (chose inline) | Probe proved the bare `$ref` is `Unresolvable` under the pinned harness validator; inlining is behaviorally equivalent and is what the brief authorized. |
| Adding `risk_assessment` to `ProfileBinding.schema.json` | NOT_RUN (would be breaking) | The contract does not declare it; the brief forbids widening. Carried in `_profile_meta` instead. |
| Deprecating `canonical_truth` (pre-existing key in the profile dict) | NOT_RUN | Removing it would be an API break beyond the three defects; the brief says stop rather than silently narrow. Retained. |
| `validate.py` edits | NOT_RUN (not needed) | Ordering was already SCHEMA-before-SEMANTIC and the pointer was already contract+pointer; no minimal improvement was required. |

---

## 8. Verdict

`S4_POSTRELEASE_NARROW_REPAIR_CANDIDATE_DELIVERED` for `CAP_S4POST_IDENTITY_TYPE`,
`CAP_S4POST_PROFILE_FAILCLOSED`, `CAP_S4POST_REGRESSION_EXACT_SETS` at the **candidate** level: the
three defects are closed, every named acceptance command exits 0, the exact sets (19/8/13) are
unchanged, and no failure was observed. Claims do not inherit; this is a maker candidate, not an
independent acceptance, and no publication gate was exercised.
