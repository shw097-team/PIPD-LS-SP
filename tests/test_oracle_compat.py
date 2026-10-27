"""Maker regression of the public adapter API; no acceptance or ratification."""
import copy
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from pipd_ls_sp import pipeline
from pipd_ls_sp.oracle_compat import CandidateRefusal

P4 = ROOT / 'skills/pipd-pi-compile'
SCHEMA_BYTES = (P4 / 'schemas/output.schema.json').read_bytes()
SCHEMA = json.loads(SCHEMA_BYTES)
SAMPLES = [json.loads(m[1]) for m in re.finditer(r'```json\s*\n(.*?)\n```',
            (P4 / 'references/examples.md').read_text(encoding='utf-8'), re.S)]
CONTROL = copy.deepcopy(next(s for s in SAMPLES if s.get('schema_version') == 'PI-PKG@1'))
# Correct only the test fixture's trace references; never alter installed examples.
for trace, atom in zip(CONTROL['trace'], CONTROL['stable_semantic_contract']['atoms']):
    trace['to_id'], trace['to_hash'] = atom['subject_id'], atom['content_hash']
SOURCE = hashlib.sha256(b'DOC-07 disposable fixture; no native authority').hexdigest()


def raw(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False).encode('utf-8')


def invoke(body=None, schema=None, **changes):
    args = dict(subject_id=CONTROL['subject_id'], subject_hash=CONTROL['content_hash'],
                canonical_source_sha256=SOURCE, expected_source_sha256=SOURCE)
    args.update(changes)
    return pipeline.propose_oracle_compatibility(raw(CONTROL) if body is None else body,
                                                SCHEMA if schema is None else schema, **args)


class OracleCompatibilityTests(unittest.TestCase):
    def test_product_api_keeps_legacy_abi_and_unsigned_ceiling(self):
        before = raw(CONTROL)
        result = invoke(before)
        self.assertEqual(result['serialized_legacy_symbol'], 'DOC-03 DOMAIN_ORACLES')
        self.assertEqual(result['proposed_semantic_owner'], 'PIPD_LS_DOC-07')
        self.assertEqual(result['resolution'], 'CR_ORACLE_001_OPEN_QUARANTINE')
        self.assertFalse(result['native_use_allowed'])
        self.assertFalse(result['native_artifact'])
        self.assertIsNone(result['owner_ratification'])
        self.assertIsNone(result['independent_checker_receipt'])
        self.assertEqual(before, raw(CONTROL))
        self.assertEqual(SCHEMA_BYTES, (P4 / 'schemas/output.schema.json').read_bytes())

    def test_duplicate_top_level_key_refused(self):
        body = b'{"subject_id":"foreign",' + raw(CONTROL)[1:]
        with self.assertRaisesRegex(CandidateRefusal, 'DUPLICATE_JSON_KEY'):
            invoke(body)

    def test_nested_duplicate_key_refused(self):
        body = raw(CONTROL).replace(b'"owner":', b'"owner":"foreign","owner":', 1)
        self.assertNotEqual(body, raw(CONTROL))
        with self.assertRaisesRegex(CandidateRefusal, 'DUPLICATE_JSON_KEY'):
            invoke(body)

    def test_schema_relaxation_refused(self):
        schema = copy.deepcopy(SCHEMA)
        schema['properties']['acceptance']['properties']['oracle_source']['const'] = 'DOC-07'
        with self.assertRaisesRegex(CandidateRefusal, 'UNTRUSTED_LEGACY_SCHEMA'):
            invoke(schema=schema)

    def test_foreign_subject_refused(self):
        with self.assertRaisesRegex(CandidateRefusal, 'FOREIGN_SUBJECT'):
            invoke(subject_hash='0' * 64)

    def test_foreign_source_refused(self):
        with self.assertRaisesRegex(CandidateRefusal, 'CANONICAL_SOURCE_MISMATCH'):
            invoke(canonical_source_sha256='0' * 64)

    def test_nonhex_source_refused(self):
        with self.assertRaisesRegex(CandidateRefusal, 'SOURCE_DIGEST_FORMAT'):
            invoke(canonical_source_sha256='g' * 64)

    def test_trace_wrong_atom_hash_refused(self):
        obj = copy.deepcopy(CONTROL)
        obj['trace'][0]['to_hash'] = '0' * 64
        with self.assertRaisesRegex(CandidateRefusal, 'TRACE_ATOM_HASH_MISMATCH'):
            invoke(raw(obj))

    def test_missing_trace_refused(self):
        obj = copy.deepcopy(CONTROL)
        obj['trace'] = obj['trace'][:1]
        with self.assertRaisesRegex(CandidateRefusal, 'TRACE_CARDINALITY_MISMATCH'):
            invoke(raw(obj))

    def test_foreign_trace_subject_refused(self):
        obj = copy.deepcopy(CONTROL)
        obj['trace'][0]['from_hash'] = '0' * 64
        with self.assertRaisesRegex(CandidateRefusal, 'FOREIGN_TRACE_SUBJECT'):
            invoke(raw(obj))

    def test_direct_namespace_migration_refused(self):
        obj = copy.deepcopy(CONTROL)
        obj['acceptance']['oracle_source'] = 'DOC-07'
        with self.assertRaisesRegex(CandidateRefusal, 'LEGACY_ABI_REFUSED:const'):
            invoke(raw(obj))

    def test_cli_exact_set_preserved(self):
        from pipd_ls_sp.cli import COMMANDS
        self.assertEqual(len(COMMANDS), 13)
        self.assertNotIn('oracle', COMMANDS)


if __name__ == '__main__':
    unittest.main()
