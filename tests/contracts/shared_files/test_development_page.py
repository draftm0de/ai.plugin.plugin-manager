"""R48: the managed development pages name every command, variable and CI step of their kind."""
from pathlib import Path
import re
import unittest

TEMPLATES = Path(__file__).resolve().parents[3] / 'skills/_shared/templates'


class DevelopmentPage(unittest.TestCase):
    def test_every_make_target_variable_and_ci_step_is_described(self):
        for kind in ('plugin', 'marketplace'):
            makefile = (TEMPLATES / kind / 'sync/Makefile').read_text(encoding='utf-8')
            targets = re.search(r'^\.PHONY: (.+)$', makefile, re.M).group(1).split()
            variables = set(re.findall(r'^(\w+) \?=', makefile, re.M)) - {'PYTHON'}
            variables |= set(re.findall(r'\$\(filter 1,\$\((\w+)\)\)', makefile))
            workflow = (TEMPLATES / kind / 'sync/.github/workflows/dm-verify.yml').read_text(encoding='utf-8')
            steps = re.findall(r'^\s*- run: (.+)$', workflow, re.M)
            self.assertTrue(targets and variables and steps)
            for language in ('de', 'en'):
                page = (TEMPLATES / kind / 'sync/docs' / language / 'development.md').read_text(encoding='utf-8')
                with self.subTest(kind=kind, language=language):
                    self.assertEqual([], [t for t in targets if f'| `make {t}` |' not in page])
                    self.assertEqual([], [v for v in sorted(variables) if not re.search('`' + v + '[=`]', page)])
                    self.assertEqual([], [s for s in steps if f'| `{s}` |' not in page])
                    self.assertEqual(len(steps), len(re.findall(r'^\| `python3 ', page, re.M)))  # no step that CI no longer runs


if __name__ == '__main__':
    unittest.main()
