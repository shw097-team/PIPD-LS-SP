# FAR retrieval channels: two present, one not selected, and NO channel discriminated

Ledger: `far-study/retrieval_ledger.json` (written by the round's own runner, 2026-10-13).
Question put to the channels: *"S4 R3 write-set allowlist widening, external acceptance readiness,
pending owner decisions"*.

| channel | status | measured result | usable as evidence? |
|---|---|---|---|
| local corpus (`知識庫` + this round's directory) | PRESENT, 5.45 s | 8 hits, **all score 5**; top hits are `RP002-Stage3-Knowledge-Map.md`, TW-ICT/SQS technical docs - none about the subject; nothing from this round's own evidence scored | **NO - not discriminating** |
| spine memory | PRESENT, 0.50 s | 8 hits, scores 5/5/4/4; hit objects carry **no `kind` and no `id` field**, so a hit cannot even be cited to a row | **NO - not citational** |
| governed web | NOT_SELECTED_WITH_REASON | not invoked; the round's policy for product work is network-off and the studied subject is on disk | n/a |

What this means for the study's claim ceiling, stated plainly: **the FAR round's evidence base is the
round's own receipts, not a retrieval result.** A retrieval channel in which every candidate scores the
same value cannot order candidates, and a hit that cannot be resolved to a spine row cannot be cited.
Reporting "the FAR harness was run" without this note would be exactly the kind of instrument-shaped
non-evidence this stack forbids (`governed-stack-audit` §10: a counter-evidence channel must
DISCRIMINATE or it is not counter-evidence; §12: the deliverable is the answer, not the instrument).

Consequence for the packet that was sent to the EXECUTE lane: every fact in it is carried with a
locator into the round's evidence tree, and the lane was instructed to answer `NOT_SUPPLIED` rather
than fill a gap. The retrieval channels contributed nothing to it and are not cited as if they had.

Follow-up worth a separate owner decision (not done here, low priority): the scoring collapse to a
constant is a property of the retrieval implementation, not of the corpus. If FAR rounds are to rely on
this channel, the scorer needs a discriminating term; until then, `governed-stack-audit` §9's advice to
verify the roots resolve to hundreds of real files is satisfied while the ranking is still useless.
