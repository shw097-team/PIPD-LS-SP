# AO12 external evidence: preserved only as an index, because the maker cannot read the root

The officer's bundle is in the tree and is complete for the review itself:
`EXTERNAL_CHALLENGE_REPORT.md` (41,805 bytes, thirteen headings), `FINDINGS.json`, `REVIEW_EVIDENCE_MANIFEST.json`
(180 hash-indexed entries, 82.33 MB referenced), `FROZEN_TRACKED_SHA256.json`, `FREEZE.json`,
`INTAKE_AT_DISPATCH.json`, `REPORT_READBACK.json`, `TEMP_WORKSPACE.txt`.

## What could not be preserved

The per-case evidence lives in the officer's external root
`C:/Users/user/AppData/Local/Temp/ao12-roo_vkak` (and `ao12-replay-*`). The maker cannot read it:

```
ls: cannot open directory 'C:/Users/user/AppData/Local/Temp/ao12-roo_vkak': Permission denied
head: cannot open '.../SOURCE_INVENTORY.json' for reading: Permission denied
icacls "C:\Users\user\AppData\Local\Temp\ao12-roo_vkak"  -> access denied, 0 files processed, 1 error
```

All 180 referenced entries raised `PermissionError`. The same applies to round 11's staged roots. The lane runs
as a different Windows identity than the repository owner, and it writes its temp evidence under ACLs that
exclude the owner.

## Consequence, stated plainly

- The review's findings survive as the tree-side bundle; the raw reproducers behind them do not.
- Every locator in the report that points into the external root is therefore **not re-runnable by the maker
  or by a third party** - it fails the skill's own locator requirement, and this is a property of the lane's
  host setup, not of the officer's work.
- The maker cannot verify or refute those reproducers independently; it can only read the officer's account
  of them, and the officer's own account says so.

## What would fix it

Have the lane hand over a readable archive into its declared write set before it exits (a tar of its root
written from inside its own identity), or run the lane under the repository owner's identity so the temp ACLs
match. Until then, a maker cannot audit an officer's raw evidence, only its report.
