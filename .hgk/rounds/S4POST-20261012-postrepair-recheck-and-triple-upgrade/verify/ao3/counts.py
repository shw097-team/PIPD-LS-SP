from pathlib import Path
import json, re, subprocess, sys
SUBJECT = Path.cwd()
OUT = SUBJECT/'.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade/verify/ao3'
CANDIDATE = Path((OUT/'snapshot-path.txt').read_text())
command = [sys.executable,'-c','import unittest,json; loader=unittest.TestLoader(); suite=loader.discover("tests",top_level_dir="."); module=loader.loadTestsFromName("tests.test_publication_projection"); print(json.dumps({"discovered_test_cases":suite.countTestCases(),"publication_module_cases":module.countTestCases(),"load_errors":loader.errors},indent=2))']
result = subprocess.run(command,cwd=CANDIDATE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(OUT/'discovery-denominator.txt').write_bytes(f'COMMAND: {subprocess.list2cmdline(command)}\nCWD: {CANDIDATE}\nEXIT_CODE: {result.returncode}\nRAW OUTPUT:\n'.encode()+result.stdout)
print(result.stdout.decode())
counts = {}
for name in ['focused','full','wheel-system-python','doctor-system-python']:
    text = (OUT/(name+'.txt')).read_text()
    counts[name] = {'success_lines':len(re.findall(r'(?:\.\.\. )?ok$',text,re.M)),'individual_skips':len(re.findall(r'^(?:test_.*\.\.\. )?skipped .*$',text,re.M)),'module_skips':len(re.findall(r'^setUpModule.*skipped',text,re.M)),'summary':[line for line in text.splitlines() if line.startswith(('Ran ','OK'))]}
(OUT/'test-counts.json').write_text(json.dumps(counts,indent=2))
print(json.dumps(counts,indent=2))
