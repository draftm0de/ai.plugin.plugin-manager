"""R26: the check before a configuration returns the finished message, in the language of the person."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HELPER = ROOT / 'skills/_shared/scripts/workflows.py'


def run(*args):
    return subprocess.run([sys.executable, '-B', str(HELPER), 'prerequisites', *args], text=True, capture_output=True)


class PrerequisitesTests(unittest.TestCase):
    def test_a_folder_without_git_gets_both_commands_with_its_name_and_nothing_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'my.market'
            folder.mkdir()
            result = run('--root', str(folder), '--message-language', 'de', '--changed', 'none')
            self.assertEqual(1, result.returncode)
            first, second = result.stderr.split('\n\n', 1)
            self.assertIn('```bash\ngit init\ngit remote add origin https://github.com/<owner>/my.market.git\n```', second)
            self.assertIn('Die Aktion setup konnte nicht abgeschlossen werden, weil der Ordner', first)
            self.assertIn('Es wurde nichts geändert.', first)
            self.assertIn('Rufe danach /plugin-manager:setup erneut auf.', second)
            self.assertEqual([], list(folder.iterdir()))

    def test_a_repository_without_origin_needs_only_the_address_and_with_it_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'with space'
            folder.mkdir()
            subprocess.run(['git', 'init', '-q', str(folder)], check=True)
            missing = run('--root', str(folder), '--message-language', 'en')
            self.assertIn('has no GitHub address yet', missing.stderr)
            self.assertIn('https://github.com/<owner>/<name>.git', missing.stderr)
            self.assertNotIn('git init', missing.stderr.split('[Technical')[0])
            subprocess.run(['git', '-C', str(folder), 'remote', 'add', 'origin', 'https://github.com/o/n.git'], check=True)
            self.assertEqual(0, run('--root', str(folder)).returncode)

    def test_the_saved_operator_language_decides_whatever_the_call_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / '.project').mkdir()
            (Path(tmp) / '.project/operator.json').write_text('{"schema_version": 1, "operator_language": "de"}')
            for extra in (('--message-language', 'en'), ()):
                self.assertIn('Die Aktion setup', run('--root', tmp, *extra).stderr)


if __name__ == '__main__':
    unittest.main()
