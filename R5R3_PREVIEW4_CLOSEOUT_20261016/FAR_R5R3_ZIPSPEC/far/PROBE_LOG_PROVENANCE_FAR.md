# Probe log provenance — R5R3 FAR sub-round

Two background processes finished after the packet was published; both were already consumed by the round, but one
of them exposes a **log-overwrite provenance gap** that this note closes rather than leaves implicit.

## P2: one superseded aborted attempt whose log was overwritten

- What happened: an earlier background attempt of `ui_probe_flow.py 0x20622 …cand-B-r5y-known-good.zip P2 --nav`
  ran the flow with navigation enabled, landed on `chatgpt.com/plugins/Plugin_5ba168f715b8819190ccbe33a4a926b0`
  (the **installed** plugin's detail page), found no add control (`add button: False`) and **aborted**, writing
  verdict `ABORTED` to `probe_P2.json` at that moment.
- Cause and correction: the add affordance lives on the **plugins home** (`chatgpt.com/plugins`), not on a plugin
  detail page. The flow was corrected by navigating home (`ui_open_plugins_home.py`) and resuming
  (`ui_probe_after_picker.py`), which produced the accepted P2 run.
- Evidence effect: the aborted attempt wrote to the **same log path** (`raw/probe_P2.log`) and was therefore
  overwritten by the successful run. The packet's `raw/probe_P2.log` and `FAR_R5R3_ZIPSPEC/probe_P2.json` are
  the **successful** run (13 steps: picker ready, native path written, ENTER, picker closed, modal listing
  `cand-B-r5y-known-good.zip`, submit, title → `PIPD-LS-SP Public Skills | ChatGPT 外掛程式` at 3 s, the transient
  `無法取得` node, modal gone). The superseded attempt's output is reproduced verbatim below so it is not
  silently lost, and its `ABORTED` verdict is **not** part of the round's probe matrix.

```
EXIT=0
  artifact cand-B-r5y-known-good.zip 2f9ae010a6eba907 68355B
  window title: 'PokéSurvivor – Juego Pokémon 免費線上 estilo Survivor.io - Google Chrome'
  url before: 'pokesurvivor.com'
  new-tab button: True
  invoke() new tab
  omnibox: True
  omnibox set to https://chatgpt.com/plugins
  ENTER sent to omnibox (trusted)
  [1s] navigated: 'chatgpt.com/plugins/Plugin_5ba168f715b8819190ccbe33a4a926b0'
  add button: False
verdict: ABORTED -> …/FAR_R5R3_ZIPSPEC/probe_P2.json
```

Lesson recorded for the driver: a freshly created tab carried the session to the **last-visited** plugin page, so
"navigate to the plugins surface" must end at the plugins **home**; a plugin detail page has no add control and
must not be treated as a failed host response.

## First checker dispatch: the gate refusal is already in the packet

- Process `proc_f28f3b476b57`: `VERIFY_SECURITY` dispatch with `--force-rank 3 --require-arm
  opencode-go/deepseek-v4.1-flash` → **EXIT=4**, `identity_gate.arms[]` listing rank 3 as
  `opencode-go/glm-5.3-flash`, message `"the required arm is not in this lane's pool"`. Raw log: `raw/verify_ds_far.log`
  (already published). Cause: the mandated arm's pool rank had moved (it now sits at rank 1). Handle: re-dispatched
  at rank 1 with the same nonce → EXIT=0, `required_arm == served_arm == opencode-go/deepseek-v4.1-flash`.
  No gate was relaxed, no pool file was edited.

## Claim ceiling

This note records provenance and a superseded attempt. It changes no probe outcome, grants no acceptance, and does
not upgrade any ceiling: the host's refusal mechanism remains undisclosed and the P1–P5 outcomes remain
UI-observed.
