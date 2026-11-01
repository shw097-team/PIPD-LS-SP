# WP-FHS-20 — Kind 面探測與分母裁定

generated_utc: 2026-11-01T07:33:59Z

探測範圍：CLI 自報 **69 個子命令**，逐個 `--help` 存檔並記 rc／bytes／sha256；根 help sha `c72cb354ff90c30ba34805377ffeca58451f2ec1a435aca730610877fbfb7177`。

## 裁定（附量測）

| 處置 | 數量 | Kind |
|---|---:|---|
| 有主機安裝面 | 4 | AGENT_SKILL, PROFILE, PLUGIN, CLI_TOOL |
| 有可載入面、無安裝動詞 | 1 | SIMPLE_AGENT |
| 完全無面 | 3 | AGENT_OS, AI_SYSTEM, GENIE/GENIE.md |

**blocker 的 7 與我先前的 5，兩者都撤回**：實測為 3 個完全無面、1 個有面無安裝器、4 個有安裝面。

## 逐 Kind 證據

### AGENT_SKILL — INSTALL_SURFACE_MEASURED
- `skills` rc=0 sha256=92063796456f3b2029abd1f395c5370412987835e69f1c6bdf0985a0d731393a 『{trust,untrust,browse,search,install,inspect,list,check,update,audit,uninstall,reset,list-modified,diff,opt-out,opt-in,repair-official,publish,snapshot,tap,config} ...』

### PROFILE — INSTALL_SURFACE_MEASURED
- `profile create` rc=0 sha256=fa9c98c9f390108e5456b2fd4cea50b9dcc293bb5d21abd6466a3538c0343b0c 『hermes profile create <name>』

### PLUGIN — INSTALL_SURFACE_MEASURED
- `plugins` rc=0 sha256=8063f0eca98aff6708d53073faffe75d064a981938b13b12ebd3bc156cb47875 『{install,search,browse,validate,update,adopt,trust-update-url,check-updates,check,remove,rm,uninstall,list,ls,enable,disable,capabilities,doctor,pack,show,info} ...』
- `plugins validate (real plugin inside the cell home)` rc=0 sha256=4c7f512ed2770cc31bd2353027a375905e90d6b95647d912e59eaa6e74bba10f 『disk-cleanup copied into home-base/plugins validates rc=0』

### CLI_TOOL — INSTALL_SURFACE_MEASURED
- `lsp` rc=0 sha256=4c2905dd7b8627efac675ee0e6217dac9f3a7099cd53fce231a3b663c3e139cd 『install             Install a server binary』
- `computer-use` rc=0 sha256=3a4d22fb639b88e57aaec380162f01f5268cedaa382b5f2f82c0d3bb695710f3 『Install or check the cua-driver binary used by the `computer_use` toolset.』
- `mcp` rc=0 sha256=01ec95ead7a7c73bb8c0043b56388e958ed8ef09e5ac260aff378bab6a615bf6 『{add,remove,rm,list,ls,test,configure,config,login,reauth,picker,catalog,install} ...』
- **更正**：my earlier CLI_TOOL=NO_SURFACE was wrong: the host carries three literal binary/package installers

### SIMPLE_AGENT — SURFACE_EXISTS_NO_INSTALL_VERB
- `dir C:/Users/user/.claude/agents` rc=0 sha256=檔案／目錄量測 『ocx-gpt-5-4-mini.md, ocx-gpt-5-5.md, ocx-gpt-5-6-luna.md, ocx-gpt-5-6-sol.md, ocx-gpt-5-6-terra.md』
- `pets` rc=0 sha256=e31c0266ac4ba6605dcbaa55373f95d21f99ba6bc5937dbc87a1b91e13e962c1 『install             Install a pet from the gallery』
- 註：no install verb for agent definitions was found on either host; placement is by file

### AGENT_OS — NO_SURFACE_MEASURED
- `acp` rc=0 sha256=a86af3b7c59ad2f4435ca7859792ce55e9412a2f944d84522a1aff2d5d9bb89c 『Start Hermes Agent in ACP mode for editor integration (VS Code, Zed,』
- 註：69 verbs probed; none installs an operating runtime

### AI_SYSTEM — NO_SURFACE_MEASURED
- `chat` rc=0 sha256=6fb4a3e0e5ee846a9733b9cc966ebe59ff86cb5db269c11276b2246ac14a9cb4 『--pass-session-id     Include the session ID in the agent's system prompt』
- 註：no verb packages a system prompt as a unit

### GENIE/GENIE.md — NO_SURFACE_MEASURED
- `find + 69 help probes` rc=0 sha256=檔案／目錄量測 『0 hits for GENIE*.md outside HG-KSEOS design docs; 0 verbs mention genie』

## 後果

- WP-FHS-20 收斂到 **AGENT_SKILL／PROFILE／PLUGIN／CLI_TOOL** 四個有安裝面的 Kind（前兩者已有 18／12 格實跑）。
- **SIMPLE_AGENT** 需在 Claude Code 主機另開 cells；本次只記錄 5 份定義存在，不宣稱已驗。
- **AGENT_OS／AI_SYSTEM／GENIE** 以 `NO_HOST_SURFACE` 作為可接受 cell 狀態，解除條件＝上表探測；主機新增安裝面時重跑 `tools/wp20_kind_surface_probe.py` 即推翻。

檔案 sha256：`KIND_SURFACE_RULING.json` c0f85cd01a7f8b1997c47295a72c4351ee5e665cb37512a17ad8c18e9a28e380
