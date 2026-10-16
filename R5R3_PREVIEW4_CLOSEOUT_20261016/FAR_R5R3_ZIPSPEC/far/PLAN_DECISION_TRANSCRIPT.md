# PLAN decision — transcription with provenance

Source of record: `raw/plan_far_glm.log` (the PLAN lane's raw stdout, model `glm-5.3-flash` via
`opencode-go`, in-Hermes one-shot, session `20261016_142351_eba290`, EXIT=0, 12,265 bytes).

**Transcription disclosure.** The lane's output is NOT machine-parsable as JSON: the value of
`discrimination_order.precondition_every_probe` was emitted truncated (`…每>());`), which leaves an
unterminated string and an illegal control character at line 17 — a minimal repair (control-character
sanitation, then a targeted replacement of that one value) still fails with `Expecting ',' delimiter`.
The raw log is therefore the artifact of record, and this file is a hand transcription. Content is not
paraphrased; the fields below quote the lane's own wording.

## Head-on answer (far_verdict_zh.head_on_answer)

> 否——依現有證據，「ZIP 相關規格不符合 GPT 外掛程式建立的要求」不能成立為這次拒收的原因；但今日仍不能
> 指認出真正原因（UNATTRIBUTED），需依 discrimination_order 執行判別後才能定案。

Spec-surface violation: refuted by byte-level evidence, confidence HIGH (re-derived locally this round):
56 members, identical names/sizes/order/zip metadata; only `RELEASE_RECEIPT.json` and
`SOURCE_TO_PLUGIN_MAPPING.json` differ in content (three field values); `plugin.json` byte-identical
(`9ba0eace19e9…`, `plugin_id=pipd-ls-sp-public-skills`, `version=0.1.1`). B is the archive the same
account already accepted + installed + invoked, so the host demonstrably accepted this spec surface.

## Surviving hypotheses ranked by the lane

| id | hypothesis | confidence (lane's own wording) |
|---|---|---|
| H2 | `plugin_id`+`version` collides with the installed plugin | 中 — best surviving hypothesis, unproven |
| H1 | transient host failure | 低至中 — one permitted retry decides it |
| H3 | undocumented rule on the two provenance fields | 低 |
| H4 | root-wrapper layout | 已駁斥 (A and B have identical layout; B was accepted) |

What the evidence does NOT support (lane): any attributed conclusion; the premise that the R5Y plugin is
still installed was not re-read today; whether the account accepts any upload at all is unknown.

## Discrimination order (lane's own probe definitions)

1. **P1-TRANSIENT-RETRY-A** — modal already holds A; re-check digest, press 新增外掛程式 once.
   ACCEPT ⇒ H1 explains it, close with zero packaging change. REJECT ⇒ H1 eliminated (A refused twice,
   retry cap reached) → P2.
2. **P2-KNOWN-GOOD-B** — upload B. ACCEPT ⇒ "account/platform refuses everything" eliminated and a
   same-identity re-upload is not refused (H2 heavily weakened); with "host rules unchanged since R5Y",
   A's refusal is localised by elimination to the two provenance members (H3 upgraded). REJECT ⇒ H2 or the
   account/platform side survives → P3.
3. **P3-MINIMAL-DISTINCT-ID-D** — upload D (`pipd-smoke-minimal`, `0.1.0`, 2 members).
   ACCEPT (read with a P2 REJECT) ⇒ H2 becomes the best attribution, with the caveat that D also changes the
   member set. REJECT ⇒ the account/platform refuses all uploads; every packaging change is worthless;
   hand to the owner.
4. **P4-CONDITIONAL-ROOT-LAYOUT-C** — only on (P2 REJECT and P3 ACCEPT) and a further owner nod.
   Not to be run otherwise; no new variants to be designed (over-engineering guard).

Stop rules: any ACCEPT stops the chain; A is submitted at most twice in total; a withheld refusal/timed-out
consent = NOT_ATTEMPTED_CONSENT_WITHHELD, never retried.

## Decision (decision_zh) — the lane's best engineering decision

> 不重建、不改欄位——先判別，後最小變更。

- Artifact to rebuild now: **none**. Fields to change now: **none**.
- Conditional minimum changes: P1 ACCEPT ⇒ zero change. P2 ACCEPT + P1 REJECT ⇒ candidate-level change:
  the upload candidate drops (or host-neutralises) the two provenance files; the released asset is not
  touched. P2 REJECT + P3 ACCEPT ⇒ minimal packaging change: a candidate that changes **only** the version
  (e.g. `0.1.2`), same `plugin_id`, repacked with the existing deterministic packager — or the zero-packaging
  route where the owner first removes the R5Y install and re-uploads the original. P3 REJECT ⇒ zero packaging
  change, hand to the owner.
- Why minimum sufficient: each branch moves exactly one causal axis (identity / provenance / transient) and
  proposes no new release and no rewrite of a released asset.
- What an acceptance report may say NOW (lane): spec-surface violation refuted by byte evidence; cause
  awaiting discrimination; no probe executed. It must not record any probe result or attribution.

## Falsifiers the lane bound to its own decision

- F1: P1 REJECT and P2 ACCEPT ⇒ H3 becomes the leading cause.
- F2: the host changed its upload-validation rules after R5Y ⇒ the byte-identity argument's premise fails;
  P2's REJECT tests this directly.
- F3: the host starts naming a file/field/rule id ⇒ discard the elimination plan.
- F4: the account's plugin list no longer contains the R5Y plugin ⇒ H2 loses its premise.
- F5: a probe's offline digest disagrees with `CANDIDATES.json`, or consent is refused ⇒ that probe has zero
  discriminating power and no attribution may rest on it.

## PIPD-PKG contract note (lane)

> Pre-upload identity check — packaging a host-upload candidate SHALL record the target account's installed
> `(plugin_id, version)` set; if the candidate's pair matches one of them and the manifest does not declare
> reinstall intent (a `reinstall_intended` marker plus an owner-consent ref), packaging FAILS CLOSED and emits
> no ZIP.

## Claim ceiling, as the lane wrote it

FILE_LEVEL_EVIDENCE_ONLY; this is a plan, not a probe result; the cause is UNATTRIBUTED today; H2/H3 are prior
rankings, not conclusions; the byte-identity argument rests on an untested premise (host rules unchanged since
R5Y); the installed-plugin list was not read today; the lane contacted no host, executed no upload, and wrote
no file. It also flagged a **data defect in this round's own record**: `FAR_R5R3_ZIPSPEC/RESEARCH_INPUT.json`
carried a wrong tail for B's `sha256`; the local artifact's value —
`2f9ae010a6eba90787037a93a17e77f50bbc29dea5628f6fbe3e0f278fd2d199` — is authoritative. That record has since
been corrected, with the correction disclosed in place.
