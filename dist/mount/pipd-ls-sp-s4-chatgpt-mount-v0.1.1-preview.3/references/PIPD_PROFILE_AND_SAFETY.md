# PIPD_PROFILE_AND_SAFETY — LITE / STANDARD / ASSURED and the fail-closed rule

> Release identity: **v0.1.1-preview.3** — release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`.
> Derived, read-only content. Source: `src/pipd_ls_sp/profiles.py`, `schemas/ProfileBinding.schema.json`.

## The three profiles

The profile selector resolves a requested profile and an axis set into an effective **ProfileBinding**.
Exactly three profiles exist.

| profile | artifact depth | assurance | target resolution | max axes |
| --- | --- | --- | --- | --- |
| `LITE` | `L1_SCHEMA_CONTRACT` | deterministic_validator | package | 3 |
| `STANDARD` | `L3_INTEGRATION_RUNTIME` | deterministic_validator, negative_security | integration | 6 |
| `ASSURED` | `L4_FAILURE_RECOVERY` | deterministic_validator, negative_security, adversarial, independent_checker | runtime | 10 |

The **nine canonical axes** driving the veto: `intent`, `knowledge`, `verification`, `release`,
`trust_boundary`, `preexisting_repo`, `profile`, `tech_candidates`, `host_surface`.

## Behaviour: one normalisation, fail-closed

The selector and the emitted record are derived from the **same normalised axis list**, so the
escalation basis and the shipped binding can never disagree. It refuses, typed, when:

- the requested profile is not `LITE | STANDARD | ASSURED`;
- the axis set is not a list of non-empty strings;
- an axis appears **more than once** (duplicates are refused, not silently de-duplicated);
- an axis is **unknown** (not one of the nine canonical axes).

The axis **count** is a complexity proxy that drives escalation. It is **never** presented as a risk
score.

## Rule: unknown risk is NOT_ASSESSED, never low-risk

Risk evidence is an **input**. When no risk evidence is supplied, the emitted record marks the risk
assessment as:

```
risk_assessment = "NOT_ASSESSED"
```

and `vetoes` stays `[]`. **No `LOW_RISK_VERIFIED` and no "low-risk" verdict is ever minted without
evidence.** A design assistant must therefore:

- say "not assessed" (or `NOT_ASSESSED`) rather than "low-risk", "safe", "verified" or "no risk";
- refuse an ask to declare a risk level the host did not compute (`UNKNOWN_RISK_NOT_ASSESSED`).

## What this does not claim

- `LITE` does not execute a per-axis risk assessment. It now **states** that absence instead of
  implying an assessment ran.
- No profile implies a production readiness or a live host certification.
- The chat host computes no profile at all; it only helps a user reason about one. The actual
  computation runs in an authorised executor.

## Source Locators

Bound to `v0.1.1-preview.3` (release tag target `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`; build source commit `cbf69756d7fc90fc1cdfb3a45a1cc42cc603cb0a`).

| object | source locator |
| --- | --- |
| profile trio + normalisation | `src/pipd_ls_sp/profiles.py` |
| profile record contract | `schemas/ProfileBinding.schema.json` |
| pipeline profile record | `src/pipd_ls_sp/pipeline.py` |
| router axes | `dist/web/PIPD_ROUTER_PROFILES.md` |
| profile skill | `skills/pipd-profile-tailor/SKILL.md` |
| risk fail-closed pin | `tests/test_postrelease_contract_hardening.py` |

Derived content; no normative body copied. No token, credential or PII.
