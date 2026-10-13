C1a is confirmed by the evidence for the installed wheel: Block 1 documents a wheel built from the Stage A tree, installed with `--no-index --no-deps` into a fresh venv, and resolved from that installed package path. Its inline installed-file listing contains `registry.json` plus all 19 schema files, and the tool’s installed-vs-tree check reports identity. That establishes the built wheel ships the registry, beyond a source-tree-only observation.

C1b is confirmed. Block 1 reports `schemas_source_mode: "INSTALLED"` from the installed venv, 19 families, and a name-for-name match with the expected ordered list. Blocks 3 and 4 independently record the same `INSTALLED` mode with families=19.

C1c is now settled by Block 4. Step 5 names the exact doctor argv, cwd under `C:\hgkrcpt\neutral`, observed rc `0`, and expected rc `0`, plus the doctor stdout showing `mode: INSTALLED`. Block 2’s sdist route also independently records `doctor_exit_code: 0`.

C1d is confirmed. Block 2’s `sdist_to_wheel.json` reports a successful sdist build, wheel-from-sdist build, install, doctor exit 0, verdict PASS, `doctor_mode: "INSTALLED"`, and families 19. Block 4 steps 17 and 18 independently corroborate that the sdist-route doctor ran from the sdist venv and reported `INSTALLED` with 19 families.

The failed tar re-attempt is explained in Block 2 as a shell invocation defect; it neither supports nor undermines the verified Python-backed receipt. Block 4 therefore settles C1a through C1d while preserving C1a’s distinction between the built artifact and merely a source tree.

HGK_LANE_NONCE_OK