# R5 S4 — independent deterministic check (PIPD-R5-AO-DETERMINISTIC-CHECKER/1)

- maker: `R5-WO1/WO2/WO3 codex lanes + orchestrator`
- verdict: **PASS_CHECK_DETERMINISTIC**
- counts: `{"PASS": 17}`
- wheel: `pipd_ls_sp-0.1.0-py3-none-any.whl` sha256 `e49d38e519117d67de57153658779eafa139eb0dda5a6d15f486facb44fd00e2`

| case | verdict | actual |
|---|---|---|
| A1-A3 wheel completeness | PASS | members=38 schemas=19 registry=True manifest_members=38 |
| A2 wheel members == source bytes | PASS | mismatches=[] |
| A4 FALSIFY missing schema member | PASS(held) | START / TYPED ValidationFail schema file missing for ArtifactIdentity |
| B dream destinations refused | PASS | rows=[['repo root', 2, True], ['cwd dot', 2, True], ['parent', 2, True], ['source descendant', 2, True], ['filesystem root', 2, True], ['empty', 2, True], ['whitespace', 2, True],  |
| B symlink/junction escape | PASS | via=junction exit=2 {
 "code": "UNSAFE_DESTINATION",
 "message": "refusing destination C:\\Users\\user\\AppData\\Local\\Packages\\ |
| B positive control | PASS | exit=0 web=5 host=3 ir=True residue=[] |
| B nonempty refusal + allow-replace | PASS | refused=True replaced=True backup=C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\r5-ao\subject\allowed\good.pipd-backup-f93e8 |
| B dry-run zero writes | PASS | exit=0 exists=False |
| C1 export writes a bundle | PASS | exit=0 landed=['SHA256SUMS', 'bundle.tar.gz', 'export_manifest.json'] |
| C2 independent recompute | PASS | rows=71 members=71 bad=[] archive_sha=True sums=True |
| C3 dry-run zero writes | PASS | exit=0 exists=False |
| C4 no --out keeps read-only mode | PASS | exit=0 mode=READ_ONLY_MANIFEST wrote_nothing=True |
| C5 FALSIFY planted secret | PASS(held) | exit=2 artifacts=[] out={
 "code": "EXPORT_SECRET_SCAN",
 "message": "secret scan found 2 hits",
 "verdict": "FAIL"
}
 |
| D1 install purity | PASS | exit=0 mod=atch\r5-ao\uat\venv\Lib\site-packages\pipd_ls_sp\__init__.py fam=19 |
| D2 two-process replay | PASS | hashes=['c1af2963133c7e69c53db774778a5ff697c9ad262e5e03daa368bb6415b0131b', 'c1af2963133c7e69c53db774778a5ff697c9ad262e5e03daa368bb6415b0131b'] |
| E1 maker==checker refused | PASS | exit=2 out={
 "code": "TQ_SOD",
 "message": "maker must not be the independent checker (case/whitespace-insensitive)",
 "verdict": "FAIL"
}
 |
| E2 product tree untouched by the checker | PASS | src canary=60621cc34b4ba5d7… |

## Falsification attempts

- `A4 FALSIFY missing schema member` → **PASS(held)** — START | TYPED ValidationFail schema file missing for ArtifactIdentity
- `C5 FALSIFY planted secret` → **PASS(held)** — exit=2 artifacts=[] out={
 "code": "EXPORT_SECRET_SCAN",
 "message": "secret scan found 2 hits",
 "verdict": "FAIL"
}


## Limits

This checker is deterministic and does not replace an LLM acceptance officer.
The two container checker lanes were killed by a provider 429 storm; no
`INDEPENDENT_PASS` is claimed anywhere in this round.
