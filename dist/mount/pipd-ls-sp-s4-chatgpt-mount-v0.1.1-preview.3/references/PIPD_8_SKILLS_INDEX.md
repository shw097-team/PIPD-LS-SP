# PIPD_8_SKILLS_INDEX — the eight existing skills

> Release identity: **v0.1.1-preview.3** — release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`.
> Derived, read-only content. Each entry is a summary of an existing `skills/pipd-*/SKILL.md`; the
> skill is the authority, this index is a projection.

This pack's `SKILL.md` is a **dispatcher over these eight skills** — it adds none. Each skill below
lists its use case, its inputs/outputs, and the conditions under which it refuses. All eight carry a
`schemas/` (typed input/output) and `tests/cases.yaml` (POS/NEG/EDGE/SEC) in the repository.

---

## 1. `pipd-route-intake`

- **Use case:** capture an unbound goal that carries source locators as a typed **IntentCard** with
  requirement atoms, before any compilation.
- **Inputs:** `goal` (string, non-blank); `sources[].rel` (locators, no `..`, at least one);
  optional `constraints[]`, `non_goals[]`.
- **Outputs:** IntentCard — `subject_id` `INTENT-<16 hex>`, `content_hash` (64 hex), `atoms[]`
  (one per matched axis).
- **Refuses:** blank goal; zero source locators; a locator that traverses out of the admitted root.
- **Hands off to:** `pipd-pi-compile` (never compiles directly from prose).

## 2. `pipd-authority-source`

- **Use case:** freeze source families into a **SourceFreezeManifest** with `AuthorityBinding` records
  before any compiler reads them.
- **Inputs:** `families[].name`; `families[].manifest_sha256` (64 hex); `families[].files[].rel`
  (no `..`, at least one).
- **Outputs:** SourceFreezeManifest + `AuthorityBinding[]` (family 02).
- **Refuses:** a family with no files; a manifest digest that is not 64 hex; a traversing locator.
- **Consumers:** all compilers/adapters.

## 3. `pipd-profile-tailor`

- **Use case:** resolve a requested profile + axis set into an effective **ProfileBinding** through the
  safety veto.
- **Inputs:** `profile` (`LITE|STANDARD|ASSURED`); `axes[]` (the nine canonical axes, unique);
  `provider_off_required` (boolean).
- **Outputs:** ProfileBinding — `profile`, `escalated`, `artifact_depth` (`L1|L3|L4`).
- **Refuses:** unknown profile; duplicate / non-string / empty / unknown axis. **Fails closed** —
  unknown risk is `NOT_ASSESSED`, never low-risk.
- **Consumers:** Skills/JIT/HGK.

## 4. `pipd-pi-compile`

- **Use case:** compile a frozen IntentCard + effective profile into a **PI-PKG** with a stable semantic
  contract and trace links.
- **Inputs:** `intent.subject_id` (`INTENT-<16 hex>`); `profile`; `atoms[]` (req_id + source_clause +
  owner + acceptance_cue + risk_guard).
- **Outputs:** PI-PKG (family 06) — `stable_semantic_contract`, `acceptance.mode` = `bound`,
  `trace[]` (one link per atom).
- **Refuses:** an unfrozen intent; atoms that disagree with the profile.
- **Consumers:** PD binder.

## 5. `pipd-pd-bind`

- **Use case:** late-bind a compiled PI-PKG to a real **RepoContext** into a **PD-PKG**.
- **Inputs:** `pi.subject_id` (`PI-<16 hex>`); `repo_context.root` (must resolve),
  `repo_context.currentness` (`FRESH|STALE`), `repo_context.writable_scope` (no `..`, not `**`).
- **Outputs:** PD-PKG (family 07) — `RepoContext` (root + head + tracked_files), `currentness`
  (recorded, never inferred), `late_bound_construction_binding`.
- **Refuses:** a root that does not resolve; currentness absent; a widened writable scope.
- **Consumers:** execution handoff.

## 6. `pipd-execution-contract`

- **Use case:** turn a bound PD-PKG into a **ConstructionContract** + an **ECP** fixing effect,
  permission, retries, idempotency, readback and rollback.
- **Inputs:** `pd.subject_id` (`PD-<16 hex>`); `pi.subject_id` (`PI-<16 hex>`).
- **Outputs:** ConstructionContract (family 10) + ECP (family 12) — `writable_scope[]` (non-empty, no
  `..`, never `**`), `permission.token_required` = true, `rollback.required` = true.
- **Refuses:** an unbound PD; a writable scope that is `**` or traversing.
- **Consumers:** HGK adapter, TQAEP.

## 7. `pipd-assurance-tqaep`

- **Use case:** assure a PI-PKG + ECP through a **TQAEP** with an independent checker, per-atom oracles
  and positive/negative fixtures.
- **Inputs:** `pi.trace[]` (at least one); `maker`; `checker` (**distinct** from maker);
  `checker_execution_receipt` (never `SELF_ATTESTED`).
- **Outputs:** TQAEP (family 13) — `tests[]` (one per atom), `acceptance[]` = `INDEPENDENT_CASE_PASS`
  with `distinct=true`, `requalification` = `affected-only`.
- **Refuses:** missing trace; checker identical to maker; a self-attested receipt (separation of duties).
- **Consumers:** independent checker/release.

## 8. `pipd-package-project`

- **Use case:** close the artifact bundle into a **ClaimCeiling** with `EvidenceExpectation` records and
  a trace-closure verdict before handoff.
- **Inputs:** `bundle.artifacts[]` (name + subject_id + content_hash); `allowed_claims[]`; `approval`
  (required only at `LOCAL_QUALIFIED+`).
- **Outputs:** ClaimCeiling (family 16) + `EvidenceExpectation[]` + TraceClosureReport —
  `forbidden_escalation[]`, `evidence[]` (`RAW_RECEIPT`, `LOCAL`), `trace_closure.verdict`.
- **Refuses:** an artifact with no identity; a claim above the ceiling; `LOCAL_QUALIFIED+` without an
  approval receipt.
- **Consumers:** all planes.

---

## Source Locators

Bound to `v0.1.1-preview.3` (release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`).

| skill | source locator |
| --- | --- |
| all eight | `skills/pipd-route-intake/`, `skills/pipd-authority-source/`, `skills/pipd-profile-tailor/`, `skills/pipd-pi-compile/`, `skills/pipd-pd-bind/`, `skills/pipd-execution-contract/`, `skills/pipd-assurance-tqaep/`, `skills/pipd-package-project/` |
| per-skill contract | `skills/<name>/references/contract.md` |
| per-skill IO | `skills/<name>/schemas/input.schema.json`, `output.schema.json` |
| per-skill cases | `skills/<name>/tests/cases.yaml` |
| exact-set evidence (8/8 loaded) | `.hgk/rounds/POSTRELEASE-20261011-s4-narrow-repair/lane/EXACT_skills.log` |

Derived content; no normative body copied. No token, credential or PII.
