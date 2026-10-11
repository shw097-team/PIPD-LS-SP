import json,sys
sys.path.insert(0,r'C:\Projects\Agent_Workspace\var\s4r2m-m2-clone\src')
from pipd_ls_sp import pipeline, validate
rec,_=pipeline.profile_record('LITE',['intent'])
rec=json.loads(json.dumps(rec))
out={}
legal=validate.validate_record('ProfileBinding',rec,r'C:\Projects\Agent_Workspace\var\s4r2m-m2-clone\schemas')
out['legal_exit']=0 if not legal else 1
out['legal_findings']=legal
for name,val in [('axes_str','intent'),('axes_int_item',['intent',42]),('profile_int',42),('vetoes_str','veto')]:
    r2=json.loads(json.dumps(rec))
    r2[{'axes_str':'axes','axes_int_item':'axes','profile_int':'profile','vetoes_str':'vetoes'}[name]]=val
    f=validate.validate_record('ProfileBinding',r2,r'C:\Projects\Agent_Workspace\var\s4r2m-m2-clone\schemas')
    out[name]={'exit':0 if not f else 1,'findings':f[:2]}
print(json.dumps(out))
