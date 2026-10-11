# MERGE_DECISION_S4R2M — one page

**Round** `S4R2M-20261012-merge-and-preview3` · **Gate** M3 (main integration) · **State**
`MERGE_READY_HITL_PENDING`

## 1. Subject tuple

| identity | value |
|---|---|
| base (pre-change) commit | `3f6c7dc52b73cfcba03dccbe576ade75bec1890d` (tree `de2c8541d22d0ac5046e3cfda5a4368dfced7bd5`) |
| candidate commit | `58a1f334464675081d0573476d70e2165143bdd8` (tree `c9d96316ea7717ab8cb74f0858dd6f05d0ec7db4`) |
| round evidence commit | `E` — recorded in `CANDIDATE_TUPLE.json` after the evidence commit lands |
| frozen checker product (unchanged) | `7c00b64960d86fc1e94848c9955c512a3626a85f` (tree `b08b961061f510d1eb78a944307ecaa446d68eed`) |
| current `main` (local = remote, anonymous and credentialed reads agree) | `4445db5a6d1b3138946fd7c4fe3b712e4faf1af7` (tree `13edaa8ec8775506015310d1c60c977ff5d09e9c`) |
| public release `v0.1.0-preview.2` | `8faa64e581e8c25f5ec355475e29561847da3ead` — immutable |
| `preview.3` | does not exist |

## 2. Merge base and shape

`git merge-base --is-ancestor 4445db5a 3f6c7dc5` → **true**. `main` is an ancestor of the candidate, so
the integration is a **fast-forward**, not a merge commit: no history is created, rewritten or reordered.
Base diff `main...candidate` touches documentation, tests, schemas already accepted on the s4-r2 branch,
and round evidence — see §4.

## 3. Change paths

The candidate is the s4-r2 tip plus one documentation commit. That commit changes only:

```
M README.md
A tests/test_s4r2m_docs_route.py
A openspec/changes/pipd-ls-sp-s4r2m-conditional-merge/**
A .hgk/rounds/S4R2M-20261012-merge-and-preview3/**      (evidence commit, path-disjoint from source)
```

`src/**`, `schemas/**`, `dist/**` are **not** touched by this round.

## 4. What the approval would be for

Advancing `refs/heads/main` on `github.com/shw097-team/PIPD-LS-SP` to the candidate commit by
fast-forward, under the credential broker, with a remote ref readback afterwards — and nothing else.

Explicitly **not** included: any force-push, any tag creation or movement, any release asset change,
any rewrite of `v0.1.0-preview.1` / `.2`.

## 5. Why this needs the owner (and what is already granted)

- Creating a **new immutable tag + prerelease** is already inside the standing R5Q grant
  (`action: create_new_immutable_tag_and_prerelease`). That is the M4 release gate, not M3.
- **Advancing `main` is not named by that grant**, and the round's governing prompt sets
  `human_gate: REQUIRED_FOR_MAIN_INTEGRATION_AND_PUBLIC_RELEASE`. See
  `far/FAR-PIPD-S4R2M-RELGRANT-003.md`. This is a reading the owner settles; the round does not
  self-clear it.

## 6. Readiness evidence (all raw, all in this round's tree)

| item | artefact | result |
|---|---|---|
| native prompt-contract gate | `compiler/S4R2M.*.receipt.json`, `compiler/out/` | `PROMPT_COMPILE_PASS`, 0 errors, all four stages; duplication 0.0166 / 0.0047 |
| HGK typed admission | `admission/S4R2M_ADMISSION_READBACK.json` | 4 requirements / 4 taskspecs / 4 workorders, write-set = candidate worktree, checkpoint taken |
| board + named-method route | `kanban/` | swarm root + 4 workers + verifier + synthesizer; 14 named-method activation invariants all 0 |
| M1 documentation change | `execute/WO-DOC-CAL-01.exec-*.log`, README diff | lane exit 0; orchestrator re-ran the named modules |
| M2 isolated affected regression | `verify/M2_ISOLATED_REGRESSION.json`, `M2_PROFILE_MUTANTS.json` | 9 modules 107 tests OK in a byte-equivalent clone; 19 schemas + registry / 8 skills / 13 CLI; subject unchanged (1341 files, identical digest) |
| independent officer | `verify/VERIFY_RECEIPT_*.json` | see the receipt; recorded as its own claim, never merged into the maker figure |
| credential scope | `evidence/M3_READINESS.json` | broker preflight OK with the live credential; push `--dry-run` exit 0; remote ref unchanged |

## 7. Residuals carried into main if approved

- `S4R2-POST-F03` partially: `main` would carry the repairs, but the **published wheel still does not**.
  Anyone installing from `v0.1.0-preview.2` still gets the old bytes; that gap closes only at M4.
- `S4R2-POST-F04` (version grammar) — deferred with a named trigger.
- `S4R2-POST-F06` (native web skill load) — `NOT_RUN`.
- `S4R2-POST-F07` (12-axis risk engine) — claim bound unchanged; `NOT_ASSESSED` stays honest.
- Verdict ceiling unchanged: `FULL_S0_S4_INDEPENDENT_PASS`, `G_RELEASE_FULL_PASS`,
  `PRODUCTION_VERIFIED`, `S5_RUNTIME_READY`, `WEB_NATIVE_EFFECTIVE_LOAD` all still not granted.

## 8. One owner action, if approved

> Approve fast-forwarding `main` to the candidate commit above.

The round then runs §3's exact command under the broker and reads the ref back. If the owner does not
approve, the round ends here with the candidate preserved and nothing merged.
