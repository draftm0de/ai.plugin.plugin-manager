"""R50: the question before writing and the list of written files are finished texts of the helper."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/setup/scripts'))
from state import messages, reporting  # noqa: E402


class Ctx:
    lock_path = '.project/plugins/fictional/skeleton.json'


def plan(files=(), updates=(), auto=(), rule=False, ignore='', pending=(), cleanup=(), lock=True):
    return {'files': dict(files), 'updates': list(updates), 'removals': {'auto': list(auto), 'lock_cleanup': list(cleanup)},
            'rule_pending': rule, 'ignore_text': ignore, 'pending': list(pending), 'lock_exists': lock}


class WriteRequest(unittest.TestCase):
    def test_every_file_is_named_with_what_happens_to_it(self):
        entries = reporting.pending_writes(Ctx, plan(files={'b.md': 'missing', 'c.md': 'identical'}, updates=['a.md'],
                                                     auto=['d.md'], rule=True, ignore='x', pending=['c.md']))
        self.assertEqual('Ich möchte Datei(en) ändern:\n\n* .gitignore (ändern)\n* a.md (ändern)\n* b.md (anlegen)\n* d.md (löschen)\n\n'
                         'Darf ich schreiben?', messages.write_request(entries, 'de'))

    def test_the_evidence_file_is_named_only_when_nothing_else_is_written(self):
        entries = reporting.pending_writes(Ctx, plan(pending=['c.md'], lock=False))
        self.assertEqual([(Ctx.lock_path, 'create')], entries)
        self.assertIsNone(messages.write_request(reporting.pending_writes(Ctx, plan()), 'en'))

    def test_the_result_lists_the_files_per_kind_of_change(self):
        self.assertEqual('Aktualisiert habe ich:\n- a.md\n- b.md\n\nNeu angelegt habe ich:\n- c.py',
                         messages.write_result(updated=['b.md', 'a.md'], created=['c.py'], language='de'))
        self.assertIsNone(messages.write_result(language='de'))


class FlowTexts(unittest.TestCase):
    def test_the_skeleton_flow_asks_before_it_runs_setup(self):
        text = (ROOT / 'skills/setup/flows/skeleton.md').read_text(encoding='utf-8')
        self.assertLess(text.index('write_request'), text.index('setup --target'))
        self.assertIn('Only an explicit yes', text)


if __name__ == '__main__':
    unittest.main()
