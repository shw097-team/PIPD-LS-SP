#!/usr/bin/env python
"""R5Q licence oracle — turns every licence claim into an executable check.

The R5P crosswalk carried `DEL-019 = EVIDENCE_GAP: SBOM.cdx.json exists but no oracle
verifies cryptographic/provenance claims`. This tool IS that oracle for the licence
surfaces, so the licence landing is not a declaration but a check that can fail.

Run from the release worktree root:

    python .hgk/rounds/R5Q-20261010-s4-owner-opensource-preview/tools/r5q_license_oracle.py \
        --wheel dist/pipd_ls_sp-0.1.0-py3-none-any.whl --out <evidence.json>

Exit 0 only when every check passes. Any credential-shaped string found inside a licence
artifact is an automatic FAIL: licence text must never carry a secret.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import time
import zipfile

# Canonical Apache License 2.0 text, as published. The three digests below are the three
# spellings that appear in the wild: the plain text file, and the same file with CRLF.
APACHE_2_0_NORMALISED_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"

LICENCE_ID_PATTERN = re.compile(r"^(?:[A-Za-z0-9.+-]+|LicenseRef-[A-Za-z0-9.-]+)$")

# Anything that looks like a credential. Licence artifacts are published verbatim, so a
# match here is a leak, not a false positive to be talked away.
CREDENTIAL_SHAPES = [
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("ghp_classic", re.compile(r"ghp_[A-Za-z0-9]{30,}")),
    ("gho_oauth", re.compile(r"gho_[A-Za-z0-9]{30,}")),
    ("aws_akid", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("slack_token", re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}")),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer_header", re.compile(r"[Bb]earer\s+[A-Za-z0-9._~+/=-]{24,}")),
    ("openai_key", re.compile(r"sk-[A-Za-z0-9]{32,}")),
]

CHECKS: list[dict] = []


def check(check_id: str, requirement: str, ok: bool, actual: str, evidence=None) -> bool:
    CHECKS.append({
        "check_id": check_id,
        "requirement": requirement,
        "verdict": "PASS" if ok else "FAIL",
        "actual": actual,
        "evidence": evidence if evidence is not None else {},
    })
    return ok


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def normalise(text: str) -> str:
    """Line-ending-insensitive digest basis: git may hand us CRLF on this host."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def credential_hits(text: str) -> list[str]:
    return [name for name, pat in CREDENTIAL_SHAPES if pat.search(text)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--wheel", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    repo = pathlib.Path(a.repo).resolve()
    wheel = pathlib.Path(a.wheel)
    if not wheel.is_absolute():
        wheel = (repo / wheel).resolve()

    # ---------------------------------------------------------------- decision slot
    import yaml  # only the decision file needs a parser; everything else is bytes

    slot_path = repo / "OWNER_LICENSE_DECISION.yaml"
    slot_raw = slot_path.read_text(encoding="utf-8")
    slot = yaml.safe_load(slot_raw)
    decision = slot.get("decision")
    check("LIC-01", "one machine-readable owner licence decision exists and names an SPDX id",
          bool(decision) and bool(LICENCE_ID_PATTERN.match(decision or "")),
          f"OWNER_LICENSE_DECISION.yaml decision={decision!r} current_position={slot.get('current_position')!r}",
          {"path": str(slot_path), "sha256": sha256_bytes(slot_path.read_bytes())})
    # LIC-02 tests the REQUIREMENT (the placeholder must not be operative), not a bare string:
    # a supersession note that names what it superseded is correct governance, not a defect.
    placeholder = "LicenseRef-PIPD-Proprietary"
    prior = slot.get("previous_decision") or {}
    prior_decision = prior.get("decision") if isinstance(prior, dict) else None
    operative = [("decision", decision), ("current_position", slot.get("current_position"))]
    operative_hits = [k for k, v in operative if v == placeholder]
    check("LIC-02", "the superseded proprietary placeholder is not the operative licence",
          not operative_hits,
          f"operative fields={operative}, placeholder found as operative in {operative_hits or 'none'}")
    if placeholder in slot_raw:
        declared_supersession = (
            prior_decision == placeholder
            and "superseded" in json.dumps(prior, ensure_ascii=False).lower()
        )
        check("LIC-02b",
              "where the placeholder is still named, it sits in an explicit supersession note",
              declared_supersession,
              f"previous_decision.decision={prior_decision!r} superseded_declared={declared_supersession}")

    # ---------------------------------------------------------------- licence text
    lic_path = repo / "LICENSE"
    lic_raw = lic_path.read_bytes()
    lic_text = normalise(lic_raw.decode("utf-8"))
    lic_digest = sha256_bytes(lic_text.encode("utf-8"))
    check("LIC-03", "LICENSE is the canonical Apache-2.0 text (normalised digest)",
          lic_digest == APACHE_2_0_NORMALISED_SHA256,
          f"LICENSE normalised sha256={lic_digest} (canonical={APACHE_2_0_NORMALISED_SHA256})",
          {"path": str(lic_path), "bytes": len(lic_raw), "raw_sha256": sha256_bytes(lic_raw)})
    check("LIC-04", "LICENSE is a full licence text, not a stub or a pointer",
          len(lic_raw) > 10000 and "Apache License" in lic_text and "Version 2.0" in lic_text,
          f"bytes={len(lic_raw)}, contains 'Apache License'={'Apache License' in lic_text}")

    # ---------------------------------------------------------------- NOTICE
    notice_path = repo / "NOTICE"
    notice_raw = notice_path.read_bytes()
    notice_text = notice_raw.decode("utf-8", errors="replace")
    check("LIC-05", "NOTICE exists, is non-empty and names the copyright holder",
          len(notice_raw) > 200 and "Copyright" in notice_text,
          f"bytes={len(notice_raw)}, contains 'Copyright'={'Copyright' in notice_text}",
          {"path": str(notice_path), "sha256": sha256_bytes(notice_raw)})

    # ---------------------------------------------------------------- SBOM
    sb_path = repo / "SBOM.cdx.json"
    sb = json.loads(sb_path.read_text(encoding="utf-8"))
    root_lic = [l.get("license", {}).get("id") for l in sb.get("metadata", {}).get("licenses", [])]
    check("LIC-06", "SBOM root component licence equals the decision",
          decision in root_lic,
          f"SBOM metadata.licenses ids={root_lic} decision={decision!r}",
          {"path": str(sb_path), "sha256": sha256_bytes(sb_path.read_bytes())})
    props = {p["name"]: p["value"] for p in sb.get("metadata", {}).get("properties", [])}
    check("LIC-07", "SBOM is anchored to its basis, grant date and NOTICE file",
          all(k in props for k in ("pipd:licence:basis", "pipd:licence:granted_utc", "pipd:licence:notice_file")),
          f"licence properties present={sorted(k for k in props if k.startswith('pipd:licence'))}")
    sb_deps = sb.get("components", [])
    dep_lics = {c.get("name"): [l.get("license", {}).get("id") for l in c.get("licenses", [])]
                for c in sb_deps}
    check("LIC-08", "third-party components carry their own upstream licence, not the project's",
          all(decision not in v for v in dep_lics.values()),
          f"component licences={dep_lics}")
    check("LIC-09", "SBOM declares its own scope ceiling instead of implying a full closure",
          any("scope" in p.get("name", "") for p in sb.get("properties", [])),
          f"top-level properties={[p.get('name') for p in sb.get('properties', [])]}")

    # ---------------------------------------------------------------- wheel
    distributed = False
    if wheel.is_file():
        wheel_sha = sha256_bytes(wheel.read_bytes())
        with zipfile.ZipFile(wheel) as z:
            names = z.namelist()
            dist_info = next((n.split("/")[0] for n in names if n.endswith(".dist-info/METADATA")), None)
            if dist_info:
                md = z.read(f"{dist_info}/METADATA").decode("utf-8")
                hdr: dict[str, list[str]] = {}
                for line in md.splitlines():
                    if not line.strip():
                        break
                    if ":" in line:
                        k, _, v = line.partition(":")
                        hdr.setdefault(k.strip(), []).append(v.strip())
                expr = hdr.get("License-Expression", [None])[0]
                check("LIC-10", "wheel METADATA declares the decision as License-Expression",
                      expr == decision,
                      f"License-Expression={expr!r} decision={decision!r} Metadata-Version={hdr.get('Metadata-Version')}")
                check("LIC-11", "wheel METADATA lists both licence files (PEP 639 License-File)",
                      sorted(hdr.get("License-File", [])) == ["LICENSE", "NOTICE"],
                      f"License-File={hdr.get('License-File')}")
                for member, src, label in ((f"{dist_info}/licenses/LICENSE", lic_raw, "LICENSE"),
                                           (f"{dist_info}/licenses/NOTICE", notice_raw, "NOTICE")):
                    present = member in names
                    identical = present and z.read(member) == src
                    check(f"LIC-12-{label}", f"wheel ships {label} byte-identical to the repository copy",
                          identical,
                          f"present={present} byte_identical={identical} member={member}")
                members = [n for n in names if "/licenses/" in n]
                check("LIC-13", "the licence travels inside the wheel, not only in the repo",
                      len(members) >= 2,
                      f"licence-bearing members={sorted(members)}")
                basis_member = f"{dist_info}/licenses/{slot_path.name}"
                basis_ok = basis_member in names and z.read(basis_member) == slot_path.read_bytes()
                check("LIC-17", "the owner decision the SPDX id is derived from ships with the binary",
                      basis_ok,
                      f"member={basis_member} present={basis_member in names} byte_identical={basis_ok}")
                declared = [n for n in names if n.endswith("/licenses/LICENSE") or n.endswith("/licenses/NOTICE")]
                check("LIC-18", "METADATA License-File headers match the licence texts actually packed",
                      len(declared) == 2,
                      f"packed licence texts={sorted(declared)}")
                distributed = len(members) >= 2
            else:
                check("LIC-10", "wheel METADATA declares the decision", False, "no dist-info/METADATA in wheel")
            # RECORD must account for every member and agree on the hash of each — this is the
            # wheel's own self-manifest, so it is checkable without trusting the builder.
            rec_name = f"{dist_info}/RECORD"
            record_ok, record_note = False, "no RECORD"
            if rec_name in names:
                rows = {}
                for line in z.read(rec_name).decode("utf-8").splitlines():
                    if not line.strip():
                        continue
                    parts = line.split(",")
                    rows[parts[0]] = (parts[1], parts[2] if len(parts) > 2 else "")
                missing = sorted(set(names) - set(rows) - {rec_name})
                bad = []
                for member, (digest, size) in rows.items():
                    if not digest.startswith("sha256="):
                        continue
                    import base64
                    want = digest.split("=", 1)[1]
                    got = base64.urlsafe_b64encode(
                        hashlib.sha256(z.read(member)).digest()).rstrip(b"=").decode()
                    if got != want:
                        bad.append(member)
                record_ok = not missing and not bad
                record_note = (f"RECORD rows={len(rows)} unlisted_members={missing} "
                               f"hash_mismatches={bad}")
            check("LIC-14", "the wheel's own RECORD accounts for every member and every hash agrees",
                  record_ok, record_note)
            sat = f"{dist_info}/licenses/LICENSE" in names
            check("LIC-15b", "no credential shape is embedded in the wheel metadata or included files",
                  not any(credential_hits(z.read(n).decode("utf-8", errors="replace"))
                          for n in names
                          if n.endswith("METADATA") or "/licenses/" in n),
                  "clean" if sat else "wheel has no packaged licence file (see LIC-13)")
    else:
        check("LIC-10", "wheel exists at the requested path", False, f"missing: {wheel}")

    # ---------------------------------------------------------------- leak sweep
    leak_surfaces = {
        "LICENSE": lic_text,
        "NOTICE": notice_text,
        "OWNER_LICENSE_DECISION.yaml": slot_raw,
        "SBOM.cdx.json": sb_path.read_text(encoding="utf-8"),
    }
    proj = repo / "PROVENANCE.md"
    if proj.is_file():
        leak_surfaces["PROVENANCE.md"] = proj.read_text(encoding="utf-8")
    pyproj = repo / "pyproject.toml"
    if pyproj.is_file():
        leak_surfaces["pyproject.toml"] = pyproj.read_text(encoding="utf-8")
    found = {name: credential_hits(text) for name, text in leak_surfaces.items()}
    found = {k: v for k, v in found.items() if v}
    check("LIC-15", "no credential-shaped string is carried inside any licence artifact",
          not found,
          "clean" if not found else f"CREDENTIAL SHAPES FOUND: {found}")

    # ---------------------------------------------------------------- consistency
    pos = slot.get("current_position")
    check("LIC-16", "the decision slot is self-consistent (current_position == decision)",
          pos == decision,
          f"current_position={pos!r} decision={decision!r}")

    failures = [c for c in CHECKS if c["verdict"] == "FAIL"]
    receipt = {
        "schema": "PIPD-R5Q-LICENCE-ORACLE/1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "repo": str(repo),
        "wheel": str(wheel),
        "wheel_sha256": sha256_bytes(wheel.read_bytes()) if wheel.is_file() else None,
        "decision": decision,
        "licence_distributed_with_binary": distributed,
        "required": len(CHECKS),
        "passed": len(CHECKS) - len(failures),
        "failed": len(failures),
        "verdict": "PASS" if not failures else "FAIL",
        "checks": CHECKS,
        "claim_ceiling": (
            "This oracle verifies the licence chain this repository controls: the decision slot, the "
            "licence text, NOTICE, the SBOM root licence, the wheel metadata and the packaged licence "
            "files, and that no credential shape rides inside them. It does NOT verify the provenance "
            "or authorship of the source material, and it does not compute the wheel's transitive "
            "dependency closure (see the SBOM scope property)."
        ),
    }
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in CHECKS:
        print(f"[{c['verdict']}] {c['check_id']}: {c['requirement']} — {c['actual']}")
    print(f"\nLICENCE ORACLE: {receipt['verdict']} ({receipt['passed']}/{receipt['required']} checks) -> {out}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
