# 指定獨立驗收車道：裁決與處置（如實刊登）

> 車道：owner 指定 VERIFY/SECURITY — **CODEX CLI**，checker model **`gpt-6.1-sol`**（provider `openai`，OAuth，reasoning effort medium）
> 凍結主體：`389d3973da73e5740f0b4d290bacb92d1e8982f8`（tree `488d12c1a4bef899f6d38543ab50874d79996e3a`）
> 車道執行紀錄：`verify/r3/AO_VERIFY_SUBJECT_389D3973_gpt-6.1-sol_medium.log`（模型身分標頭為證）
> 檢查器原始產物：`verify/r3/ao_lane/`（33 檔，未經改寫）

## 1. 裁決（原文照刊）

**`FAIL_CHALLENGE`**

| 主張 | 判定 |
|---|---|
| C1 聚焦套件（108） | **VERIFIED** |
| C2 全量套件（572） | **VERIFIED** |
| C3 套件不變異 | **FAILED** |
| C4 §3 驗收區塊可逐字執行 | **FAILED** |
| C5 負向對照 fail-closed | **VERIFIED** |
| C6 正向對照 | **FAILED** |
| C7 官方 vendor schema 下載比對 | INCONCLUSIVE（車道無網路） |
| C8 證據包雜湊形態 | **FAILED** |
| C9 CI 綠燈 | INCONCLUSIVE（離線無法查核 hosted run） |
| C10 主體無 gitlink | **VERIFIED** |
| C11 登記簿狀態 | INCONCLUSIVE（多數狀態無法自 clone 查核） |
| C12 FAR 的實測主張有可定位產物 | **FAILED** |
| C13 頭條揭露敘述準確 | **FAILED** |
| C14 無有利於己的rounded-up | **FAILED** |

檢查器自列的 `not_verified` 另含：CI 執行結論與 head_sha、歷史 checkout/wheel 失敗、release 資產下載回讀、**歷史 OS 隔離與 route/model/provider 身分（它自身以 `…-1000` 執行，非 `…-1004`）**、HGK DB／Kanban／GSTACK／OpenSpec 的實際狀態、本機 `main` 分支（僅存在 `origin/main`）。

## 2. 處置：真缺陷 vs 車道範圍限制

| 判定 | 性質 | 處置 |
|---|---|---|
| **C3** | **真**（我的敘述過寬） | 套件在**全新 clone** 內會建立 3 個被 gitignore 的 `__pycache__/`；我先前「兩種視圖皆零新增」是**環境相依**（我的工作樹已有快取）。已改為精確敘述（見 `FAR_MEASUREMENT_RECEIPTS.json.C3_non_mutation`） |
| **C4** | **真**（我的文件 bug）＋車道範圍 | §3 有一段用 `"$R/..."` 卻已 `cd "$R"` → **重複前綴**不可執行。已修（一律從 clone 根執行）；另註明 clone/curl 步驟需網路，離線檢查器無法執行屬範圍限制 |
| **C6** | **真**（我的工具 bug＋我的編輯） | 我的定位器 `SKIP` 以 `^` 錨定，行內 URL 被切成 `s://host/...`。**且**我在最後一次提交把 URL 寫進受對照文件後**沒有重測**。已修工具（v2 遮蔽 URL）並重測：**exit 0 / 9 in-tree / 0 違規**（見 `LOCATOR_CHECK_R3_POSITIVE.json` v3） |
| **C8** | **真**（標籤不精確） | 我記的 `log_sha256_worktree_eol` 實為**原始 Windows CRLF 形態**；在 `.gitattributes` 正規化後，**clone 磁碟上量到的是 blob（LF）形態**。已改為兩種形態明確標示 |
| **C12** | **真**（缺可定位產物＋數字錯） | ①`com.ao3` 實為 **3 檔**（全為本回合自撰紀錄，產品面 **0**），我先前的「1 檔」**是錯的**；②ADJ-1 的寫入集數字與 commit 對未綁定；③已補 `FAR_MEASUREMENT_RECEIPTS.json` 使每個「實測」主張皆有產物 |
| **C13** | **真**（我的解釋不完整） | 「紅燈只因 base 選錯」**不成立**：以宣告基底重跑守衛**仍 exit 1**，因其拒絕集合同時包含本次獲准新增的 `ci.yml` 與四筆 gitlink 移除。已改為兩段式正確敘述 |
| **C14** | 綜合上述 | 逐項已折入各文件 |
| C7 / C9 / C11 | **車道範圍限制** | 離線／單一身分無法查核者，車道正確地判 INCONCLUSIVE，未推測 |

## 3. 揭露：車道自身也抓到我 3 次「量測後又編輯、未重測」

C6、C12（數字）、C14 的共同根因不是能力不足，而是**我在提交前改動了被量測的對象卻未重跑量測**。這是本輪最值得記下的系統性缺陷，已寫入技能 `adversarial-verification-rounds`。

## 4. 輪數與上限

依 `HARNESS_FREEZE_AND_AO_LOOP_CAP.md` R8：同回合外部複驗 **≤2 輪**。本車道為**第 1 輪**（owner 指定車道）。缺陷已就地折入（fold-in），**未**重開載具、**未**新增軸、**未**因 FAIL 而擴建。

## 5. 宣稱天花板（未變）

`PIPD_S4_FULL_PASS` **未授予**；發行閘門 **`FAIL-CLOSED / HOLD`**；本車道裁決為 **`FAIL_CHALLENGE`**，且為**揭露性**證據，不構成放行。maker 對本裁決的處置**不改變**裁決本身——上表列的是我修了什麼，不是說裁決錯了。
