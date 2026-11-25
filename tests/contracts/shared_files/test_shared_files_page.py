"""R46: :docs generates "Shared files" with the trees of what the Manager delivers, and verify requires its headings."""
from pathlib import Path
import json
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
import documentation  # noqa: E402
from verify import docs  # noqa: E402

ORDER = (('plugin', 'sync'), ('plugin', 'seed'), ('marketplace', 'sync'), ('marketplace', 'seed'))


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
    def test_the_four_trees_hold_exactly_what_the_manager_delivers(self):
        for language in ('de', 'en'):
            text = (ROOT / 'docs' / language / 'files.md').read_text(encoding='utf-8')
            blocks = re.findall(r'(?s)```text\n(\.\n.*?)\n```', text)
            self.assertEqual(len(ORDER), len(blocks))
            for (kind, part), block in zip(ORDER, blocks):
                with self.subTest(language=language, kind=kind, part=part):
                    self.assertEqual(template_files(kind, part), tree_files(block))

    def test_the_committed_pages_are_what_docs_generates(self):
        policy = documentation.language_policy(ROOT)
        facts = documentation.installation_facts(ROOT, documentation.read_manifest(ROOT).get('marketplace_url'))
        for language, name in ((l, n) for l in policy['languages'] for n in documentation.GENERATED_PAGES['plugin']):
            if name == 'installation.md' and not all(facts.values()):
                continue  # a fresh clone lacks the local facts
            skills = [path.parent.name for path in sorted((ROOT / 'skills').glob('*/SKILL.md'))]
            generated = documentation.generated_page(policy, language, 'plugin', name, facts, root=ROOT, skills=skills)
            self.assertEqual(generated, (ROOT / 'docs' / language / name).read_text(encoding='utf-8'), name)
            self.assertIn('/plugin-manager:docs', generated.rstrip().split('\n')[-1])

    def test_a_generated_page_is_refreshed_and_a_changed_heading_is_a_finding(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'docs').mkdir()
            (root / 'docs/documentation.json').write_text(json.dumps(
                {'schema_version': 1, 'documentation': {'languages': ['de'], 'default_language': 'de'}}))
            self.assertEqual(['docs/de/installation.md', 'docs/de/skills.md', 'docs/de/concepts.md', 'docs/de/development.md', 'docs/de/files.md'], documentation.write_generated_pages(root))
            self.assertEqual([], documentation.write_generated_pages(root))
            page = root / 'docs/de/files.md'
            self.assertFalse([e for e in docs.validate(root) if e.startswith('docs/de/files.md: the headings')])
            page.write_text(page.read_text().replace('### Seed', '### Eigenes', 1))
            self.assertTrue([e for e in docs.validate(root) if e.startswith('docs/de/files.md: the headings')])
            self.assertEqual(['docs/de/files.md'], documentation.write_generated_pages(root))


if __name__ == '__main__':
    unittest.main()
