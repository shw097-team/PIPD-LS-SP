from pathlib import Path
import hashlib
import json

ROUND = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORKTREE = ROUND.parents[2]
SRC = Path('C:/Users/user/AppData/Roaming/npm/node_modules/@bitkyc08/opencodex/src')
evidence = []

def add(identifier, location, ranges, role='historical round artifact'):
    absolute = location if isinstance(location, Path) else ROUND / location
    raw = absolute.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    excerpts = []
    for first, last in ranges:
        assert 1 <= first <= last <= len(lines), (identifier, first, last, len(lines))
        excerpts.append({'start_line': first, 'end_line': last, 'quote': '\n'.join(lines[first-1:last])})
    try:
        display = absolute.relative_to(WORKTREE).as_posix()
    except ValueError:
        display = absolute.as_posix()
    evidence.append({'id': identifier, 'path': display, 'role': role, 'bytes': len(raw),
                     'sha256': hashlib.sha256(raw).hexdigest(), 'line_count': len(lines), 'excerpts': excerpts})

for identifier, stamp in [('E01','101452'),('E02','101611'),('E03','102527')]:
    add(identifier, 'stage-b/MODEL_DECLARED_20261012T'+stamp+'Z.txt', [(1,1)])
for identifier, lane, error, ws, tools in [('E04','B1',612,85,[(88,90),(119,121)]),('E05','B2',1007,58,[(61,63),(322,324)]),('E06','B3',181,85,[(88,90),(117,119)])]:
    add(identifier, 'stage-b/'+lane+'_20261012T101452Z.log', [(1,10),(ws,ws)]+tools+[(error,error+1)])
    add(identifier+'X', 'stage-b/'+lane+'_20261012T101452Z.exit', [(1,1)])
for identifier, lane, stamp, ws in [('E07','B1','101611',85),('E08','B2','101611',58),('E09','B3','101611',85),('E10','B4','102527',92)]:
    filename = 'stage-b/'+lane+'_attempt3_20261012T'+stamp+'Z.log'
    ranges = [(1,10),(ws,ws)]
    if lane=='B2': ranges += [(1498,1500),(1537,1544)]
    add(identifier, filename, ranges)
    add(identifier+'X', filename[:-4]+'.exit', [(1,1)])
for identifier, name in [('E11','probe_opencode-go_deepseek-v4_1-flash.log'),('E12','probe_opencode-go_deepseek-v4-flash.log'),('E13','probe_gpt-6.1-sol.log')]:
    add(identifier,'stage-b/'+name,[(1,10),(13,24)])
add('E14','stage-b/PROBE.md',[(1,3)])
add('E15','stage-b/run_lanes_v2.sh',[(1,24)])
add('E16','stage-b/run_lanes_v3.sh',[(1,30)])
add('E17','stage-b/fallback-green.log',[(1,1)])
add('E18','AO2_RESULT.md',[(3,8),(35,43)])
add('E19','SELF_ITERATION_AFTER_AO.md',[(3,11),(35,43)])
add('E20','ROUND_RESULT.md',[(3,5),(64,68),(78,80),(103,107)])
add('E21','verify/ao/AO_VERDICT_STAGEB.md',[(278,294)])
add('E22','stage-b/FAR_20261012T115535Z.log',[(1,10),(2767,2767),(2781,2782)])
add('E22X','stage-b/FAR_20261012T115535Z.exit',[(1,1)])
current='current host snapshot; not a frozen 10:14Z configuration or proof of code loaded then'
add('E23',Path('C:/Users/user/.codex/desktop-model-catalog.json'),[(2,3),(65,67),(75,93),(224,226),(234,262)],current)
add('E24',Path('C:/Users/user/.codex/config.toml'),[(1,11)],current)
add('E25',Path('C:/Users/user/.codex/desktop-model-router/config.json'),[(2,5),(24,24),(26,26),(247,254),(272,274),(284,284)],current)
add('E26',Path('C:/Users/user/.codex/desktop-model-router/router.ts'),[(1,2),(33,41)],current)
add('E27',SRC/'providers/registry.ts',[(352,353),(1087,1088),(1132,1133)],current)
add('E28',SRC/'adapters/openai-chat.ts',[(332,354)],current)
add('E29',SRC/'router.ts',[(288,288),(598,625),(656,665)],current)
add('E30',SRC/'server/index.ts',[(682,689)],current)

report = {
 'finding_id':'FAR-S4POST-MODEL-DEVIATION-20261012-001',
 'subject':'Declared EXECUTE opencode-go/deepseek-v4.1-flash: three failed lanes; reruns requested opencode-go/deepseek-v4-flash with effort none. Test maker thinking-mode adapter attribution, transport, and serving identity.',
 'scope':{'mode':'READ_ONLY_RESEARCH_AND_REPORT','date':'2026-10-12','timezone':'Asia/Taipei','writes':'Only this round verify/far: two reports and this UTF-8 writer; no candidate repair, model substitution, live inference, commit, push, or credential use.',
          'path_resolution':'Round records resolved to this round root, not the literal ../../ from stage-b (which would leave the round). Prior FAR is stage-b/FAR_20261012T115535Z.log. B4 rerun actually has stamp 102527Z, not 101611Z; no invented B4 101611 file.'},
 'evidence':evidence,
 'sequence':[
  {'order':1,'time_utc':'2026-10-12T10:13:15.561537Z','event':'v4.1/high probe: local websocket 426, then PROBE_OK and generated MODEL_SEEN=claude; no probe exit artifact supplied.','evidence':['E11','E14']},
  {'order':2,'time_utc':'2026-10-12T10:13:23.938664Z','event':'v4/high probe: same websocket 426, then PROBE_OK and generated MODEL_SEEN=gpt-5-codex. gpt-6.1-sol/medium probe has metadata warning and MODEL_SEEN=unknown; its exact start time is not recorded in these excerpts.','evidence':['E12','E13']},
  {'order':3,'time_utc':'2026-10-12T10:14:52Z','event':'Declaration v4.1; v2 starts B1/B2/B3 on loopback 10102 with catalog reference; no explicit effort override. Each CLI reports high. Each executes tools, then returns provider-reported 400 reasoning_content replay rejection and exit 1. No terminal capacity/unavailable error in these three lanes.','evidence':['E01','E04','E04X','E05','E05X','E06','E06X','E15']},
  {'order':4,'time_utc':'2026-10-12T10:16:11Z','event':'New declaration v4; v3 B1/B2/B3 changes BOTH requested model and effort to none. All exit 0 despite initial websocket 426. B2 lines 1537-1542 quote the old failed B2 log as output of Get-Content (1498-1500); these are NOT a live backup failure.','evidence':['E02','E07','E07X','E08','E08X','E09','E09X','E16']},
  {'order':5,'time_utc':'2026-10-12T10:25:27Z','event':'B4 rerun declared v4/none; websocket 426, final exit 0. Overlap with earlier writers possible: no precise completion timestamps establish non-overlap or a strict finishing order.','evidence':['E03','E10','E10X']},
  {'order':6,'time_utc':'2026-10-12T11:55:35Z (filename start stamp)','event':'Previous FAR requested gpt-6.1-sol/medium. Writer handoff error then two direct Selected model is at capacity errors; exit file 1. No FAR result existed when this research started. Capacity is a second, distinct lane-availability observation, not the cause of the earlier 400s.','evidence':['E22','E22X']}
 ],
 'probe_trust':[
  {'probe':'E11','printed':'CLI model v4.1 / provider openai / high; websocket 426 at ws://127.0.0.1:10102/v1/responses; PROBE_OK; MODEL_SEEN=claude (Anthropic; cannot verify exact version — no reliable self-introspection).','trust':'CLI header proves requested configuration, not actual upstream. Generated identity has no authentication value. The 426 proves rejection by that local websocket endpoint, not Anthropic service or total unavailability. Subsequent completion implies another functioning response path, likely HTTP fallback; exact upstream not established by this log.'},
  {'probe':'E12','printed':'CLI model v4 / provider openai / high; same local 426; PROBE_OK; MODEL_SEEN=gpt-5-codex.','trust':'Same ceiling. A successful one-shot at high neither tests history replay nor qualifies v3 effort none. The self-ID discrepancy is an identity-verification warning, NOT proof of silent GPT routing.'},
  {'probe':'E13','printed':'CLI model gpt-6.1-sol / provider openai / medium; metadata not found, defaulting to fallback metadata; PROBE_OK; MODEL_SEEN=unknown.','trust':'Metadata fallback is client capability metadata, not proven model fallback. Absence of a websocket complaint does not prove OAuth origin or direct backend identity. No transport-authenticated model receipt is in this probe.'}
 ],
 'hypotheses':[
  {'statement':'The three original lane processes failed because their continuations were rejected for the thinking-history reasoning_content requirement.','verdict':'SUPPORTED','evidence':['E04:612-613','E05:1007-1008','E06:181-182','E04X','E05X','E06X'],'qualification':'Observed immediate failure category; not exact implementation blame.'},
  {'statement':'The declared model was wholly unavailable or never answered.','verdict':'REFUTED','evidence':['E11:18-24','E04:88-90','E06:88-90'],'qualification':'It answered via the requested route enough to generate text and invoke tools; no proof of upstream model identity or universal availability.'},
  {'statement':'Websocket 426 alone caused the nonzero lanes or demonstrates that another provider served them.','verdict':'REFUTED','evidence':['E11:17-24','E12:17-24','E07:85','E07X','E09:85','E09X','E10:92','E10X','E30'],'qualification':'Same warning precedes successful probes and exit-0 reruns. Current source intentionally rejects disabled WS to trigger HTTP; historical fallback route remains inferred.'},
  {'statement':'The defect only manifests once the transcript is long.','verdict':'NOT_SEPARABLE','evidence':['E16:3-6','E06:88-119','E06:181-182'],'qualification':'Shortest failure follows two tool invocations. No controlled length variation, wire history, or threshold measurement; transcript growth is not established as the necessary trigger.'},
  {'statement':'Changing only the model fixed the defect, proving a v4.1-specific runtime implementation bug.','verdict':'NOT_SEPARABLE','evidence':['E15:15-17','E16:19-23','E04:8','E07:8'],'qualification':'Model and reasoning effort changed together. No same-model none run or v4 high multi-turn control. A successful text-only v4 high probe cannot separate them.'},
  {'statement':'Local adapter metadata omits v4.1 from the reasoning-replay eligibility list, so the currently installed adapter does not emit reasoning_content for this model on the shown path.','verdict':'SUPPORTED','evidence':['E25:247-254','E27:352-353','E27:1132-1133','E29:288','E28:338-353'],'qualification':'Both configured and registry lists omit the ID; merged eligibility gates output and cached replay. This is an observed current model-capability registration gap. Medium-confidence explanation of historical 400s because no frozen loaded source/config or historical wire capture was supplied.'},
  {'statement':'The historical failed requests used exactly the current metadata/code, and no other client/relay/upstream component lost reasoning history.','verdict':'NOT_SEPARABLE','evidence':['E04:612-613','E25','E26','E27','E28'],'qualification':'Present snapshot cannot certify code/config active at 10:14Z. Sanitized rejected request and loaded version digest are missing.'},
  {'statement':'The model actually serving the probes/writers was Claude or GPT rather than requested DeepSeek (silent model-route substitution).','verdict':'NOT_SEPARABLE','evidence':['E11:20','E12:20','E15:15-16','E29:598-625'],'qualification':'Self-report is not identity evidence. Current resolver handles configured explicit namespace without falling to default provider; this weighs against local silent fallback for that config but does not prove historical or upstream routing. Actual silent substitution is a distinct provenance defect class, not demonstrated here.'},
  {'statement':'The harness allowed a requested-model deviation and did not fail closed when child lanes failed.','verdict':'SUPPORTED','evidence':['E01','E02','E03','E15:7-23','E16:11-30'],'qualification':'EXEC_MODEL override and v3 default permit changed declaration without comparing to immutable round assignment. Children record exits; final echo LANES_DONE normally returns 0. Outer historical exit is not supplied, so this is a control-flow defect, not a fabricated observed parent exit.'},
  {'statement':'The backup B2 itself emitted the same fatal 400 shown at lines 1537-1538.','verdict':'REFUTED','evidence':['E08:1498-1500','E08:1537-1544','E08X'],'qualification':'Nested historical log output, same old request ID, then continuation and final exit 0.'},
  {'statement':'The earlier FAR suffered an additional lane-capacity failure.','verdict':'SUPPORTED','evidence':['E22:2781-2782','E22X'],'qualification':'Exact direct observations; cannot attribute to concurrency, rate limit, or provider pool. Writer encoding failure is separate.'}
 ],
 'root_cause':{
  'statement':'Immediate original failure: provider-reported thinking-history replay contract rejection during tool continuation. Best-supported mechanistic lead: v4.1 is advertised in the client catalog but absent from BOTH current relay and registry reasoning-content preservation lists; the current adapter gates replay on those lists. Deviation-enabling root: the launcher lacks immutable assignment admission, multi-turn qualification, and child-exit aggregation, so a text-only probe plus a model-and-effort switch could produce candidates without proving the assigned execution route.',
  'confidence':'MEDIUM',
  'confidence_breakdown':'HIGH for the observed 400/exit-1 category and visible launcher gap; HIGH for current replay-registration omission; MEDIUM for that omission as historical implementation root; LOW for any claim of actual serving-model identity.',
  'residual_uncertainty':'No captured outgoing assistant history, frozen loaded adapter/config digest, or correlated resolved/upstream model response. Cannot rule out additional history loss in Codex/relay/upstream, or isolate effort none from model change. Cannot establish transcript-size necessity or silent upstream model substitution.',
  'evidence':['E04','E05','E06','E15','E16','E23','E25','E27','E28','E29']
 },
 'document_cross_check':[
  {'document':'stage-b/run_lanes_v3.sh:3-6,14','finding':'The observed 400 text and 3/3 original failures are supported. Calling it a v4.1 adapter bug once transcript grows is more precise than historical logs permit. Current registration omission provides a concrete candidate component, not historical proof. Healthy one-line echo is only a text-path check.'},
  {'document':'AO2_RESULT.md:3-5,37-38; SELF_ITERATION_AFTER_AO.md:4-5','finding':'They identify requested checker gpt-6.1-sol/openai and describe different-model independence; these are role/request records, not transport-authenticated served-model identity. Neither diagnoses the writer 400 root cause. Do not turn them into such evidence.'},
  {'document':'ROUND_RESULT.md:66,78-80; verify/ao/AO_VERDICT_STAGEB.md:278-294','finding':'Round result points to lane-substitution disclosure and says no independent checker receipt for its then-subject, whereas later AO/AO2 report challenges of different subject tips. These are differently scoped/time-versioned records, not a model-cause contradiction. No thinking-adapter diagnosis in the three round-root documents or first AO verdict; the precise causal assertion is in v3 script, not validated by these acceptance records.'},
  {'document':'stage-b/fallback-green.log:1','finding':'BUILT fallback.md ... DOC_MOUNT_ONLY is a web/document packaging result, not model failover, model availability, or authenticated model identity evidence.'}
 ],
 'remedy':{
  'recommendation':'Lowest-friction prevention is a fail-closed admission gate in the launching harness: pin the immutable round model AND effort; refuse any changed model before writers start; run a no-candidate-write two-tool-roundtrip qualification through the identical CLI/endpoint/catalog/effort and require process exit 0; aggregate actual child exits. This would expose the observed replay rejection before the production writer pool and block the later changed-model run. It does not claim to authenticate upstream identity.',
  'smallest_diff_pseudocode':[
   'ROUND_MODEL := approved immutable assignment (v4.1 here); ROUND_EFFORT := approved explicit effort (high for original failing config)',
   'MODEL := EXEC_MODEL or ROUND_MODEL; if MODEL != ROUND_MODEL: emit MODEL_DEVIATION_REQUIRES_OWNER_DECISION; exit nonzero',
   'preflight := same CLI + 10102 endpoint + same catalog + MODEL + ROUND_EFFORT, no candidate write permissions, two harmless tool calls each followed by another assistant request',
   'if preflight child exit != 0 or required tool/result continuations did not complete: emit PREFLIGHT_FAILED plus actual transport error; exit nonzero; start zero writers',
   'start writers only on qualified config; retain immutable assignment plus requested configuration, receipt and raw preflight log separately',
   'wait each child; if any child exit != 0 or exit record missing: final harness exit nonzero; never overwrite assignment or automatically substitute a model'
  ],
  'hard_signal':'Child/process status and provider 400 rejection are cheap non-generated signals. Structured tool/result completion can qualify the exercised path; generated PROBE_OK/MODEL_SEEN cannot. A finite preflight cannot guarantee all later transcript lengths, so child-exit aggregation remains necessary.',
  'cost':{'files_touched_if_adopted':['stage-b/run_lanes_v2.sh','stage-b/run_lanes_v3.sh','one immutable assignment input plus one harness negative-test fixture in owner-selected harness test location'],
          'owner':'Round/harness owner; shared launcher owner should consolidate later rather than duplicate policy indefinitely.',
          'credential_or_service':'No new service or human credential for pin/equality and exit aggregation. A live preflight uses existing lane access, two harmless tool cycles, small token/latency cost; may refuse on capacity. Changed model/effort requires an owner decision and a new explicitly approved assignment, not an automatic retry.',
          'not_applied':'Research only: none of these files or runtime configuration was modified.'},
  'mechanistic_repair_candidate_not_authorized':{'change':'After owner confirms historical loaded route/version and an on-wire replay test, add deepseek-v4.1-flash to opencode-go.preserveReasoningContentModels in desktop-model-router/config.json (one list entry), or have adapter maintainer add the equivalent registry entry and regression. Confirm replay cache/parser handling as well; do not assume a list entry fixes missing thinking data.',
          'cost':'Desktop relay owner, one user-owned config file and reload/restart outside this lane authority; no new service/credential. Durable upstream registry support would touch providers/registry.ts and adapter regression tests; requires maintainer decision. Current source plus config strongly motivate this candidate but historical certainty is not available.',
          'verification':'Same v4.1/high two-tool replay fixture: before must reproduce missing reasoning_content/400, after must preserve prior assistant reasoning in outgoing payload and complete; capture sanitized request IDs and loaded config/source hashes. No live reproducer or repair was run here.'},
  'identity_extension_owner_decision':'For actual serving-model enforcement, require the RELAY resolver to refuse unknown/mismatched aliases before inference and return a request-correlated non-generated resolved provider/model receipt; launcher refuses missing/mismatch. Existing evidence does not demonstrate an available strict-route handshake. If this guarantee is required, relay owner must supply it; do not invent a header/API. A receipt that merely echoes the request is not sufficient, and relay-resolved identity still does not cryptographically authenticate vendor internals.',
  'candidate_tradeoffs':[
   'Immutable assignment equality plus aggregate exits: cheapest deterministic defense against the observed explicit substitution/hidden child status. Cannot establish actual upstream model.',
   'Two-cycle exact-config preflight: low incremental cost, catches this family of tool-history rejection earlier; adds inference latency and consumes existing quota.',
   'Current replay list registration: smallest plausible root repair, but owner-controlled, historical attribution uncertain, and separate from deviation prevention.',
   'Strict relay resolution receipt/refusal: right defense against silent model routing, but more owner work; not inferable from websocket status or client metadata.',
   'Reject every websocket 426 or merely disable websocket: cheap but wrong; it also occurs before successful runs and does not fix replay or identity.',
   'Self-ID probe/catalog-only admission/manual log review/long benchmark: respectively untrustworthy, insufficient, late, or higher friction than a startup gate.'
  ],
  'negative_tests':[
   'Set EXEC_MODEL=v4 while immutable assignment is v4.1: launcher MUST exit nonzero MODEL_DEVIATION_REQUIRES_OWNER_DECISION with zero writer starts.',
   'Stub exact-config preflight: first response/tool succeeds, continuation returns original provider 400 and exit 1 (even with PROBE_OK/MODEL_SEEN claiming v4.1): launcher MUST refuse and launch zero writers.',
   'Run fixture with children exiting 0,1,0 or missing exit receipt: lane-set MUST exit nonzero despite any candidate artifact or LANES_DONE text.',
   'Return websocket 426 then a successful authenticated configured HTTP path/tool completion: 426 alone MUST NOT fail qualification; failed HTTP continuation MUST fail it.',
   'If strict-route extension is adopted, resolve requested v4.1 to v4 or default OpenAI, or omit receipt: MUST refuse before inference/writers. Matching generated self-ID MUST NOT override refusal.',
   'If replay registration repair is adopted, remove the v4.1 entry: outgoing-history assertion and exact-config continuation test MUST go red, not succeed by falling back.'
  ],
  'must_not_do':[
   'Never relabel backup-produced artifacts as declared v4.1 outputs or erase original assignment/failure logs; preserve both requested histories and deviation.',
   'Never silently change model or effort, remove the declared model from the record, or make failed children green because files exist.',
   'Never authenticate identity with assistant self-report, catalog presence, a header echo, or websocket 426; never call the document fallback-green log model health.',
   'Do not infer model unavailability from these 400s or blame a particular historical adapter component as proved without historical payload/version evidence.',
   'Do not treat this research as acceptance, publication approval, or permission to modify runtime/code.'
  ]
 },
 'claim_ceiling':'RESEARCH FINDING ONLY. The three original requested-config lanes failed with thinking-history 400s; requested backup/none reruns exited 0. Current relay replay metadata omits v4.1 and supplies a concrete historical root-cause lead, not a frozen historical proof. No authenticated actual serving model, no controlled model-versus-effort causal isolation, no proof of universal model unavailability, no historical parent exit assertion, no live reproduction/repair, no release or acceptance grant.',
 'additional_observation':'Prior FAR log directly reports Selected model is at capacity twice (2781-2782), separately from UTF-8 patch handoff failure (2767). Capacity origin/concurrency not established; this run did not silently substitute a model or encounter a new capacity error.',
 'verification':{'all_listed_inputs_read':'All evidence entries decoded from full bytes and SHA-256 recorded; quotes retain original text with one-based line numbers. No credentials reproduced; current config excerpts selected only for non-secret routing metadata.',
                 'reports':'Writer reopens each distinct UTF-8/LF output, validates JSON and nontrivial size, prints byte count and SHA-256. No pre-existing reports were found; appended lane-mechanics observations are included without dropping required sections.'}
}

json_path = OUT / 'FAR_MODEL_DEVIATION_RESEARCH_RESULT.json'
md_path = OUT / 'FAR_MODEL_DEVIATION_SINGLE_EVIDENCE.md'
with json_path.open('w', encoding='utf-8', newline='\n') as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
    stream.write('\n')

md = ['# FAR model-deviation research — single evidence report', '',
      '**Finding:** '+report['finding_id'], '', '**Subject:** '+report['subject'], '',
      '## Bottom line', '', report['root_cause']['statement'], '',
      '**Confidence: MEDIUM.** '+report['root_cause']['confidence_breakdown'], '',
      '**Residual uncertainty:** '+report['root_cause']['residual_uncertainty'], '',
      'Evidence: '+', '.join(report['root_cause']['evidence'])+'.', '',
      '## Scope and path resolution', '', json.dumps(report['scope'],ensure_ascii=False,indent=2), '',
      '## Failure sequence', '']
for step in report['sequence']:
    md.append(str(step['order'])+'. **'+step['time_utc']+'** — '+step['event']+' Evidence: '+', '.join(step['evidence'])+'.')
md += ['', '## Probe trust and endpoint ceiling', '']
for item in report['probe_trust']:
    md += ['### '+item['probe'], '', item['printed'], '', item['trust'], '']
md += ['## Hypothesis testing', '']
for item in report['hypotheses']:
    md += ['### '+item['verdict']+' — '+item['statement'], '', item['qualification'], '', 'Evidence: '+', '.join(item['evidence'])+'.', '']
md += ['## Documents versus raw logs', '']
for item in report['document_cross_check']:
    md += ['- **'+item['document']+'** — '+item['finding']]
md += ['', '## Lowest-friction remedy (proposal only)', '', report['remedy']['recommendation'], '', '### Smallest concrete harness change', '', '~~~text']
md += report['remedy']['smallest_diff_pseudocode']
md += ['~~~', '', report['remedy']['hard_signal'], '', '### Adoption cost and ownership', '',json.dumps(report['remedy']['cost'],ensure_ascii=False,indent=2), '', '### Mechanistic repair candidate — NOT applied', '',json.dumps(report['remedy']['mechanistic_repair_candidate_not_authorized'],ensure_ascii=False,indent=2), '', '### Serving-identity guarantee', '',report['remedy']['identity_extension_owner_decision'], '', '### Friction comparison', '']
md += ['- '+item for item in report['remedy']['candidate_tradeoffs']]
md += ['', '### Negative tests (not run; adoption acceptance)', '']
md += ['- '+item for item in report['remedy']['negative_tests']]
md += ['', '### Must NOT do', '']
md += ['- '+item for item in report['remedy']['must_not_do']]
md += ['', '## Additional host hazards', '',report['additional_observation'], '', '## Claim ceiling', '',report['claim_ceiling'], '', '## Raw evidence, exact quotes and byte provenance', '', 'Paths below are workspace-relative unless absolute. Line numbers are one-based. Current host snapshots are explicitly marked and do not establish historical loaded state. Full input hashes bind the bytes read; only the relevant non-secret excerpts are reproduced.', '']
for item in evidence:
    md += ['### '+item['id']+' — '+item['path'], '', 'Role: '+item['role']+'. Bytes: '+str(item['bytes'])+'; lines: '+str(item['line_count'])+'; SHA-256: '+item['sha256']+'.', '']
    for excerpt in item['excerpts']:
        md += ['**'+item['path']+':'+str(excerpt['start_line'])+'–'+str(excerpt['end_line'])+'**', '', '~~~text']
        md += [str(excerpt['start_line']+offset)+': '+line for offset,line in enumerate(excerpt['quote'].splitlines())]
        md += ['~~~','']
md += ['## Artifact write verification', '', json.dumps(report['verification'],ensure_ascii=False,indent=2), '']
with md_path.open('w', encoding='utf-8', newline='\n') as stream:
    stream.write('\n'.join(md))
for location in [json_path,md_path]:
    raw=location.read_bytes()
    decoded=raw.decode('utf-8')
    assert len(raw)>10000 and '\r\n' not in decoded
    if location.suffix=='.json':
        parsed=json.loads(decoded)
        assert len(parsed['evidence'])==len(evidence)
        assert all(h['verdict'] in ['SUPPORTED','REFUTED','NOT_SEPARABLE'] for h in parsed['hypotheses'])
    print(str(location)+' bytes='+str(len(raw))+' sha256='+hashlib.sha256(raw).hexdigest())
print('READ_BACK_OK; evidence_files='+str(len(evidence))+'; no candidate or runtime changes performed')
