"""Capture the 1010x listeners robustly (bash + byte-safe decode) and patch the two round records."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

R = Path("C:/Projects/Agent_Workspace/HG-KSEOS/var/R5S-20261015-s4-preview4-verify-close")
p = subprocess.run(["C:/Program Files/Git/bin/bash.exe", "-c", "netstat -an"], capture_output=True)
net = p.stdout.decode("utf-8", errors="replace") + p.stderr.decode("utf-8", errors="replace")
listeners = sorted({m.group(1) for m in re.finditer(r"TCP\s+(\S+)\s+\S+\s+LISTENING", net) if m.group(1).endswith(("10100", "10101", "10102", "10103", "10105"))})
stamp = datetime.now(timezone.utc).isoformat()

fz = R / "00_freeze/R5S_FREEZE.json"
d = json.loads(fz.read_text(encoding="utf-8"))
d["lane_transport_after_remediation"] = {"listeners_1010x": listeners, "captured_utc": stamp}
fz.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")

lc = R / "01_lane/LANE_ROOT_CAUSE.json"
c = json.loads(lc.read_text(encoding="utf-8"))
c["verified_root_cause"]["ports_before_remediation"] = []
c["remediation_applied_this_session"]["ports_after"] = listeners
c["remediation_applied_this_session"]["ports_capture"] = {
    "command": "bash -c 'netstat -an' filtered for TCP ... LISTENING on 10100/10101/10102/10103/10105",
    "decoded": "utf-8 with errors=replace (the raw netstat output is not valid UTF-8 on this host, which is why a naive capture reads as empty)",
    "captured_utc": stamp,
}
lc.write_text(json.dumps(c, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"listeners": listeners}, indent=1))
