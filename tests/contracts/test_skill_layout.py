"""R52: every skill file of the Manager is built the same way."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SECTIONS = ['Read first', 'Start', 'Steps', 'Boundaries', 'Messages']


class SkillLayout(unittest.TestCase):
    def test_title_and_sections_are_the_same_in_every_skill(self):
        for path in sorted((ROOT / 'skills').glob('*/SKILL.md')):
            name = path.parent.name
            body = path.read_text(encoding='utf-8').split('---\n', 2)[2]
            with self.subTest(skill=name):
                self.assertEqual([f'# {name} (`/plugin-manager:{name}`)'], re.findall(r'^# .+$', body, re.M))
                self.assertEqual(SECTIONS, re.findall(r'^## (.+)$', body, re.M))


if __name__ == '__main__':
    unittest.main()
