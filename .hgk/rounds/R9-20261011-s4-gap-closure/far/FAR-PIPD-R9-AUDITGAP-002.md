# FAR-PIPD-R9-AUDITGAP-002 — the 4 active SPEC/DEL rows that cannot be closed by a closure round

Round `R9-20261011-s4-gap-closure`, obligation `REQ-PIPD-R9-AUDITGAP-002`.
Companion to `evidence/SPEC_DEL_ACTIVE_GAPS_AUDIT.md` (the per-row audit).

## 1. What the audit established

The denominator was recounted from the crosswalk rather than restated from prose, and it matches:
**57 rows = 28 evidenced + 10 active + 19 deferred**. Of the 10 active rows, **6 were adjudicated**
with the artefact actually opened; **4 could not be**, and — this is the finding — not because nobody
looked, but because **the object each row requires does not exist**.

| row | requires | what exists instead | status |
|---|---|---|---|
| `PIPD-SP-SPEC-002` | a materialised `PIPD-LIFECYCLE-SPEC@1.1.0` SSOT object | a retrieval-index **hit** for the query `PIPD-LIFECYCLE-SPEC` (a text match, not an object) | **OPEN — object absent** |
| `PIPD-SP-SPEC-030` | an MCP materialization object | a technology-admission **design** row: `DESIGN_CONTRACT_SPECIFIED_NOT_INSTALLED`, `NOT_EXECUTED` | **OPEN — object absent** |
| `DEL-004` | `SPEC_REGISTRY@1` | only `PIPD-S0-CONTRACT-REGISTRY/1` — a registry of the **19 S0 contracts**, a different thing | **OPEN — object absent (external)** |
| `DEL-015` | `ADAPTER_REGISTRY@1` | only a host-projection manifest: 3 hosts, `live_status NOT_RUN`, `FIXTURE_MOCK_ONLY` | **OPEN — object absent** |

**Independently probed, not taken on trust.** A workspace-wide search for the four object names finds
them only in the crosswalk itself, in a prior round's row-evidence file, and in HG-KSEOS SWOF bundle
*chunks* — never as an object. So "absent" is measured, not inferred.

## 2. The temptation this study exists to refuse

The obvious move is to **author the four missing objects** and watch the counter go 10 → 6. That would
be **falsification**: an object brought into existence for the purpose of moving a coverage number
evidences nothing about the system it is supposed to describe. The academic-integrity rule this
project already applies elsewhere — *`EVIDENCED != PASS`* — has a sibling here: **`EXISTS != TRUE`.**

A second temptation is to re-scope the crosswalk so the rows stop being active. That is the same act
with better manners.

## 3. Options

| | option | assessment |
|---|---|---|
| **A** | **Record the 4 as `OPEN — OBJECT ABSENT`, with the reason and the probe that established it.** | Recommended *for this round*. It is the only option that is both true and cheap, and it converts a vague count (`10 active`) into a precise statement (`6 adjudicated, 4 blocked on absent objects`). |
| **B** | Open a **substantive authoring round** for the three in-repo objects (`PIPD-LIFECYCLE-SPEC@1.1.0`, the MCP materialization object, `ADAPTER_REGISTRY@1`). | Recommended as the **next** round, not this one. Authoring an SSOT object is a design act with its own admission, contract and review — it is not a gap-closure chore, and it must be justified object-by-object on its own merits rather than by the counter. |
| C | Author the objects now, inside this closure round | Rejected. This round exists to close gaps with evidence, not to manufacture the evidence. |
| D | Re-scope the crosswalk to drop the rows | Rejected — hides the gap instead of stating it. |
| E | Treat `DEL-004` as closable here | **Impossible in principle**: the SPEC registry lives in the **external blueprint**, outside this repository. This row is genuinely in the *external-dependency* class, alongside the items reserved for external acceptance. |

**Adjudication: A now; B as the next substantive round; E recorded as external.**

## 4. Resulting honest denominator

```
57 rows total
  28 evidenced
  19 deferred      (S5-S8, PRE-W3, 22 inactive external technologies - unchanged, by decision)
  10 active
      6 adjudicated with evidence opened
      4 OPEN — object absent   (3 need an authoring round; DEL-004 needs the external blueprint)
```

`PARTIAL_CHALLENGE` **stays**. What changes is that its content is now specific: it is no longer
"10 unexplained active gaps" but "4 named rows blocked on named missing objects".

## 5. What this does NOT claim

- That the 6 adjudicated rows are `PASS`. Adjudicated means *evidenced with what was opened*, and
  several are evidenced as design-only or not-executed; the audit file states each one.
- That the 3 authoring rows *should* be authored. That is an owner call, and B is proposed rather
  than assumed.
- That authoring 3 objects would move the challenge to `FULL_PASS`. It would not: the deferred 19 and
  the absence of external acceptance still stand.

**Claim ceiling:** `SPEC_DEL_ACTIVE_GAPS_ADJUDICATED_6_OF_10__4_OPEN_ON_MISSING_OBJECTS`.
