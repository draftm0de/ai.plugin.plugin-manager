"""R54: the documentation of a marketplace (fictional data)."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
import documentation  # noqa: E402


class MarketplaceDocs(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        (self.root / 'marketplace.json').write_text(json.dumps({'name': 'fictional-market', 'displayName': 'Fictional', 'plugins': [
            {'name': 'demo', 'displayName': 'Demo Plugin', 'description': 'Does fictional things.', 'repository': 'https://github.com/example/demo.git'}]}))
        (self.root / 'assets').mkdir()
        (self.root / 'assets/icon.png').write_bytes(b'x')
        (self.root / 'docs').mkdir()
        (self.root / 'docs/documentation.json').write_text(json.dumps({'schema_version': 1, 'extra_sources': [], 'open_questions': [],
            'documentation': {'languages': ['de', 'en'], 'default_language': 'de'}, 'marketplace_url': 'https://github.com/example/market'}))
        self.result = documentation.run(self.root, self.root)

    def pages(self):
        return sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*.md'))

    def test_four_pages_and_nothing_per_plugin(self):
        expected = ['README.en.md', 'README.md'] + [f'docs/{l}/{n}.md' for l in ('de', 'en') for n in ('concepts', 'development', 'installation')]
        self.assertEqual(sorted(expected), self.pages())
        readme = (self.root / 'README.md').read_text()
        self.assertIn('## 📦 Plugins\n\n### Demo Plugin\n\nDoes fictional things.\n\n📖 [Demo Plugin – Mehr dazu](https://github.com/example/demo#readme)', readme)
        install = (self.root / 'docs/de/installation.md').read_text()
        self.assertIn('Das installiert noch kein Plugin', install)
        self.assertNotIn('plugin install', install)
        for name in self.pages():
            self.assertNotIn('files.md', (self.root / name).read_text(), name)

    def test_only_the_introduction_is_open_and_a_former_page_or_missing_entry_is_a_warning(self):
        self.assertEqual({'README.md', 'README.en.md'}, {w.split(':')[0] for w in documentation.validate(self.root)})
        (self.root / 'docs/de/plugins.md').write_text('# old')
        readme = self.root / 'README.md'
        readme.write_text(readme.read_text().replace('### Demo Plugin', '### Anderes'))
        found = ' '.join(documentation.validate(self.root))
        self.assertIn('docs/de/plugins.md: page of the former structure', found)
        self.assertIn('lacks the entry ### Demo Plugin', found)

    def test_a_new_marketplace_receives_a_start_page_in_the_expected_structure(self):
        import workflows
        for language, name in (('de', 'README.md'), ('en', 'README.en.md')):
            (self.root / name).write_text(workflows.marketplace_start_page(language, name, 'Fictional', []))
        self.assertEqual([], [w for w in documentation.validate(self.root) if w.startswith('README') and 'lacks the entry' not in w])


if __name__ == '__main__':
    unittest.main()
