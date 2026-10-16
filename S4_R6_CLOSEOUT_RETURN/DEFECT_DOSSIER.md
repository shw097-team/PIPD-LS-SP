# FAR-R17 DEFECT DOSSIER — checker capability gap + control-plane pool ordering

Round: PIPD-S4-R6-CLOSEOUT-20261016 / pass far-r17 (read-only reconnaissance sub-agent)
Subject binding cited throughout: commit `552bbde073806e254f84e95039f05c9767608aa1`, tree `a95579bf8c1bc77550d1044d12b2de7ed2028ae5` (frozen copy at `C:/Projects/Agent_Workspace/PIPD-S4R6-wt`).
Everything marked **INFERRED** is reasoning carried from read values, not a value read from a file. Nothing in any repository was modified by writing this dossier; the only file written is this one.

---

## QUESTION 1 — checker lane capability gap: no network fetch, no usable temp storage

### What the checker itself recorded (not re-created, quoted)

Source: `_handover/PIPD-S4-R6-CLOSEOUT-20261016/S4_R6_CLOSEOUT_RETURN/checker_verdict.json`
`"verdict": "PARTIAL"`, `"checker": {"lane": "VERIFY_SECURITY", "model": "openai-codex/gpt-6.1-sol (transport model gpt-6.1-sol, OpenAI OAuth)"}`, `verify_turn2`: `used_rank: 2`, `used_transport_model: "gpt-6.1-sol"`, `receipt_ok: true`, `nonce_present_in_stdout: true`.
`qualification_limits` (verbatim, checker's own words):

> "The checker's sandbox denied network access (WinError 10013), so it could not fetch the served release ZIP; that item is its NOT_RUN, while the maker's own fresh HTTPS recomputation is recorded in diff_and_tests/release_readback.json and is re-runnable by anyone."
> "The checker's sandbox had no usable temporary storage, so its pytest invocation failed before collecting tests; its verdict is therefore PARTIAL rather than PASS."

Source: `lane/verify/verdict_text_run1.txt` (tool receipt section 7, pytest):
`status: NOT_RUN`
`FileNotFoundError: [Errno 2] No usable temporary directory found in ['C:\\Users\\user\\AppData\\Local\\Temp', 'C:\\Users\\user\\AppData\\Local\\Temp', 'C:\\Users\\user\\AppData\\Local\\Temp', 'C:\\Users\\user\\AppData\\Local\\Temp', 'C:\\WINDOWS\\Temp', 'c:\\temp', 'c:\\tmp', '\\temp', '\\tmp', 'C:\\Projects\\Agent_Workspace\\PIPD-S4R6-wt']`
(same file, section 13, the release-ZIP fetch): `status: NOT_RUN` —
`URLError: <urlopen error [WinError 10013] 嘗試存取通訊端被拒絕，因為存取權限不足。>`
(same file, section 16, corroborating write-refusal outside the workspace): `warning: could not open directory '.pytest_cache/': Permission denied`

Source: `lane/verify/verdict_text_run2.txt`:
- pytest: `Status: NOT_RUN` — `PermissionError: [Errno 13] Permission denied: 'C:\\Projects\\Agent_Workspace\\HG-KSEOS\\.venv\\Lib\\site-packages\\sniffio\\__init__.py'` (run2's import chain tripped on a venv read/write the sandbox class refused; a different symptom, same controller)
- release fetch: `URLError: <urlopen error [WinError 10013] 嘗試存取通訊端被拒絕，因為存取權限不足。>` with the checker's own note `No workaround or retry followed this denial.`
- `Tool receipt: web.open of the supplied release-ZIP URL / Exit code: not supplied by tool / Raw response: empty; no artifact bytes obtained.`

Both runs ended `verdict: PARTIAL` with the same two-part ceiling: the pytest suite could not execute and the published ZIP could not be fetched.

### a) Default sandbox per lane, and the dispatcher's own comment on workspace-write vs danger-full-access

Source: `HG-KSEOS/scripts/hgk-lane-dispatch.py` line 90:

```python
SANDBOX_BY_LANE = {"EXECUTE": "danger-full-access", "VERIFY_SECURITY": "read-only", "PLAN": "read-only"}
```

So the VERIFY_SECURITY checker lane defaults to **`read-only`**. The rank scale is defined at line 91: `SANDBOX_RANK = {"read-only": 0, "workspace-write": 1, "danger-full-access": 2}` — "raising" a lane means moving up this rank.

The dispatcher's measured comment (lines 83–89) is the important second half:

```python
# Sandbox per lane. MEASURED 2026-10-10 (T5 outside the workspace root, T5b/T6 inside it): under
# `workspace-write` NO command_execution item is emitted at all and nothing lands, while the turn
# still reports exit 0 + the nonce; the only `error` item is a model-metadata warning. So the exit
# code and the nonce are not evidence that any work happened. `danger-full-access` emits a real
# command_execution item (exit 0) and the side effect lands. An artifact-writing lane therefore
# needs danger-full-access, and a read-only SUBJECT is enforced by a frozen copy plus a post-hoc
# digest comparison - not by the sandbox.
```

Header comment line 18: *"Sandbox defaults are role-shaped: a checker is read-only; a writer gets danger-full-access."* And line 22: *"A sandbox stricter-than-role default may only be escalated with --allow-sandbox-escalation, so a single flag cannot give a checker lane writer-grade access (round-5 checker finding)."*

The dispatcher's own measurement therefore says, verbatim: **on this host `workspace-write` is measured unusable for command execution (no `command_execution` item, no side effects, but a green-looking exit 0 + nonce), and only `danger-full-access` actually lands side effects.** A `read-only` checker also cannot write the temporary files pytest needs (`__pycache__`, temp dirs) before it even collects tests — which is exactly the run1 failure shape quoted above.

Also load-bearing for command execution: the pool declares (config/lane-route-slots.candidate.json, every lane's `codex_home_config`) `"windows_sandbox": "elevated", "required_for_modes": ["read-only", "workspace-write"]`, and the dispatcher injects it only in those modes (lines 1082–1086: `if _ws and sandbox in _modes: cmd += ["-c", f'windows.sandbox="{_ws}"']`). INFERRED from the field names plus the recorded WinError 10013 socket/temp denials: the injected restrictive Windows sandbox layer is the plane on which the checker's command executions were denied.

### b) Flags that raise a lane's sandbox, and what an ESCALATED CHECKER requires

- `--sandbox <level>` (defined at line 1376, default `None`) — sets the lane's sandbox explicitly; unknown values refused typed (`ERR_SANDBOX_UNKNOWN`, line 1674).
- Raising it above the role default additionally requires **`--allow-sandbox-escalation`** (line 1377, help: *"required to use a sandbox stricter-than-role than the lane default"*). The refusal without it (lines 1679–1683), exact:

```
ERR_SANDBOX_ESCALATION_REFUSED
"lane {args.lane} defaults to {role_default_sandbox!r}; {args.sandbox!r} needs --allow-sandbox-escalation"
```

(`escalated` is defined at line 1678 as `SANDBOX_RANK[args.sandbox] > SANDBOX_RANK[role_default_sandbox]`.)

- What an **escalated checker** additionally requires: a **`--guard-subject`** (repeatable flag, lines 1398–1400, help: *"file/dir whose digest must not change during the turn (repeatable). removed/changed => the verdict is VOID; this is what makes an escalated-sandbox checker safe"*). The guard is mandatory (lines 1853–1860), exact refusal message:

```
ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER
"lane {args.lane} is escalated from {role_default_sandbox!r} to {args.sandbox!r} with no --guard-subject: nothing would measure the subject"
say: "an unbounded escalated lane is refused; pass --allow-unguarded-escalation to record the exception explicitly"
```

The record-only exception is **`--allow-unguarded-escalation`** (line 1401–1403), which is *recorded in the receipt*, never silent (line 2193: `unguarded_escalation_acknowledged`). The code's rationale, line 1851: *"danger-full-access has no sandbox root, so the guard is the only bound an escalated checker has."* A guard root that resolves but holds zero files is separately refused (`ERR_GUARD_ROOT_EMPTY`, line 1821), and harness output paths living inside a guard root are refused (`ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`, line 1872).

### c) Is the network denial a property of the sandbox level, or something else?

Evidence points to the checker's **sandboxed-session execution space**, not the network path and not the release server:

1. **The denial text is an OS-class socket-permission error, not a network failure.** Verbatim in both runs: `URLError: <urlopen error [WinError 10013] 嘗試存取通訊端被拒絕，因為存取權限不足。>` — Windows "attempt to access a socket in a way forbidden by its access permissions." There is no DNS, TLS, or HTTP-status failure text anywhere in either verdict; the same session's other commands executed fine (git, python) and only ops needing writes/outside-scoped access died (temp dirs, `.pytest_cache/`, sniffio read, sockets).
2. **The windower is the sandboxed child process, and the pool declares that layer.** The pool's `codex_home_config` declares `windows_sandbox: elevated` for exactly the modes `read-only`/`workspace-write` and notes: *"absent this declaration codex denies every command in read-only/workspace-write while the turn still exits 0"* (pool file, each lane's `codex_home_config.note`; dispatcher lines 1717–1739 refuse the run when neither is declared). The checker ran in `read-only` (its role default). INFERRED (consistent, not re-measured here): the socket/temp/msg-level denials are properties of that restrictive execution space, which is a *sandbox-level* property of the session the checker ran under.
3. **A maker on an unconfined writer lane reached the same URL repeatedly.** The closeout's own `qualification_limits` records the maker-side fetch as a *rerunnable* recomputation (`diff_and_tests/release_readback.json`, fresh HTTPS SHA256), i.e., the serving path works from a lane whose sandbox is `danger-full-access`.
4. **The checker tried three surfaces and got three refusals, no workaround:** direct `urllib` (WinError 10013 both runs), its `web.open` tool (`empty; no artifact bytes obtained`), and never retried (`No workaround or retry followed this denial.`). Everything deny-shaped; nothing network-shaped.

Conclusion (within evidence): the denial was a property of the checker's sandboxed execution level — `read-only` lane sandbox plus the pool-declared `windows_sandbox: elevated` injected in `read-only`/`workspace-write` modes — not of the relay, DNS, or the release server. INFERRED corollary the pool itself encodes: with `--sandbox danger-full-access`, the `windows.sandbox="elevated"` injection is *skipped* (`required_for_modes` excludes it, dispatcher line 1084), so that restrictive layer is not applied to the escalated run.

### d) Exact minimal dispatch command that gives the checker network + usable temp storage while still bound to a frozen subject

Per the dispatcher's own measurements (a) and gates (b), the minimal raising of the checker lane that is expressible in flags:

```bash
python C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py \
  --lane VERIFY_SECURITY \
  --sandbox danger-full-access \
  --allow-sandbox-escalation \
  --guard-subject C:/Projects/Agent_Workspace/PIPD-S4R6-wt \
  --require-arm openai-codex/gpt-6.1-sol \
  --round PIPD-S4-R6-CLOSEOUT-20261016 \
  --prompt "<checker brief>" \
  --json-out var/PIPD-S4-R6-CLOSEOUT-20261016/verify/checker_receipt.json
```

Why these flags and only these:
- `--sandbox danger-full-access` — the only level whose command_execution is measured real on this host (comment lines 83–89); writing temp dirs and opening sockets in the child happen in the unconfined execution space (`danger-full-access` has *no sandbox root*, line 1851), and the `windows.sandbox="elevated"` layer is not injected because `required_for_modes` excludes it (pool `codex_home_config`, dispatcher lines 1082–1086).
- `--allow-sandbox-escalation` — mandatory to seat that sandbox on the read-only-defaulted checker lane (refusal text in (b)).
- `--guard-subject C:/Projects/Agent_Workspace/PIPD-S4R6-wt` — the frozen subject; mutation of it voids the verdict (`ERR_CHECKER_MUTATED_SUBJECT`, line 2263) and removing/any change voids. This is precisely how the contract keeps a writer-grade checker honest ("a read-only SUBJECT is enforced by a frozen copy plus a post-hoc digest comparison - not by the sandbox," lines 87–88).
- `--require-arm openai-codex/gpt-6.1-sol` — fail-closed on the mandated checker identity instead of silently degrading to another arm (lines 1395–1397). (Strictly optional for the two named goals; included because it is part of what makes the run *this* checker.)

**What I could not re-verify, and will not guess (INFERRED, measured-not-established here):** the flags remove every sandbox-level blocker the dispatcher or pool declares — lane sandbox level and the `windows.sandbox="elevated"` injection being the exact mechanism the pool's text names — but this recon pass did not re-run the dispatch, so the residual possibility that Windows-/host-level egress policy also blocks sockets from the checker's Codex home independent of the sandbox level is **not excluded by my reading**; the maker's repeated successes from an unsandboxed writer lane make that residual unlikely but not disproven. If a rerun under the exact command above still yields `WinError 10013`, the fix is **outside the lane contract flags** (a host/firewall policy change) and must be stated as such rather than papered over with more flags.

---

## QUESTION 2 — control-plane pool ordering defect

Sources read: `C:/Projects/Agent_Workspace/HG-KSEOS/config/lane-route-slots.candidate.json` (present, revision 10, status `CANDIDATE`, rev field 9, per `change_log` rev 9→10 owner order 2026-10-16) and `C:/Projects/Agent_Workspace/HG-KSEOS/config/lane-routing-registry.yaml` (present, `epoch: 22`, `status: CANDIDATE`).

### EXECUTE ordered pool (verbatim, pool file)

| rank | provider | model | feasibility / dispatchable |
|---|---|---|---|
| 1 | opencode-go | deepseek-v4.1-flash | `DISPATCHABLE (verified end-to-end on the real lane transport after the credential fix)` |
| 2 | openai-codex | gpt-6-luna | `REACHABLE_VIA_HUMAN_HOME_TRANSPORT` |
| 3 | nvidia | deepseek-ai/deepseek-v4.1-flash | `UNREACHABLE_MEASURED_20261011` + `"dispatchable": false` |

### VERIFY_SECURITY ordered pool (verbatim, pool file)

| rank | provider | model | feasibility / dispatchable |
|---|---|---|---|
| 1 | opencode-go | deepseek-v4.1-flash | `DISPATCHABLE` |
| 2 | openai-codex | gpt-6.1-sol | `REACHABLE_VIA_HUMAN_HOME_TRANSPORT` |
| 3 | opencode-go | glm-5.3-flash | `DISPATCHABLE` |
| 4 | nvidia | deepseek-ai/deepseek-v4.1-flash | `UNREACHABLE_MEASURED_20261011` + `"dispatchable": false` |

Both rank-1 arms are `opencode-go/deepseek-v4.1-flash`; both are `DISPATCHABLE`. The pool's own `selection_semantics` state the consequence: `"no_session_instruction": "rank 1 (默認/首選) is used"` — a default dispatch of the VERIFY lane serves deepseek-v4.1-flash, unconditionally. The pool itself records the intrinsic definition this creates: `"sod": "NOT enforced at this revision (owner D1). Identity overlaps are recorded as facts only, not as refusals."` and `identity_overlaps_recorded_not_enforced[0]`: *"deepseek-v4.1-flash is rank 1 (EXECUTE/VERIFY) and ranks 1-2 (PLAN) — the same identity can occupy all three lanes."* The registry (epoch 22) declares the same collision as `sod_invariants.declared_conflicts[SOD006-C3]` with `status: OWNER_ORDERED_IN_FORCE`, noting *"the lane guard refuses this pair when the declaration is absent (measured ERR_LANE_SOD_VIOLATION), so this entry is load-bearing, not documentation."* The registry's `sod_invariants.provider_axis_required: false` and the EXECUTE/VERIFY pair running both on `opencode-go` mean even provider separation does not hold on this pair.

### Defect statement (one sentence)

**With `VERIFY_SECURITY` rank 1 = the exact model `EXECUTE` rank 1 serves (`opencode-go/deepseek-v4.1-flash`), a governed round that simply "dispatches the VERIFY lane" gets a checker that is the same model identity as its maker — no model-axis separation of duties — because the pool's default-selection rule is rank 1 and SoD is declared not-enforced at D1.**

### The mandated checker and what its transport arm needs

- Mandated checker arm: `openai-codex/gpt-6.1-sol` = VERIFY_SECURITY pool **rank 2**, reachability class verbatim: `"feasibility": "REACHABLE_VIA_HUMAN_HOME_TRANSPORT"`; role label verbatim `"DEFAULT/首選"` (label/behavior mismatch inside the JSON worth noting: a rank-2 entry carries the DEFAULT role string).
- Transport-token rule for this arm: `transport_model: gpt-6.1-sol` — the **bare** id; the dispatcher header lines 12–14: *"the openai arm REQUIRES the bare id, because 'openai-codex/<model>' is routed to the default provider and answers HTTP 400."*
- Which flag the transport gate needs: **`--allow-human-home-transport`** (dispatcher line 1404, help: *"acknowledges that the run points --codex-home at a home holding a login, so the key-auth arms' 'no human-attended identity' claim is NOT being made for this run"*). INFERRED from three read values in agreement: (1) the arm's reachability class is `REACHABLE_VIA_HUMAN_HOME_TRANSPORT` and its `identity_requirement` is `relay_pool`, (2) the registry's transport ceiling for this arm is the router-mediated human home (`human_home_egress: C:\\Users\\user\\.codex\\config.toml -> base_url=127.0.0.1:10102`, pool `human_home_probe: "codex exec -c model_provider=\"openai\" --model gpt-6.1-sol -> turn.completed"`), and (3) the isolation gate (lines 1709–1715) refuses faithfully with `ERR_LANE_HOME_NOT_ISOLATED` and then explicitly instructs: `pass --allow-human-home-transport to acknowledge it`. Paired with `--require-arm openai-codex/gpt-6.1-sol` (`ERR_LANE_REQUIRED_ARM_ABSENT` / `ERR_REQUIRED_ARM_NOT_SERVED` both fail closed if this arm is not actually served).

### CANDIDATE patch proposal — **documented, NOT APPLIED; a measuring round must not apply it itself**

This is a reordering of `lanes[].VERIFY_SECURITY.ordered_pool` in config/lane-route-slots.candidate.json so the default (rank-1) dispatch of the checker lane serves the openai-codex/gpt-6.1-sol arm and restores maker/checker model-axis separation with EXECUTE (deepseek vs gpt-6.1-sol, as the registry's SOD006-C2 history records held once *between PLAN/VERIFY*). Note explicitly: the **current ordering exists BY OWNER ORDER** — the file's `declared_by` states *"VERIFY/SECURITY deepseek-v4.1-flash rank 1"* under owner order 2026-10-16 (round ROUND3-LANE-REBIND-AND-CLOSURE-20261016) — so this reordering **reverses that owner order and is therefore a policy decision only the owner can make**. It is recorded here (fenced diff form) as a documented candidate; the flip side is stated below the diff.

```diff
--- a/config/lane-route-slots.candidate.json (revision 10)
+++ b/config/lane-route-slots.candidate.json (revision 11, CANDIDATE — NOT APPLIED)

@@ "lanes" / entry lane == "VERIFY_SECURITY" / "ordered_pool" @@

   {
-    "rank": 1,
-    "role": "FALLBACK2/備援2",
-    "provider": "opencode-go",
-    "model": "deepseek-v4.1-flash",
-    "auth": "env_ref:OPENCODE_GO_API_KEY",
-    "measured": {
-      "relay_http": 200,
-      "relay_latency_s": [ 1.0, 1.52 ]
-    },
-    "feasibility": "DISPATCHABLE",
-    "transport_model": "opencode-go/deepseek-v4.1-flash",
-    "identity_requirement": "none"
-  },
-  {
-    "rank": 2,
-    "role": "DEFAULT/首選",
     "rank": 1,                       // becomes rank 1 = the DEFAULT the no-instruction dispatch serves
     "provider": "openai-codex",
     "model": "gpt-6.1-sol",
     "reasoning_effort": "medium",
     "auth": "openai_oauth",
     "feasibility": "REACHABLE_VIA_HUMAN_HOME_TRANSPORT",
     "transport_model": "gpt-6.1-sol",        // bare id required on this arm
     "identity_requirement": "relay_pool"
   },
+  {
+    "rank": 2,                       // demoted: no longer the default fate of every default dispatch
+    "role": "FALLBACK2/備援2",
+    "provider": "opencode-go",
+    "model": "deepseek-v4.1-flash",
+    "auth": "env_ref:OPENCODE_GO_API_KEY",
+    "feasibility": "DISPATCHABLE",
+    "transport_model": "opencode-go/deepseek-v4.1-flash",
+    "identity_requirement": "none"
+  },
   { rank 3 opencode-go/glm-5.3-flash (unchanged) },
   { rank 4 nvidia/deepseek-ai/deepseek-v4.1-flash (unchanged, dispatchable: false) }
```

Accompanying edits the promotion would require (to remain internally coherent):
1. `change_log` entry rev 10 → rev 11 naming the owner order plus the mechanism; a superseding `declared_by`/`selection_note` (the current selection_note states deepseek-v4.1-flash is rank 1 "declared in sod_invariants.declared_conflicts as SOD006-C3"); the registry `identity_overlaps_recorded_not_enforced` and reclassification `SOD006-C3 OWNER_ORDERED_IN_FORCE → SUPERSEDED (by the new owner order)`.
2. Per the file's own `placement_rationale` the registry parent (config/lane-routing-registry.yaml / config/model-lane-assignment.json) is drift-pinned (`source_of_routes.revision/sha256`) at 90 live sites across three live sites, so a fully synchronized sweep plus a registry/assignment epoch bump is required; server-side reruns on the pool file alone would produce `ERR_LANE_SOURCE_STALE` at the pre-dispatch lane guard.
3. Dispatch consequence that must ride along: the new rank-1 arm serves only through the human home (reachability class `REACHABLE_VIA_HUMAN_HOME_TRANSPORT`), so any default dispatch of the checker lane after this reorder must carry `--allow-human-home-transport` (else `ERR_LANE_HOME_NOT_ISOLATED`) and, to remain fail-closed, `--require-arm openai-codex/gpt-6.1-sol`.

**Explicitly:** **A measuring round must NOT apply this reordering itself.** It is an owner-order-adjacent control-plane change: the existing rank-1 assignment is by owner order 2026-10-16 (round ROUND3-LANE-REBIND-AND-CLOSURE-20261016, recorded as SOD006-C3 OWNER_ORDERED_IN_FORCE in the registry), and control-plane pool ordering is governed (candidate-file publication is a separate decision step). The measuring round's correct action is exactly what it did here — dispatch the mandated checker by asking for it *by identity* (`--require-arm openai-codex/gpt-6.1-sol --allow-human-home-transport`), which the lane contract already supports — while a future patch to close this defect is deferred to an approved change.

---

## What I could not determine

1. **Whether flags alone, in practice, remove every last blocker behind the WinError 10013.** The evidence in (c) pins the denial to the checker's sandboxed execution space and to the pool-declared `windows.sandbox="elevated"` layer in `read-only`/`workspace-write` modes; the command in (d) removes both per the source. Whether Windows host policy independently blocks egress from the checker's `codex-hermes` home is **not excluded** and was not re-measured here (read-only pass); if a rerun under the exact command above still returns `WinError 10013`, the residual cause is outside the lane contract (a host/firewall policy question) rather than a defect to fix with more flags.
2. **Run 2's pytest failure surfaced as a `PermissionError` on a venv file read** (`PermissionError ... sniffio\\__init__.py`) instead of run 1's temp-dir shape (`FileNotFoundError: No usable temporary directory`). That the two symptoms belong to the same permission-restricted execution space is **INFERRED** — consistent, but the differing surface was not chased to a single cause beyond what the checker's own outputs record.
3. **The exact flag inventory used for the real `verify_turn1`/`verify_turn2` dispatches.** The closeout's `despatches[]` receipts record lane, required arm, used rank and transport model but no per-attempt flag list, and no dispatch receipt JSON with `--sandbox`/`--allow-human-home-transport`/`--require-arm` values was found in the read set. The (c)/(d) analysis of which sandbox plane produced the denials is therefore **INFERRED from the checker's recorded outputs plus the dispatcher/pool source, not read off a stored receipt that names the flags**.
4. **The current truth of the VERIFY rank-2 arm's transport at this moment** — its reachability class is a *recorded* status (`REACHABLE_VIA_HUMAN_HOME_TRANSPORT`, `measured` block with `relay` http 404 + `human_home_probe` 200); no current re-verification by this pass; only the recorded/remeasured class standings the given texts state.

---

## Receipts

### Files read in full, as evidence:

- `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/S4_R6_CLOSEOUT_RETURN/checker_verdict.json` — 53 lines; `despatches[]` (turn1/turn2 receipts), `qualification_limits[]`, `claim_ceiling`, `verdict: PARTIAL`.
- `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/lane/verify/verdict_text_run1.txt` — full text, py1 pytest at tool-items section: #7 (temp dirs, FileNotFoundError from Python with the quoted list of all 10 candidate temp dir paths tried, each refused), #13 (URLError WinError 10013), #16 (warning about `.pytest_cache/` permission denied), tool receipts for both the header paragraphs and the tail paths.
- `C:/Projects/Agent_Workspace/_handover/PIPD-S4-R6-CLOSEOUT-20261016/lane/verify/verdict_text_run2.txt` — full text; explicit NOT_RUN records for pytest (`PermissionError: [Errno 13] ... sniffio\\__init__.py`) and the release fetch (`URLError ... WinError 10013`); `web.open` tool receipt (`empty; no artifact bytes obtained`); final nonce marker `HGK_LANE_NONCE_OK` (the dispatcher's `--nonce` default, confirming run2 passed the nonce check), `verdict: PARTIAL`.
- `C:/Projects/Agent_Workspace/HG-KSEOS/scripts/hgk-lane-dispatch.py` — read in full (2275 lines).
- `C:/Projects/Agent_Workspace/HG-KSEOS/config/lane-route-slots.candidate.json` — read in full (533 lines).
- `C:/Projects/Agent_Workspace/HG-KSEOS/config/lane-routing-registry.yaml` — read in full (700 lines).

### Values quoted verbatim by line number:

- `scripts/hgk-lane-dispatch.py:90` — `SANDBOX_BY_LANE = {"EXECUTE": "danger-full-access", "VERIFY_SECURITY": "read-only", "PLAN": "read-only"}`.
- `scripts/hgk-lane-dispatch.py:91` — `SANDBOX_RANK = {"read-only": 0, "workspace-write": 1, "danger-full-access": 2}`.
- `scripts/hgk-lane-dispatch.py:83-89` — the T5/T5b/T6 MEASURED comment block on workspace-write being no-op on this host and danger-full-access being the only real executor.
- `scripts/hgk-lane-dispatch.py:18` and `:22` — "Sandbox defaults are role-shaped: a checker is read-only; a writer gets danger-full-access" / "A sandbox stricter-than-role default may only be escalated with --allow-sandbox-escalation, so a single flag cannot give a checker lane writer-grade access".
- `scripts/hgk-lane-dispatch.py:1678` — definition of `escalated`.
- `scripts/hgk-lane-dispatch.py:1679-1683` — `ERR_SANDBOX_ESCALATION_REFUSED` refusal message (quoted exactly above).
- `scripts/hgk-lane-dispatch.py:1853-1860` — `ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER` refusal message (quoted exactly above).
- `scripts/hgk-lane-dispatch.py:1398-1403` — `--guard-subject` / `--allow-unguarded-escalation` flag declarations and their semantics strings.
- `scripts/hgk-lane-dispatch.py:1082-1086` — `codex_home_config.windows_sandbox` injection on the argv, gated by `required_for_modes: ["read-only", "workspace-write"]`.
- `scripts/hgk-lane-dispatch.py:1395-1397` — `--require-arm` semantics (fail-closed).
- `scripts/hgk-lane-dispatch.py:1709-1715` — `ERR_LANE_HOME_NOT_ISOLATED` refusal instructing `pass --allow-human-home-transport to acknowledge it`.
- `scripts/hgk-lane-dispatch.py:2263` — `ERR_CHECKER_MUTATED_SUBJECT` voiding the verdict and the guard's own meaning.
- `config/lane-route-slots.candidate.json:228-246, 247-265, 266-299` (EXECUTE rank 1/2/3) and `:317-333, 334-350, 351-370, 371-402` (VERIFY_SECURITY rank 1/2/3/4) — the ordered pools and their per-arm `feasibility`/`dispatchable` fields (tables reproduced verbatim above).
- `config/lane-route-slots.candidate.json:80-85` — `selection_semantics` incl. `"sod": "NOT enforced at this revision (owner D1)"`.
- `config/lane-route-slots.candidate.json:404` — `selection_note` stating deepseek-v4.1-flash is rank 1 for VERIFY/SECURITY *declared in sod_invariants.declared_conflicts as SOD006-C3*.
- `config/lane-routing-registry.yaml:222-277` (EXECUTE route row) and `:278-350` (VERIFY_SECURITY route row, arms A/B/C incl. arm B = openai-codex/gpt-6.1-sol, role fallback1_operator_selectable, `prior_revision_note`) — plus `:350` `admission_status: UNPROVEN` on VERIFY_SECURITY.
- `config/lane-routing-registry.yaml:401-431` — `sod_invariants.declared_conflicts[SOD006-C1, C3, C2]` and their `status: OWNER_ORDERED_IN_FORCE` / `SUPERSEDED` / (C2, C1) / `OPEN` (SOD-APPLY-01) classification text.
- `config/lane-routing-registry.yaml:141-142` and `:79-87` — `source_of_routes` (`path: config/model-lane-assignment.json`, `revision: 22`) and Transport Model Constraints block mentioning the openai-codex entry needs the bare id.

### Explicitly NOT done (boundary)

- No repository file was written, edited, or removed anywhere; the only file created by this pass is this dossier. The proposed pool reorder in Question 2 is `NOT APPLIED` — it exists only as the fenced candidate diff recorded in this dossier.
- No lane dispatch was re-run (read-only pass); the (d) command above is a statement of the exact line, not a measured turn.
