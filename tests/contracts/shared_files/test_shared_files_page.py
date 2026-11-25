"""R46: the Manager's documentation names every shared file of both kinds with its class."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
HEADINGS = {'de': {'plugin': '## Dateien eines Plugins', 'marketplace': '## Dateien eines Marketplace'},
            'en': {'plugin': '## Files of a plugin', 'marketplace': '## Files of a marketplace'}}
LABELS = {'de': {'sync': '**Sync:**', 'seed': '**Seed:**'}, 'en': {'sync': '**Synced:**', 'seed': '**Seed:**'}}


def template_files(kind, part):
    base = ROOT / 'skills/_shared/templates' / kind / part
    names = set()
    for path in base.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            name = path.relative_to(base).as_posix().replace('docs/de/', 'docs/<lang>/').replace('docs/en/', 'docs/<lang>/')
            names.add('.gitignore' if name == 'gitignore.txt' else name)
    return names


class SharedFilesPage(unittest.TestCase):
    def test_every_file_of_both_kinds_is_listed_with_its_class(self):
        for language, headings in HEADINGS.items():
            text = (ROOT / 'docs' / language / 'files.md').read_text(encoding='utf-8')
            for kind, heading in headings.items():
                section = text.split(heading + '\n', 1)[1].split('\n## ', 1)[0]
                for part, label in LABELS[language].items():
                    line = next(line for line in section.splitlines() if line.startswith(label))
                    listed = set(line[len(label):].strip().strip('`').split('`, `'))
                    with self.subTest(language=language, kind=kind, part=part):
                        self.assertEqual(listed, template_files(kind, part))


if __name__ == '__main__':
    unittest.main()
