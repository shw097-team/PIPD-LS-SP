"""Extract the checker lane's JSON verdict from its persisted attempt stdout.

The dispatcher's timeout/error branches drop the child's stdout, so the verdict is located by GLOBBING the
attempt directories for any file carrying the run's nonce, and the LAST complete JSON object containing that
nonce wins (a lane may print partial JSON mid-turn). Writes raw/CHECKER_VERDICT_R5R3.json on success and
prints what it found; on failure it prints the reason and exits non-zero rather than inventing a verdict.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROUND = pathlib.Path("C:/Projects/Agent_Workspace/_handover/R5R3-20261016-preview4-closeout")
NONCE = "R5R3-VERIFY-20261016-b7c41e9d"


def objects_in(text: str) -> list[dict]:
    """Every top-level JSON object in `text`, by brace matching (JSON-escape aware enough for our lanes)."""
    found, depth, start, in_str, esc = [], 0, None, False, False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    found.append(json.loads(text[start:i + 1]))
                except Exception:  # noqa: BLE001
                    pass
                start = None
    return found


def main() -> int:
    roots = [ROUND / "raw" / "verify_ds_attempts2", ROUND / "raw" / "verify_ds_attempts", ROUND / "raw"]
    hits: list[tuple[pathlib.Path, dict]] = []
    for root in roots:
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.stat().st_size > 8_000_000:
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:  # noqa: BLE001
                continue
            if NONCE not in text:
                continue
            for obj in objects_in(text):
                if obj.get("nonce") == NONCE and "items" in obj:
                    hits.append((p, obj))
    if not hits:
        print("NO_VERDICT: no JSON object carrying the nonce was found in the attempt trees")
        return 2
    path, verdict = hits[-1]
    (ROUND / "raw" / "CHECKER_VERDICT_R5R3.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"source": str(path).replace("\\", "/"), "nonce": verdict.get("nonce"),
                      "items": {k: v.get("verdict") for k, v in (verdict.get("items") or {}).items()},
                      "weakest_claim": verdict.get("weakest_claim"),
                      "over_reach_found": verdict.get("over_reach_found")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
