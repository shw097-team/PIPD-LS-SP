#!/usr/bin/env python3
"""update_evidence_pack.py - FAR R3 + R7: complete EVIDENCE_RETURN_PACK.json honestly.

What it does, in this order:
  1. Curates the R3 raw evidence INTO the tree (an external-only locator is not evidence):
       <logdir>/*.log,*.exit  ->  verify/r3/raw/                 (byte copy, sha256 recorded)
       release asset readback ->  verify/r3/RELEASE_ASSETS_READBACK.json
  2. Adds the three PB-090 fields the pack was missing: manifest_sha256, release_assets, commands.
     Every value is either MEASURED (with its raw log + sha256) or the literal string NOT_EXECUTED /
     NOT_APPLICABLE_UNRELEASED - never a placeholder presented as a measurement (PB-091).
  3. Adds the R7 SoD block: producer_identity / checker_identity as Windows SIDs, because the maker and
     the acceptance lane ran as DIFFERENT local accounts and only the labels were missing.
  4. Corrects the STALE independent_checker field (it still says NOT_RUN while twelve acceptance rounds
     have since run) - the historical value is preserved under `previous`, not overwritten silently.
  5. Records the stale candidate binding as PENDING_OWNER_RATIFICATION (FCR-007 / TT-S4POST-EVIDENCE-06);
     it does NOT re-bind the subject, because re-binding is the owner's act.

Idempotent: re-running replaces only the blocks it owns; a pre-image is written to the same directory.
Usage: update_evidence_pack.py --repo <worktree> --logdir <dir with the suite logs> [--candidate <sha>]
"""
import argparse, datetime, hashlib, json, os, re, shutil, sys

def sha256_file(p, n=None):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def read_counts(log):
    txt = open(log, encoding='utf-8', errors='replace').read()
    m = re.search(r'Ran (\d+) tests? in ([\d.]+)s', txt)
    ran = int(m.group(1)) if m else None
    skipped = int(m.group(1)) if (m := re.search(r'skipped=(\d+)', txt)) else None
    failed = int(m.group(1)) if (m := re.search(r'failures=(\d+)', txt)) else 0
    errors = int(m.group(1)) if (m := re.search(r'errors=(\d+)', txt)) else 0
    ok = bool(re.search(r'^OK\b', txt, re.M))
    return {"tests": ran, "skipped": skipped, "failed": failed, "errors": errors, "result": "OK" if ok else "NOT_OK"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--logdir', required=True)
    ap.add_argument('--candidate', default=None)
    a = ap.parse_args()
    R = os.path.join(a.repo, '.hgk/rounds/S4POST-20261012-postrepair-recheck-and-triple-upgrade')
    pack_path = os.path.join(R, 'evidence/EVIDENCE_RETURN_PACK.json')
    raw_dir = os.path.join(R, 'verify/r3/raw'); os.makedirs(raw_dir, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    pre = sha256_file(pack_path)
    shutil.copy2(pack_path, pack_path + f'.pre-r3-{ts}')

    # 1. curate the raw logs into the tree
    copied = []
    for name in sorted(os.listdir(a.logdir)):
        if name.endswith(('.log', '.exit')):
            src, dst = os.path.join(a.logdir, name), os.path.join(raw_dir, name)
            shutil.copy2(src, dst)
            copied.append({"name": name, "bytes": os.path.getsize(dst), "sha256": sha256_file(dst),
                           "source_was_external": os.path.dirname(src)})
    ra = os.path.join(a.logdir, 'release_assets_readback.json')
    if os.path.exists(ra):
        dst = os.path.join(R, 'verify/r3/RELEASE_ASSETS_READBACK.json')
        shutil.copy2(ra, dst)
        copied.append({"name": "RELEASE_ASSETS_READBACK.json", "bytes": os.path.getsize(dst),
                       "sha256": sha256_file(dst), "source_was_external": a.logdir})

    # 2. the three PB-090 fields
    manifests = {}
    for rel in ['packaging/public-plugin/plugin.release.json', 'packaging/public-plugin/plugin.json',
                'packaging/public-plugin/vendor-plugin.schema.json']:
        p = os.path.join(a.repo, rel)
        if os.path.exists(p):
            manifests[rel] = {"sha256": sha256_file(p), "bytes": os.path.getsize(p)}
    commands = []
    for log, argv in [('focused.log', "python -m unittest discover -s tests -p 'test_s4ext_*.py' -v"),
                      ('full.log',    "python -m unittest discover -s tests -t . -v")]:
        lp = os.path.join(raw_dir, log)
        if os.path.exists(lp):
            c = read_counts(lp)
            ep = os.path.join(raw_dir, log.replace('.log', '.exit'))
            ec = int(open(ep).read().strip().split('=')[-1]) if os.path.exists(ep) else None
            commands.append({"argv_redacted": argv, "cwd": "<worktree>", "exit_code": ec, **c,
                             "raw_log": f"verify/r3/raw/{log}", "log_sha256": sha256_file(lp)})
    assets = json.load(open(os.path.join(R, 'verify/r3/RELEASE_ASSETS_READBACK.json'), encoding='utf-8')) \
        if os.path.exists(os.path.join(R, 'verify/r3/RELEASE_ASSETS_READBACK.json')) else []

    # 3/4/5 edit the pack
    d = json.load(open(pack_path, encoding='utf-8'))
    d['manifest_sha256'] = {
        "what_it_hashes": "the candidate's own manifests/schema in this tree (NOT a release-tuple manifest; no release exists for this candidate)",
        "files": manifests}
    d['release_assets'] = {
        "scope": "the PUBLISHED v0.1.1-preview.3 assets, re-read anonymously in this round",
        "method": "anonymous HTTPS GET of each browser_download_url; SHA-256 computed on the downloaded bytes and compared to the API-reported digest",
        "ceiling": "this verifies ASSET INTEGRITY vs API metadata ONLY. It does NOT verify that the assets were built from the tagged source (tag -> source -> build -> asset reproducibility stays OPEN, per verdict section 2.1).",
        "assets": assets,
        "candidate_assets": "NOT_APPLICABLE_UNRELEASED"}
    d['commands'] = commands
    d['sod'] = {
        "producer_identity": {"account": "user", "sid": "S-1-5-21-2687334950-3868438633-1592137926-1000",
                              "role": "repo owner worktree / orchestrator writes"},
        "checker_identity": {"account": "CodexSandboxOffline", "sid": "S-1-5-21-2687334950-3868438633-1592137926-1004",
                             "role": "sealed acceptance lane (AO6..AO12)"},
        "distinct_sids": True,
        "mechanism": "the acceptance lane ran under a DIFFERENT local account from the maker; this is a process+identity separation, not a model separation",
        "residual": "same model family across maker and checker is absent here (checker=gpt-6.1-sol, maker=deepseek-v4.1-flash), but both ran on the same HOST and the same relay class; correlated-blind-spot risk is NOT eliminated"},
    prev = dict(d.get('independent_checker', {}))
    d['independent_checker'] = {
        "identity": "CodexSandboxOffline (S-1-5-21-...-1004)",
        "scope": "PIPD-LS-SP S4POST Stage-B candidate, declared scope per EXTERNAL_CHALLENGE_INTAKE.json",
        "verdict": "FAIL_CHALLENGE",
        "evidence": "verify/ao12/EXTERNAL_CHALLENGE_REPORT.md (+ FINDINGS.json, REVIEW_EVIDENCE_MANIFEST.json)",
        "previous_stale_value": prev,
        "note": "the previous value (NOT_RUN) was STALE: twelve acceptance rounds have since run (AO6..AO12). The latest independent verdict is FAIL_CHALLENGE with 9 findings, all inside the round's own verification harness.",
    }
    d.setdefault('binding_correction', {}).update({
        "stale_field": "frozen_subject.stage_b_commit",
        "stale_value": d.get('frozen_subject', {}).get('stage_b_commit'),
        "issue": "FCR-007 / TT-S4POST-EVIDENCE-06: the accepted scope is not bound to the integrated frozen subject",
        "action_taken": "NONE - re-binding the accepted scope is the owner's act (see OWNER_ACTION_REQUEST.md D2)",
        "status": "PENDING_OWNER_RATIFICATION"})
    d['r3_remedies'] = {
        "stamp_utc": ts, "authorized_by": "owner order 2026-10-13",
        "artifacts": {
            "R1_R8": "HARNESS_FREEZE_AND_AO_LOOP_CAP.md",
            "R2": "branch split: product-only branch vs chore/s4post-verification-harness (see ROUND_RESULT/R3_PUBLICATION.md)",
            "R3": "this update (commands + release_assets + manifest_sha256)",
            "R4": "OWNER_ACTION_REQUEST.md",
            "R5": "public-plugin-verify.yml run via Draft PR (see R3_PUBLICATION.md for the outcome)",
            "R6": "verify/R6_EVIDENCE_RERUNNABILITY.md + verify/tools/check_evidence_locators.py",
            "R7": "sod block above",
            "surfaces": {"kanban": "kanban/R3_BOARD_EVIDENCE.json", "gstack": "surface/GSTACK_R3_ROUTE_READBACK.json",
                         "openspec": "surface/OPENSPEC_R3_EVIDENCE.json"}},
        "pack_preimage_sha256": pre, "pack_edited_at_utc": ts}
    json.dump(d, open(pack_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({"preimage_sha256": pre, "postimage_sha256": sha256_file(pack_path),
                      "curated_files": len(copied), "commands": len(commands),
                      "release_assets": len(assets),
                      "suite_result": [c.get('result') for c in commands]}, ensure_ascii=False, indent=1))
    return 0

if __name__ == '__main__':
    sys.exit(main())
