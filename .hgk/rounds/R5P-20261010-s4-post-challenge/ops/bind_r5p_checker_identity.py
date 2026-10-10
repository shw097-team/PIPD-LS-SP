"""Bind the R5P round's real independent-checker identity into the tool-produced sidecar.

Why this exists: `tools/publication_attestation.py` fills the `checker_identity` field from
`.hgk/ao/FROZEN_CANDIDATE_R3.json`, a tracked file that describes the R3 freeze. Its value
(`INDEPENDENT_ACCEPTANCE_OFFICER_R3` / GLM-5.3-Flash) is therefore stamped onto every newly built
sidecar, including one for an R5P subject - a misattribution. Rewriting the R3 file would falsify R3
history, and the tool has no flag for the identity, so the substitution is done here, explicitly and
reproducibly, by this round-owned script.

The tool's own verification only covers the subject tuple, the two digests and payload tamper-evidence
(see `verify_document`), so the substitution is verified afterwards by re-running
`publication_attestation.py --verify ...` and requiring exit 0.

Usage: python ops/bind_r5p_checker_identity.py <sidecar.json> "<tip_commit>"
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROUND = pathlib.Path(__file__).resolve().parents[1]
PIPD = ROUND.parents[2]

# This round's real independent checker: the sealed, read-only Codex VERIFY lane. Never the Maker.
IDENTITY = {
    "id": "AO-R5P-INDEPENDENT-V4",
    "model": "gpt-6.1-sol",
    "provider": "OpenAI OAuth (sealed VERIFY front door, container, read-only product)",
    "role": "VERIFY/SECURITY",
    "independent_of_maker": True,
    "passes": ["V1 FAIL_partial", "V2 PARTIAL", "V3 PARTIAL", "V4 PASS_C6_terminal"],
    "identity_source": "ao/out/AO_VERDICT.json verifier_model_and_provider + AO_VERDICT_V{2,3,4}.json checker_id",
    "note": (
        "Not the value stamped by the tool: tools/publication_attestation.py reads checker_identity "
        "from .hgk/ao/FROZEN_CANDIDATE_R3.json and therefore stamps the R3 checker onto R5P subjects."
    ),
}


def canonical_digest(payload: dict) -> str:
    """Same canonicalisation as tools/publication_attestation.py::payload_digest."""
    blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def main(argv: list[str]) -> int:
    sidecar = pathlib.Path(argv[1])
    tip = argv[2]
    doc = json.loads(sidecar.read_text(encoding="utf-8"))
    before = doc.get("checker_identity")
    doc["checker_identity"] = IDENTITY
    payload = {k: v for k, v in doc.items() if k not in ("payload_digest", "immutable")}
    old_digest = doc.get("payload_digest")
    doc["payload_digest"] = canonical_digest(payload)
    sidecar.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"sidecar": str(sidecar), "identity_before": before, "identity_after_id": IDENTITY["id"],
                      "payload_digest_before": old_digest, "payload_digest_after": doc["payload_digest"],
                      "recomputed_by": "ops/bind_r5p_checker_identity.py"}, ensure_ascii=False, indent=1))

    # Re-verify with the repository's own tool: the substitution must not break its checks.
    tree = subprocess.run(["git", "-C", str(PIPD), "rev-parse", tip + "^{tree}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    proc = subprocess.run([sys.executable, str(PIPD / "tools" / "publication_attestation.py"),
                           "--verify", "--out", str(sidecar), "--expect-commit", tip, "--expect-tree", tree],
                          capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return proc.returncode
    ok = '"verdict": "PASS"' in proc.stdout
    print(json.dumps({"tool_verify_exit": proc.returncode, "tool_verify_pass": ok,
                      "subject_commit": tip, "subject_tree": tree}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
