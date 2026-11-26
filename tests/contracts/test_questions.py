"""R55: one catalogue of questions in both languages; the flows use it and the skill pages show the same wording."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'skills/setup/scripts'))
from state import questions  # noqa: E402

PAGES = {'setup': ('kind', 'name', 'display_name', 'publisher', 'description', 'documentation_languages', 'license', 'copyright_year',
                   'rights_holder', 'marketplace', 'differs', 'template_gone'),
         'modify': ('run_setup', 'change', 'new_value'), 'docs': ('run_setup', 'documentation_languages')}


def read(relative):
    return (ROOT / relative).read_text(encoding='utf-8')


def fixed_part(question):
    """The longest wording between placeholders, without the suggestion and the hint about free answers."""
    return max((part.strip() for part in re.split(r'\{[a-z_]+\}|(?<=\?) ', question)), key=len)


class QuestionCatalogue(unittest.TestCase):
    def test_both_languages_carry_the_same_questions_and_placeholders(self):
        german, english = questions.questions('de'), questions.questions('en')
        self.assertEqual(set(german), set(english))
        for key in german:
            if key not in ('language', 'write'):
                self.assertEqual(len(german[key]['choices']), len(english[key]['choices']), key)
                self.assertEqual(re.findall(r'\{[a-z_]+\}', german[key]['question']), re.findall(r'\{[a-z_]+\}', english[key]['question']), key)

    def test_the_skill_pages_show_the_wording_that_is_asked(self):
        for language in ('de', 'en'):
            catalogue = questions.questions(language)
            for page, keys in PAGES.items():
                text = read('docs/%s/skills/%s.md' % (language, page))
                for key in keys:
                    with self.subTest(language=language, page=page, question=key):
                        self.assertIn(fixed_part(catalogue[key]['question']), text)

    def test_the_gate_and_the_language_flow_carry_the_catalogue_wording(self):
        for language in ('de', 'en'):
            entry = questions.questions(language)['run_setup']
            for part in (entry['question'], *entry['choices']):
                self.assertIn(part, read('skills/_shared/flows/gate.md'))
        self.assertIn(questions.LANGUAGE_QUESTION[0], read('skills/setup/flows/language.md'))

    def test_the_command_answers_in_the_saved_language_and_writes_nothing(self):
        helper = str(ROOT / 'skills/setup/scripts/setup_state.py')
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / '.project').mkdir()
            (project / '.project/operator.json').write_text('{"schema_version": 1, "operator_language": "de"}')
            result = subprocess.run([sys.executable, '-B', helper, 'questions', '--target', directory, '--message-language', 'en'],
                                    capture_output=True, text=True)
            answer = json.loads(result.stdout)
            self.assertEqual((0, 'de', 'Wer ist der Herausgeber?'), (result.returncode, answer['language'], answer['questions']['publisher']['question']))
            self.assertEqual(['operator.json'], [p.name for p in (project / '.project').iterdir()])


if __name__ == '__main__':
    unittest.main()
