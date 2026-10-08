# FAR-PIPD-LICENSE-001 — Synthesis

**Decision question.** What is the actual licence position of the PIPD corpus and product, and what is the
minimum-resistance *compliant* option for the `TT-PIPD-LICENSE-001` → `PUBLICATION_APPROVED` gate?

**Answer.** The corpus declares **no licence over itself**. Every licence token found (MIT, Apache-2.0,
LGPL-2.1, CC BY 3.0) names a **third-party technology's** licence and is consumed as a
`TechnologyAdmission` `license_ref` — an input field about *someone else's* artefact. Across 35 corpus
files there are 5,251 lines mentioning licence-ish words; 42 of them name a real licence in a licence
context; **zero** constitute a grant over the PIPD material. The product tree's own `LICENSE` already
says "NO LICENSE IS GRANTED", its SBOM carries `metadata.licenses = null`, and GitHub reports
`NOASSERTION`.

**So the blocker is an authority boundary, not a technical unknown.** Only the owner can grant a licence
over the owner's material. The agent has no standing, and the R2 order's own forbidden list forbids
"公開來源授權不明" arising into a grant without real authorization.

**Minimum-resistance compliant option (chosen).** Do not grant anything. Instead:
1. make the existing non-grant **precise** (corpus-derived vs agent-authored, each stated separately);
2. make it **machine-readable** (`LicenseRef-PIPD-Proprietary` in the SBOM) so no consumer is left guessing;
3. prepare a **single-action owner ratification slot** so the human gate becomes one signature rather than
   an open research question;
4. keep `PUBLICATION_APPROVED` **NOT CLAIMED**, and state that public visibility is not approval.

**Rejected.** Agent-granted MIT/Apache-2.0 (false grant, no standing); silence (permanently un-actionable);
privatise (contradicts the delivered state and does not answer the question); asking the user in chat
(delegated FAR research on an authority boundary — FAR prepares the decision, the human ratifies).

**Claim ceiling.** FAR local research plus in-scope product-root documentation changes. This is **not** an
acceptance verdict and does not close `TT-PIPD-LICENSE-001`; it makes the gate *precisely answerable*.
