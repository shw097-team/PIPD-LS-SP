# Independent acceptance - R9, cross-model (CODEX CLI / VERIFY_SECURITY lane)

Round R9-20261011-s4-gap-closure. Verdict produced by the VERIFY_SECURITY lane served by
openai-codex/gpt-6.1-sol (OAuth, effort medium) - a different model family from the maker
(opencode-go/deepseek-v4.1-flash). The could_not_verify list and the evidence array below are
embedded verbatim from the checker report, not paraphrased.

## 1. Verdict

```
verdict = PASS    nonce = HGK_LANE_NONCE_OK
```

## 2. Which model actually served it (receipt, not the flag we passed)

- ok = True
- mode = forced_rank
- required_arm = openai-codex/gpt-6.1-sol
- served_arm = openai-codex/gpt-6.1-sol
- used_rank = 4
- used_seconds = 226.38
- attempts[0] = rank 4 / openai-codex / gpt-6.1-sol / exit 0 / nonce True
- attempts[0] usage = provider openai-p6a1fe3 / model gpt-6.1-sol / status 200 / effort medium

required_arm == served_arm, and the relay usage row independently names the same provider/model/status.

## 3. Non-mutation of the subject tree

```
mutated = False
files   = 3905 -> 3905
added/removed/changed = [] / [] / []
digest before = f4754d4da1b6b692df8ce97a0df679a0c4bd12252635f60dd887e74b2a250963
digest after  = f4754d4da1b6b692df8ce97a0df679a0c4bd12252635f60dd887e74b2a250963
```

## 4. Checks

- check 1 : PASS
  - command: ['git ls-remote https://github.com/shw097-team/PIPD-LS-SP.git']
- check 2 : PASS
  - command: ['curl -q -sSL https://api.github.com/repos/shw097-team/PIPD-LS-SP/releases/tags/v0.1.0-preview.2']
- check 3 : PASS
  - command: ['curl -q -f -sSL https://github.com/shw097-team/PIPD-LS-SP/releases/download/v0.1.0-preview.2/pipd-ls-sp-v0.1.0-preview.2-source.zip -o C:/Users/user
- check 4 : PASS
  - command: ['C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -B -m venv C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCac
- check 5 : PASS
  - command: ['C:/Users/user/AppData/Local/Programs/Python/Python311/python.exe -B -m unittest tests.test_ce_repair_regression -v', 'git -C C:/Projects/Agent_Works

## 5. could_not_verify - quoted in full, unabridged (this block is the verdict boundary)

```json
[
  "Historical permanence of remote tags cannot be proven by a current anonymous ref snapshot; exact tag identities matched at observation time.",
  "The presence of G_RELEASE_FULL_PASS in release prose does not verify the underlying full-release-gate claim; only the requested checks and nine-test regression module were executed.",
  "SHA256SUMS does not publish a hash for itself; its own served bytes were hashed, but no independent expected digest for SHA256SUMS was supplied."
]
```

## 6. The checker own claim ceiling

> PASS covers only the observed anonymous preview.2 release metadata and asset integrity, exact requested tag identities, downloaded-wheel CE-1 and trace-rejection behavior on Windows CPython 3.11, the nine-test local regression module, and byte-identical preservation of the inspected release tree.

## 7. Two earlier runs, preserved not deleted

This was the THIRD attempt. Both earlier verdicts are kept in the round record.

- Earlier run THIS ROUND: receipt was clean (ok:true; arm, guard and relay all correct) yet the
  verdict was FAIL on 1 of 5 checks. Cause: the prompt told the checker to confirm
  branch main -> a pinned sha that was the PRE-merge tip. This round deliberately advanced main,
  so the checker correctly failed a comparison that should never have been requested. The subject
  was not at fault; the PROMPT was. Fixed by asserting only the immutable tags and requiring the
  branch to be reported rather than compared.
- R8 run 1: --require-arm verified the arm survived the identity gate but did not restrict the
  candidate list; the run walked the pool in rank order and served rank 1 - the maker own model -
  returning ERR_REQUIRED_ARM_NOT_SERVED. See FAR-PIPD-R8-DISPATCH-004.md.

## 8. Claim ceiling for this round

R9_LOCALLY_VERIFIED_AND_CROSS_MODEL_RE_DERIVED_CANDIDATE. Cross-model means a different model
family on the SAME control plane and the SAME host. It is not external acceptance: no third party,
no signing identity, nothing verified off this machine. FULL_S0_S4_INDEPENDENT_PASS and
G_RELEASE_FULL_PASS remain NOT GRANTED. The maker did not sign this.
