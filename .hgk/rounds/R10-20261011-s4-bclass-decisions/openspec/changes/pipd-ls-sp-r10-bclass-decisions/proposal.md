# pipd-ls-sp-r10-bclass-decisions

## Why

R9 closed the A-class gaps it could and named the remainder. Two items were left as owner calls and
are now authorised for adjudication and execution:

1. Three active SPEC/DEL crosswalk rows (`PIPD-SP-SPEC-002`, `PIPD-SP-SPEC-030`, `DEL-015`) require
   SSOT objects that do not exist. Producing them merely to move a coverage counter would be
   fabrication - `EXISTS != TRUE` - so the real question is whether the project OWES each object and
   whether it can be materialised FAITHFULLY from material already in the repository.
2. The R9 credential broker lives in agent scratch, which is pruned when idle, so it cannot serve
   the unattended runs it was built for. It needs a durable home and a governance route - and because
   that home is a control plane, it must not be installed as a side effect of a product round.

## What changes

- An **adjudication** per row, with a per-row verdict, rather than three manufactured objects. A
  verdict of "not owed here" or "requires owner design" is a valid, recordable outcome.
- Only artefacts that are **truthful restatements of material already in the repo** may be authored.
- The credential tooling gets a **determined durable home plus an apply-ready candidate**, and the
  install itself is routed as its own admitted change rather than ridden in here.

## What this does NOT change

- It does not rewrite the crosswalk, any schema, or any validator.
- It does not move a published tag, force-push, or rewrite history.
- It does not grant `G_RELEASE_FULL_PASS`, `FULL_S0_S4_INDEPENDENT_PASS` or `PRODUCTION_VERIFIED`;
  those remain outside this round by definition.
- It does not claim a crosswalk row is PASS because a related file exists.
