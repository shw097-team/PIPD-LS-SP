import json,os,re,subprocess
from pathlib import Path
root=Path.cwd(); ao=root/'.ao-r3b'; rnd=root/'.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
workflow=(root/'.github/workflows/public-plugin-verify.yml').read_text(encoding='utf-8')
script=workflow.split('        run: |',1)[1].split('\n      - name:',1)[0]
script='\n'.join(line[10:] for line in script.splitlines() if line.strip())+'\n'
(ao/'workflow-guard-verbatim.sh').write_text(script,encoding='utf-8')
records=[]
for name,base in [('main','224591431a164ab72a9423cd180e417e8a762403'),('stacked','52542c395a0f91dc2ba4bd6123acd4cdecd780dc')]:
    env=os.environ.copy(); env['PR_BASE_SHA']=base; env['STACKED_BASE_SHA']='52542c395a0f91dc2ba4bd6123acd4cdecd780dc'
    result=subprocess.run(['C:/Program Files/Git/usr/bin/bash.exe','.ao-r3b/workflow-guard-verbatim.sh'],cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (ao/('guard-'+name+'.log')).write_bytes(result.stdout)
    records.append(dict(name=name,base=base,exit=result.returncode,output=result.stdout.decode('utf-8',errors='replace')))
    print(name,result.returncode,records[-1]['output'][-800:])
receipts=json.loads((rnd/'verify/r3/FAR_MEASUREMENT_RECEIPTS.json').read_text(encoding='utf-8'))
findings=json.loads((rnd/'verify/ao12/FINDINGS.json').read_text(encoding='utf-8'))
extra=dict(guards=records,findings_count=len(findings),missing_series_locator=not (rnd/'SELF_ITERATION_AFTER_AO.md').exists(),vendor_bytes=(root/'packaging/public-plugin/vendor-plugin.schema.json').stat().st_size,receipt=receipts,skills=sorted(path.parent.name for path in (root/'skills').glob('*/SKILL.md')))
(ao/'supplement.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2),encoding='utf-8')
