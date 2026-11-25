"""R4: finished skeleton pages are real Markdown files (templates/skeleton-docs), not a JSON with placeholders."""
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
SHARED = ROOT / 'skills/_shared'
sys.path.insert(0, str(SHARED / 'scripts'))
from docs_rules import OUTLINE  # noqa: E402


class SkeletonDocsTests(unittest.TestCase):
    def test_every_outline_page_exists_finished_with_only_the_title_placeholder(self):
        outline = OUTLINE['plugin']
        for template, headings in outline.items():
            if template.endswith(('/concepts.md', '/development.md')):  # managed pages (R36, R42)
                continue  # the managed page (R36), not part of the skeleton templates
            with self.subTest(page=template):
                text = (SHARED / 'templates/skeleton-docs' / template).read_text(encoding='utf-8')
                found = re.findall(r'\{\{[A-Z_0-9]+\}\}', text)
                if template.endswith('/installation.md'):  # filled from the facts of the repository (R35)
                    self.assertEqual({'{{PLUGIN_LABEL}}', '{{MARKETPLACE_URL}}', '{{PLUGIN_ID}}', '{{MARKETPLACE_NAME}}'}, set(found))
                else:
                    expected = ['{{TITLE}}'] if template.startswith('README') else ['{{SKILL_ROWS}}', '{{SKILL_SECTIONS}}'] if template.endswith('/skills.md') else []
                    self.assertEqual(expected, found)
                self.assertEqual(headings, re.findall(r'^## (.+)$', text, re.M))

    def test_json_content_file_is_gone_and_no_page_is_unlisted(self):
        self.assertFalse((SHARED / 'templates/skeleton-content.json').exists())
        outline = OUTLINE['plugin']
        found = {str(p.relative_to(SHARED / 'templates/skeleton-docs')) for p in (SHARED / 'templates/skeleton-docs').rglob('*.md')}
        self.assertEqual({page for page in outline if not page.endswith(('/concepts.md', '/development.md'))}, found)

    def test_each_kind_has_a_template_for_every_page_of_its_outline(self):  # R34
        outline = OUTLINE
        self.assertEqual({'plugin', 'marketplace'}, set(outline))
        self.assertNotIn('docs/en/skills.md', outline['marketplace'])
        self.assertIn('docs/en/plugins.md', outline['marketplace'])
        for kind, pages in outline.items():
            found = {str(p.relative_to(SHARED / 'templates/documentation' / kind)) for p in (SHARED / 'templates/documentation' / kind).rglob('*.md')}
            self.assertEqual({page for page in pages if not page.endswith(('/concepts.md', '/development.md'))}, found, kind)
            for page in pages:
                if page.endswith(('/concepts.md', '/development.md')):
                    self.assertTrue((SHARED / 'templates' / kind / 'sync' / page).is_file(), (kind, page))


if __name__ == '__main__':
    unittest.main()
