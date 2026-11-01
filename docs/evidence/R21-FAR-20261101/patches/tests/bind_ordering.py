import json, sys
from pathlib import Path
sys.path.insert(0, r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\patches\PIPD\tools')
import importlib.util
spec = importlib.util.spec_from_file_location('hs', r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\patches\PIPD\tools\hotswap.py')
hs = importlib.util.module_from_spec(spec); spec.loader.exec_module(hs)
grant = json.loads(Path(r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp13\grant_covering.json').read_text(encoding='utf-8'))
issued = grant['issued_at']
entry = Path(r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp13\fixture-covering\candidate.py')
cand = Path(r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\wp13\fixture-covering\candidate.py')
out = {}
for label, started in (('started_after_grant', issued + 5), ('started_before_grant', issued - 5)):
    info, problems = hs.bind_grant(Path('C:\\Projects\\Agent_Workspace\\var\\FHS-R21-FAR-TT-20261101\\wp13\\grant_covering.json'), entry, cand, __import__('hashlib').sha256(cand.read_bytes()).hexdigest(),
                                   Path(r'C:\Projects\Agent_Workspace\HG-KSEOS\scripts\issue_grant.py'), started_epoch=started)
    out[label] = {'issued_before_effect': info.get('issued_before_effect'),
                  'ordering_reference': info.get('ordering_reference'), 'problems': problems}
print(json.dumps(out, indent=1))
