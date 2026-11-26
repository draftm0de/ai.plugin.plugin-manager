"""R53: docs answers with one finished message from the helper."""
import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
import documentation  # noqa: E402


class DocsResult(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        (self.root / 'plugin.json').write_text(json.dumps({'name': 'fictional'}))

    def message(self, created=(), updated=(), warnings=(), facts=()):
        return documentation.result_message(self.root, list(created), list(updated), list(warnings), list(facts), 'de')

    def test_with_nothing_to_report_only_the_status_line(self):
        self.assertEqual('Plugin fictional Doku: vollständig', self.message())

    def test_changes_and_open_points_are_listed_before_the_status(self):
        text = self.message(created=['docs/de/skills/x.md'], updated=['docs/de/skills.md'],
                            warnings=['docs/de/skills/x.md: "Ablauf" is still to be written: the steps',
                                      'docs/de/skills/x.md: "Beispiel" is still to be written: one'])
        self.assertEqual('Neu geschrieben:\n- docs/de/skills.md\n\nNeu angelegt:\n- docs/de/skills/x.md\n\n'
                         'Noch zu schreiben:\n- docs/de/skills/x.md: "Ablauf", "Beispiel"\n\nPlugin fictional Doku: 2 Warnungen', text)

    def test_every_warning_is_shown_and_counted(self):
        placeholder = 'docs/de/skills.md: unresolved template placeholders'
        text = self.message(warnings=['README.md: broken', placeholder])  # no open skill page explains it
        self.assertEqual('Warnungen:\n- README.md: broken\n- docs/de/skills.md: enthält noch Platzhalter\n\nPlugin fictional Doku: 2 Warnungen', text)
        text = self.message(warnings=['docs/de/skills/x.md: "Ablauf" is still to be written: steps', placeholder])
        self.assertNotIn('Platzhalter', text)
        self.assertIn('1 Warnung', text)

    def test_every_warning_text_of_the_check_has_a_german_translation(self):
        tree = ast.parse((ROOT / 'skills/_shared/scripts/verify/docs.py').read_text(encoding='utf-8'))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('validate', 'feature_errors', 'plugin_entry_errors')]
        samples = []
        for node in (x for f in functions for x in ast.walk(f)):
            if isinstance(node, ast.JoinedStr):
                text = ''.join(part.value if isinstance(part, ast.Constant) else '3' for part in node.values)
                if text.startswith('3: ') or (text.startswith('docs/') and ': ' in text):
                    samples.append(text)
        self.assertGreater(len(samples), 20)
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertNotEqual(sample, documentation.translate(sample, 'de'))
                self.assertEqual(sample, documentation.translate(sample, 'en'))
        self.assertIn('Warnungen:\n- README.md: Linkziel fehlt: x.md', self.message(warnings=['README.md: missing link target: x.md']))

    def test_the_saved_operator_language_is_used(self):
        self.assertEqual('en', documentation.operator_language(self.root))
        (self.root / '.project').mkdir()
        (self.root / '.project/operator.json').write_text(json.dumps({'operator_language': 'de'}))
        self.assertEqual('de', documentation.operator_language(self.root))


if __name__ == '__main__':
    unittest.main()
