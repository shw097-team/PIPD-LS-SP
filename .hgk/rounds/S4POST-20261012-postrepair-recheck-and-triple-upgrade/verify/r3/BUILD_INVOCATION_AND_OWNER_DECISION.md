# 建構呼叫的精確形式，與需 owner 裁決的一點

> 依據：R8 第 2 輪獨立檢查器（claim 11）實測 `REFUSED ICON_MISSING`；其 §12 要求 owner 就「無生成模式建構是否為必要驗收契約」作出決定。

## 1. 事實

在**全新 clone** 內，`packaging/public-plugin/assets/icon-128.png` **不存在**——該目錄的 `.gitignore` 自述逐字：
「Icons under this directory are GENERATED, never committed as opaque binaries」，並指明以 `--generate-icons` 重新產生。
因此**不含 `--generate-icons` 的建構呼叫在全新 clone 內必然 fail-closed 拒絕**（`ICON_MISSING`），這是**設計**，不是缺陷。

## 2. 精確可重跑的呼叫（owner 授權供給後）

```bash
python tools/build_public_plugin.py \
  --source-root . \
  --ledger <round>/verify/r3/FROZEN_SOURCE_LEDGER.json \
  --source-commit 3233c817cc0a8fcd3f80f49219f219544235d25a \
  --packaging-root packaging/public-plugin \
  --out-dir <一個在 repo 之外的目錄> \
  --generate-icons
# 實測：BUILT …/pipd-ls-sp-public-skills.zip sha256=83e5ce5b4b3ac85e1be4842e16132c5450d2ae6074406a210debdc8a05bb4d87
#       members=56 claim_ceiling=LOCAL_PACKAGER_PASS_ONLY official_portal_verification=NOT_EXECUTED
```

第 2 輪檢查器以「補充模式」（= 上述含 `--generate-icons` 的形式）獨立得到**相同 sha256 `83e5ce5b…`** ✓；
而其「精確命令」（不含生成）則按設計拒絕。兩者不衝突：**差別就是前置條件**。

## 3. 需 owner 裁決的一點（檢查器 §12 提出）

**問**：`--generate-icons` 這個前置條件是否即為預期的驗收契約？
**maker 建議**：**是**。理由——(a) 圖檔依設計不入版控（避免提交不可審的不透明二進位）；(b) 產生器是確定性的，重跑得到**同一 sha256**（本輪兩次獨立產生一致）；(c) 若不接受生成前置，唯一替代是把產生的 PNG 提交入版控，那將牴觸該目錄自己明文的設計原則。
**在 owner 裁定前**：本輪不把「無生成模式建構」的成功當作任何主張，也不修改該設計。
