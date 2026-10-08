"""`pipd` CLI - exactly the 13 commands of 總藍圖 §5.9.3 (exact-set, no 14th)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__, pipeline, profiles, registry, validate, workspace
from .errors import PipdError

COMMANDS = ("init", "intake", "profile", "compile-pi", "bind-pd", "compile-ecp",
            "compile-tqaep", "validate", "doctor", "project", "export", "diff", "repair")
FAILURE_CODES = {
    "init": "INIT_CONFLICT/PROFILE_STALE",
    "intake": "INTAKE_INVALID/AUTHORITY_UNKNOWN",
    "profile": "PROFILE_VETO/UNSUPPORTED_SURFACE",
    "compile-pi": "PI_SCHEMA/PI_SEMANTIC/TRACE_FAIL",
    "bind-pd": "REPO_CONTEXT_MISSING/STALE_PROVIDER",
    "compile-ecp": "ECP_PERMISSION/EFFECT_UNKNOWN",
    "compile-tqaep": "TQ_TRACE/TQ_ORACLE/TQ_SOD",
    "validate": "VALIDATION_FAIL",
    "doctor": "TOOL_DRIFT/HOST_UNSUPPORTED/COLLISION/RESIDUE/SEMVER",
    "project": "PROJECTION_LOSS/ADAPTER_FAIL",
    "export": "EXPORT_HASH/SECRET_SCAN",
    "diff": "DIFF_INCOMPATIBLE_SCHEMA",
    "repair": "REPAIR_SCOPE/DEPENDENCY/SELF_ACCEPT",
}


def _emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pipd", description=f"PIPD-LS-SP compiler CLI {__version__} (13 commands)")
    p.add_argument("--root", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    s = sub.add_parser("intake"); s.add_argument("--goal", required=True)
    s.add_argument("--source", action="append", default=[])
    s.add_argument("--constraint", action="append", default=[])
    s.add_argument("--non-goal", action="append", default=[])
    s = sub.add_parser("profile"); s.add_argument("--profile", default="LITE")
    s.add_argument("--axis", action="append", default=[])
    s = sub.add_parser("compile-pi"); s.add_argument("--intent", type=Path, required=True)
    s.add_argument("--profile", default="LITE")
    s = sub.add_parser("bind-pd"); s.add_argument("--pi", type=Path, required=True)
    s.add_argument("--repo-root", type=Path); s.add_argument("--head", default="")
    s = sub.add_parser("compile-ecp"); s.add_argument("--pd", type=Path, required=True)
    s.add_argument("--pi", type=Path, required=True)
    s = sub.add_parser("compile-tqaep"); s.add_argument("--pi", type=Path, required=True)
    s.add_argument("--ecp", type=Path, required=True)
    s.add_argument("--maker", default="HERMES-MAKER")
    s.add_argument("--checker", default="GLM-5.3-FLASH-AO-LANE")
    s.add_argument("--checker-receipt", dest="checker_receipt", default="")
    s = sub.add_parser("validate"); s.add_argument("--bundle", type=Path, required=True)
    sub.add_parser("doctor")
    s = sub.add_parser("project"); s.add_argument("--out", type=Path, default=None)
    s = sub.add_parser("export"); s.add_argument("--out", type=Path, default=None)
    s = sub.add_parser("diff"); s.add_argument("--a", type=Path, required=True)
    s.add_argument("--b", type=Path, required=True)
    s = sub.add_parser("repair"); s.add_argument("--subject", required=True)
    s.add_argument("--authorized-root", dest="authorized_root", default="")
    s.add_argument("--scope", action="append", default=[])
    s.add_argument("--maker", default="HERMES-MAKER")
    return p


def run(args: argparse.Namespace) -> dict:
    root: Path = args.root.resolve()
    cmd = args.command
    if cmd == "init":
        return workspace.init_workspace(root)
    if cmd == "intake":
        return pipeline.intake(args.goal, sources=args.source,
                               constraints=args.constraint, non_goals=args.non_goal)
    if cmd == "profile":
        return profiles.compute_profile(args.profile, axes=args.axis or ["intent"])
    if cmd == "compile-pi":
        card = json.loads(args.intent.read_text(encoding="utf-8"))
        return pipeline.compile_pi(card, args.profile)
    if cmd == "bind-pd":
        pi = json.loads(args.pi.read_text(encoding="utf-8"))
        ctx = None
        if args.repo_root:
            ctx = {"root": str(args.repo_root), "head": args.head,
                   "tracked_files": sum(1 for _ in args.repo_root.rglob("*") if _.is_file()),
                   "currentness": "FRESH", "writable_scope": "src/**"}
        return pipeline.bind_pd(pi, ctx)
    if cmd == "compile-ecp":
        return pipeline.compile_ecp(json.loads(args.pd.read_text(encoding="utf-8")),
                                    json.loads(args.pi.read_text(encoding="utf-8")))
    if cmd == "compile-tqaep":
        return pipeline.compile_tqaep(json.loads(args.pi.read_text(encoding="utf-8")),
                                      json.loads(args.ecp.read_text(encoding="utf-8")),
                                      maker=args.maker, checker=args.checker,
                                      checker_execution_receipt=args.checker_receipt)
    if cmd == "validate":
        bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
        return validate.validate_bundle(bundle, root / "schemas")
    if cmd == "doctor":
        return workspace.doctor(root)
    if cmd == "project":
        return workspace.project_surfaces(root, args.out or (root / "dist" / "web"))
    if cmd == "export":
        return workspace.export_manifest(root)
    if cmd == "diff":
        return workspace.semantic_diff(json.loads(args.a.read_text(encoding="utf-8")),
                                       json.loads(args.b.read_text(encoding="utf-8")))
    if cmd == "repair":
        return workspace.repair_candidate(args.subject, scope=args.scope, maker=args.maker,
                                          authorized_root=args.authorized_root or str(ROOT))
    raise AssertionError(cmd)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run(args)
    except PipdError as exc:
        _emit(exc.as_dict())
        return 2
    _emit(result)
    return 0 if result.get("verdict", "PASS") != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
