"""R49: inspect names the sources of a marketplace, which has no skills (fictional data)."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
import documentation  # noqa: E402


class InspectMarketplace(unittest.TestCase):
    def test_the_existing_files_of_a_marketplace_are_its_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / 'marketplace.json').write_text(json.dumps({'name': 'fictional', 'plugins': []}))
            for relative in ('SCOPE.md', 'Makefile', '.github/workflows/own.yml', 'README.md'):
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).write_text('x')
            (root / 'CUSTOM.mk').symlink_to(root / 'Makefile')  # a symlink is never a source
            result = documentation.inspect(root)
            self.assertEqual(('fictional', []), (result['name'], result['skills']))
            self.assertEqual(['marketplace.json', 'SCOPE.md', 'Makefile', '.github/workflows/own.yml'], result['evidence_files'])


if __name__ == '__main__':
    unittest.main()
