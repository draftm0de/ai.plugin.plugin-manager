"""R51: one script per check; make, CI and the pre-commit hook call the same ones; the copies are identical."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = ROOT / 'skills/_shared/templates'
CHECKS = {'plugin': ['structure', 'standards', 'conventions', 'docs', 'hashes'], 'marketplace': ['structure', 'standards', 'docs']}


def called(path):
    return re.findall(r'scripts/verify/(\w+)\.py', path.read_text(encoding='utf-8'))


class CheckScripts(unittest.TestCase):
    def test_make_ci_and_pre_commit_call_the_same_checks_of_their_kind(self):
        for kind, names in CHECKS.items():
            base = TEMPLATES / kind / 'sync'
            with self.subTest(kind=kind):
                self.assertEqual(names + ['scope'], called(base / 'Makefile'))
                self.assertEqual(names, called(base / '.github/workflows/dm-verify.yml'))
        self.assertEqual(CHECKS['plugin'], called(TEMPLATES / 'plugin/sync/githooks/pre-commit'))

    def test_every_delivered_script_is_identical_to_the_manager_runtime(self):
        for kind in CHECKS:
            folder = TEMPLATES / kind / 'sync/scripts/verify'
            names = sorted(p.name for p in folder.glob('*.py'))
            self.assertEqual(sorted(n + '.py' for n in CHECKS[kind] + ['common', 'scope']), names)
            for name in names:
                runtime = (ROOT / 'skills/_shared/scripts/verify' / name).read_bytes()
                with self.subTest(kind=kind, script=name):
                    self.assertEqual(runtime, (folder / name).read_bytes())
                    self.assertEqual(runtime, (ROOT / 'scripts/verify' / name).read_bytes())
        self.assertEqual((ROOT / 'scripts/build_hashes.py').read_bytes(), (TEMPLATES / 'plugin/sync/scripts/build_hashes.py').read_bytes())


if __name__ == '__main__':
    unittest.main()
