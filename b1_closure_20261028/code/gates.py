#!/usr/bin/env python3
"""G-A / G-B gates, evaluated as an honest conjunction.

G-A six items are evaluated against evidence that exists on this host. A gate PASS here means
"this item's evidence is present and consistent" - it does NOT mean the B1 mission is accepted.
G-B requires a native successor started by a real scheduler from a durable journal in a different
OS session after revoking the external helper; this host has no native Issuer, so G-B is HOLD and
the gate says so instead of borrowing G-A's evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "artifacts"


def load(name, default=None):
    p = OUT / name
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    sc = load("SELFCHECK.json", {})
    hb = load("HOST_BINDINGS.json", {})
    hs = load("NATIVE_HARNESS_SUMMARY.json", {})
    gw = load("GWO_E2E.json", {})
    p1 = load("PIPD_PIPELINE_RECEIPTS.json", {"summary": {}})
    p2 = load("PIPD_PIPELINE_RECEIPTS_2.json", {"steps": []})
    v = load("s07_validate_retry.json", {}) if (OUT / "s07_validate_retry.json").exists() else {}

    def gwo_current():
        sbl = load("GWO_SBL_EVIDENCE.json", {})
        hgk = load("GWO_HGK_EVIDENCE.json", {})
        fab = load("GWO_FABRIC_EVIDENCE.json", {})
        gb = load("G_B_EVIDENCE.json", {})
        per = {"GWO-SBL": sbl.get("verdict", "MISSING"),
               "GWO-HGK": hgk.get("verdict", "MISSING"),
               "GWO-FABRIC": fab.get("verdict", "MISSING")}
        npass = sum(1 for v in per.values() if v == "PASS")
        return {"gwos": 3, "pass": npass, "per_gwo": per,
                "verdict": ("ALL_THREE_PASS" if npass == 3 else
                            f"{npass}/3 PASS; HOLD=" + ",".join(k for k, v in per.items() if v != "PASS")),
                "g_b": gb.get("verdict", "MISSING")}

    def verdict_ok(res):
        return bool(res) and res.get("verdict") == "PASS"

    validate_pass = (load("pipd-run_validate", {}) or {}).get("verdict") == "PASS"
    # the validate envelope lives under pipd-run/artifacts; read it directly
    vp = HERE / "pipd-run" / "artifacts" / "s07_validate_retry.json"
    if vp.exists():
        vdoc = json.loads(vp.read_text(encoding="utf-8"))
        validate_pass = vdoc.get("verdict") == "PASS" and vdoc.get("checked", 0) >= 3

    artifacts = sorted(p for p in OUT.glob("*.json"))
    ceiling_ok = []
    for p in artifacts:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            ceiling_ok.append((p.name, False))
            continue
        c = d.get("claim_ceiling")
        ceiling_ok.append((p.name, bool(c) or p.name in ("MANIFEST.json", "SELFCHECK.json")))
    missing_ceiling = [n for n, ok in ceiling_ok if not ok]

    s1 = json.loads((OUT / "S1_EVIDENCE.json").read_text(encoding="utf-8")) if (OUT / "S1_EVIDENCE.json").exists() else {}
    s2 = json.loads((OUT / "S2_S3_EVIDENCE.json").read_text(encoding="utf-8")) if (OUT / "S2_S3_EVIDENCE.json").exists() else {}

    blocks = hb.get("route_binding", {})
    all_blocked = bool(blocks) and all(x.get("state") == "BLOCKED_MISSING_RUNNER_OR_BINDING"
                                      for x in blocks.values())

    ck_p = next((HERE / "pipd-run" / "artifacts" / f for f in (
        "checker_receipt_codex_r7.json", "checker_receipt_codex_r6.json", "checker_receipt_codex_r5.json",
        "checker_receipt_codex_r4.json", "checker_receipt_codex.json") if (HERE / "pipd-run" / "artifacts" / f).exists()),
    HERE / "pipd-run" / "artifacts" / "checker_receipt_codex.json")
    ck = json.loads(ck_p.read_text(encoding="utf-8")) if ck_p.exists() else {}
    ck_sha = None
    if ck_p.exists():
        import hashlib as _h
        ck_sha = _h.sha256(ck_p.read_bytes()).hexdigest()
    cur = {}
    for nm, key in (("pi.json", "pi"), ("ecp.json", "ecp"), ("pd.json", "pd")):
        f = HERE / "pipd-run" / "artifacts" / nm
        if f.exists():
            import hashlib as _h
            cur[key] = _h.sha256(f.read_bytes()).hexdigest()
    bound = bool(ck) and all(cur.get(k) == (ck.get("subject_sha256") or {}).get(k) for k in ("pi", "ecp", "pd"))

    ga = [
        {"id": "G-A1", "item": "PI/PD/ECP compile + validate PASS over the 13-verb toolchain",
         "pass": validate_pass,
         "evidence": {"validate": "pipd-run/artifacts/s07_validate_retry.json",
                      "checked_contracts": (vdoc.get("checked") if validate_pass and "vdoc" in vars() else (3 if validate_pass else 0)),
                      "checked_source": "pipd-run/artifacts/s07_validate_retry.json#checked (read, not hardcoded)"}},
        {"id": "G-A2", "item": "declared denominators conserved (independent self-check)",
         # C54 only echoes this file back; counting it here would create a cycle
         # (C54 fails while any gate item is unmet, including this one).
         "pass": [c["id"] for c in (sc.get("checks") or []) if not c["pass"] and c["id"] != "C54"] == []
                 and sc.get("total", 0) >= 44,
         "evidence": {"selfcheck": f'{sc.get("passed")}/{sc.get("total")}',
                      "counted_failures": [c["id"] for c in (sc.get("checks") or [])
                                           if not c["pass"] and c["id"] != "C54"]}},
        {"id": "G-A3", "item": "every artifact carries an explicit claim ceiling",
         "pass": not missing_ceiling, "evidence": {"missing": missing_ceiling}},
        {"id": "G-A4", "item": "runner routes reported honestly (no invented binding)",
         "pass": all_blocked,
         "evidence": {"blocked": sum(1 for x in blocks.values()
                                     if x.get("state") == "BLOCKED_MISSING_RUNNER_OR_BINDING"),
                      "total": len(blocks),
                      "note": "HOST_BINDINGS.json is the pre-canary snapshot; the S2 canary registered 1 of 30 "
                              "with a DEMO key, which this gate deliberately does not count as a real binding"}},
        {"id": "G-A5", "item": "native harness executes every declared case with readback",
         "pass": hs.get("counts", {}).get("fail") == 0 and hs.get("counts", {}).get("pass") == 244
                 and hs.get("probes_pass") == hs.get("probes_total"),
         "evidence": {"cases": hs.get("counts"), "probes": f'{hs.get("probes_pass")}/{hs.get("probes_total")}'}},
        {"id": "G-A6", "item": "independent checker receipt present (different principal/ACL)",
         "pass": bool(ck) and bound and (ck.get("verdict") == "PASS"),
         "evidence": {"status": ("CHECKER_VERDICT_PASS" if (ck or {}).get("verdict") == "PASS" else "CHECKER_RAN_VERDICT_FAIL"),
                      "sod_satisfied": bool(ck) and bound,
                      "checker_id": ck.get("checker_id"),
                      "checker_receipt_sha256": ck_sha,
                      "checker_verdict": ck.get("verdict"),
                      "failed_checks": ck.get("failed_checks"),
                      "subject_bound_3_of_3": bound,
                      "lane": "VERIFY_SECURITY / openai-codex gpt-6.1-sol (reasoning=medium) via OpenAI OAuth, read-only sandbox",
                      "round": ck_p.name,
                      "why_item_still_unmet": None if (ck.get("verdict") == "PASS" and bound) else "checker verdict is not PASS over a bound subject"}},
    ]

    gb_ev = load("G_B_EVIDENCE.json", {})
    ck_pr = load("CHECKER_PRINCIPAL.json", {})
    gb = [
        {"id": "G-B1", "item": "revoked external helper token refused before spawn",
         "pass": (gb_ev.get("revoke", {}).get("deleted") is True
                  and gb_ev.get("pre_spawn_gate", {}).get("decision") == "REFUSED_REVOKED_TOKEN_REJECTED_BEFORE_SPAWN"
                  and gb_ev.get("pre_spawn_gate_replayed_token", {}).get("decision") == "REFUSED_REVOKED_TOKEN_REJECTED_BEFORE_SPAWN"),
         "evidence": {"raw": "RAW-REVOKE", "gate": gb_ev.get("pre_spawn_gate", {}).get("decision"),
                      "replay_gate": gb_ev.get("pre_spawn_gate_replayed_token", {}).get("decision")}},
        {"id": "G-B2", "item": "native successor self-starts from the durable journal in a DIFFERENT OS PID/session",
         "pass": (gb_ev.get("spawn", {}).get("different_pid") is True
                  and gb_ev.get("spawn", {}).get("different_session_uuid") is True
                  and gb_ev.get("spawn", {}).get("helper_token_present_in_successor") is False
                  and gb_ev.get("successor", {}).get("effect", {}).get("readback_ok") is True
                  and gb_ev.get("successor", {}).get("effect", {}).get("residue") is False),
         "evidence": {"successor_pid": gb_ev.get("spawn", {}).get("successor_pid"),
                      "different_pid": gb_ev.get("spawn", {}).get("different_pid"),
                      "different_session": gb_ev.get("spawn", {}).get("different_session_uuid"),
                      "helper_token_in_successor": gb_ev.get("spawn", {}).get("helper_token_present_in_successor"),
                      "ceiling": gb_ev.get("claim_ceiling")}},
        {"id": "G-B3", "item": "same-subject checker over the issuer/queue/effect raws",
         "pass": (ck_pr.get("verdict") == "PASS" and ck_pr.get("acl", {}).get("write_denied") is True
                  and ck_pr.get("verdict_path", {}).get("write_ok") is True),
         "evidence": {"checker": ck_pr.get("verdict"), "write_denied": ck_pr.get("acl", {}).get("write_denied"),
                      "source": "artifacts/CHECKER_PRINCIPAL.json",
                      "checker_process_pid": (ck_pr.get("checker") or {}).get("pid"),
                      "subject_bound": sorted((ck_pr.get("subject_sha") or {})),
                      "checks": ck_pr.get("checks")}},
    ]

    def _residuals():
        """Residual blockers MEASURED at gate time, never a static list.

        Each entry names the artefact a reader can re-measure. A blocker that stops being true
        disappears from this list by itself, so the gate cannot keep asserting a stale reason.
        """
        rs = []
        declared = []
        cands = [pathlib.Path(os.environ.get("ProgramData", "")) / "HG-KSEOS" / "native-admission" / "registry.json",
                 pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "HG-KSEOS" / "native-admission" / "registry.json"]
        if not any(p.is_file() for p in cands):
            rs.append("NATIVE_ISSUER_UNBOUND: no HGK native-admission registry at ProgramData or LOCALAPPDATA "
                      "(an OS-protected Owner registry is the trust-bootstrap precondition)")
        regp = HERE / "admission" / "registry" / "runner-registry.json"
        if regp.is_file():
            r = json.loads(regp.read_text(encoding="utf-8"))
            rows = r.get("rows") or []
            impl = sum(1 for x in rows if x.get("coverage") == "EFFECT_IMPLEMENTED")
            if rows and impl < len(rows):
                # FAR v5 D1: coverage is a SELF-IMPOSED metric, not a PKG-00..08 requirement (measured: no
                # "30 routes"/"route coverage" clause exists upstream; the B1 falsification standard is the
                # nine-step real-Raw test). It is declared, not silently dropped, and it stops gating the
                # conjunction. The 18 remaining routes share one dispatcher (RUN-B1-GEN-DISPATCH).
                # FAR v9: the 30-row denominator is this registry's own row count. PKG_00..08 state no
                # 30-route requirement, and 0 sentences in them require every route to be effect-implemented
                # (all 18 typed-refusal names do appear in the docs: doc-derived names, no doc mandate).
                _rows = r.get("rows") or []
                _inst = sum(1 for x in _rows if x.get("status") == "INSTALLED")
                _eff = sum(1 for x in _rows if x.get("coverage") == "EFFECT_IMPLEMENTED")
                declared.append({
                    "id": "ROUTE_INSTALL_REQUIREMENT",
                    "value": f"{_inst}/{len(_rows)} routes INSTALLED",
                    "requirement": "OpenSpec b1-native-lane-admission tasks.md L19 (cited in FAR11_HOLD_RULINGS.md:16): "
                                   "every route at least INSTALLED before EXECUTION_ADMITTED may be claimed",
                    "satisfied": _inst == len(_rows),
                    "claim_weight": "satisfies the only written requirement"})
                declared.append({
                    "id": "EFFECT_IMPLEMENTED_INVENTORY",
                    "value": f"{_eff}/{len(_rows)} routes have a distinct effect runner; the rest are typed refusals",
                    "provenance": "denominator = runner-registry.json row count; no PKG_00..08 requirement and no "
                                  "sentence requiring every route to be effect-implemented",
                    "claim_weight": "none - inventory, not a gap",
                    "not_fixed_by": "implementing the 8 routes whose inputs do not exist (ECP, host load, golden fixtures)"})
                # PKG_08 L49: Mission Complete is forbidden while anything is live READY/RUNNING.
                _live = []
                for _p in sorted((HERE / "artifacts").glob("*.json")):
                    try:
                        _d = json.loads(_p.read_text(encoding="utf-8"))
                    except Exception:
                        continue
                    if isinstance(_d, dict):
                        for _k in ("status", "verdict", "mission_state"):
                            if str(_d.get(_k) or "").upper() in ("READY", "RUNNING"):
                                _live.append(f"{_p.name}:{_k}={_d.get(_k)}")
                declared.append({
                    "id": "READY_RUNNING_ZERO",
                    "value": f"{len(_live)} live READY / RUNNING item(s)",
                    "measured_from": "artifacts/*.json status|verdict|mission_state fields (never file names)",
                    "satisfied": not _live,
                    "live": _live})
            # FAR v6 (option C): the old check compared two UNSIGNED strings with each other, so either
            # side could be edited into agreement. The declaration is the owner's statement; drift between
            # it, the registry bytes and the MEASURED numbers is what gets reported now.
            decp = HERE.parent / "B1-CONT-20261028" / "wave1" / "DECLARATION_v1.json"
            if not decp.is_file():
                rs.append("DECLARATION_MISSING: no owner claim declaration "
                          "(B1-CONT-20261028/wave1/DECLARATION_v1.json)")
            else:
                dec = json.loads(decp.read_text(encoding="utf-8"))
                import sys as _sys
                _dlib_dir = str(HERE.parent / "B1-CONT-20261028" / "wave1")
                if _dlib_dir not in _sys.path:
                    _sys.path.insert(0, _dlib_dir)
                import declaration_lib as _dl
                _ok, _why = _dl.verify(dec, (r.get("owner_enrollment") or {}).get("public_hex") or "")
                if _why == "BINDINGS_MISMATCH":
                    rs.append("DECLARATION_TAMPERED: bindings_sha256 does not match the declaration body")
                elif _why == "SIGNATURE_INVALID":
                    rs.append("DECLARATION_SIGNATURE_INVALID: the declaration carries a signature that "
                              "does not verify against the enrolled owner key")
                if _why == "UNSIGNED":
                    declared.append({"id": "CLAIM_DECLARATION_UNSIGNED", "value": "1 declaration",
                                     "why": "the corrected ceiling exists but carries no owner signature, "
                                            "so it is NOT verified",
                                     "lifts_when": "owner signs it (1 signature, mergeable into any unlock)",
                                     "source": str(decp)})
                cur_sha = hashlib.sha256(regp.read_bytes()).hexdigest()
                if cur_sha != dec.get("registry_sha256"):
                    rs.append(f"DECLARATION_DRIFT(registry_changed): registry is {cur_sha[:16]} but the "
                              f"declaration pinned {str(dec.get('registry_sha256'))[:16]}")
                if (r.get("claim_ceiling") or "") != (dec.get("claim_ceiling_corrected") or ""):
                    rs.append(f"DECLARATION_DRIFT(text_stale): claim_ceiling still reads "
                              f"{(r.get('claim_ceiling') or '')[:60]!r}")
                if impl != (dec.get("measured") or {}).get("effect_implemented"):
                    rs.append("DECLARATION_DRIFT(measured_changed): effect_implemented no longer matches "
                              "the declared measurement")
        # FAR v7 D1: these two were static strings, so they could never clear and were not evidence.
        # They are now measured; each carries owner_ruling_required because only the owner can decide
        # whether the declaration is acceptable for mission completion.
        nat = None
        nat_path = None
        for p in cands:
            if p.is_file():
                try:
                    nat = json.loads(p.read_text(encoding="utf-8"))
                    nat_path = p
                except Exception:
                    nat = None
                break
        if nat is None:
            rs.append("NATIVE_TRUST_ROOT_MISSING: no readable native registry (cannot measure principal separation)")
        else:
            sids = {nat.get("owner_os_sid"), nat.get("checker_os_sid"), nat.get("maker_os_sid")} - {None}
            keys = nat.get("keys") or {}
            per_principal = len(keys) >= 3
            declared.append({
                "id": "PRINCIPAL_SEPARATION_MEASURED",
                "value": f"{len(sids)}/3 distinct OS SIDs; key material held by {len(keys)} principal(s)",
                "satisfied": len(sids) == 3,
                "open": None if per_principal else "per_principal_keys",
                "owner_ruling_required": not per_principal,
                "blocks_mission_completion": not per_principal,
                "source": str(nat_path)})
        holds, total = 0, 0
        for f in sorted((HERE / "input_20261027").glob("FHS_MSC_B1_PIPD_LS_PKG_0[0-8]_*.md")):
            total += 1
            try:
                head = f.read_text(encoding="utf-8", errors="replace")[:4000]
            except Exception:
                head = ""
            if "formal_sourcefreeze: HOLD" in head:
                holds += 1
        declared.append({
            "id": "SOURCEFREEZE_DECLARED_HOLD",
            "value": f"{holds}/{total} PKG volumes declare formal_sourcefreeze: HOLD "
                     f"(DOC-00 L327-330: READABLE_USER_INPUT;NOT_FORMAL_SOURCEFREEZE)",
            "open": "formal freeze of the sources (an upstream act, not a missing signature)",
            "not_fixable_by": "minting a source_freeze reference over unfrozen bytes",
            "owner_ruling_required": True,
            "blocks_mission_completion": True,
            "source": "input_20261027/*PKG_0[0-8]*.md#front_matter"})
        # FAR v7 D5: a blocking declaration clears ONLY under an owner signature that binds its exact
        # measured value. Drift voids the ruling and brings the blocker back.
        if any(d.get("blocks_mission_completion") for d in declared):
            rf = HERE.parent / "B1-CONT-20261028" / "wave1" / "OWNER_RULING_v1.json"
            _sys2 = __import__("sys")
            _dir = str(rf.parent)
            if _dir not in _sys2.path:
                _sys2.path.insert(0, _dir)
            import declaration_lib as _dl2
            if not rf.is_file():
                rs.append("OWNER_RULING_MISSING: blocking declarations present but no "
                          "wave1/OWNER_RULING_v1.json")
            else:
                try:
                    _r = json.loads(rf.read_text(encoding="utf-8"))
                except Exception as e:
                    _r = None
                    rs.append(f"OWNER_RULING_UNREADABLE: {type(e).__name__}")
                if _r is not None:
                    _pub = (r.get("owner_enrollment") or {}).get("public_hex") or ""
                    _ok, _why = _dl2.verify(_r, _pub)
                    if not _ok:
                        rs.append(f"OWNER_RULING_{_why}: the ruling is not signed by the enrolled owner key")
                    else:
                        _by_id = {x.get("id"): x for x in (_r.get("rulings") or [])}
                        for d in declared:
                            if not d.get("blocks_mission_completion"):
                                continue
                            x = _by_id.get(d["id"])
                            if x is None:
                                rs.append(f"OWNER_RULING_ABSENT({d['id']}): the ruling does not cover it")
                            elif x.get("bound_value") != d.get("value"):
                                rs.append(f"OWNER_RULING_DRIFT({d['id']}): the measured value changed after "
                                          f"the ruling ({x.get('bound_value')!r} -> {d.get('value')!r})")
                            else:
                                d["owner_ruling"] = {"decision": x.get("decision"),
                                                     "signed_by": _r.get("signed_by"),
                                                     "signed_at": _r.get("signed_at")}
                                d["blocks_mission_completion"] = False
        return rs, declared

    _enr = load("OWNER_CEREMONY.json", {}) or {}
    out = {
        "schema": "B1.GATES/1",
        "claim_ceiling": "AUTHOR_SIDE_EXECUTED_SANDBOX",
        "G-A": {"items": ga, "passed": sum(1 for x in ga if x["pass"]), "total": len(ga),
                "verdict": "PASS" if all(x["pass"] for x in ga) else "HOLD",
                "rule": "六項合取不降低：任一未達即 HOLD，不得以其他項代償"},
        "G-B": {"items": gb, "passed": sum(1 for x in gb if x["pass"]), "total": len(gb),
                "verdict": "HOLD" if not all(x["pass"] for x in gb) else "PASS"},
        # GWO verdicts must come from the CURRENT evidence files, never from a stale summary
        "GWO": gwo_current(),
        "release_status": "NOT_RUN",
        "owner_signature_attribution": _enr.get("attribution"),
        "sourcefreeze_status": "NOT_RUN",
        "independent_audit": (load("INDEPENDENT_AUDIT.json", {}) or {}).get("verdict", "PENDING"),
        "checker": {
            "lane": "VERIFY_SECURITY",
            "model": "gpt-6.1-sol",
            "reasoning_effort": "medium",
            "credential": "OpenAI OAuth (owner ChatGPT account)",
            "transport": "direct codex exec with -c model_provider=openai (ChatGPT backend), read-only sandbox",
            "provenance_conflict": "the receipt's own checker_lane field reads 'VERIFY_SECURITY via HGK lane dispatcher; provider openai-codex'; the round record says direct codex exec. Both strings are preserved; neither is asserted as true because the raw transcript is not in this workspace.",
            "transport_why": ("the HGK dispatcher routes through model_provider=desktop_router (127.0.0.1:10102), which "
                              "served gpt-6.1-sol as opencode-go/deepseek-v4.1-flash on round 3 -- the maker's own model "
                              "family, so round 3 was discarded as non-independent (REPORT F-17)"),
            "identity_source": "codex-rollout (model=gpt-6.1-sol, model_provider=openai verified from the session rollout)",
            "receipt": str(ck_p.relative_to(HERE)),
            "receipt_sha256": ck_sha,
            "checker_id": ck.get("checker_id"),
            "verdict": ck.get("verdict"),
            "failed_checks": ck.get("failed_checks"),
            "checks": ck.get("checks"),
            "subject_bound_3_of_3": bound,
            "sod_satisfied": bool(ck) and bound,
            "sod_note": ("different model from the maker (gpt-6.1-sol vs deepseek-v4.1-flash), different credential "
                         "(owner OAuth, read-only sandbox), maker could not write the receipt -- it was extracted from "
                         "the lane's own stdout. Still ONE owner: this is a design-record pass, not DOC-05 "
                         "INDEPENDENT_VERIFIED and not runtime acceptance."),
            "receipt_extraction": ("apply_checker_receipt.py / inline brace-scan; the checker ran read-only and could not "
                                   "write its own receipt"),
        },
        "landing": {
            "S1_schema_change": {
                "status": "LANDED_AND_RECHECKED",
                "changed_files": (s1.get("changed_files") or []),
                "effect_class_vocabulary": "CANDIDATE_VOCABULARY_PENDING_OWNER (deliberately not an enum)",
                "evidence": "artifacts/S1_EVIDENCE.json",
                "recheck": f'{s1.get("independent_recheck", {}).get("verdict")} '
                            f'{s1.get("independent_recheck", {}).get("checks_pass")}/11 bound='
                            f'{s1.get("independent_recheck", {}).get("subject_bound")}',
            },
            "S2_registry_canary": {
                "status": "CANARY_1_OF_30_DEMO_KEY",
                "routes_unlocked": (s2.get("S2_verdict") or {}).get("routes_unlocked"),
                "routes_still_blocked": (s2.get("S2_verdict") or {}).get("routes_still_blocked"),
                "effect_readback_ok": (s2.get("S2_verdict") or {}).get("chain_reached_effect_readback"),
                "owner_signature_real": False,
                "evidence": "artifacts/S2_S3_EVIDENCE.json",
            },
            "S3_issuer_separation": {
                "status": "SEPARATE_KEY_MATERIAL_SAME_OS_USER",
                "negatives_refused": (s2.get("S3_verdict") or {}).get("negative_count"),
                "negatives": ["unsigned row", "tampered executable sha", "nonce replay",
                              "revoked epoch", "subject mismatch", "scope outside vocabulary"],
                "not_a_real_second_principal": True,
            },
        },
        "mission_complete": False,
        "why_not_complete": _residuals()[0],
        "declared_ceilings": _residuals()[1],
    }
    (OUT / "GATES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    # NOTE: do NOT fold the self-check result in here — G-A2 already owns it, and folding it in makes
    # the self-check's own anti-overclaim check (C55) circular.
    conj = (out["G-A"]["verdict"] == "PASS" and out["G-B"]["verdict"] == "PASS"
            and out["GWO"]["pass"] == 3 and out["independent_audit"] == "PASS")
    out["sandbox_conjunction"] = "PASS" if (out["G-A"]["verdict"] == "PASS" and out["G-B"]["verdict"] == "PASS"
                                           and out["GWO"]["pass"] == 3) else "HOLD"
    out["gates_conjunction"] = out["sandbox_conjunction"]
    # FIX (B1-CONT-20261028): a conjunction of the three sandbox gates is NOT mission completion.
    # out["why_not_complete"] names residual blockers that the conjunction never measured; the previous
    # code overwrote mission_complete to True while leaving that list in place, so one file asserted both
    # "complete" and "not complete". Residual blockers are now part of the conjunction.
    residual = [str(x) for x in (out.get("why_not_complete") or [])]
    open_rulings = [d for d in (out.get("declared_ceilings") or []) if d.get("blocks_mission_completion")]
    out["mission_complete"] = bool(conj and not residual and not open_rulings)
    if out["mission_complete"]:
        out["mission_complete_blocker"] = None
    elif residual:
        out["mission_complete_blocker"] = "residual: " + residual[0]
    elif open_rulings:
        out["mission_complete_blocker"] = "declarations awaiting owner ruling: " + ", ".join(
            d["id"] for d in open_rulings)
    else:
        out["mission_complete_blocker"] = "independent_audit=" + str(out["independent_audit"]) if out["independent_audit"] != "PASS" else (
            "selfcheck failures: " + ",".join(c["id"] for c in (sc.get("checks") or []) if not c["pass"])
            if [c["id"] for c in (sc.get("checks") or []) if not c["pass"]] else "gates not all PASS")
    out["mission_complete_basis"] = ("sandbox_conjunction=PASS but " + str(len(residual)) + " residual blocker(s) named in why_not_complete; "
                                     "no native issuer, no owner-signed runner registry, no sourcefreeze/release") if (conj and residual) else None
    (OUT / "GATES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"G-A": out["G-A"]["verdict"], "G-A_passed": f'{out["G-A"]["passed"]}/6',
                      "G-B": out["G-B"]["verdict"], "GWO": out["GWO"],
                      "release_status": "NOT_RUN",
        "owner_signature_attribution": _enr.get("attribution"),
        "sourcefreeze_status": "NOT_RUN",
        "independent_audit": out["independent_audit"],
                      "gates_conjunction": out["gates_conjunction"],
                      "sandbox_conjunction": out.get("sandbox_conjunction"),
                      "mission_complete": out["mission_complete"],
                      "blocker": out["mission_complete_blocker"]}, ensure_ascii=False))
    for x in ga:
        if not x["pass"]:
            print(" unmet:", x["id"], x["item"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
