# Checker failover record - AO9

The owner's ruling of 2026-10-12: if the checker model GPT 6.1 SOL-MEDIUM (OpenAI OAuth) runs out
of quota, the checker model switches to the declared backup GLM-5.3-Flash (OPENCODE GO).

| | model | route | stamp | child exit | lane log |
|---|---|---|---|---|---|
| primary | `gpt-6.1-sol` | `openai` | `20261012T142905Z` | 1 | `/tmp/hgk-lanes/AO9_20261012T142905Z.log` |
| backup  | `opencode-go/glm-5.3-flash` | `catalog` | `20261012T142913Z` | 1 | `/tmp/hgk-lanes/AO9_20261012T142913Z.log` |

Exhaustion signature matched in the primary log: `      2 usage limit;`

**This changes the checker's identity.** Any verdict produced under the backup was produced by a
different model than the assigned checker, and the verdict document must say so. The failover does
not transfer, and does not create, any acceptance this round would not otherwise have.
