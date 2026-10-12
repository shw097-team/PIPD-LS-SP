import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from tests.test_public_plugin_packaging import temp_env, PLUGIN_ID

for link_kind in ('symlink', 'hardlink'):
    with temp_env() as env:
        ledger = env.freeze()
        env.write_packaging(ledger)
        env.out.mkdir()
        sentinel = env.root / 'SENTINEL.txt'
        original = b'INDEPENDENT_AO_SENTINEL_DO_NOT_OVERWRITE\n'
        sentinel.write_bytes(original)
        output_member = env.out / (PLUGIN_ID + '.zip.sha256')
        try:
            if link_kind == 'symlink':
                os.symlink(sentinel, output_member)
            else:
                os.link(sentinel, output_member)
        except OSError as exc:
            print(f'{link_kind}: NOT_EXECUTED link creation failed: {exc!r}')
            continue
        print(f'{link_kind}: before={sentinel.read_bytes()!r}')
        try:
            report = env.build(ledger)
            print(f'{link_kind}: builder_verdict={report["verdict"]}')
        except Exception as exc:
            print(f'{link_kind}: builder_exception={exc!r}')
        print(f'{link_kind}: after={sentinel.read_bytes()!r}')
        print(f'{link_kind}: sentinel_untouched={sentinel.read_bytes() == original}')
