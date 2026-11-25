"""R34: the start page of a plugin has a short, linked Features entry for every skill."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
from verify import docs  # noqa: E402


def page(text='Counts fictional things.', link='docs/en/skills/count.md', title=':count'):
    return f'# Demo\n\n## Features\n\n### {title}\n\n{text}\n\n[More]({link})\n\n## Documentation\n'


class Features(unittest.TestCase):
    def errors(self, text, skills=('count',)):
        return ' '.join(docs.feature_errors('README.md', text, list(skills), 'en'))

    def test_a_short_linked_entry_per_skill_passes(self):
        self.assertEqual('', self.errors(page()))
        self.assertEqual('', self.errors(page('x' * docs.FEATURE_LIMIT)))  # the link line does not count

    def test_findings(self):
        self.assertIn('lacks the entry ### :other', self.errors(page(), ('count', 'other')))
        self.assertIn('no skill of the plugin', self.errors(page(title=':gone', link='docs/en/skills/gone.md')))
        self.assertIn('201 characters', self.errors(page('x' * (docs.FEATURE_LIMIT + 1))))
        self.assertIn('needs a link', self.errors(page(link='docs/en/installation.md')))
        self.assertIn('no explanation', self.errors(page('')))


if __name__ == '__main__':
    unittest.main()
