"""Opt-in: real host CLIs install and update the development snapshots in isolated profiles."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / 'skills/_shared/templates/marketplace/sync/scripts'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('local_plugins', SCRIPTS / 'local_plugins.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
NAMES = ('fictional-alpha', 'fictional-beta')


class NativeLocalPluginTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('AI_PLUGIN_TEST_NATIVE') == '1' and shutil.which('claude') and shutil.which('codex'),
                         'Opt-in isolated native shared marketplace')
    def test_both_hosts_install_and_update_the_checkouts_without_git(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            market, home = base / 'market', base / 'home'
            shutil.copytree(SCRIPTS, market / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
            for folder in (home / '.claude', home / '.codex', market / '.local'):
                folder.mkdir(parents=True)
            checkouts = {name: base / name for name in NAMES}
            entries = []
            for name, path in checkouts.items():
                repository = 'https://github.com/example/' + name
                (path / 'skills/example').mkdir(parents=True)
                (path / 'skills/example/SKILL.md').write_text('---\nname: example\ndescription: Fictional.\n---\n# Example\n')
                (path / 'plugin.json').write_text(json.dumps({'name': name, 'description': 'Fictional', 'repository': repository,
                    'extensions': {'io.zyris.distribution': {'skillRoot': 'skills', 'catalogs': False}}}))
                entries.append({'name': name, 'displayName': name, 'description': 'Fictional', 'repository': repository + '.git'})
            (market / 'marketplace.json').write_text(json.dumps(
                {'name': 'fictional-market', 'displayName': 'Fictional Market', 'owner': {'name': 'Fixture'}, 'plugins': entries}))
            (market / '.local/marketplace.json').write_text(json.dumps(
                {'sources': {name: str(path) for name, path in checkouts.items()}}))
            isolated = {'HOME': str(home), 'CLAUDE_CONFIG_DIR': str(home / '.claude'),
                        'CODEX_HOME': str(home / '.codex'), 'DISABLE_AUTOUPDATER': '1'}
            with patch.dict(os.environ, isolated):
                for host in ('claude', 'codex'):
                    first = engine.install_local(host, root=market)
                    for path in checkouts.values():
                        skill = path / 'skills/example/SKILL.md'
                        skill.write_text(skill.read_text() + 'Updated for ' + host + '.\n')
                    second = engine.install_local(host, root=market)
                    for name in NAMES:
                        version = second['plugins'][name]['version']
                        self.assertNotEqual(first['plugins'][name]['version'], version)
                        cache = (home / ('.' + host) / 'plugins/cache/fictional-market-dev' / name / version /
                                 'skills/example/SKILL.md')
                        if host == 'claude' and not cache.exists():
                            listing = json.loads(subprocess.check_output(['claude', 'plugin', 'list', '--json']))
                            item = next(i for i in listing if i['id'] == name + '@fictional-market-dev')
                            cache = Path(item.get('readFromFolder') or item['installPath']) / 'skills/example/SKILL.md'
                        self.assertEqual((checkouts[name] / 'skills/example/SKILL.md').read_bytes(), cache.read_bytes())


if __name__ == '__main__':
    unittest.main()
