"""The tests a marketplace receives are the ones that cover the marketplace scripts here: one source."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TEMPLATES = Path(__file__).resolve().parents[3] / 'skills/_shared/templates/marketplace'


class ManagedMarketplaceTests(unittest.TestCase):
    def test_the_managed_tests_pass_against_the_managed_scripts(self):  # R40
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            ignored = shutil.ignore_patterns('__pycache__')
            for source in ('sync/scripts', 'sync/tests'):
                shutil.copytree(TEMPLATES / source, root / source.split('/')[1], ignore=ignored)
            for package in ('tests/__init__.py', 'tests/contracts/__init__.py'):
                shutil.copy2(TEMPLATES / 'seed' / package, root / package)
            result = subprocess.run([sys.executable, '-B', str(root / 'scripts/run_tests.py')],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('Ran 16 tests', result.stderr)


if __name__ == '__main__':
    unittest.main()
