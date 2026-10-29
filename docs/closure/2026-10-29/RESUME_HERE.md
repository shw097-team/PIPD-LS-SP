# RESUME_HERE — B1 PIPD-LS-PKG 00..08（2026-10-27 SESSION 結束點）

> 給下一個 SESSION：**不要重新推導**。照 §1 讀三個檔即可接續；§3 是可直接執行的下一步。

> **結案狀態（2026-10-29）**：`CLOSEOUT.md`＋`artifacts/HANDOVER.json` 已產出並上推
> `PIPD-LS-SP@b1/closure-20261029`（`fc55ecc`，`docs/closure/2026-10-29/`，未動 main、未 force）。
> `release/sourcefreeze = SIGNED`（專用窗口 `WIN-ce63de72d674`，2/4 ops，已關閉）；本地啟用 `artifacts/ACTIVE.json`。

## 1. 先讀（依序，3 檔）

1. `artifacts/STATE.json` — 機器可讀狀態（board、卡 id、artifacts sha256、findings、next_actions）
2. `REPORT.md` — 本輪做了什麼、分母實測、Host 事實、缺陷 F-01..F-07
3. `CLAIM_CEILING.md` — 可以講／不可以講的邊界

## 2. 現況（一句）

自檢 **83/83**；**S1 已落 canonical**（`PIPD` commit `38e363b`＋`03fc739`，validate PASS/4，r7 11/11 PASS 綁定 3/3）；**車道模型已改為指令可選**（`lanes/lane_select.py`，三方互斥 `DISTINCT_ROLES`，本輪 VERIFY=mimo）；**oracle 三角已實跑**：作者 deepseek／oracle owner gpt-6.1-sol／checker mimo，O4 **27/27 REJECT（stub 無 expected/predicate/source）**、O5 **PASS 11/11**；**S2 canary 1/30（demo key）**、**S3 六負例全拒（同 OS 使用者，非真 principal）**。**native 正式面仍 HOLD**：G-A 6/6 PASS（設計級）、G-B HOLD、29/30 route 未註冊、sourcefreeze／release NOT_RUN。`mission_complete=false`。

## 3. 下一步（依 depends_on 排序，皆為合法 L0/L1 或需 Owner 的 L2）

| 順序 | 動作 | 前置（缺即 HOLD） | 產出 |
|---|---|---|---|
| 1 | ~~S1 schema 落地~~ **已完成 2026-10-27**（`38e363b`） | — | `artifacts/S1_EVIDENCE.json` |
| 1b | **Owner 用真金鑰簽 canary row**（現在是 demo key），或一次簽 30 列 | Owner 私鑰 | 30 route 由 BLOCKED → DISCOVERED |
| 1c | **Owner 認可 `effect_class` 值集**，之後才能把 `x-s0-vocabulary` 收斂成 enum | Owner 裁決 | schema 再一版 |
| 2 | 修 F-02：`supersedes_subject_sha256` 自我引用 → 應為前版（r2 `273591a3…` 或 10-26 r3 實測值） | Owner 同意改 frontmatter | 每冊 lineage 可機械驗 |
| 3 | **註冊 runner registry 九欄**（canary 已做 1 列，剩 29 列）（runner_id / abi_version / schema_id / executable_path / sha256 / allowed_os / read_scope / permission_scope / owner_signature） | Owner 簽章 | 30 route 才能由 BLOCKED → DISCOVERED |
| 4 | R1：讀 `Trust Profile → Resolver → Receiver`，記 Host/SID/key fingerprint/ACL/binary SHA/policy epoch | 無（唯讀） | receiver ABI 事實卡 |
| 5 | R2：確認既有 Hermes Executor/SharedSpine 身分、lease journal、wakeup；**禁另造 Scheduler** | 無（唯讀） | 續航事實卡 |
| 6 | R3：Fabric stage/active/loaded/consumer 三 Raw（不同 event） | Activator + Consumer 綁定 | RAW-FAB-STAGE/LOADED/CONSUMER |
| 7 | R4：PLAN/EXECUTE/VERIFY 同 epoch served readback | 三 Lane 真 request | lane 收據 |
| 8 | GWO-SBL：先確認 user-effect issuer 是否存在；無 → `NOFIT_USER_ISSUER_UNBOUND` zero effect | user consent + issuer | 不可用 OPS/DEV token 代 |

## 4. 已 blocked 的兩張卡（解鎖條件）

- `t_6aa833d7` NATIVE GATES — 解鎖：runner registry 九欄 + issuer/queue/checker 三項真收據。
- `t_4df6b978` METHODS — 解鎖：安裝 Codex CLI（或 Owner 書面改 lane 政策）＋ GStack 路由 registry；否則永遠只能記 `NOT_SELECTED/NOT_NOFIT`，不得寫 INVOKED。

## 5. 重跑（完全可重現，約 30 秒）

```bash
cd /c/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027
python measure_packs.py        # 兩包 digest/分母/body diff
python build_artifacts.py      # 7 個機器工件
python probe_host.py           # 17 surface 真探測（唯讀動詞）
python build_obligations.py    # 40 條義務
python run_pipeline.py         # 13 動詞工具鏈（isolated pipd-run/）
python finish_pipeline.py      # project + export + validate（需 TQAEP 才有第 4 份契約）
python run_native.py           # 244 案例 + 4 協定探針
python gwo.py                  # 三張 GWO（GWO-SBL 走真 sbl_cli）
python -m pytest test_b1run.py -q -p no:cacheprovider   # 9 條協定測試
python gates.py                # G-A 5/6、G-B HOLD
python finalize_state.py && python selfcheck.py && python selfcheck2.py && python fix_ceilings.py
python sync_state.py           # 把 SELFCHECK 計數同步進 STATE
```

## 6. 檔案地圖

```
var/B1-PIPD-PKG-20261027/
├── input_20261027/                  # 交付件複本（9 冊，釘 sha256）
├── sandbox/pipd-root/               # pipd doctor 的隔離 root（無 effect）
├── artifacts/                       # 12 個 JSON（見 REPORT §2；含 SWARM_CROSSCHECK）
├── measure_packs.py build_artifacts.py probe_host.py
├── build_obligations.py finalize_state.py selfcheck.py
├── kanban_setup.py                  # board/卡建立（冪等 key: b1pkg-*）
├── REPORT.md CLAIM_CEILING.md RESUME_HERE.md
```

## 7. 跨回合接續（前次 SESSION 的未結項，勿重工）

`HG-KSEOS/var/B1-HERMES-R10/B1_HERMES_R10_RESUME_CHECKPOINT.json` 列的 R10 未結項（receiver 綁定、Fabric activator、lane served、dispatcher 身份、delete 觸發器）**與本輪 §3 的 3–8 項一一對應**；本輪未動它們，狀態維持 NOT_RUN。

## 8. 交接紀律

- board `b1-pipd-pkg-20261027` 目前 12 完成 / 2 blocked；**不要**把 blocked 卡標完成來「收尾」。
- 任何新證據請寫進 `artifacts/` 並重跑 `selfcheck.py`，勿手改既有 JSON。
- 不得以本輪 `DOC_STATIC_PASS` 推稱 SOURCEFREEZE / ADMITTED / LOADED / SERVED / RELEASE。

## 9. 第三輪（2026-10-27 晚，獨立 checker 車道）

### 9.1 怎麼把 VERIFY_SECURITY 跑起來（可重現）

```bash
export HGK_LANE_RELAY_BASE="https://chatgpt.com/backend-api/codex"
export HGK_LANE_IDENTITY_SOURCE="codex-rollout"
export HGK_LANE_HUMAN_HOME="C:/Users/user/.codex"
bash run_checker_round3.sh          # 內含: 先 stash 舊 receipt → 把 NONCE 寫進 brief → 派工 → 還原
```

- `--lane VERIFY_SECURITY --require-arm "openai-codex/gpt-6.1-sol"`（**必須 qualified id**，bare 會 `ERR_LANE_REQUIRED_ARM_ABSENT`）。
- `--codex-home C:/Users/user/.codex --allow-human-home-transport`；封存 home `HG-KSEOS/codex-hermes` **沒有 auth.json**，直接用它會 401。
- `--sandbox read-only`：checker 因此**無法寫自己的 receipt**，判決只存在 attempt stdout，需 `apply_checker_receipt.py <logs> <out>` 抽取並驗 subject 綁定。
- nonce 必須**寫進 brief**（dispatcher grep 自己的 `--nonce`），否則 `ERR_NO_ARM_EMITTED_NONCE`、`served_arm=null`。
- dispatcher 仍會回 `ERR_REQUIRED_ARM_NOT_SERVED`（rollout 記 `desktop_router/gpt-6.1-sol`，pool 宣告 `openai-codex`）——標籤缺陷，不是執行失敗。

### 9.2 逐輪判決（同一份 brief）

| 輪 | 受檢位元組 | verdict | 失敗項 | 備註 |
|---|---|---|---|---|
| r1 | pi `d1a0741a` / ecp `ba03e970` / pd `44f08b4a` | FAIL | C4 C5 C6 C8 C9 C10 C11 | 首輪；`ok=false`（arm 標籤） |
| r2 | 修補後（C4/C6/C8/C9） | FAIL | **C9 only** | `prior_receipts_consulted=false`；C9 指 ECP 缺 `explain`、`replay.subject_id` 自指矛盾 |
| r3 | 同 r2 | **不計** | — | rollout 記 `served_arm=desktop_router/opencode-go/deepseek-v4.1-flash` → 被本地 router 換成 maker 同族模型，**獨立性不成立**（F-17） |
| r4 | pi `d1a0741a` / ecp `44dbfd14` / pd `335ffec6` | FAIL | C7 C11 | 直打 `model_provider=openai`，rollout 驗明 `model=gpt-6.1-sol provider=openai`；C11 指出 PI 的 explain/replay 不受 hash 覆蓋（ECP 有、PD 無） |
| r5 | PI/ECP 的 explain+replay 全部 re-seal、C7 題目改為 prefix 慣例 | FAIL | C2 | 只剩 27 個 trace parent 仍指向 re-seal 前的 PI 身分（我造成的真缺陷） |
| r6 | PI 重新 seal 後把 27 個 trace parent 重指到新身分 | **PASS** | — | **11/11 PASS**，receipt `75a007f6…`，綁定 3/3；rollout 驗明 `model=gpt-6.1-sol provider=openai` |

### 9.3 結論

- G-A **6/6 PASS**（設計級）；G-B 仍 HOLD；`mission_complete=false`。
- **r7**（S1 落地後重檢）11/11 PASS，receipt `97496bbb…（末次輸出；同輪先前另有一次較冗長的發佈，內容判決相同）`，綁定 `6b53e814`／`47d4237c`／`b25f8767` 3/3，`subject_sha256 == subject_sha256_end`。
- TQAEP 已以 **r7** receipt 重新編譯（27 fixture／27 oracle／27 test）：`independent_acceptance=NOT_GRANTED`。
- 天花板：同一 owner、無 runtime、無 DOC-05 真 Principal → 這是**設計級獨立通過**，不是驗收、不是 release。
- 若再改動 pi/ecp/pd 任何 byte，r7 receipt 立即失效，必須重跑 `bash run_checker_round7.sh`（改成 r8 檔名；stash 清單已含 r4–r7）。
- `finalize_s1.py` 讀 `PIPD/.b1_evidence/PRE_CHANGE_DIGESTS.json`；該目錄已搬到 `artifacts/PRE_CHANGE_DIGESTS.json`，重跑前先複製回去。

### 9.4 新增檔案

- `run_checker_round2.sh` / `run_checker_round3.sh` — 派工腳本（stash + nonce 注入 + 還原）
- `apply_checker_receipt.py` — 從 attempt stdout 抽 `CheckerReceipt@1`，驗 3/3 subject 綁定才落盤
- `_round2_receipt_raw.json` — r2 判決原文（含 C9 的 measured 細節）

## 2026-10-27 追加（FAR-4 丙案）
- canonical `d0d748f`：`compile-cc` 動詞＋`compile_slot_contract()`；PD-PKG@1 未動。
- 31 份 CC 於 `pipd-run/artifacts/cc/`；provenance `artifacts/cc_provenance.json`（10 KB / 21 delivered-only）。
- 124 條 slot oracle 於 `artifacts/slot_oracles.json`；`tqaep.json` 尚未替換（27 vs 31 分母待裁決）。
- 待 owner：①21 列來源裁決 ②oracle 分母（27 REQ-keyed vs 31 slot-keyed）③真金鑰 BOM ④第二 OS principal。

## 2026-10-27　FAR-7→Q6（最新）

- **推翻假設**：6 條不需 BOM 真鑰／第二 principal；簽 29 列不會生出 runner（registry 原僅 1 個 READ_ONLY_PROBE runner）。
- **已做**：2 支 HOST_OPERATIONS runner、registry 1→3（demo owner key）、2 條真跑並讀回（`artifacts/runtime_bindings.json`）、ORACLE_OWNER v9→v11 三輪收斂、CHECKER O5F（mimo 第三跑 PASS 4/4 ＋ deepseek 交叉 PASS 4/4）。
- **狀態**：2 executed（B1/B2/B3 PASS）／3 capability／1 owner；自檢 94/94；G-A 6/6；G-B HOLD；`mission_complete=false`。
- **下一步**：A3/B3-OPS/C1 需能力裁決（queue、DEV handoff、promotion），C4 需 owner 授予；要宣稱獨立驗收才需第二 OS principal，要 freeze/release 才需簽 `AuthorityBinding`。

## 2026-10-27 追加：FAR-8 → R1–R4

- A3/B3-OPS **真跑**（hermes_queue on SharedSpine 唯讀 cursor + 本地同 schema ledger；bridge_handoff 消費真實 commit `995c7ad`）。
- C1 只跑**拒絕路徑**（Fabric 政策禁 agent 自動晉升）；C4 POS 無 grant → `REFUSED_OWNER_GRANT_ABSENT`，NEG/SEC 已跑。
- registry runners **7**；自檢 **98/98**；G-A 6/6；G-B HOLD；`mission_complete=false`。
- 待 owner：C4 是否授予（principal/scope/ttl）；C1 正例需獨立 acceptance receipt。

## 2026-10-28 追加：PKG_08 GWO 收斂

- GWO-SBL **PASS**（7 raws、隔離 DataDir 已移除）；GWO-HGK **PASS**（issuer 驗簽／queue v1 lease 1 cursor 1931／effect rollback）。
- GWO-FABRIC **HOLD**（政策需 acceptance receipt、禁 agent 自晉升）；G-B **HOLD**（需第二 OS principal）。
- OpenSpec **13/18**；自檢 **104/104**；gates GWO 誠實為 `2/3 PASS`。
- 待 owner：acceptance receipt（FABRIC）、第二 principal（G-B）、30 route 簽章（1.4）、native issuer 主體（2.2）。

## 2026-10-28 追加二：PKG_08 三閘門全綠（等獨立稽核）

- OWNER 簽章儀式已跑：registry_rev **9**、**30/30 INSTALLED**、merkle `5f9fe5fc…`、`OWNER_SIGNATURE_VERIFIED`。
- **GWO-FABRIC PASS**（4 raws 同 sha/epoch、receipt 由 ACCEPT-AUTH 簽、3 個 typed NEG）；**G-B PASS**（revoke＋新 PID/session successor）；**3.2 PASS**（ACL deny ＋ 樹外 verdict）。
- OpenSpec **18/18**、自檢 **107/107**、gates：G-A 6/6、G-B PASS、GWO 3/3、`gates_conjunction=PASS`。
- 唯一 blocker：`independent_audit=PENDING`（codex 第三輪）。稽核 PASS 後 gates 會自動把 `mission_complete` 翻 true；`sourcefreeze`／`release` 仍 NOT_RUN。

## 2026-10-28 最終狀態（可直接接手）

- **mission_complete = true**（G-A 6/6、G-B PASS、GWO 3/3、獨立稽核 PASS、自檢 107/107、OpenSpec 18/18）。
- **未完成／仍 NOT_RUN**：`sourcefreeze`、`release`（DOC-13 L2775）、第二 OS principal（不需要）、外部人類獨立驗收。
- 重跑指令：`python -B gates.py` → `python -B selfcheck2.py` → `python -B sync_state.py`。三個必須同輪跑，`gates` 讀 `SELFCHECK.json`。
- 簽章：registry_rev 9、`OWNER-B1-d42c654cd1afba80`；`admit.py` 對未簽 registry 回 rc 6 `REFUSED_REGISTRY_UNSIGNED`。
- 已知陷阱：`CREATE_NEW_CONSOLE|DETACHED_PROCESS` 會 WinError 87；icacls deny 需在解析後套用；codex `-s read-only` 在本機無法 exec（checker 改用獨立進程 + 獨立 profile）。

## F-43/FAR-12 接手點（owner 待做一步）

- 現況：`owner_signature_attribution=ADMINISTRATIVE_ONLY`（明文金鑰可被同使用者進程讀取）。
- owner 執行：`python owner_ceremony.py --workspace C:/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027 --secure`
  → 輸入口令（≥12 字、不落檔）→ 就地包裝 `owner.key.enc`、刪除明文、寫 `artifacts/OWNER_ATTESTATION.json`、驗證 rev 9 仍有效。
- 之後自檢 C109 會自動改判 `CRYPTOGRAPHIC_OWNER_CONTROL`；若 envelope 存在但無口令，簽章回 `REFUSED_OWNER_KEY_LOCKED`。
- 不要做的事：直接 `--rotate`（cosmetic）、第二 OS 使用者、HSM。

## FAR-12 已完成（2026-10-28）

- owner key 已包裝：`~/.hgk-owner/owner.key.enc`（scrypt+AES-GCM）、明文已刪、`unlock.dpapi` 託管、rev 9 仍驗簽通過。
- attribution = `CRYPTOGRAPHIC_OWNER_CONTROL_WITH_LOCAL_ESCROW`（C109 會在狀態不符時報紅）。
- 要升級到「owner 獨占」：owner 執行 `python owner_ceremony.py --workspace C:/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027 --repass`（輸入新口令，工具會刪除託管檔）。
- 驗證指令：`python owner_ceremony.py … --verify-unlock`（只印指紋與 registry 驗簽結果）。

## FAR-13：owner 獨占（待 owner 一步）

- 現況 `CRYPTOGRAPHIC_OWNER_CONTROL_WITH_LOCAL_ESCROW`；**已量測**：鎖住金鑰後 `selfcheck 108/108`、`mission_complete=true`、registry 不變 → 委外託管不是無人值守的必要條件。
- owner 執行 `--repass` 後 → `CRYPTOGRAPHIC_OWNER_CONTROL`（無託管）；口令遺失走 `--rotate`（rev+1，舊信封歸檔）。
- 新增：`--rotate`、`RECOVERY.md`、`prove_unattended.py`、`owner_vault.status()` 三態。

## 2026-10-28 11:40 — owner key 已達 `CRYPTOGRAPHIC_OWNER_CONTROL`

- 無託管、無明文；簽章需 owner 口令；`--verify-unlock` 無口令回 `REFUSED_OWNER_KEY_LOCKED`。
- registry 仍 rev 9、`OWNER_SIGNATURE_VERIFIED`；自檢 108/108；`mission_complete=true`。
- 口令遺失 → `python owner_ceremony.py --workspace … --rotate`（rev+1、舊信封歸檔）。
- 不可再跑 `--secure`／`--seal`（需要 escrow，會回 `REFUSED_*`）；如需改口令用 `--rotate` 重新provision。

## 2026-10-28 FAR-14 完成（F-49 已封）

- `admit.py`：`HGK_REGISTRY_PATH` 可覆寫；`init-keys`／`sign-canary` 對已簽 registry 回 rc 6 `REFUSED_LEGACY_DEMO_PATH_ON_SIGNED_REGISTRY`；`selftest` 回 rc 7（F-36）。
- `run_s2_s3.py`：改寫 `admission/demo/registry/runner-registry.json`（首次自動以 pre-ceremony 備份 seed，標 `demo:true`），並在 `S2_EVIDENCE.json` 記錄 live 前後 sha（`unchanged: true`）。
- 自檢 **110/110**（C110／C112 新增）；`mission_complete=true`；live registry **rev 10**、驗簽通過、未被本輪觸碰。
- 並行 writer（F-50）：修補前已快照 `artifacts/f49_snapshot/`；若另一 session 繼續改同一批檔案，請先比對該快照。

## FAR-15 之後：每個回合先做這兩件事

```bash
cd /c/Projects/Agent_Workspace/var/B1-PIPD-PKG-20261027
python -B owner_preflight.py --ops <宣告的 op> --task <task_id>   # rc0=NONE rc10=WINDOW_READY rc11=DEDICATED
python -B owner_window.py status
python -B writer_lease.py status
```

- 簽章窗口：`python -B owner_window.py open --task <id> --ttl-hours 8 --max-ops 60`
  → 彈出 **tkinter 原生視窗**（遮蔽輸入、口令不出本進程；`HGK_OWNER_UI=ps` 可退回 PowerShell）
  → 之後 `owner_ceremony.py` 自動走窗口、**不再提示**；`ui_impl` 記在 window.json／SIGNING_LOG。
- 路由全表見 `GOVERNANCE_ROUTING.md`；`release/sourcefreeze/policy-authority/trust-anchor/owner_enrollment`
  永遠要當場口令，窗口會拒絕。
- 「沒有窗口」不是 BLOCKED，正確講法是 `NEEDS_OWNER_WINDOW`（開窗即續）。