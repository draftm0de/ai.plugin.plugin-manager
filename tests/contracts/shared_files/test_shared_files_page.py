"""R46: the Manager's documentation shows every shared file of both kinds, with its class, as a tree."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
HEADINGS = {'de': {'plugin': '## Dateien und Ordner eines Plugins', 'marketplace': '## Dateien und Ordner eines Marketplace'},
            'en': {'plugin': '## Files and folders of a plugin', 'marketplace': '## Files and folders of a marketplace'}}
LABELS = {'de': {'sync': '### Sync', 'seed': '### Seed'}, 'en': {'sync': '### Synced', 'seed': '### Seed'}}


def template_files(kind, part):
    base = ROOT / 'skills/_shared/templates' / kind / part
    names = set()
    for path in base.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            name = path.relative_to(base).as_posix().replace('docs/de/', 'docs/<lang>/').replace('docs/en/', 'docs/<lang>/')
            names.add('.gitignore' if name == 'gitignore.txt' else name)
    return names


def tree_files(block):
    stack, files = [], set()
    for line in block.split('\n')[1:]:  # the first line is the root "."
        match = re.match(r'^((?:[│ ]   )*)[├└]── (.+)$', line)
        depth, name = len(match[1]) // 4, match[2]
        del stack[depth:]
        stack.append(name.rstrip('/'))
        if not name.endswith('/'):
            files.add('/'.join(stack))
    return files


class SharedFilesPage(unittest.TestCase):
    def test_every_file_of_both_kinds_is_in_its_tree(self):
        for language, headings in HEADINGS.items():
            text = (ROOT / 'docs' / language / 'files.md').read_text(encoding='utf-8')
            for kind, heading in headings.items():
                section = text.split(heading + '\n', 1)[1].split('\n## ', 1)[0]
                for part, label in LABELS[language].items():
                    block = section.split(label + '\n\n```text\n', 1)[1].split('\n```', 1)[0]
                    with self.subTest(language=language, kind=kind, part=part):
                        self.assertEqual(template_files(kind, part), tree_files(block))


if __name__ == '__main__':
    unittest.main()
