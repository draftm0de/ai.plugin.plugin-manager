"""verify on a plugin and a marketplace root: kind detection, drift, local mapping and read-only behaviour."""
import json
import subprocess
import sys
import unittest

from tests.support.marketplace_fixture import attach
from tests.support.workflow_fixture import ROOT, WorkflowFixture, verify

HELPER = ROOT / 'skills/_shared/scripts/verify.py'
CLAUDE, CODEX = '.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'


class VerifyContextTests(WorkflowFixture, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.create()
        self.catalog = attach(self.plugin)
        subprocess.run([sys.executable, '-B', 'scripts/marketplace.py', 'sync'], cwd=self.catalog,
                       check=True, capture_output=True)

    def files(self):
        return {str(p): p.read_bytes() for root in (self.plugin, self.catalog)
                for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}

    def change(self, path, update):
        original = path.read_bytes()
        data = json.loads(original)
        update(data)
        path.write_text(json.dumps(data))
        return original

    def assert_rejected(self, root, path, update):
        original = self.change(path, update)
        before = self.files()
        self.assertFalse(verify.verify(root)['valid'], path)
        self.assertEqual(before, self.files())
        path.write_bytes(original)
        self.assertTrue(verify.verify(root)['valid'], path)

    def test_each_root_is_recognized_and_a_mismatching_kind_fails(self):
        self.assertEqual('marketplace', verify.verify(self.catalog)['kind'])
        self.assertEqual('plugin', verify.verify(self.plugin)['kind'])
        self.assertFalse(verify.verify(self.catalog, 'plugin')['valid'])
        self.assertFalse(verify.verify(self.plugin, 'marketplace')['valid'])

    def test_an_ambiguous_root_needs_an_explicit_kind(self):
        (self.catalog / 'plugin.json').write_text('{}')
        self.assertFalse(verify.verify(self.catalog)['valid'])
        self.assertTrue(verify.verify(self.catalog, 'marketplace')['valid'])

    def test_verification_is_read_only_and_never_executes_target_code(self):
        for path in (self.catalog / 'scripts/marketplace.py', self.plugin / 'scripts/plugin.py'):
            path.write_text("raise RuntimeError('target code must never run')\n")
        before = self.files()
        report = verify.verify(self.catalog)
        self.assertTrue(report['valid'], report)
        self.assertFalse(report['target_code_executed'])
        self.assertEqual(before, self.files())

    def test_the_default_source_is_the_working_directory_not_the_installation(self):
        empty = self.root / 'empty'
        empty.mkdir()
        result = subprocess.run([sys.executable, '-B', str(HELPER)], cwd=empty, capture_output=True, text=True)
        self.assertEqual(1, result.returncode)
        self.assertEqual(str(empty), json.loads(result.stdout)['source'])

    def test_remote_content_is_reported_as_not_verified(self):
        self.assertFalse(verify.verify(self.catalog)['plugins'][0]['remote_content_verified'])

    def test_a_missing_or_broken_local_mapping_does_not_invalidate_the_structure(self):
        local = self.catalog / '.local/marketplace.json'
        for content in (None, '{broken'):
            with self.subTest(content=content):
                local.unlink() if content is None else local.write_text(content)
                report = verify.verify(self.catalog)
                self.assertTrue(report['valid'], report)
                self.assertEqual('unavailable', report['local_development']['status'])

    def test_catalog_and_host_manifest_drift_are_errors_and_nothing_is_rewritten(self):
        self.assert_rejected(self.catalog, self.catalog / CODEX, lambda data: data['plugins'].pop())
        self.assert_rejected(self.catalog, self.catalog / CODEX,
                             lambda data: data['plugins'][0]['policy'].update(installation='UNKNOWN'))
        for relative in (CLAUDE, CODEX):
            self.assert_rejected(self.catalog, self.catalog / relative, lambda data: data.update(unexpected='preserve'))
        manifest = self.plugin / '.claude-plugin/plugin.json'
        for update in ({'name': 'wrong'}, {'unexpected': 'preserve'}):
            self.assert_rejected(self.plugin, manifest, lambda data: data.update(update))

    def test_a_quoted_skeleton_marker_is_no_implementation_status(self):
        entry = next(self.plugin.glob('skills/*/SKILL.md'))
        marker = '<!-- plugin-skeleton: unimplemented -->'
        original = entry.read_text().replace(marker, '')
        for quote in ('    ' + marker, '`' + marker + '`', '```md\n' + marker + '\n```'):
            entry.write_text(original + '\n' + quote + '\n')
            self.assertEqual('not_assessed', verify.verify(self.plugin)['implementation_status'], quote)
        entry.write_text(original + '\n' + marker + '\n')
        self.assertEqual('skeleton', verify.verify(self.plugin)['implementation_status'])

    def test_a_dangling_host_local_skill_link_is_rejected_and_kept(self):
        link = self.plugin / '.claude/skills'
        link.parent.mkdir(exist_ok=True)
        link.symlink_to(self.plugin / 'missing')
        self.assertFalse(verify.verify(self.plugin)['valid'])
        self.assertTrue(link.is_symlink())


if __name__ == '__main__':
    unittest.main()
