# WP-FHS-12 — evidence index (author side, claim ceiling AUTHOR_SIDE_LOCAL)

generated_utc: 2026-11-01T06:03:32Z

## What was measured, what was changed

| item | value |
|---|---|
| target | `D:/Hermes-Recovery/live22/bin/hermes.cmd` |
| preimage | `a9d680b00f163669b7edd9c002df6eda8e34267d6765249fc0b031ce610a487c` (1550 B) |
| postimage | `d5c83a8f469ba1d55ddeb9859ba6f6394b6c22288bebe9a7688e4d629495d68b` |
| backup | `hermes.cmd.wp12-backup` (byte-identical to preimage) |
| negative control | rc=1, stdout 0 B, stderr 3249 B, `ModuleNotFoundError: No module named 'pm.environments'` (2/2 identical) |
| after repair | 4 entries byte-identical: `--version` 178 B, `status` 741 B, rc=0 |
| permit | `PERMIT-WP12-HOST-20261101-01`, effect `HOST_OPERATIONS`, window `WIN-91b01b7cd918`, ops 1/40, signature verified |

## Files (sha256)

| file | bytes | sha256 |
|---|---:|---|
| apply_wp12.py | 7057 | `62608a6fb8cbe2c1e83813df72c872e79ff6b83c2f143b62c10c3664ab91a2ef` |
| ENTRY_DEEP_PROBE.json | 1748 | `99a2d8f3a8fa01eb9af2906b9bbd6e4bffb9191020588b75590cebf0e1eb4b06` |
| ENTRY_EQUIVALENCE_AFTER_REPAIR.json | 2377 | `fb8ee01c234abc9a15df6d0890fa165b507524710a8fb54b93c541bd8cd07eb5` |
| ENTRY_MATRIX.json | 2958 | `2f8a2a9281f084d1a6e5148c3e1dbc9bb49792baa202643b2ba51de09e647eba` |
| ENTRY_STATUS_PROBE.json | 1385 | `5683e037631ee78d7601648b094d5fd0ef01f8cc84d97d16b90f008f1fccb006` |
| PATH_FORWARDER_FAILURE.txt | 3375 | `4e0c5c84c38046bf9d7a34969a37289c53025247dc6dce1f375771c557a858a4` |
| RUNTIME_PATH_LAB.v2.json | 10814 | `ca0466f53dbbb5cab8e6dd2b44831fcc4868f124ae99282d80fe064bf1ceb0a5` |
| WP12_HOST_REPAIR_CHECK.json | 1395 | `31f9f0b2de4f13851fda118a63537defa0e208cffef2462d199d4b910eb75956` |
| WP12_HOST_REPAIR_RECEIPT.json | 2899 | `e8e4d0f896feff3e5da8531df68be5b66a0f4ace0661f9ef2cde39991c7e6493` |
| WP12_HOST_REPAIR_RECEIPT.v2.json | 4357 | `276a2f4d92e736c74f2c0f89d49330e6c3bf1c78ff6fe2a5b6f5c7461424b895` |
| WP12_PERMIT_SIGNED.json | 2546 | `f5dac199d4fe9a2b1eb54ad6bc97ba0b9a8e165992d0ea825224ee8a34d642c1` |

## Reproduce

```bash
python var/FHS-R21-FAR-TT-20261101/wp12/apply_wp12.py --check        # negative control + preimage sha
python var/FHS-R21-FAR-TT-20261101/tools/sign_permit.py               # signs the permit in the open owner window
python var/FHS-R21-FAR-TT-20261101/wp12/apply_wp12.py --apply --preimage a9d680b0...
python var/FHS-R21-FAR-TT-20261101/tools/build_wp12_lab_v2.py         # rebuilds RUNTIME_PATH_LAB.v2
python var/FHS-R21-FAR-TT-20261101/wp12/apply_wp12.py --rollback      # restore preimage
```

## Claim ceiling

HOST_INSTALL_OF_ONE_FORWARDER. This is not a WP-12 acceptance, not a native PASS and not a release.
Independent re-sit of AO clause 2 is delegated to a separate read-only principal; its verdict is the gate.
