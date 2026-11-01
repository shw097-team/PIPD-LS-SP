import sys, json
from pathlib import Path
from pipd_ls_sp.abi import Need, make_consumer, ABI_VERSION
path = Path(r'C:\Projects\Agent_Workspace\var\FHS-R21-FAR-TT-20261101\patches\tests\t1\occupant_v2need.py')
try:
    c = make_consumer(Need('cap.attest', ABI_VERSION, ('identity',)), path)
    print(json.dumps({'ok': True, 'value': c.serves('identity')}))
except Exception as e:
    print(json.dumps({'ok': False, 'type': type(e).__name__, 'code': getattr(e, 'code', None), 'msg': str(e)[:160]}))
