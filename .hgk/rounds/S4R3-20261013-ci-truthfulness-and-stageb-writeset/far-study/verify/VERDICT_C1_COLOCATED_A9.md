C1a: CONFIRMED. Block 1 ties the named wheel hash to a fresh installed-prefix listing containing `registry.json` and all schema files under `pipd_ls_sp\schemas`; that shows the wheel shipped the registry surface, not just a source tree.

C1b: CONFIRMED. Block 1 reports `schemas_source_mode=INSTALLED`, 19 installed families, the expected and installed name lists in the same explicit order, and required equality checks all `true`.

C1c: INCONCLUSIVE. No inline block contains a doctor receipt with both the exit code and the command that produced it. Block 2’s sdist JSON has `doctor_exit_code: 0` but no command field; Block 1 and the CI extracts lack both. Missing block: an unredacted doctor receipt showing `doctor_exit_code` alongside the exact invocation/command.

C1d: CONFIRMED. Block 2’s sdist-route JSON reports `wheel_from_sdist_rc: 0`, `install_rc: 0`, `doctor_verdict: PASS`, `doctor_mode: INSTALLED`, and `doctor_families: 19`.

C1 overall: NOT CONFIRMED, because the doctor-command half of C1c is not settled by inline blocks.

HGK_LANE_NONCE_OK