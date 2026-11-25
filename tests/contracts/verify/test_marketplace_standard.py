"""R41: every marketplace has the same managed SCOPE.md; verify reports deviations, and its review is complete."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
TEMPLATES = ROOT / 'skills/_shared/templates/marketplace'
sys.path.insert(0, str(ROOT / 'skills/_shared/scripts'))
import workflows as flow
import verify

STANDARD = 'SCOPE.md'


class MarketplaceStandardTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.market = Path(temp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.market)], check=True)
        subprocess.run(['git', '-C', str(self.market), 'remote', 'add', 'origin', 'https://github.com/example/catalog.git'], check=True)
        flow.create_marketplace(self.market, 'fictional-market', 'Fictional Market', 'Fictional Publisher')

    def assert_finding(self, text):
        report = verify.verify(self.market)
        self.assertFalse(report['valid'], report)
        self.assertIn(text, report['errors'][0])

    def test_a_new_marketplace_has_the_managed_files_and_is_valid(self):
        for path in (STANDARD, 'AGENTS.md'):
            self.assertEqual((TEMPLATES / 'sync' / path).read_bytes(), (self.market / path).read_bytes())
        self.assertTrue((self.market / 'CUSTOM.AGENTS.md').is_file())
        agents = (self.market / 'AGENTS.md').read_text()
        self.assertIn('@CUSTOM.AGENTS.md\n@' + STANDARD, agents)
        self.assertNotIn('skills/<skill>', agents)
        report = verify.verify(self.market)
        self.assertTrue(report['valid'], report)

    def test_a_missing_or_changed_standard_or_agents_file_is_a_finding(self):
        for path, expected in ((STANDARD, STANDARD), ('AGENTS.md', 'AGENTS.md')):
            original = (self.market / path).read_bytes()
            (self.market / path).write_bytes(original + b'Own addition.\n')
            self.assert_finding(expected + ' differs')
            (self.market / path).unlink()
            self.assert_finding(expected + ' is missing')
            (self.market / path).write_bytes(original)

    def test_standard_text_copied_into_an_own_file_is_a_finding(self):
        line = next(line for line in (self.market / STANDARD).read_text().splitlines() if len(line) >= 60)
        for name in ('CUSTOM.AGENTS.md',):
            original = (self.market / name).read_text()
            (self.market / name).write_text(original + line + '\n')
            self.assert_finding(name + ' copies standard text')
            (self.market / name).write_text(original)

    def test_the_review_of_a_new_marketplace_has_no_findings(self):
        review = verify.scope_review(self.market)
        self.assertEqual([], review['findings'])
        self.assertEqual(['R1', 'R2', 'R3', 'R4'], [item['id'] for item in review['requirements']])

    def test_the_copy_inside_the_marketplace_compares_with_the_committed_lock(self):  # as in its CI
        lock = self.market / '.project/plugins/plugin-manager/skeleton.json'
        lock.parent.mkdir(parents=True, exist_ok=True)
        manifest = json.loads((ROOT / 'skills/_shared/manifests/marketplace.sync.json').read_text())
        lock.write_text(json.dumps({'files': {path: {'source_hash': manifest['files'][path]['sha256']}
                                              for path in (STANDARD, 'AGENTS.md')}}))
        def run():
            return subprocess.run([sys.executable, '-B', 'scripts/verify.py'], cwd=self.market, capture_output=True, text=True)
        self.assertEqual(0, run().returncode, run().stdout)
        (self.market / STANDARD).write_text('changed\n')
        self.assertIn('differs', run().stdout)


if __name__ == '__main__':
    unittest.main()
