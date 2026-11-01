#!/usr/bin/env python3
"""work_queue -- the delivery's WPs as control-plane rows, so "what is next" is computed, not remembered.

Why this exists: the remaining work for this round kept living in a session's context. Two turns ago that
produced a WP ordering that contradicted the delivery's own DAG (10 → 11 → 12 → 13 → 17 → 20 where the
dependencies require 17 → 20 → 11 → 13 → 10 → 12). A queue in `hg-kseos.db` cannot be lost to a compaction.

Rows are seeded from the delivery's `DAG dependency` lines, not from prose written by hand, and refreshed with
the verdict actually present in `acceptances`.

Usage:
  work_queue.py init      [--delivery PATH]        seed/refresh rows from the delivery
  work_queue.py show                               every row, in DAG order, with what blocks it
  work_queue.py next      [--json]                 the one WP that may run now, and its phase
Exit 0 always for show/next (an empty queue is a result, not an error); init exits 2 if the delivery is unreadable.
"""

from __future__ import annotations


try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass


import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db")


def _delivery() -> Path:
    """Resolve the DAG inside the delivered package, by measurement rather than by a remembered path.

    Measured defect: this constant named the `SBL_PIPD/` segment, which does not exist; the package lives under
    `FHS/`. `work_queue.py init` therefore could not read the DAG at all, and the failure looked like a missing
    file rather than a stale path. Candidates are tried in order and the miss is named, not guessed.
    """
    base = Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric")
    tail = Path("FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1"
                "/01_FHS-MSC_PIPD-LS-PKG_BODY/11_WORKPACKAGES_AND_DAG.md")
    for head in ("FHS", "SBL_PIPD"):
        cand = base / head / tail
        if cand.is_file():
            return cand
    raise SystemExit(f"DELIVERY_NOT_FOUND: tried FHS/ and SBL_PIPD/ under {base}")


DELIVERY = _delivery()

SCHEMA = """
CREATE TABLE IF NOT EXISTS work_queue (
    wp_id       TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    depends_on  TEXT NOT NULL DEFAULT '',   -- comma separated WP-FHS-nn
    effect_class TEXT NOT NULL DEFAULT '',
    state       TEXT NOT NULL DEFAULT 'PENDING',
    evidence_ref TEXT,
    updated_at  TEXT NOT NULL
)
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.execute(SCHEMA)
    return con


def parse_delivery(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[dict] = []
    for block in re.split(r"###\s+", text)[1:]:
        m = re.match(r"WP-FHS-(\d\d)｜(.+)", block)
        if not m:
            continue
        wp = f"WP-FHS-{m.group(1)}"
        dep = re.search(r"\*\*DAG dependency\*\*：(.+?)\n", block)
        eff = re.search(r"\*\*EffectClass / Admission\*\*：(.+?)\n", block)
        deps = re.findall(r"WP-FHS-\d\d", dep.group(1)) if dep else []
        rows.append({"wp_id": wp, "title": m.group(2).strip(), "depends_on": ",".join(deps),
                     "effect_class": (eff.group(1).split("`")[1] if eff and "`" in eff.group(1) else "")})
    return rows


def verdicts(con: sqlite3.Connection) -> dict[str, str]:
    """A WP is PASS only if some acceptance row for it says PASS (a -V2 upgrade counts; history stays)."""
    out: dict[str, str] = {}
    try:
        rows = con.execute(
            "SELECT acceptance_id, verdict FROM acceptances WHERE acceptance_id LIKE 'ACC-WP-FHS-%'"
        ).fetchall()
    except sqlite3.OperationalError:
        return out
    for aid, verd in rows:
        wp = "WP-FHS-" + aid.replace("ACC-WP-FHS-", "").split("-")[0]
        if out.get(wp) != "PASS":
            out[wp] = verd
    return out


def refresh(con: sqlite3.Connection) -> None:
    v = verdicts(con)
    for wp, state in v.items():
        con.execute("UPDATE work_queue SET state=?, updated_at=? WHERE wp_id=?", (state, now(), wp))
    con.commit()


def cmd_init(args) -> int:
    path = Path(args.delivery)
    if not path.is_file():
        print(json.dumps({"error": "DELIVERY_UNREADABLE", "path": str(path)}))
        return 2
    rows = parse_delivery(path)
    if not rows:
        print(json.dumps({"error": "NO_WORK_PACKAGES_PARSED", "path": str(path)}))
        return 2
    con = connect()
    for r in rows:
        con.execute(
            "INSERT INTO work_queue (wp_id,title,depends_on,effect_class,state,updated_at) "
            "VALUES (?,?,?,?,'PENDING',?) ON CONFLICT(wp_id) DO UPDATE SET "
            "title=excluded.title, depends_on=excluded.depends_on, effect_class=excluded.effect_class",
            (r["wp_id"], r["title"], r["depends_on"], r["effect_class"], now()),
        )
    con.commit()
    refresh(con)
    n = con.execute("SELECT COUNT(*) FROM work_queue").fetchone()[0]
    print(json.dumps({"seeded": n, "delivery": str(path), "classes": sorted({r["effect_class"] for r in rows})}))
    return 0


def load(con: sqlite3.Connection) -> list[dict]:
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(
        "SELECT wp_id,title,depends_on,effect_class,state,evidence_ref FROM work_queue ORDER BY wp_id")]


def blockers(row: dict, by_id: dict[str, dict]) -> list[str]:
    if not row["depends_on"]:
        return []
    return [d for d in row["depends_on"].split(",") if d and by_id.get(d, {}).get("state") != "PASS"]


def phase(wp: str) -> str:
    """What has to happen next for this WP. Briefs live in a fixed queue directory so the driver is stateless."""
    q = Path(r"C:/wg/queue") / wp
    brief = q / "brief.md"
    # The officer writes its verdict wherever its brief tells it to -- measured 2026-10-30: the WP-FHS-11 officer
    # wrote `officer/verdict.json`, the driver looked only at the queue root, so the phase never advanced and the
    # unit was re-dispatched on every tick. Search the tree, do not assume the path.
    verdict = next(iter(q.rglob("verdict.json")), None)
    if not brief.is_file():
        return "NO_BRIEF"
    if verdict is None:
        return "BRIEF_READY"
    return "AWAITING_RECORD"


def cmd_settle(args) -> int:
    """Record what a phase actually produced, so the loop stops re-running a unit that FAILED.

    Without this the driver had no way to move past a FAIL: the officer failed WP-FHS-11 with
    HOST_SP_MATRIX_INCOMPLETE, the queue kept it in FAIL, `next` kept returning it, and every tick would have
    dispatched it again -- the repeat-block the owner asked me to watch for, built into my own loop.
    A settled FAIL stays visible as NEEDS_RULING; it is not a PASS and it is not silently dropped.
    """
    con = connect()
    cur = con.execute("SELECT state, evidence_ref FROM work_queue WHERE wp_id=?", (args.wp,))
    row = cur.fetchone()
    if row is None:
        print(json.dumps({"error": "UNKNOWN_WP", "wp": args.wp}))
        return 2
    prior_state, prior_evidence = row
    # A3: a second settle of an already-terminal item is a duplicate claim, not a correction.
    if prior_state == "PASS":
        print(json.dumps({"error": "ERR_ALREADY_SETTLED", "wp": args.wp, "state": prior_state,
                          "detail": "terminal PASS may not be overwritten; use unsettle with a named reason"}))
        return 7
    if prior_evidence and getattr(args, "evidence", None) == prior_evidence:
        print(json.dumps({"error": "ERR_DUPLICATE_CLAIM", "wp": args.wp, "evidence": prior_evidence}))
        return 7
    if getattr(args, "verdict", None) in ("PASS", "BLOCKED") and not (getattr(args, "evidence", "") or "").strip():
        print(json.dumps({"error": "ERR_EVIDENCE_REQUIRED", "wp": args.wp, "verdict": args.verdict,
                          "detail": "PASS/BLOCKED must name the artefact that proves it"}))
        return 8
    con.execute("UPDATE work_queue SET state=?, evidence_ref=?, updated_at=? WHERE wp_id=?",
                (args.verdict, args.evidence, now(), args.wp))
    con.commit()
    print(json.dumps({"settled": args.wp, "state": args.verdict, "evidence": args.evidence}, ensure_ascii=False))
    return 0


def cmd_unsettle(args) -> int:
    """Clear a settled FAIL so the same unit can be judged again -- only with a reason that names what changed.

    A settled FAIL exists so the loop cannot retry blindly. When the cause has actually been removed (a real grant
    instead of a seam, a built mechanism instead of a missing one), the record must carry that reason, or this is the
    repeat-block pattern wearing a different hat.
    """
    con = connect()
    row = con.execute("SELECT state FROM work_queue WHERE wp_id=?", (args.wp,)).fetchone()
    if row is None:
        print(json.dumps({"unsettled": None, "detail": "UNKNOWN_WP"}, ensure_ascii=False))
        return 2
    con.execute("UPDATE work_queue SET state='NOT_RUN', evidence_ref=?, updated_at=? WHERE wp_id=?",
                (f"OWNER-RULING:{args.reason}", now(), args.wp))
    con.commit()
    print(json.dumps({"unsettled": args.wp, "was": row[0], "now": "NOT_RUN", "reason": args.reason},
                     ensure_ascii=False))
    return 0


def cmd_render(args) -> int:
    """Render the projections from the authority.

    Measured defect (R-7): four scoreboards disagreed because three of them were hand-maintained. A projection
    that is edited by hand is a second authority; this command makes the projections derived, so a divergence
    can only come from a stale render and never from an opinion.

    STATUS.json is deliberately NOT rendered here: it is a liveness document (running pids, in-flight nonces),
    not a scoreboard. Rendering it from the queue would erase the only record of what is actually running.
    """
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute("SELECT wp_id, state, effect_class FROM work_queue ORDER BY wp_id").fetchall()
    finally:
        con.close()
    tally = {"total": len(rows)}
    for _wp, state, _ec in rows:
        tally[state] = tally.get(state, 0) + 1
    base = Path(args.queue)
    base.mkdir(parents=True, exist_ok=True)

    todo = ["# Todo (derived from the control plane, not from a session)", ""]
    for wp, state, effect in rows:
        mark = "x" if state == "PASS" else " "
        todo.append(f"- [{mark}] {wp} {state}")
    (base / "TODO.md").write_text("\n".join(todo) + "\n", encoding="utf-8", newline="")

    snap = (f"total={tally['total']} pass={tally.get('PASS', 0)} fail={tally.get('FAIL', 0)} "
            f"pending={tally.get('NOT_RUN', 0)}")
    goal_path = base / "GOAL.json"
    goal = {}
    if goal_path.is_file():
        try:
            goal = json.loads(goal_path.read_text(encoding="utf-8"))
        except ValueError:
            goal = {}
    goal["queue_snapshot"] = snap
    if isinstance(goal.get("counts"), dict):
        goal["counts"].update({"total": tally["total"], "pass": tally.get("PASS", 0),
                               "fail": tally.get("FAIL", 0), "pending": tally.get("NOT_RUN", 0)})
    goal["projection_reconciled_at"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    goal["projection_reconciled_by"] = "work_queue.py render (authority = work_queue)"
    goal_path.write_text(json.dumps(goal, ensure_ascii=False, indent=1), encoding="utf-8", newline="")

    print(json.dumps({"ok": True, "rendered": [str(base / "TODO.md"), str(goal_path)],
                      "snapshot": snap, "tally": tally}, ensure_ascii=False))
    return 0


def cmd_show(_args) -> int:
    con = connect()
    refresh(con)
    rows = load(con)
    by_id = {r["wp_id"]: r for r in rows}
    for r in rows:
        b = blockers(r, by_id)
        print(f"{r['wp_id']}  {r['state']:<7} {r['effect_class']:<8} "
              f"{'blocked by ' + ','.join(b) if b else 'ready'}")
    print(f"\ntotal={len(rows)} pass={sum(1 for r in rows if r['state']=='PASS')} "
          f"fail={sum(1 for r in rows if r['state']=='FAIL')} "
          f"pending={sum(1 for r in rows if r['state']=='PENDING')}")
    return 0


def cmd_next(args) -> int:
    con = connect()
    refresh(con)
    rows = load(con)
    by_id = {r["wp_id"]: r for r in rows}
    settled_fail = [r["wp_id"] for r in rows if r["state"] in ("FAIL", "BLOCKED") and r.get("evidence_ref")]
    for r in rows:  # DAG order = id order minus already-done
        if getattr(args, "wp", None) and r["wp_id"] != args.wp:
            continue
        if r["state"] == "PASS":
            continue
        if r["state"] in ("FAIL", "BLOCKED") and r.get("evidence_ref"):
            continue   # settled: retrying it without a ruling is the repeat-block pattern
        b = blockers(r, by_id)
        if b:
            continue
        print(json.dumps({"wp": r["wp_id"], "title": r["title"], "effect_class": r["effect_class"],
                          "settled_failures": settled_fail,
                          "phase": phase(r["wp_id"]),
                          "queue_dir": str(Path(r"C:/wg/queue") / r["wp_id"]),
                          "remaining_fail": [x["wp_id"] for x in rows if x["state"] == "FAIL"]},
                         ensure_ascii=False))
        return 0
    print(json.dumps({"wp": None, "verdict": "QUEUE_DRAINED",
                      "remaining_fail": [x["wp_id"] for x in rows if x["state"] == "FAIL"]}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("--delivery", default=str(DELIVERY)); p.set_defaults(fn=cmd_init)
    s = sub.add_parser("settle"); s.add_argument("--wp", required=True); s.add_argument("--verdict", required=True)
    s.add_argument("--evidence", default=None); s.set_defaults(fn=cmd_settle)
    u = sub.add_parser("unsettle"); u.add_argument("--wp", required=True)
    u.add_argument("--reason", required=True); u.set_defaults(fn=cmd_unsettle)
    r = sub.add_parser("render"); r.add_argument("--queue", default=r"C:/wg/queue"); r.set_defaults(fn=cmd_render)
    sub.add_parser("show").set_defaults(fn=cmd_show)
    pn = sub.add_parser("next"); pn.add_argument("--wp", default=None); pn.set_defaults(fn=cmd_next)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
