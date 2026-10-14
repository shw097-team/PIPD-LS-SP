# R6 verification protocol — external independent verifier

Round: `R6-20261014-far-remediation-and-repair`. Control plane: HG-KSEOS. Runtime: canonical Hermes (governed).
Claim ceiling (read first): **BUILD_PASS != PORTAL_APPROVED != PUBLISHED != HOST_QUALIFIED != S4_PASS**.
This protocol is intentionally mechanical: every value below is a measurement produced in this round, not a promise.

## (a) Obtain the evidence branch anonymously

The repository is public, so no credential is needed.

```
R=https://raw.githubusercontent.com/shw097-team/PIPD-LS-SP
B=r5z-evidence-return-20261014
# R5Z session-conformance pack (lane receipts, verdicts, claim ceiling):
curl -s $R/$B/PIPD_S4_R5Z_SESSION_CONFORMANCE_RETURN/README.md
curl -s $R/$B/PIPD_S4_R5Z_SESSION_CONFORMANCE_RETURN/LANE_RECEIPT_VERIFY_arm5.json
# R4 evidence pack expanded this round:
curl -s $R/$B/PIPD_S4_R4_EVIDENCE_RETURN/EVIDENCE_RETURN_MANIFEST.json
```

The frozen implementation commit is `062d84ae3e951d02b2ba6bb732359b18799d2864` (tree
`f642e2b7900b0369f6925948d3a43aba0575016c`). Fetch that commit read-only in your own checkout; do not
push. The Tier-1 artifacts published for you are under this round's `EXECUTE/out/` (delivered beside this
protocol).

## (b) Rebuild the plugin ZIP (exact commands)

Python: `C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe`. Run from the frozen worktree
`C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt` at commit `062d84ae3e951d02b2ba6bb732359b18799d2864`.
Substitute your own OUT directory for `<OUT>` (must not overlap the repo).

```
cd C:/Projects/Agent_Workspace/PIPD/worktrees/r5y-wt
python tools/freeze_public_plugin_source.py --repo-root . --out <OUT>/zipcheck/ledger.json
python tools/build_public_plugin.py --ledger <OUT>/zipcheck/ledger.json \
  --source-commit 062d84ae3e951d02b2ba6bb732359b18799d2864 \
  --packaging-root packaging/public-plugin --out-dir <OUT>/zipcheck/c --generate-icons
```

Expected values actually measured this round:

| measurement | expected value |
|---|---|
| ledger commit | `062d84ae3e951d02b2ba6bb732359b18799d2864` |
| ledger tree | `f642e2b7900b0369f6925948d3a43aba0575016c` |
| ledger file_count / skills | 48 files / 8 skills |
| ZIP bytes | 68355 |
| ZIP sha256 | `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199` |
| ZIP entry count | 56 |
| `SKILL.md` count | 8 |
| root `plugin.json` present | yes (`pipd-ls-sp-public-skills/plugin.json`) |
| seven camelCase `com.openai.interface` fields | capabilities, category, defaultPrompt, developerName, displayName, longDescription, shortDescription — 7/7 present |
| two independent builds | byte-identical (deterministic) |

`--generate-icons` is deterministic: the icon it writes is byte-identical to the one already in the
worktree (`70bfddc3ebd2d6445f54f1a4258f1f0b0b787ee3a629b47900e47c3aa23a16e8`), so it does not move the
sha256. A local packager PASS is not portal approval: the builder stamps `claim_ceiling=LOCAL_PACKAGER_PASS_ONLY`
and `official_portal_verification=NOT_EXECUTED`.

## (c) Three evidence checks

1. **MANIFEST hash match.** For every entry in `acceptance/GOVERNING_DOCS_MANIFEST.json`, recompute the
   published file's sha256 and byte count and compare to `published_sha256` / `published_bytes`. Expected
   result: 5/5 match.
   ```
   R4_PROMPT.md                 c9a597a11ffa0ccaa07a1476220f89b68e50432cde8b8cee4b39a2f0c95e9a1b  20091
   R4_REPORT.md                 550421e990d44ce9bc596ea26ee9eaaef64e745b7c0d657a6c93db2ba21a0817  36620
   GPT_PLUGIN_PLAN.md           d7b5cc7e6b26ce5fcff62cefa2c92f4c1fe38da1c9415308b4243e8b1b05d92d  27300
   TRIPLE_UPGRADE_BLUEPRINT_R2 aca367e7d4aad7d44245c56c2ec3c9f164fc07852904078358b3be2ece01c2b4  151834
   R3_EXTERNAL_ACCEPTANCE.md    6a579d369b0bab5ac621b11cb7bac98c294a98e9ea986ef79cd7381078349e79  38257
   ```
   Also scan every published document (and the manifest itself) for the raw credential-locator substring
   built from `API`+space+`KEY`+`GITHUB-REPO_SHW097-4.txt` (with the platform path separators). Expected:
   zero hits; the token `<REDACTED_CREDENTIAL_LOCATOR>` appears in `R4_PROMPT.md` where the 2 occurrences were.
   The manifest does not reproduce the literal locator; it pins it by sha256
   `a461e3da15ee1059d3905f38f5b02f5037a39c0151f1c4cc2e9471cc244abe7b` (of the locator's UTF-8 bytes) so
   absence can be checked without planting the secret.

2. **PKG 11/11 sha256 match.** Recompute sha256 of the 11 governing packages listed in the round's
   `01_subject/PKG_INDEX_R6.json` against the mounted PKG-00..PKG-10 set. Expected: 11/11 match.
   Per-file expected sha256 (from `PKG_INDEX_R6.json`):
   ```
   PKG-00  89b60fde8b7bb93522c897a250a3ffbf9f2c4f91556493e74ee2da269710ecfe
   PKG-01  4c468e38d461595f21cd4d696dd2b97b655a438d7c8ef2fa1fec29637f8e139f
   PKG-02  decf42108f693563b1127064864b891d233ace2cf63b33db8f8e57e5ef29e977
   PKG-03  a8d61dc4ab3062f401427c0787f596093671c6e0d7408c6e924be3362423043f
   PKG-04  967c0a4906d735f7f0973987b6162993d8a87d88d8675d9bd1675f31b1055a77
   PKG-05  b01b170519b1343c6f4593b4e039b28bb9b4f3f68dbd9c17be52b198d542ff94
   PKG-06  073592099de22584e12b5ca892c52b298ccca2504f759e723c258a52c2b14dc9
   PKG-07  213b49c53f060ea780657def96a22b7e2815a222726874187d154f844a5c9872
   PKG-08  e93fe81371192b43c2b583423a33cfb728b6a6b99a7eef48ef19ff2516e18445
   PKG-09  b2952652d511ff726fac0b7f80147f807d1624ad4392c682635aa5582e386197
   PKG-10  e089fa095aa83f130be4846b478edc14bea9f410d4cc99ad52e4b6b5375391bd
   ```
   (Hashes are of the source markdown; the mounted copies in `PKG_INDEX_R6.json` also carry `chars`.)

3. **Lane binding receipt.** In `PIPD_S4_R5Z_SESSION_CONFORMANCE_RETURN/`, the binding checker receipt is
   `LANE_RECEIPT_VERIFY_arm5.json`: `ok == true`, `required_arm == served_arm == opencode-go/glm-5.3-flash`,
   and `subject_mutation.verdict == CLEAN` (guard window over the round + r5z-wt + r5y-wt). The same binding
   holds for `LANE_RECEIPT_VERIFY_arm4.json` (`ok=true`, `required_arm == served_arm == opencode-go/glm-5.3-flash`,
   `verdict CLEAN`). The receipts that do NOT bind must be read as non-passing: `LANE_RECEIPT_EXECUTE.json`
   (`ok=false`, `ERR_REQUIRED_ARM_NOT_SERVED`) and `LANE_RECEIPT_VERIFY_RECHECK.json` (`ok=false`,
   `ERR_REQUIRED_ARM_NOT_SERVED`), plus `LANE_RECEIPT_VERIFY_arm3.json` (`ok=false`,
   `ERR_CHECKER_MUTATED_SUBJECT`, window VOID).

## (d) Pass criteria

A Tier-1 artifact set passes this protocol when all hold, each with a raw value reported (never a blanket
PASS for an unrun check):

- manifest hash match is 5/5 and the raw credential-locator scan is zero hits across the published docs;
- PKG sha256 match is 11/11;
- the rebuilt ZIP is 68355 bytes / sha256 `2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199`,
  with 56 entries, 8 `SKILL.md`, root `plugin.json`, and 7/7 camelCase interface fields;
- the binding lane receipt satisfies check (c)(3);
- anti-mutation: nothing under the round tree `C:\Projects\Agent_Workspace\PIPD\.hgk\rounds\R6-20261014-far-remediation-and-repair`
  or the worktrees changed during the verifying run (only the verifier's own OUT is written).

Any check that cannot be run must be reported as `NOT_RUN` with the reason, not as PASS.

## (e) Claim ceiling

`BUILD_PASS != PORTAL_APPROVED != PUBLISHED != HOST_QUALIFIED != S4_PASS`

A successful rebuild is a local packager measurement only. It does not imply vendor/portal approval, a
release, host qualification, or acceptance of the S4 subject.

## (f) What an external verifier cannot do from the repo alone

- **Host UAT** — real first-run behaviour on ChatGPT Web Plus/Free, Agents, and Codex CLI hosts requires
  those live hosts; the repo can only carry the tests and workflow definition.
- **Portal publication** — submitting to and being reviewed by the Agent Plugins / GPT plugin portal needs
  an OpenAI developer identity (a Human Gate) that the repo does not contain.
- **Public consumer verification** — confirming download and install by an unrelated third party is a live
  event, not a repository fact.
- **Private plugin install** — installing the plugin into a private ChatGPT session requires a live
  ChatGPT session and account; this round's private-path evidence is self-account only.
- The current merge/tag/release state still lives on branches and a draft PR (#8); `main` is unchanged, so
  the verifier sees candidate-level artifacts, not a merged or released state.
