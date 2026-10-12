# AO9 lane stopped by the maker's own order - no verdict

- Primary checker `gpt-6.1-sol` (openai, OAuth, medium) **exhausted its quota** and the wrapper recorded it:
  `CHECKER_PRIMARY_EXHAUSTED lane=AO9 exit=1 signature=[      2 usage limit;]`.
- The declared backup `opencode-go/glm-5.3-flash` then started and was **stopped mid-run by the maker**
  (`termination_source: process.kill`, exit -15), on the owner's instruction that the GPT quota had
  recovered and that the checker lane must run on `gpt-6.1-sol` again.
- `verify/ao9/` therefore holds **no verdict**. Anything the backup attempt produced before it was stopped
  is partial and is not an adjudication.
- Consequence: round 9 has no verdict, exactly like round 7. Round 10 is dispatched through the canonical
  `fabric-external-independent-challenge-reviewer` lane on the primary checker.
