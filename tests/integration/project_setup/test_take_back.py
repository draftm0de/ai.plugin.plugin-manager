"""R45: a file kept on purpose is listed and can be taken back by an explicit adopt for exactly that pair."""
import unittest

from tests.support.project_setup_fixture import Sandbox, tree

OWN = b'# own instructions\n'


class TakeBackTests(unittest.TestCase):
    def setUp(self):
        self.box = Sandbox().make(); self.addCleanup(self.box.close)
        self.file = self.box.project / 'CLAUDE.md'
        self.assertEqual(0, self.box.call('language', '--language', 'de')[0])
        self.assertEqual(0, self.box.call('setup')[0])
        self.file.write_bytes(OWN)
        self.assertEqual(0, self.decide('keep', self.status()['sync']['decisions'][0])[0])

    def status(self):
        return self.box.call('status')[1]

    def decide(self, decision, item, path=None):
        return self.box.call('sync', '--decision', decision, '--path', path or item['path'],
                             '--source-hash', item['source_hash'], '--local-hash', item['local_hash'])

    def test_a_kept_file_is_listed_and_adopting_it_restores_the_template(self):
        data = self.status()
        self.assertEqual(('ready', ['CLAUDE.md']), (data['next'], [item['path'] for item in data['kept']]))
        code, result, _ = self.decide('adopt', data['kept'][0])
        self.assertEqual((0, True), (code, result['ok']))
        self.assertEqual(self.box.template('CLAUDE.md'), self.file.read_bytes())
        data = self.status()
        self.assertEqual(('ready', [], 'identical'), (data['next'], data['kept'], data['files']['CLAUDE.md']))

    def test_a_changed_file_or_a_file_without_anything_to_take_back_is_refused_with_its_reason(self):
        item = self.status()['kept'][0]
        before = tree(self.box.project)
        code, result, _ = self.decide('keep', item)
        self.assertEqual((1, False), (code, result['ok']))
        self.assertIn('keine offene Entscheidung', result['message'])
        code, result, _ = self.decide('adopt', item, path='AGENTS.md')
        self.assertEqual((1, False), (code, result['ok']))
        self.assertIn('keine offene Entscheidung', result['message'])
        self.assertIn('AGENTS.md', result['message'])
        self.assertEqual(before, tree(self.box.project))
        self.file.write_bytes(OWN + b'more\n')
        code, result, _ = self.decide('adopt', item)  # the shown pair is outdated: a new question is open
        self.assertEqual((1, False), (code, result['ok']))
        self.assertIn('geändert hat', result['message'])
        self.assertEqual(OWN + b'more\n', self.file.read_bytes())


if __name__ == '__main__':
    unittest.main()
