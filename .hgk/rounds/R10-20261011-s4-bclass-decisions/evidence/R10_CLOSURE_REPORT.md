# R10 closure — owner-decision adjudication and the control-plane credential install

Round `R10-20261011-s4-bclass-decisions`. Six obligations admitted FROZEN, 0 errors.

## 1. What the round was actually asked

Two things had been parked on the owner. Both were authorised for adjudication *and* execution:

1. Three active SPEC/DEL crosswalk rows whose required SSOT objects do not exist.
2. The R9 credential broker, which lived in ephemeral scratch and so could not serve the unattended
   runs it was built for.

## 2. Row adjudication — three rows, three different outcomes

| row | verdict | outcome |
|---|---|---|
| `PIPD-SP-SPEC-002` | **NOT-OWED-HERE-EXTERNAL** | **Refused.** `PIPD-LIFECYCLE-SPEC@1.1.0` is the external normative standard this repo *implements* (`NC-02`; located outside the repo, sha256 `6f6aafec…`). A copy here would be the "competing lifecycle SSOT" the row itself forbids. |
| `DEL-015` | **OWED-BUILDABLE-FAITHFULLY** | **Built.** `.hgk/artifacts/s3/ADAPTER_REGISTRY.json`, generated from `ADAPTER_MAPPING`. Restoration, not invention. |
| `PIPD-SP-SPEC-030` | **BUILDABLE, NEGATIVE FORM ONLY** | **Built, flagged provisional.** `.hgk/artifacts/s2/MCP_MATERIALIZATION_DECISION.json`, `materialized: false`, `canonical: false`, `ratification_required: true`. |

The material point is not that two objects appeared — it is that **one did not**, on purpose. Authoring
a lifecycle-spec copy would have moved a counter while breaking a prohibition. `EXISTS != TRUE`.

**Correction carried forward:** `.hgk/artifacts/s3/HOST_PROJECTIONS.json` is a gate **check receipt**
(`PIPD-HOST-PROJECTIONS-CHECK/1`), not a registry. Pointing the row at it would have been a mis-citation.
The registry-shaped source is `ADAPTER_MAPPING` in `src/pipd_ls_sp/projection.py`.

**Faithfulness is machine-checked, not asserted:** the source identity `ae939d9795…` is recomputed with
the **project's own** `canonical_json`/`sha256_text` by `tools/build_bclass_artifacts.py --check`, and was
independently re-derived by the checker. `DEL-018` remained at **0 violations**.

## 3. Credential broker — installed as control plane, not smuggled in as product

- Admitted as **`REQ-HGK-CREDBROKER-001`** (FROZEN) into control-plane project `HGK-CHU-20261009`, via
  the typed `SharedSpine` / `ProjectLifecycleController` API — no raw SQL. Route A.
- Installed at **`HG-KSEOS/scripts/cred/`** by **byte-preserving copy** (`cp -p`), NOT reconstruction.
  All **7 pinned sha256 verify**; **0 references** to it from `config/` or `scripts/*.py|*.ps1`, so it
  is **standing and non-activated**.
- Rationale for the separate round: `FAR-PIPD-R8-DISPATCH-004` §4 — control-plane edits must not ride
  along inside a product round. This round therefore supplied the candidate and the plan only.

**A defect found by independent verification, and fixed:** the checker returned FAIL on exactly one
item — `INSTALL_MANIFEST.json` pinned a target that **did not exist** (a Route-B admission-script path
for a round never created). The artefact was wrong, not the checker. The script that actually performed
the admission is now installed and pinned (`scripts/cred/admission/`), and **7/7 pins resolve**.

**A second defect, self-found:** git's `LF→CRLF` would have changed every pinned byte on a fresh clone.
`.gitattributes` (`* -text`) now makes the install reproducible rather than reproducible-only-here.

## 4. Independent verification (CODEX CLI / VERIFY_SECURITY, cross-model)

Receipt: `required_arm == served_arm == openai-codex/gpt-6.1-sol`, `used_rank 4`, `mode forced_rank`;
relay usage `openai-p6a1fe3` / `gpt-6.1-sol` / status `200` / effort `medium`; subject **`mutated=False`**
(3979 → 3979, identical digest), so the tree was genuinely frozen.

**Verdict: `FAIL`** — on **one** of twelve items (check 10, the dangling pin above). Items 1–9, 11 and
the read-only guard PASSED, including: tag identities exact, the registry's fields and counts, the
source hash re-derived, the MCP record's negativity, the *absence* of a lifecycle-spec object, generator
idempotence, `DEL-018`, the 7 install pins minus the dangling one, and the non-activation search.

This is the round's third verification lesson, and it is worth stating plainly: **the first two R9 FAILs
were harness artefacts of mine; this one was a genuine artefact defect.** A checker that only ever
disagrees for harness reasons would be useless, and a maker who assumes every FAIL is the harness's
fault would be worse.

The `could_not_verify` list is carried **verbatim** in
`verify-codex/INDEPENDENT_ACCEPTANCE_R10_CROSSMODEL.md`, including the two items that cut against this
round's own claims: that the receipt's no-secret assertion was **not** independently established, and
that the broader acceptance table was only **PARTIAL** on the evidence checked.

## 5. Every open item, classified by WHO can close it

**This round could have closed and did not:**

- **A re-verification of the fixed control-plane pin.** The fix is applied; a fresh cross-model run has
  not been recorded against the frozen post-fix commit. *(Owed by this line of work, not blocked.)*

**Owner only:**

- **Ratify the MCP record's shape** (`PIPD-MCP-MATERIALIZATION-DECISION/1` is provisional; no PIPD
  schema exists). If the owner reads "materialization object" as one proving MCP **is** materialized,
  that row degrades to `NEEDS-OWNER-DESIGN-DECISION` and cannot be honestly satisfied.
- **Decide the crosswalk rows' reclassification.** Two rows now have truthful evidence and one is
  refused as external. The crosswalk was **deliberately not edited**; reclassification is a recorded
  owner decision, not an authoring side effect.
- **The GitHub App setup** (4 browser-only steps; GitHub exposes no API to register an App, download
  its key, or create an installation). Until then the PAT bridge is in use and is *alive*.
- **PAT rotation** — UI-only; GitHub exposes no API to read a PAT's own expiry or renew it.

**External only:**

- `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`, `PRODUCTION_VERIFIED`; release signing /
  builder attestation (no signing identity on this host); `DEL-004`'s `SPEC_REGISTRY`, which lives in
  the external blueprint. The cross-model verdict above is **same control plane, same host** — it is
  not external acceptance.

## 6. Side effects, disclosed

- **PIPD** `main` advanced by fast-forward pushes; **both release tags unmoved** (`8faa64e…`,
  `cc9bf574…`); no force-push.
- **HG-KSEOS**: four commits, all touching **only `scripts/cred/`** (provable via `git show --stat`).
  That repo already carried ~200 pre-existing untracked entries and 9 modified tracked files, which were
  **not** swept in. **One disclosure I cannot fully close:** a directory under `HG-KSEOS/evidence/`
  carries a recent mtime I could not attribute to a specific writer. I record it as **unattributed**
  rather than claim the repo is otherwise untouched.
- **Canonical store**: the typed admission wrote to the HG-KSEOS shared spine (`var/`, gitignored).
  That is the admission's intended effect, not an incidental one.
- **No credential value** was read, printed, or written at any point; the push path confines the secret
  to a git child process's environment.
- The verification run passed `--allow-human-home-transport`, which the receipt records
  (`human_home_transport_acknowledged: true`). It is the dispatcher's own explicit acknowledgement
  flag, not a bypass — the gate had refused the run fail-closed without it.

**Claim ceiling:** `R10_LOCALLY_VERIFIED__CONTROL_PLANE_INSTALL_ADMITTED_AND_NON_ACTIVATED__CROSS_MODEL_RE_VERIFICATION_OWED`.
The maker did not sign this. `PARTIAL_CHALLENGE` stands, now specific: four named rows blocked on named
missing objects, of which one is refused as external and two now carry truthful evidence.

## 9. Re-verification (run 3) - and a SECOND dangling target, found by being re-run

The re-verification was run against the frozen post-fix commit. Receipt again clean: `required_arm == served_arm == openai-codex/gpt-6.1-sol`, `used_rank 4`, relay `openai-p6a1fe3` / `200` / `medium`, and `mutated=False` (3990 -> 3990, identical digest).

**Verdict: FAIL again** - and again the checker was right. Check 10 failed for a genuinely different reason: the manifest carried a **second** target `control_plane_admission_file.target` pointing at the same never-created Route-B round. I had repointed only the first field. A single fix to a class of defect is not a fix to the class.

Fixed in HG-KSEOS `d642525`: **every path-valued target in the manifest now resolves (zero dangling)**. The pin `e521ae86...` was already correct - only the path was wrong.

Check 12 also failed on this run, where it had been PARTIAL. The receipt acceptance table is the weak point: it states things this line of work asserts rather than things a checker can establish.

Run 3 new fact worth recording: a supplemental HG-KSEOS full-tree snapshot could not complete because `var/far-lane-sod-003/evidence/relay-supervisor.cooldown.json.lock` **denied read access**, so no full-tree HG-KSEOS integrity result is claimed in either direction.

Status: **re-verification still owed.** Two rounds of FAIL have now each surfaced a real defect in the control-plane artefact, which is exactly the value of a checker that does not agree by default.

## 10. Convergence: run 4 = PASS (12/12)

Both dangling targets repaired and the receipt table graded by evidence class; re-verified on the frozen commit with a clean receipt (`served_arm == required_arm == openai-codex/gpt-6.1-sol`, relay `openai-p6a1fe3`/`200`/`medium`, `mutated=False` 3999 -> 3999).

Verdict PASS on all twelve items, with eight could-not-verify limits carried verbatim in the acceptance file. Check 12 passed as a DISCLOSURE-ACCURACY finding, not as proof that an outside party re-ran the verifiers.

The convergence path is itself the finding: FAIL(1/12) -> fix -> FAIL(2/12, a SECOND dangling target found only by re-running) -> fix the class and grade the receipt -> PASS(12/12). The middle FAIL is the one that mattered: a re-run with no change would have missed it, and a fix with no re-run would have shipped it.

**Claim ceiling (converged):** `R10_LOCALLY_VERIFIED__CONTROL_PLANE_INSTALL_ADMITTED_AND_NON_ACTIVATED__CROSS_MODEL_RE_VERIFIED_PASS`. Cross-model means a different model family on the SAME control plane and the SAME host - not external acceptance. The maker did not sign this.
