# R5 S4 UAT matrix — 2026-10-10T15:35:08Z

wheel: `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\cache\scratch\r5q-publish\readback_dl\pipd_ls_sp-0.1.0-py3-none-any.whl` sha256 `c450dbef1c3bfbc2048dcf0562f83d655cc5e5940511e65fd44bf9f91cf14e60`

| case | mode | verdict | actual |
|---|---|---|---|
| UAT-ENV | install | INFO | bootstrap=venv--without-pip+uv install_path=uv_pip_online_index exit=0 provisioned=None |
| UAT-00 | install | PASS | venv=0 pip=0 probe=0 out_of_repo=True out={"mod": "C:\\Users\\user\\AppData\\Local\\Packages\\OpenAI.Codex_2p2nqsd0c76g0\\LocalCache\\Local\\hermes\\cache\\scratch\\r5q-uat-matrix\\uat00_venv\\venv\\Lib\\site-packages\\p |
| UAT-00N | install | PASS | healthy=0 mutated=1 restored=0 |
| UAT-01 | install | PASS | intake=0 pi=0 atoms=4 negative=2 |
| UAT-02 | install | PASS | exits=[0, 0, 0] bad=2 profile_meta_differs=True canon_hash={'LITE': '316989a031b9', 'STANDARD': '6c0feb7381ea', 'ASSURED': 'd2f8ff5dc0bc'} |
| UAT-03 | install | PASS | pd=0 ecp=0 sod=[2,2,2] design_positive=True host_derived=True identity_sentinel_observation_exit=0 |
| UAT-04 | install | PASS | good=0 tampered=1 missing=2 |
| UAT-05 | install | PASS | dry=0 writes=False canary_same=True dot=2 msys=2 |
| UAT-06 | install | PASS | project=0 web=5 host=3 ir=True negative_leaks=[] canary_ok=True src_stable=True |
| UAT-07 | install | PASS | dry=0 dry_clean=True export=0 files=3 recompute=True [rows=75 members=75 bad=[] archive_sha_recomputed=True sha256sums=True] |
| UAT-08 | install | PASS | diff=0 missing=2 repair=0 escape=2 noscope=2 |
| UAT-09 | install | PASS | exit=[0, 0] hashes_equal=True h0=adae317353022b8a |
| UAT-10 | install | PASS | steps=[0, 0, 0, 0, 0, 0] residue=[] reg=19 |
| UAT-11 | install | PASS | small_atoms=2 large_atoms=801 s2_check_exit=0 s2_preserved_fail_visible=True s2_voting=['bytes_per_atom'] s2_bytes_per_atom=1464.6 |
| UAT-12 | install | PASS | export=2 exp_exists=False leaked=False foreign=2 root=2 intake_inj=0 |
