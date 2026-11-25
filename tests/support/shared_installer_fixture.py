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
from tests.support.marketplace_fixture import attach

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
if not (ROOT / 'plugin.json').is_file():
    ROOT = ROOT.parent
spec = importlib.util.spec_from_file_location('shared_installer', ROOT / 'scripts/plugin.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
spec = importlib.util.spec_from_file_location('shared_packaging', ROOT / 'skills/_shared/templates/marketplace/sync/scripts/plugin_payload.py')
packaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packaging)


class SharedInstallerTestsFixture:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()/'plugin'
        self.root.mkdir()
        source = self.root / 'skills/fictional-skill'
        source.mkdir(parents=True)
        (source / 'SKILL.md').write_text('---\nname: fictional-skill\ndescription: Fictional test\n---\n# Test')
        self.manifest = {'name':'fictional-product', 'repository':'https://github.com/example/fictional-product','description':'Fictional plugin',
            'extensions': {'io.zyris.distribution':{'skillRoot':'skills'}}}
        self.write_manifest()
        self.market = attach(self.root)
        subprocess.run([sys.executable, '-B', 'scripts/marketplace.py', 'sync'], cwd=self.market, check=True, capture_output=True)
        with patch.object(engine, 'ROOT', self.root): engine.repository_metadata()
        for relative in ('scripts/plugin.py',):
            target = self.root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT / relative,target)
        shutil.copy2(ROOT / 'skills/_shared/templates/plugin/sync/Makefile', self.root / 'Makefile')


    def write_manifest(self):
        (self.root / 'plugin.json').write_text(json.dumps(self.manifest))


    def invoke(self, *args):
        return subprocess.run(args,cwd=self.root,capture_output=True,text=True,check=True)


    def install(self, target, dry_run=True):
        spec = importlib.util.spec_from_file_location('fixture_local', self.market / 'scripts/local_plugins.py')
        self.local = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.local)
        return self.local.install_local(target, dry_run=dry_run, root=self.market)


    def make_install(self, **kwargs):
        return subprocess.run(['make', '-s', 'install-local', 'DRY_RUN=1'], cwd=self.market, capture_output=True, text=True, **kwargs)


class LocalDevelopmentTestsFixture:
    setUp = SharedInstallerTestsFixture.setUp


    write_manifest = SharedInstallerTestsFixture.write_manifest
    install = SharedInstallerTestsFixture.install
