# PIPD-LS-SP 暫停／模型切換 Checkpoint

- 狀態：USER_PAUSED_MODEL_SWITCH；沒有背景續跑承諾。
- HGK Checkpoint：`CK-20261008-6ABC469C`
- Candidate：`829c17e87855cd7a1c88bfad1f51f1fdd1fafa5e`
- 驗收：S0–S4 均無本輪獨立 PASS。GLM 只完成工具煙測。
- 已停止兩個本輪 owned Codex invocation；FAR 子代理已結束。
- 核心候選只保存在 `C:\Projects\Agent_Workspace\HG-KSEOS\worktrees\pipd-r2-core-20261009`；未 apply／promotion。
- 原產品 writer 越界寫入 canonical edge_selfcheck.json 又自行還原；還原檔案已比對 HEAD，違規不因此消失。原事件見 SCOPE_INCIDENT_SUPERVISOR.json。
- Owner 選擇保留 Proprietary；授權檔尚未由 admitted writer 更新，不可假稱已閉合。
- HGK 原生 checkpoint 會替換 intent_json；原完整 lifecycle row 已保留，不自行 SQL 還原。
- 新模型尚未設定；恢復前須重驗 hashes 和 routing。

## 唯讀恢復檢查
```text
C:/Projects/Agent_Workspace/HG-KSEOS/.venv/Scripts/python.exe -B C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/cache/scratch/pipd_r2_pause_checkpoint_20261009.py --verify-only
```

此命令僅重驗／讀回，不會啟動 worker。
