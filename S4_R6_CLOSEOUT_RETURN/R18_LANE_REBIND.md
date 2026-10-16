# R18 — 車道改綁記錄（OWNER ORDER，2026-10-16）

**指令（owner，本 session，逐字要旨）**：因 GPT 配額即將耗盡，把
「PLAN & Orchestrator 在 HERMES 內執行」的模型，以及「Independent Acceptance Officer／VERIFY／SECURITY
（CODEX CLI checker）」的模型，都**更換為 `DeepSeek V4.1 Flash (OPENCODE GO)`**。

本回合**執行並量測**如下；每一項都有 before/after 與可重跑命令。

## 1. PLAN & Orchestrator 平面（in-Hermes）

綁定面（兩個面都改，兩面都是宣告面）：

| 面 | 檔案 | before | after |
|---|---|---|---|
| governed profile（`_plane: PLAN & Orchestrator (in-Hermes)`） | `profiles/hgk-governed/config.yaml` | `model.default: gpt-6.1-sol` / `model.provider: openai-codex` / `medium` | `model.default: deepseek-v4.1-flash` / `model.provider: opencode-go` / `medium` |
| 主設定（新 session 的 orchestrator 預設） | `config.yaml` | `model.default: glm-5.3-flash`（provider 已為 opencode-go） | `model.default: deepseek-v4.1-flash` / `opencode-go` |

改法：`HERMES_HOME=<原生路徑> python hermes_cli/main.py config set model.default|model.provider …`
（注意：HERMES_HOME 必須是 `C:/...` 原生路徑；MSYS 的 `/c/...` 會被 native python 誤解為 `\c\...`）。

## 2. 改綁後立刻撞到的阻礙（已修，必須揭露）

改綁後第一次探測**失敗**：

```
hermes -z: agent failed: No usable credentials found for provider 'opencode-go'. Set OPENCODE_GO_API_KEY.
```

原因：`profiles/hgk-governed/` 下**沒有** `.env`；該 profile 先前的 arm 是 OpenAI OAuth（由 auth.json 提供），
所以缺少 opencode-go 的金鑰來源。

**修法（不列印任何值）**：把主 home 的 `.env`（346 bytes；僅 4 個鍵名：`OPENCODE_GO_API_KEY`、
`OPENROUTER_API_KEY`、`OPENCODE_ZEN_API_KEY`、`NVIDIA_API_KEY`）**byte 複製**到 `profiles/hgk-governed/.env`。
這是把既有憑證提供給同一使用者的另一個 Hermes home，未新增、未輪替、未回顯任何密文。

**修後實測（可重跑）**：

```
HERMES_HOME=C:/.../profiles/hgk-governed python hermes_cli/main.py -z "Reply with exactly: PLAN_LANE_DEEPSEEK_PROBE_OK"
→ stdout: PLAN_LANE_DEEPSEEK_PROBE_OK        （exit 0）
```

serving row（`profiles/hgk-governed/state.db::sessions`，最新一列）：

```
model=deepseek-v4.1-flash  billing_provider=opencode-go  billing_base_url=https://opencode.ai/zen/go/v1  source=oneshot
```

（前一列為 `model=gpt-6.1-sol / billing_provider=openai-codex / …chatgpt.com/backend-api/codex`，保留為改綁前的歷史。）

## 3. Independent Acceptance Officer / VERIFY / SECURITY

- 選拔權威（`config/model-lane-assignment.json`）的 **VERIFY_SECURITY 預設就是 arm A = `opencode-go/deepseek-v4.1-flash`**
  （owner order 2026-10-16，round ROUND3-LANE-REBIND-AND-CLOSURE-20261016）。因此本次指令**不需要改 registry**：
  只要**不再釘 GPT arm**即可落到 arm A。
- 本回合的派發：`run_lane.py VERIFY_SECURITY <brief> … 1 opencode-go/deepseek-v4.1-flash`（rank 1，無 `--require-arm`）。
- **被丟棄的舊綁定**：`--force-rank 2 --require-arm openai-codex/gpt-6.1-sol`（R6/R17 兩輪均使用；本輪依令停用）。

## 4. 職責分離（SoD）後果 —— 明示，不掩蓋

| 軸 | 狀態 |
|---|---|
| 模型軸（writer vs checker） | **不存在**：EXECUTE writer 與 VERIFY arm A 同為 `opencode-go/deepseek-v4.1-flash`（registry `SOD006-C3`，`OWNER_ORDERED_IN_FORCE`） |
| 供應商軸 | 不存在（兩者皆 opencode-go；registry 記載 provider separation 非必要） |
| 程序／車道／證據路徑軸 | 仍成立（checker 為 VERIFY_ONLY、不同 lane、不同證據路徑） |
| 自我驗收 | 仍被阻止（無任何單一呼叫驗證自己的產出） |

→ 因此本回合 checker 的裁決必須標示為**同模型軸**的裁決；不得以「不同模型」描述它。

## 5. 未動但已知分歧（提請 owner）

- `config/model-lane-assignment.json` 的 `in_hermes_plan_orchestrator_plane` 鍵（round
  LANE-RELIABILITY-CLOSURE-20261016）仍宣告該平面「must be GPT 6.1 SOL-MEDIUM (OpenAI OAuth)」；
  `assignment[0]` 的 PLAN lane_group 列為 `glm-5.3-flash`。兩者**都與本次 live 綁定不一致**。
  本回合**不改 registry**（避免動到宣告權威面），僅記錄；此分歧可併入既有 finding
  `F1-PLAN-ROUTE-ROW-OUTLIER` 一併由 owner 裁決。
- 因此：宣告面（registry）與生效面（profile/main config + serving row）目前不一致，
  **生效面為本次實測者**。此不一致是 owner-visible 的，不由本回合自行消解。

## 6. 天花板

本記錄是**候選**：改動為 owner 授權的宣告套用，由 in-Hermes orchestrator 執行，**不構成**獨立驗收、
不構成 promotion，也不是對 deepseek arm 之 provider/liveness 的背書（liveness 已由上述 serving row 實測，
但那是可服務性證據，不是模型品質證據）。
