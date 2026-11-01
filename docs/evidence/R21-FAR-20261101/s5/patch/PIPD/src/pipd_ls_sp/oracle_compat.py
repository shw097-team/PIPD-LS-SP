"""Offline proposal only. No issuer, signature, acceptance, schema migration or native write.

The installed PI bytes remain the serialized legacy object. This adapter produces a
separate, unsigned compatibility proposal for the actual Oracle/schema Owners to review.
"""
import hashlib
import json
import re
from jsonschema import Draft202012Validator

class CandidateRefusal(ValueError):
    pass

# Scope pin to the actual unchanged installed P4 0.1.1 schema semantics.
# This rejects caller-supplied schema relaxation; it grants no Owner authority.
EXPECTED_SCHEMA_CANONICAL_SHA256 = '44b4d6b91165482592089e808b6729a5d66e75a1de226d68106a54f74abc5581'

def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise CandidateRefusal('DUPLICATE_JSON_KEY:' + key)
        result[key] = value
    return result

def propose(pi_bytes, schema, *, subject_id, subject_hash, canonical_owner,
            canonical_source_sha256, expected_source_sha256):
    actual_schema_pin = hashlib.sha256(json.dumps(schema, sort_keys=True,
        separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()
    if actual_schema_pin != EXPECTED_SCHEMA_CANONICAL_SHA256:
        raise CandidateRefusal('UNTRUSTED_LEGACY_SCHEMA')
    obj = json.loads(pi_bytes, object_pairs_hook=_unique_pairs)
    if not all(isinstance(s, str) and re.fullmatch(r'[0-9a-f]{64}', s)
               for s in (canonical_source_sha256, expected_source_sha256)):
        raise CandidateRefusal('SOURCE_DIGEST_FORMAT')
    errors = list(Draft202012Validator(schema).iter_errors(obj))
    if errors:
        raise CandidateRefusal('LEGACY_ABI_REFUSED:' + errors[0].validator)
    if canonical_owner != 'PIPD_LS_DOC-07':
        raise CandidateRefusal('FOREIGN_CANONICAL_OWNER')
    if not canonical_source_sha256 or canonical_source_sha256 != expected_source_sha256:
        raise CandidateRefusal('CANONICAL_SOURCE_MISMATCH')
    if obj['subject_id'] != subject_id or obj['content_hash'] != subject_hash:
        raise CandidateRefusal('FOREIGN_SUBJECT')
    atoms = obj['stable_semantic_contract']['atoms']
    targets = {(a['subject_id'], a['content_hash']) for a in atoms}
    traces = obj['trace']
    if len(targets) != len(atoms) or len(traces) != len(atoms):
        raise CandidateRefusal('TRACE_CARDINALITY_MISMATCH')
    if any(t['from_id'] != subject_id or t['from_hash'] != subject_hash for t in traces):
        raise CandidateRefusal('FOREIGN_TRACE_SUBJECT')
    if {(t['to_id'], t['to_hash']) for t in traces} != targets:
        raise CandidateRefusal('TRACE_ATOM_HASH_MISMATCH')
    return {
        'artifact_kind': 'UNSIGNED_OFFLINE_ORACLE_COMPATIBILITY_PROPOSAL',
        'native_artifact': False,
        'resolution': 'CR_ORACLE_001_OPEN_QUARANTINE',
        'subject_id': subject_id,
        'subject_hash': subject_hash,
        'legacy_bytes_sha256': hashlib.sha256(pi_bytes).hexdigest(),
        'serialized_legacy_symbol': obj['acceptance']['oracle_source'],
        'proposed_semantic_owner': canonical_owner,
        'canonical_source_sha256': canonical_source_sha256,
        'owner_ratification': None,
        'independent_checker_receipt': None,
        'native_use_allowed': False,
        'rollback': 'Discard separate proposal; original PI and installed schema bytes unchanged',
    }
