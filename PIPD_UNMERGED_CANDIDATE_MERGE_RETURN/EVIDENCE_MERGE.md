# Evidence - which unmerged candidates were merged into main (2026-10-16)

**Round** `PIPD-UNMERGED-CANDIDATES-20261016` | **Study** `FAR-20261016-022`
**Question answered:** of every candidate not in `main`, which ones should be merged directly into it?

`main` moved `d3bd5456` -> **`dd0d5ce9acba65df74a5ac8dfe6293270edbf82d`**: three `--no-ff` merges of PR #18,
PR #17 and the 2026-10-16 front-page/handover refresh. 18 of the 21 branches were deliberately left alone:
9 are evidence carriers (their purpose is to hold evidence, not to change `main`), 8 conflict with the
current `main` and are superseded by content that landed through later pull requests, 1 is neither small nor
clearly wanted.

## What is granted, and what is not

| Claim | Status |
|---|---|
| The three candidates are now in `main` (`dd0d5ce`) | **granted**, independently readable with `git ls-remote` / `git log origin/main` |
| The merged tree passes the full local suite (632 passed, 0 failed) and the doc-identity guard (11/11) | **granted**, locally |
| Nothing under `src/`, `schemas/` or `skills/` changed | **granted**, empty diff vs the previous `main` |
| `v0.1.1-preview.4` tag and its assets are untouched | **granted** (tag object unchanged); no release API call was made |
| `S4_FULL_PASS`, four-host qualification, `PRODUCTION`, a new release | **NOT_GRANTED** |
| PR #18 / PR #17 shown as merged on the hosting side | **NOT achieved** - both remain `open / not-merged`; the content is in `main`, the pull-request records are not marked. Owner action. |

## Authority for the merge itself

The governor's blueprint carries `merge_tag_release: OWNER_GATE_ONLY`, and the external final review
advised that the merge be a **human** operation. The owner superseded that advice by instruction and
directed the agent to execute it: this is recorded as `OVERRIDDEN_BY_OWNER`, **not** as external
acceptance. The scope of that instruction was the three branches above and nothing else.

**SoD:** PLAN/EXECUTE/VERIFY share one arm (`opencode-go/deepseek-v4.1-flash`, registry `SOD006-C3`);
model-axis segregation does not exist and no part of this pack claims cross-model independence.
