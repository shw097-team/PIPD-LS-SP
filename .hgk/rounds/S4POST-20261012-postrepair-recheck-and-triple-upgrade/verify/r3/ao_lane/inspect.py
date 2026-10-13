import subprocess
import os
import json
import hashlib
import re
from pathlib import Path
ROOT = Path.cwd()
OUT = ROOT / '.ao-r3'
ROUND = '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade'
SUBJECT = '389d3973da73e5740f0b4d290bacb92d1e8982f8'
def git(*args):
    result = subprocess.run(['git', *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise RuntimeError(result.stderr.decode())
    return result.stdout
pack = json.loads((ROOT / ROUND / 'evidence/EVIDENCE_RETURN_PACK.json').read_text(encoding='utf-8'))
rows = []
for entry in pack['commands']:
    path = ROUND + '/' + entry['raw_log']
    blob = git('cat-file', '-p', SUBJECT + ':' + path)
    disk = (ROOT / path).read_bytes()
    rows.append({'path':path,'blob_bytes':len(blob),'disk_bytes':len(disk),'blob_sha256':hashlib.sha256(blob).hexdigest(),'disk_sha256':hashlib.sha256(disk).hexdigest(),'declared_blob':entry['log_sha256_committed_blob'],'declared_disk':entry['log_sha256_worktree_eol'],'same_bytes':blob == disk})
schema = (ROOT / 'packaging/public-plugin/vendor-plugin.schema.json').read_bytes()
schema_blob = git('cat-file','-p',SUBJECT + ':packaging/public-plugin/vendor-plugin.schema.json')
result = {'C8':rows,'C7':{'disk_bytes':len(schema),'disk_sha256':hashlib.sha256(schema).hexdigest(),'blob_bytes':len(schema_blob),'blob_sha256':hashlib.sha256(schema_blob).hexdigest()},'C10':{ref: [line for line in git('ls-tree','-r',ref).decode().splitlines() if line.startswith('160000 ')] for ref in ['HEAD','refs/remotes/origin/main']}}
for ref in ['52542c395a0f91dc2ba4bd6123acd4cdecd780dc','refs/remotes/origin/main']:
    paths = git('diff','--name-only',ref+'...'+SUBJECT).decode().splitlines()
    allowed = re.compile(r'^(packaging/public-plugin/|tools/freeze_public_plugin_source\.py$|tools/build_public_plugin\.py$|tools/build_web_fallback\.py$|tests/test_public_plugin_packaging\.py$|tests/test_web_fallback\.py$|docs/install/|docs/adr/|openspec/changes/s4post-triple-upgrade/|\.github/workflows/public-plugin-verify\.yml$|README\.md$|\.hgk/rounds/S4POST-20261012)')
    denied = re.compile(r'^(skills/|src/|schemas/|dist/)')
    result[ref] = {'changed_count':len(paths),'frozen_paths':[p for p in paths if denied.match(p)],'outside_allowlist':[p for p in paths if not denied.match(p) and not allowed.match(p)]}
tracked = git('ls-tree','-r','--name-only',SUBJECT).decode().splitlines()
hits = []
for path in tracked:
    if path.endswith(('.md','.json','.py','.tsv','.yml','.toml','.txt')):
        data = git('cat-file','-p',SUBJECT+':'+path)
        if b'com.ao3' in data:
            hits.append(path)
result['com.ao3_files'] = hits
(OUT / 'measurements.json').write_text(json.dumps(result, indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))

