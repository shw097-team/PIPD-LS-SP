# arm3 freeze note

- Subject document (frozen): `07_acceptance/SESSION_CONFORMANCE_ANSWER.md` sha256 `a431ac09342d5e55dc88004d540fb59d08d2cdd20deb2c923788290c75d4f0ba`
- arm3 verdict: `VERDICT_ARM3_PASS.json` / `.md` — `overall = PASS`, `unresolved_locators = []`
- The answer document is now FROZEN at this sha. Any later finding is recorded in NEW files under `06_verification/`
  and in the evidence pack, so the arm3 pass basis is never silently invalidated.
- arm3's own note: it observed the subject change mid-run (v4 557f9882 → v5 a431ac09) because the maker appended the
  attempts.ndjson section while arm3 ran; the pass therefore applies to the FINAL content, which is the sha above.
- Decisive binding evidence is the dispatcher receipt (`dispatch_receipt_arm3.json`); the lane's self-report
  (`opencode-go/glm-5.3-flash`) is NOT accepted as binding. Receipt pending at write time.
