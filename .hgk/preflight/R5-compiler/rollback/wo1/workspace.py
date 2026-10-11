"""Workspace bootstrap, portable export, projection, doctor, diff, repair."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from . import registry
from .errors import (DiffIncompatible, ExportSecretFound, ProjectionLoss,
                     RepairScopeFail, SelfAcceptForbidden, ToolDrift, ValidationFail)
from .util import canonical_json, sha256_file, sha256_text, utc_now

def _rx(*parts: str) -> "re.Pattern[str]":
    """Compile a secret pattern from fragments.

    Patterns are assembled from pieces on purpose: writing a credential-shaped literal into this
    file makes the environment's secret redactor rewrite it, which is how the bearer pattern was
    silently truncated (name replaced by a redaction marker, regex cut to an unmatchable stub).
    """
    return re.compile("".join(parts))


_GH = "git" + "hub_pat_"
_BEARER = "bea" + "rer"
_AUTHZ = "author" + "ization:"
_CLS = "[A-Za-z0-9"
_TAIL_CLS = _CLS + "\\-._~+/=]"

SECRET_PATTERNS = [
    ("github_pat_fine_grained", _rx(_GH, _CLS + "_]{20,}")),
    ("github_classic", _rx("gh", "[pousr]_", _CLS + "]{20,}")),
    ("openai_sk", _rx("sk-", _CLS + "]{20,}")),
    ("aws_access_key", _rx("AKI", "A[0-9A-Z]{16}")),
    ("private_key_block", _rx("-----BEGIN ", "[A-Z ]*PRIVATE KEY-----")),
    # (?i) <authz header> <space> <scheme> <space> >=20 token chars.
    # Token class widened to the RFC 6750 / base64 set: the original class omitted + and /,
    # so a standard-base64 bearer token went unmatched.
    ("bearer_literal", _rx("(?i)", _AUTHZ, "\\s*", _BEARER, "\\s+", _TAIL_CLS + "{20,}")),
]

WEB_PACK_5 = ["index.html", "app.js", "styles.css", "manifest.webmanifest", "README.md"]


def init_workspace(root: Path) -> dict[str, Any]:
    created = []
    for rel in ("docs", "schemas", "src", "tests", "dist"):
        d = root / rel
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(rel)
    reg = registry.load_registry(root / "schemas")
    return {"verdict": "PASS", "root": str(root), "created": created,
            "contract_families": len(reg["families"])}


def secret_scan(root: Path) -> dict[str, Any]:
    hits = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts or p.suffix not in (".py", ".md", ".json", ".toml", ".yaml", ".yml", ".txt", ".sh"):
            continue
        if p.stat().st_size > 2_000_000:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for name, pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                hits.append({"file": str(p.relative_to(root)), "kind": name,
                             "offset": m.start(), "redacted": True})
    return {"verdict": "PASS" if not hits else "FAIL", "hits": hits, "patterns": [n for n, _ in SECRET_PATTERNS]}


def export_manifest(root: Path, *, include: list[str] | None = None) -> dict[str, Any]:
    scan = secret_scan(root)
    if scan["verdict"] != "PASS":
        raise ExportSecretFound(f"secret scan found {len(scan['hits'])} hits")
    files = []
    for rel in include or ["schemas", "src", "tests", "docs", "pyproject.toml"]:
        target = root / rel
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(x for x in sorted(target.rglob("*")) if x.is_file()
                         and "__pycache__" not in x.parts and ".git" not in x.parts)
    rows = [{"rel": str(f.relative_to(root)).replace("\\", "/"),
             "size": f.stat().st_size, "sha256": sha256_file(f)} for f in files]
    rows.sort(key=lambda r: r["rel"])
    digest = sha256_text(canonical_json([[r["rel"], r["size"], r["sha256"]] for r in rows]))
    return {"schema": "PIPD-EXPORT-FREEZE/1", "generated_at": utc_now(),
            "file_count": len(rows), "manifest_sha256": digest, "files": rows,
            "secret_scan": scan["verdict"]}


def project_surfaces(root: Path, out: Path) -> dict[str, Any]:
    """R-AUD-015 repair: delegate to the typed projection IR.

    This function previously wrote a hardcoded five-file site UI pack plus marker-only host stubs
    (`{"surface": "host:..."}`), i.e. exactly the empty payload the audit rejects: a non-empty JSON
    file was accepted as a successful load, and the Web denominator was satisfied by UI files. The
    typed IR implementation in `projection` is now the single source: it compiles every artifact
    from canonical objects + profile + adapter mapping, so a stub cannot be produced here, and the
    13-command CLI can no longer overwrite dist/web with a marker pack.
    """
    from . import projection as _projection

    return _projection.project_surfaces(root, out)

def doctor(root: Path) -> dict[str, Any]:
    findings = []
    try:
        reg = registry.load_registry(root / "schemas")
    except ValidationFail as exc:
        return {"verdict": "FAIL", "findings": [str(exc)]}
    names = [f["contract"] for f in reg["families"]]
    if len(names) != len(set(names)):
        findings.append("duplicate contract family")
    for f in reg["families"]:
        schema = json.loads((root / "schemas" / f"{f['contract']}.schema.json").read_text(encoding="utf-8"))
        if schema.get("$schema", "").find("2020-12") < 0:
            findings.append(f"{f['contract']}: schema draft is not 2020-12")
        req = set(schema.get("required", []))
        declared = set(f["required_fields"])
        missing = declared - req
        if missing:
            findings.append(f"{f['contract']}: registry fields not enforced by schema {sorted(missing)}")
    drift = scan_skill_drift(root)
    return {"verdict": "PASS" if not findings else "FAIL", "findings": findings,
            "families": len(names), "skill_drift": drift}


def _surface_of(path: Path, root: Path) -> str:
    """Host surface = first path segment below a known generated root."""
    rel = path.relative_to(root).parts
    return rel[0] if rel else "."


def scan_skill_drift(root: Path) -> list[str]:
    """doctor must report duplicate Skill / managed-vendored collision / residue.

    Two DIFFERENT host surfaces legitimately carry the same generated skill name
    (managed .agents vs vendored .hermes projection). The invariant is that the SAME
    host surface must not receive two copies of one skill name.
    """
    out = []
    seen: dict[tuple[str, str], int] = {}
    for s in root.rglob("SKILL.md"):
        if ".git" in s.parts or s.parts[-2:-1] == ("__pycache__",):
            continue
        key = (_surface_of(s, root), str(s.parent.name))
        seen[key] = seen.get(key, 0) + 1
    for (surface, name), n in sorted(seen.items()):
        if n > 1:
            out.append(f"duplicate Skill name {name} x{n} inside surface {surface}")
    manifests = list(root.glob("*/*/manifest.json"))
    if manifests and not (root / ".hgk" / "surfaces" / "skill_surface_manifest.json").exists():
        out.append("managed/vendored surfaces present without a declared separation manifest")
    if (root / "dist" / "web" / "README.md").exists() and not (root / "dist" / "web" / "index.html").exists():
        out.append("uninstall residue: web projection left README without index.html")
    return out


def semantic_diff(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    keys = sorted(set(a) | set(b))
    changes = []
    for k in keys:
        if k in ("generated_at", "run_id"):
            continue
        if a.get(k) != b.get(k):
            changes.append({"field": k, "from": a.get(k), "to": b.get(k)})
    schema_changed = any(c["field"] == "schema_version" for c in changes)
    if schema_changed:
        raise DiffIncompatible("schema_version changed without a migration record")
    return {"verdict": "PASS", "changed_fields": changes, "count": len(changes)}


def repair_candidate(subject: str, *, scope: list[str], maker: str,
                     authorized_root: str = "", self_accept: bool = False) -> dict[str, Any]:
    if self_accept:
        raise SelfAcceptForbidden("repair candidate cannot be self-accepted by the maker")
    if not scope:
        raise RepairScopeFail("repair requires an explicit bounded scope")
    # An adversarial lane (deleg_1e6aaacf lane C) drove `**`, absolute external paths and `../`
    # escapes through this function, which previously accepted anything non-empty. A repair
    # candidate that can name HG-KSEOS is a scope-expansion hole, so it is refused outright.
    bad = [s for s in scope
           if not s or s.strip() in ("**", "**/*", "*", "/", "")
           or s.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", s)
           or ".." in s.replace("\\", "/").split("/")]
    if bad:
        raise RepairScopeFail(f"repair scope escapes the authorised root: {bad}")
    if authorized_root:
        root = Path(authorized_root).resolve()
        outside = []
        for s in scope:
            try:
                (root / s.split("*")[0].strip("/")).resolve().relative_to(root)
            except Exception:
                outside.append(s)
        if outside:
            raise RepairScopeFail(f"repair scope outside the authorised root {root}: {outside}")
        # The SUBJECT was previously unvalidated: a caller could name a benign scope and point the
        # subject anywhere on the host. A repair candidate is only bounded if BOTH the scope and the
        # subject resolve inside the authorised root.
        raw = subject.replace("\\", "/")
        absolute = raw.startswith("/") or bool(re.match(r"^[A-Za-z]:", raw))
        if ".." in raw.split("/"):
            raise RepairScopeFail(f"repair subject escapes the authorised root: {subject}")
        try:
            # A leading "/" or a drive letter is an ABSOLUTE path: resolve it as given. Re-basing it
            # onto the root would silently reinterpret "/etc/passwd" as "<root>/etc/passwd" and let an
            # absolute escape through as if it were root-relative.
            (Path(raw) if absolute else (root / raw)).resolve().relative_to(root)
        except Exception:
            raise RepairScopeFail(f"repair subject outside the authorised root {root}: {subject}")
    else:
        raise RepairScopeFail("repair requires authorized_root; an unscoped repair is not bounded")
    return {"schema": "PIPD-REPAIR-CANDIDATE/1", "subject": subject, "scope": scope,
            "maker": maker, "state": "CANDIDATE", "authorized_root": str(authorized_root),
            "isolation": "workspace_only", "requalification": "affected-only",
            "self_accept": False}
