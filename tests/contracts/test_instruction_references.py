"""R52: instructions name only scripts that exist, and a skill does not carry the rules of another one."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SHARED = ROOT / 'skills/_shared'
SCRIPT = re.compile(r'[\w./<>{},-]*\.py\b')


def instruction_files():
    # seed templates show examples for a new repository; the managed standards are checked through their copy in docs/
    return sorted([*(path for path in (ROOT / 'skills').rglob('*.md') if 'templates' not in path.parts), *(ROOT / 'docs/standards').glob('*.md'),
                   *(path for path in (ROOT / 'AGENTS.md', ROOT / 'CUSTOM.AGENTS.md') if path.is_file())])


def exists(name, file):
    name = name.replace('<plugin-root>/', '')
    if '<' in name or '{' in name or name.startswith('/path/to/'):
        return True  # a placeholder, not a file name
    if '/' not in name:
        return any((ROOT / 'skills').rglob(name)) or any((ROOT / 'scripts').rglob(name))
    bases = [file.parent, *file.parent.parents[:2], SHARED, ROOT, SHARED / 'templates/plugin/sync', SHARED / 'templates/marketplace/sync']
    return any((base / name).is_file() for base in bases)


class InstructionReferences(unittest.TestCase):
    def test_every_named_script_exists(self):
        missing = [f'{file.relative_to(ROOT)}: {name}' for file in instruction_files()
                   for name in sorted(set(SCRIPT.findall(file.read_text(encoding='utf-8')))) if not exists(name, file)]
        self.assertEqual([], missing)

    def test_a_removed_script_is_found(self):
        self.assertFalse(exists('scripts/verify.py', SHARED / 'WORKFLOWS.md'))

    def test_the_shared_file_holds_no_rules_of_a_single_action(self):
        shared = (SHARED / 'WORKFLOWS.md').read_text(encoding='utf-8')
        for own in ('--dry-run', 'catalog_entry_remains', 'scaffold --source', 'verify/structure.py'):
            self.assertNotIn(own, shared)


if __name__ == '__main__':
    unittest.main()
