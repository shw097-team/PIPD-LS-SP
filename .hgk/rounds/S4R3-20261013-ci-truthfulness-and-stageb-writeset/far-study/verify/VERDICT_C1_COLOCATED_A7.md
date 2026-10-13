- **C1a: CONFIRMED** — Block 1 shows an installed-package surface at a venv `site-packages` path rather than the source tree, listing 19 schema files plus `registry.json` inside the installed package. The receipt explicitly ties this to a wheel built from the Stage A head.
- **C1b: CONFIRMED** — Block 1’s positive run reports `schemas_source_mode: "INSTALLED"` and matches the expected 19 families by count, set, and order.
- **C1c: INCONCLUSIVE** — the inline material does not contain a doctor receipt naming the command that produced it. Block 2’s sdist receipt carries `doctor_exit_code: 0`, but no producing command is shown.
- **C1d: CONFIRMED** — Block 2’s `sdist_to_wheel.json` explicitly reports `doctor_mode: "INSTALLED"` and `doctor_families: 19`.

TOKEN: C1a=CONFIRMED; C1b=CONFIRMED; C1c=INCONCLUSIVE; C1d=CONFIRMED