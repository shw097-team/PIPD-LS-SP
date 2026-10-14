# Closure and handover — this session, closed out against the governing corpus

Single entry point. Read this first, then follow the artifact it names for whatever you need to check.

**Alignment premise (highest):** `知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/PIPD/PIPD-LS-SP_PIPD-PKG`.
Every disposition below is shaped by that corpus rather than by local preference, and each cites the rule
it obeys with the rule's own first-failure code, so a reviewer can check the form as well as the content.

**Claim ceiling, stated before anything else.** This session reached `OFFERED` in the PKG-05 state
machine. It did not reach `RECEIVER_ACCEPT_HANDOFF`, `EXECUTION_ADMITTED`, `OPERATIONAL_ACCEPTED` or
`PRODUCTION_PASS`, and it asserts none of them. `NO_MERGE` / `NO_PUBLIC_RELEASE` /
`S4_FULL_PASS NOT_GRANTED` all hold. No acceptance row was run and none was filled.

## 1. What this session actually produced

| layer | artifact |
|---|---|
| the finding | the stage-b allowlist carried two entries beyond the frozen subject while an admitted requirement forbade widening; the gate file also said the opposite in a comment |
| the remedy | `.hgk/**` excluded from the governed PRODUCT write set **by declaration and printed**, not by an allowlist permission; both round-directory entries removed; nothing added; the surviving addition measured as load-bearing |
| the verification | local gate 2/2 clean with self-tests green, stacked invariant restored by merge, gate-file copies differ in exactly one line, hosted CI green at both heads, and a lane bundle audit returning six-of-six CONFIRMED at v2 |
| the closure | `CLOSURE_DISPOSITION.json`, `SUPERSESSION_LEDGER.json`, `AFFECTED_ONLY_INVALIDATION.json`, `EVIDENCE_ENVELOPE.json` |
| the handover | `RECEIVER_HANDOFF_BUNDLE.json` (typed, admission fields deliberately empty) |

## 2. The closure, in the corpus's own terms

The corpus does not let a maker declare a finding CLOSED. `PIPD-PKG-06 DOC-05` names the route
`OPEN → ASSIGNED → PATCHED → CHECK_PENDING → CLOSED` and its first failure is
`TT_CLOSURE_WITHOUT_CHECKER`; qualification comes from an external issuer's signed receipt, and
`PIPD-PKG-01 3.2` distinguishes author-side design receipts from external gates, which need
**target-scoped, checker-observed** evidence.

So this session moves its two findings to **CHECK_PENDING**, carrying owner evidence and a lane bundle
audit as the checker leg, and stops there. The lane's own capability ceiling is measured and disclosed: it
cannot read the tree or execute anything, so its evidence is **bundle-scoped, not target-scoped**. A
reviewer wanting CLOSED needs the external leg; nothing here pretends to be it.

Superseded revisions are recorded rather than dropped (`SUPERSESSION_LEDGER.json`: old and new hashes plus
a predecessor link, with the invariant recomputed from the carried values), and the head advance's impact
is **affected-only**: 35 artefacts cite a superseded revision and are marked affected, 3 cite only the
current heads and are untouched, and nothing is deleted. Where no output delta could be proven the
conservative branch was taken, per `PIPD-PKG-09 DOC-03`.

## 3. How to falsify this session's claims

Each of these is a command you can run, not a claim you have to trust:

```bash
git clone https://github.com/shw097-team/PIPD-LS-SP.git && cd PIPD-LS-SP && git fetch origin
git rev-parse origin/fix/s4r3-stage-a-ci-truthfulness-20261013 origin/feat/s4r3-stageb-successor-20261013
git merge-base <A> <B>            # must equal the stage A head
git ls-remote origin refs/heads/main refs/tags/v0.1.1-preview.3   # both untouched
```

| claim | falsifier |
|---|---|
| the allowlist carries one addition and no round-directory entry | re-run `scripts/measure_allowlist_minimum.py` at the head; any UNLISTED product path, or a surviving round-directory entry, falsifies it |
| the exclusion is declared, printed and unreachable from product paths | read the gate step's output; an unprinted skip falsifies it; the self-test prints the check it ran |
| the two branch copies differ in exactly one line | `git diff` them; a second differing line falsifies it |
| the affected-only set is correct | for any entry marked untouched, show it cites a superseded revision; for any marked affected, show its citation is the current head |
| no state was silently promoted | read `CLOSURE_DISPOSITION.json`; a CLOSED item, a non-empty admission receipt, or a P3–P5 claim falsifies it |

## 4. What is handed over, and to whom

`RECEIVER_HANDOFF_BUNDLE.json` is the typed offer: subject identity, scope in and out, permissions granted
(none — a handoff is not a permission), DEV/OPS/TQAEP at design-only, rollback refs at the two frozen
refs, and **empty** admission fields with the reason recorded. `PIPD-PKG-05 0.5` puts admission in the
receiver's hands alone; `PIPD-PKG-10 0.6` blocks self-promotion. Both are honoured by leaving the fields
empty rather than by filling them plausibly.

## 5. What only the owner can decide

Eleven items are enumerated in `CLOSURE_DISPOSITION.json`, each with its next legal state, the artifact
that state requires, its decision owner and the first-failure code for skipping it. They fall into four
kinds: **accept or rule on the remedy**; **supply owner-gated inputs** (F003 publisher identity and
validator, four-host UAT); **rule on external effects** (preview.3 wheel rebuild, PR dispositions,
`.hgk` archive policy); and **apply a routing change** (the PLAN-leg divergence, which is a global
config change and therefore not a maker action).

Nothing in this session crossed those lines, and the disposition records where each line is instead of
implying it was crossed.
