# HOST UAT - Hermes Agent (canonical HERMES_HOME), UPG-G08 scoped

**Status: `PARTIAL` - trust and discovery VERIFIED, effective load NOT verified.**
This is NOT a Host pass, and must not be reported as one.

## What actually ran

| Step | Command shape | Raw result |
|---|---|---|
| trust | `python -B -m hermes_cli.main skills trust <project>` | `Trusted: ...\\verify\\uat\\hermes\\project` ; `8 project skill(s) will load in sessions started inside this repo (they take precedence over same-named profile skills).` |
| POS probe | one-shot session started inside the trusted project, asking only which `pipd-*` skills are loaded | all 8 names returned: `pipd-assurance-tqaep, pipd-authority-source, pipd-execution-contract, pipd-package-project, pipd-pd-bind, pipd-pi-compile, pipd-profile-tailor, pipd-route-intake` - **the model itself qualified this as "directory visible only, contents not loaded"** |
| non-trigger probe | one-shot session, off-topic question (weather) | `NONTRIGGER_OK` - no pipd workflow fired |

## Why this is PARTIAL and not a pass

The PIPD host contract (UPG-G08 / TR-27) separates **site loaded** from **files discovered**.
The probe session could *see the directory listing* of the eight skills, and it said so out loud.
It never demonstrated that a skill body was loaded and acted on by a triggering task, which is the
`discover -> effective load -> invoke` edge the gate actually requires.

* discovery of the 8 names inside a trusted project: **VERIFIED**
* skill body actually loaded into the session and applied to a bounded PIPD task: **NOT VERIFIED**
* positive PIPD PI/PD/ECP/TQAEP task, typed NACK on missing source, adversarial self-approve /
  token-print probe: **NOT RUN**

## Required to convert this to a scoped Host pass

Run the four fixed scenarios (UAT-POS-01, UAT-NONTRIG-02, UAT-REFUSE-03, UAT-ADV-04) inside the same
trusted project, capture the full transcript per scenario, and show a skill body being applied -
not merely listed. Until then the Hermes row stays `PARTIAL / EFFECTIVE_LOAD_NOT_VERIFIED`, and the
non-trigger result above counts as one scenario only, not as the set.
