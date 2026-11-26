"""R50: the generators ask first (--plan writes nothing), list what they wrote and create files with the usual mode."""
import os
import stat
import subprocess
import unittest

from tests.support.workflow_fixture import WorkflowFixture, flow


class GeneratorQuestionTests(WorkflowFixture, unittest.TestCase):
    def new_checkout(self, name):
        folder = self.root / name
        folder.mkdir()
        subprocess.run(['git', 'init', '-q', str(folder)], check=True)
        subprocess.run(['git', '-C', str(folder), 'remote', 'add', 'origin', 'https://github.com/example/' + name + '.git'], check=True)
        return folder

    def test_a_plan_writes_nothing_and_names_every_file_then_the_run_lists_them(self):
        market = self.new_checkout('second-market')
        facts = dict(name='second-market', display_name='Second Market', owner='Fictional Publisher', message_language='de')
        asked = flow.create_marketplace(market, plan=True, **facts)
        self.assertEqual(['.git'], [p.name for p in market.iterdir()])
        self.assertTrue(asked['write_request'].startswith('Ich möchte Datei(en) ändern:'))
        self.assertTrue(asked['write_request'].endswith('Darf ich schreiben?'))
        done = flow.create_marketplace(market, **facts)
        for path in done['changed']:
            relative = os.path.relpath(path, market)
            self.assertIn('* %s (anlegen)' % relative, asked['write_request'])
            self.assertIn('- ' + relative, done['result_message'])
        self.assertIsNone(flow.create_marketplace(market, plan=True, **facts)['write_request'])

    def test_new_files_get_the_usual_mode_and_a_changed_file_keeps_its_own(self):
        market = self.new_checkout('modes')
        (market / '.gitignore').write_text('x\n')
        os.chmod(market / '.gitignore', 0o640)
        mask = os.umask(0o022)
        try:
            flow.create_marketplace(market, 'modes', 'Modes', 'Fictional Publisher')
        finally:
            os.umask(mask)
        self.assertEqual(0o644, stat.S_IMODE((market / 'marketplace.json').stat().st_mode))
        self.assertEqual(0o640, stat.S_IMODE((market / '.gitignore').stat().st_mode))

    def test_a_plugin_plan_writes_nothing_in_either_repository_and_names_both(self):
        before = {p: p.read_bytes() for root in (self.plugin, self.market) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
        asked = flow.create_plugin(self.plugin, self.market, skeleton=True, name=self.plugin.name, display_name='Fictional Plugin',
                                   description='Fictional', author='Fictional Publisher', license='deferred',
                                   languages=['de', 'en'], default_language='de', plan=True)
        self.assertIn('* plugin.json (create)', asked['write_request'])
        self.assertIn('* ../market/marketplace.json (change)', asked['write_request'])
        self.assertEqual(before, {p: p.read_bytes() for root in (self.plugin, self.market) for p in root.rglob('*') if p.is_file() and '.git' not in p.parts})


if __name__ == '__main__':
    unittest.main()
