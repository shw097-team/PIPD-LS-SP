# KANBAN / SWARM state — verified, not asserted

Round `R9-20261011-s4-gap-closure`, obligation `REQ-PIPD-R9-KANBAN-006`.

## 1. Correction: the R8 board claim is withdrawn

During R8 I stated in the round report that a kanban board and a swarm (root `t_930df231`) had been
created. The R9 obligation was to **verify or explicitly record** that state. Verification result:

```
grep -rl "t_930df231" PIPD-r7-release HG-KSEOS   ->  no matches
find PIPD-r7-release/.hgk/rounds/R8-.../ -type f ->  admission/ evidence/ far/ verify-codex/ only
```

**There is no on-disk artefact for that board or swarm id anywhere.** The claim was an assertion
about a live system state that left no trace, and under this project's own standard — governance
records are evidence, not narration — it **cannot stand**. It is withdrawn here rather than quietly
dropped.

Two things are worth separating:

- The **HGK lifecycle admission for R8 was real and is evidenced**: 5 obligations reached `FROZEN`
  with TaskSpec + WorkOrder in `admission/r8_admission.json`. That is the part that matters for
  governance and it is intact.
- The **kanban/swarm board state was not evidenced** and is therefore recorded as `UNVERIFIED`
  rather than `done`. A count of 6/6 done was never something I could have shown.

## 2. What this round does instead

Rather than restate a board, this round writes the artefacts to disk so the state is checkable by
someone who was not here.

### 2.1 Kanban — `kanban/ROUND_KANBAN.json`

The obligations admitted by `hgk_r9_admission.py` (6 requirements, all `FROZEN`, 0 errors), each
carrying the artefact that closes it:

| id | priority | closes on |
|---|---|---|
| `REQ-PIPD-R9-SRCSCAN-001` | P0 | `far/FAR-PIPD-R9-SRCSCAN-001.md` + `evidence/SOURCE_SCAN_*` |
| `REQ-PIPD-R9-AUDITGAP-002` | P0 | `evidence/SPEC_DEL_ACTIVE_GAPS_AUDIT.md` |
| `REQ-PIPD-R9-DEL018MAIN-003` | P0 | `far/FAR-PIPD-R9-DEL018MAIN-003.md` |
| `REQ-PIPD-R9-CLEANTREE-004` | P0 | `verify-codex/INDEPENDENT_ACCEPTANCE_R9_CLEANTREE.md` |
| `REQ-PIPD-R9-CREDROT-005` | P0 | `far/FAR-PIPD-R9-CREDROT-005.md` |
| `REQ-PIPD-R9-KANBAN-006` | P1 | this file + `openspec/changes/pipd-ls-sp-r9-gap-closure/` |

Status is recorded per item as `CLOSED` / `OPEN` / `UNVERIFIED`. A requirement is `CLOSED` only when
the named artefact exists on disk and says what the requirement asked for.

### 2.2 Swarm — `swarm/SWARM_ROSTER.json`

Two isolated subagents ran in parallel (`deleg_da9bc861`), plus the in-Hermes PLAN lane and the
CODEX CLI lanes. Each entry names its role, its model, and the artefact it produced — so the roster is
a record of work products, not a claim about threads being alive.

### 2.3 OpenSpec — `openspec/changes/pipd-ls-sp-r9-gap-closure/`

`proposal.md` + `tasks.md`, in the same shape as the R5Q/R5R/R7/R8 changes.

## 3. What is NOT claimed

- That a live board exists right now. What exists is a **file** whose contents can be checked.
- That the R8 board ever existed. It is recorded `UNVERIFIED`; absence of an artefact is consistent
  with "it was created and left no trace" and with "the id was misread", and I cannot distinguish
  those from here — so I assert neither.
- That this file's status column is authoritative on its own; it is a pointer to artefacts, and the
  artefacts are the evidence.

**Claim ceiling:** `KANBAN_SWARM_OPENSPEC_ARTEFACTS_ON_DISK_R8_BOARD_STATE_UNVERIFIED`.
