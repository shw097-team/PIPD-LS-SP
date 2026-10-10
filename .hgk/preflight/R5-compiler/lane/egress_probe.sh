#!/usr/bin/env bash
set -uo pipefail
python3 - <<'PY'
import urllib.request, socket
def probe(url, t=6):
    try:
        with urllib.request.urlopen(url, timeout=t) as r:
            return f"HTTP{r.status}"
    except Exception as exc:
        return f"{type(exc).__name__}:{str(exc)[:60]}"
print("[egress] model_endpoint=" + probe("http://host.docker.internal:10100/v1/models"))
print("[egress] external_http=" + probe("http://example.com", 8))
try:
    socket.setdefaulttimeout(5); socket.getaddrinfo("example.com", 80); print("[egress] dns_external=RESOLVED")
except Exception as exc:
    print("[egress] dns_external=BLOCKED:" + type(exc).__name__)
PY
