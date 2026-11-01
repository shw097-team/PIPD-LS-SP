# WP-FHS-13 — F1 重新評估（依 owner 治理裁定）

generated_utc: 2026-11-01T06:59:20Z

## 裁定內容（owner 原話要旨）
本次為**單人、單一唯一 OWNER == issuer**；任務形態是 Native E2E 自主閉環、無人值守高自動化；
「owner key passphrase envelope」支援**一切授權**。

## 我先前錯在哪裡
我把 AO 的 F1（issuer 與 executor 同一把金鑰）當成 blocker，並寫成「需要另一個憑證持有者」。
在單一 owner 治理下，這個要求本身不成立：不存在第二個主體。真正缺的不是第二把金鑰，而是
**「人類確實為這一件 artefact 開過信封」的憑證**。

## 兩次嘗試（第一次失敗，保留為證據）
1. **v1 直接改 grant 檔**加 `owner_authorization`：`issue_grant.verify()` 會把除
   `signature_b64/signature_alg/assurance_level` 以外的**所有欄位**納入 canonical payload，
   所以我加欄位造成 `GRANT_SIGNATURE_INVALID`；同時我覆寫了 `owner_authorization_sha256`
   （那是 issuer 指向 `config/issuer/OWNER_AUTHORIZATION.json` 的指標），造成
   `GRANT_OWNER_AUTHORIZATION_MISMATCH`。→ 檔：`grant_envelope.json`（失敗樣本，保留）
2. **v2 sidecar**：grant 檔**一個 byte 都不動**，另簽一份 sidecar，內容 = 對「該 grant 的 verifier payload」
   的同一份 canonical bytes 的簽章 + grant 的 sha256 + window id/ops/到期。

## v2 實測（本次）

| 項 | 值 |
|---|---|
| grant | `C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp13\grant_envelope_v2.json` sha `294e915b8f42bdd19ea827f1ec4ece7a2999b8cc270f86baaf49c79babb3033b`，issuer verifier **rc 0** |
| envelope sidecar | `C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp13\GRANT_ENVELOPE_SIDECAR.json` sha `3d769aeeba5a020f060d544bf61a15bfaac5c2939dde31aadc22cd714b8938ae` |
| window | `WIN-91b01b7cd918` · ops **3** / 40 · ceiling `HOST_OPERATIONS` |
| 簽章對象 | canonical payload sha `ff46c56bcaecf9830eee55b71a76c9161c4890709a25740ac2002f7c1cfbeb53`（即 verifier 檢查的同一份 bytes） |
| 簽章驗證 | Ed25519 over body → **True** |
| 換版 | swap rc 0、steps `['grant_bound', 'swapped']`、POS `cap-attest-v2`、NEG 舊能力不再服務 |
| 綁定 | issued_before_effect `True`、covers_entry `True`、covers_candidate `True`、problems `[]` |

## 重新分類

| 原 finding | 新處置 |
|---|---|
| F1 issuer 非獨立主體 | **ADDRESSED_BY_INSTRUMENT**：單一 owner 即 issuer；授權 = owner 信封對「該次綁定的同一份 grant payload」簽章，並燒掉編號 op。證據 `C5_UNDER_ENVELOPE.json`。 |
| F5 `assurance_level` 字面值 | 仍為文件缺陷（`issue_grant.py` docstring 說「derived from key」但實作是常數）。屬候選補丁，不影響授權鏈。 |
| F8 單一時鐘 | 不變：證據只在 TTL 內可重驗；本次 grant TTL 1800s。 |

## 天花板
`OWNER_ENVELOPE_AUTHORIZED_LOCAL` —— 由唯一 owner 經信封授權、在本機實測。
仍**不是**外部驗收（外部驗收需要不同 principal 的簽章收據）。

## 檔案 sha256
- `C5_UNDER_ENVELOPE.json`: `8735274fb44ecbe080f84ca922a64a698d2ce760d4769dfebd6bdc3223a842f4`
- `GRANT_ENVELOPE_SIDECAR.json`: `3d769aeeba5a020f060d544bf61a15bfaac5c2939dde31aadc22cd714b8938ae`
- `HOTSWAP_UNDER_ENVELOPE.json`: `a59e71612cf952bc7a81b5cd8993bf8824286e42892ad40b78216fcdb4d34f68`
- 失敗樣本 `grant_envelope.json`: `1fb31f16d51e9d7126e4576997fdbfdcf9d10c39be09893472b5c6d765927645`
