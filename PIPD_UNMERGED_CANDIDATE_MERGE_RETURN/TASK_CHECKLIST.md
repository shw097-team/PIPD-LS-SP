# 任務執行清單（證據 commit 前回填；殘留 `[ ]` = 缺陷）

- [ ] `T-01` HGK typed admission（`PIPD-MERGE-UNMERGED`）
- [ ] `T-02` GSTACK route check（含負向對照）
- [ ] `T-03` OpenSpec change ＋ `validate --strict`
- [ ] `T-04` KANBAN gate 鏈（M0–M7）
- [ ] `T-05` M1 本地 scratch worktree 依序合併 #18 → #17 → docs 候選（`--no-ff`）
- [ ] `T-06` M2 **G1** 併後全套測試；**G2** PR #18 guard 在併後 main 上跑
- [ ] `T-07` M3 **G3** 逐位元確認 `.4` tag／資產、`src/`、`schemas/` 未變
- [ ] `T-08` M4 單一 push `origin HEAD:refs/heads/main` ＋ 遠端尖端／PR 狀態回讀
- [ ] `T-09` M5 證據包（含裁決全文、逐條分類、併前後尖端、測試輸出摘要）＋自 shipped bytes 清冊
- [ ] `T-10` M5 自 origin 位元獨立複驗（方法異於建包）
- [ ] `T-11` M6 VERIFY 車道（CODEX CLI）獨立複驗併後狀態；裁決逐字入包
- [ ] `T-12` M7 FAR learning ＋ skill ＋ memory ＋ Owner 交還包
- [ ] `T-13` 明確不做項留痕（tag／release／`.4`／刪分支／關 PR／第 4 條分支）
