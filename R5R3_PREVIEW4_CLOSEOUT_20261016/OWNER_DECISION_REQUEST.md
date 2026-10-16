# OWNER DECISION REQUEST — round R5R3-20261016 (preview.4 closeout)

Three decisions, each one action away. Nothing below has been executed. Each item states the act, the
evidence that makes it safe to decide, the consequence of each answer, and the rollback.

---
## ODR-1 — Consent: import the published plugin ZIP on the private host

**Act requested:** one consented import attempt of the published `v0.1.1-preview.4` plugin ZIP
(`pipd-ls-sp-public-skills.zip`, 68,357 B, sha256 `545e359a…`) into the private ChatGPT host.

**Why it is still open:** the 2026-10-14 attempts were refused server-side ("cannot add plugin, try again"),
twice, no error code. Cause remains UNRESOLVED.

**What the round has since excluded (measured, re-runnable):**
- Build nondeterminism: the published bytes are reproduced byte-for-byte by two independent builds at the
  recorded source commit `cc6c193` (same 68,357 B / same SHA-256).
- Manifest drift (location and fields): every member shared with the previously ACCEPTED R5Y package is
  byte-identical; only 2 provenance members differ (`RELEASE_RECEIPT.json`, `SOURCE_TO_PLUGIN_MAPPING.json`).

**Surviving hypothesis:** account/platform side (H3). A single attempt with the previously accepted package
discriminates it: if the accepted package is also refused now, the account/platform is refusing everything and
no packaging change can help.

**Answer A: grant** → one attempt of the published package, then (only if refused) the previously accepted
package; both recorded verbatim.
**Answer B: decline** → the round records `NOT_ATTEMPTED_CONSENT_WITHHELD` and the cause stays open.
**Rollback:** none needed; no state is changed by a refused import. The account is not modified by an attempt.

---
## ODR-2 — Consent: the two prepared diagnostic variants

**Act requested:** consent to upload the two structural variants prepared earlier (root-manifest projection;
minimal member set), in the same consented session as ODR-1, and only if ODR-1's package is refused.

**Why:** they split "manifest projection" from "member set" as candidate causes. They are only worth an
attempt if ODR-1 was refused; running them first is wasted consent.
**Answer A: grant** / **Answer B: decline** (variants stay untested and are recorded as such).
**Rollback:** none; a refused import changes nothing.

---
## ODR-3 — NEW_RELEASE: successor release carrying the later repairs

**Act requested:** decide whether to cut a successor prerelease whose assets carry repair commit `749dc32`
(the per-segment / no-space clause-boundary repairs) on top of the released surface.

**Why it is NOT being executed by the round:** `NEW_RELEASE` is NOT_GRANTED. Measured fact that motivates it:
the released wheel's `requirements.py` predates those repairs, so a user downloading today gets the
first-round repairs only — the repairs exist on `main`, not in any published asset.

**Recommendation (not an act):** decide this only AFTER ODR-1. If the import succeeds, the successor's value
is strictly the repaired behaviour, which can be released on its own schedule. If the import is refused again,
the successor should carry both the repairs and whatever the discrimination found.
**Answer A: grant now** (round prepares the release plan; a separate human release approval still gates the tag)
/ **Answer B: defer** (carried as an open ticket with this rationale).
**Rollback:** a release is immutable; the successor is issued, never rewritten. This is why the decision is
yours and not the round's.

---
## Standing disclosures for this request

- Owner gates still NOT_GRANTED: `NEW_RELEASE`, `PRIVATE_HOST_INSTALL`, `PUBLIC_DIRECTORY`, `PRODUCTION`,
  `S4_FULL_PASS`. This round executed no such act.
- The round's only external effect is the evidence push to the repository (authorised for external acceptance).
- Mandated model plan for this round was PLAN=GLM-5.3-Flash, EXECUTE=DeepSeek V4.1 Flash (CODEX CLI),
  VERIFY/SECURITY=DeepSeek V4.1 Flash (CODEX CLI). Writer and checker on the same model means model-axis
  independence is ABSENT; independence rests on process, lane, fresh context and re-derivation by the checker.
- A pre-existing canonical collision was measured this round: `check_sod(PLAN, VERIFY_SECURITY)` reports
  `SOD_VIOLATION` because both are `gpt-6.1-sol` in the live registry (epoch 21, CANDIDATE). Not caused by this
  round. Resolving it is a canonical route change, i.e. an owner/WorkOrder act — handed over, not patched here.
