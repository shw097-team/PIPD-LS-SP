# Tasks

> Status legend: `[x]` = executed **and re-run by the orchestrator against the frozen tree**, not merely
> claimed by the writer lane. `[~]` = executed as far as this host allows, with the residue named.
> `[ ]` = not executed.

## WS-A — release identity and install route

- [x] Re-derive the live subject: `origin/main` = `dba4b194…`, `v0.1.1-preview.4` tag object
      `0618d73c…` → target `cc6c1930…`, tree `7d277a0a…` (git, no network).
- [x] Download all seven served release assets and recompute sha256; reconcile against the release's
      own `SHA256SUMS` (6/6 match) and the GitHub API digest/size fields (7/7 match).
- [x] Record the divergence that motivated the change: README's route named the superseded R5Y ZIP
      (68,355 B / `2f9ae0…`) while the release serves 68,357 B / `545e359a…`.
- [x] `README.md`: route → release asset + served digest; R5Y build kept and labelled superseded;
      the R5Y-time "no tag and no release was created" gate row replaced by the published identity.
- [x] `docs/install/README.md`: version-pin bullet names the real tag object/target/tree and the real
      identity sources; the non-existent `RELEASE_TUPLE_v0.1.1-preview.4.json` asset is no longer named.
- [x] `docs/RELEASE_TUPLE.json`: `v0.1.1-preview.4` entry with tag facts, a **scoped** build-source claim,
      all **seven** served asset identities (`sha256sums_coverage`: 6/6 of the release's own checksum
      entries are represented, the seventh record being `SHA256SUMS` itself), and `pack_dir`/`zip` null on
      purpose (the release ships no mount pack).
- [x] `tests/test_r5r3_install_route_identity.py`: derived guard (git re-derivation + digest checks).
- [x] Guard proven non-vacuous: the mutation control `mutation_control_route_rule.py` shows the
      per-paragraph rule fires when the superseded digest is placed in the route paragraph and that the
      live text is clean.
- [x] First acceptance run was RED (`README.md:74` — a per-line rule failing on a correct wrapped
      disclosure). The guard was corrected to a per-paragraph rule and re-run; the failure and the
      correction are recorded, not hidden.
- [x] Focused acceptance: 35 tests, `OK`, exit 0.

## WS-B — full-suite regression on the modified tree

- [ ] Full suite on the modified tree, real exit code, compared against the unmodified-tree baseline
      (`Ran 614 tests`, `OK (skipped=4)`, exit 0).

## WS-C — publication

- [ ] Commit the four files on `fix/r5r3-preview4-identity-and-route`; push; open a pull request.
- [ ] Independent checker (CODEX CLI, `openai-codex/gpt-6.1-sol`) re-derives the decisive claims.
- [ ] Owner decides the release/main drift recorded in the round report (the served wheel predates the
      R5R2 clause-boundary refinement on `main`). **No new tag or release is created by this change set.**

## Explicitly out of scope

`PUBLICATION_APPROVED`, `RELEASED` for a new tag, `S4_FULL_PASS`, `PRODUCTION_VERIFIED`, the public
directory route, and any product-code change.
