"""R37, R47: the scripts a repository runs in CI check the documentation structure and the sync hash files."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

R = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
sys.path.insert(0, str(R / 'skills/_shared/scripts'))
from verify import docs, hashes  # noqa: E402


class DocumentationCheck(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()

    def test_without_selected_languages_nothing_is_checked_and_the_result_says_so(self):
        result = docs.check(self.root)
        self.assertEqual((True, 'not_created'), (result['valid'], result['documentation']))

    def test_with_selected_languages_missing_pages_are_findings(self):
        (self.root / 'docs').mkdir()
        (self.root / 'docs/documentation.json').write_text(json.dumps(
            {'schema_version': 1, 'documentation': {'languages': ['en'], 'default_language': 'en'}}))
        result = docs.check(self.root)
        self.assertTrue(result['valid'])  # findings are warnings, never a failure
        self.assertIn('docs/en/development.md: missing page', result['warnings'])
        for actions, annotated in (('true', True), ('', False)):  # captured: a test must not annotate the real CI run
            output = io.StringIO()
            with patch.dict(os.environ, {'GITHUB_ACTIONS': actions}), contextlib.redirect_stdout(output):
                self.assertEqual(0, docs.main(['--source', str(self.root)]))
            self.assertEqual(annotated, '::warning::docs/en/development.md: missing page' in output.getvalue())
        self.assertIn('"Example" is still to be written: one fictional example',
                      ' '.join(docs.open_sections('docs/en/skills/x.md', '## Example\n\n{{SKILL_1_3}}\n', 'en')))

    def test_the_copy_in_a_repository_runs_without_the_manager_and_writes_nothing(self):
        shutil.copytree(R / 'scripts/verify', self.root / 'scripts/verify', ignore=shutil.ignore_patterns('__pycache__'))
        result = subprocess.run([sys.executable, '-B', 'scripts/verify/docs.py'], cwd=self.root, capture_output=True, text=True)
        self.assertEqual((0, 'not_created'), (result.returncode, json.loads(result.stdout)['documentation']), result.stderr)
        self.assertEqual([], list(self.root.rglob('__pycache__')))


class TemplateHashCheck(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.base = self.root / 'skills/fictional'
        (self.base / 'templates/thing/sync').mkdir(parents=True)
        (self.base / 'manifests').mkdir()
        self.template = self.base / 'templates/thing/sync/rules.md'
        self.template.write_text('fictional\n')
        self.write({'rules.md': {'sha256': hashlib.sha256(b'fictional\n').hexdigest(), 'executable': False}})  # canonical form

    def write(self, files, removed=()):
        (self.base / 'manifests/thing.sync.json').write_text(hashes.render(files, list(removed)))

    def finds(self, text):
        self.assertIn(text, ' '.join(hashes.check(self.root)))

    def test_matching_hash_files_pass_and_a_plugin_without_sync_templates_is_untouched(self):
        self.assertEqual([], hashes.check(self.root))
        shutil.rmtree(self.base)
        (self.root / 'skills/other/templates/site').mkdir(parents=True)  # templates without sync/ are not sync structures
        self.assertEqual([], hashes.check(self.root))

    def test_a_changed_template_is_a_finding(self):
        self.template.write_text('changed\n')
        self.finds('rules.md: hash differs')

    def test_an_unlisted_and_a_missing_file_are_findings(self):
        (self.template.parent / 'new.md').write_text('x')
        self.finds('new.md: in sync/ but not listed')
        (self.template.parent / 'new.md').unlink()
        self.template.unlink()
        self.finds('rules.md: listed but missing')

    def test_a_missing_hash_file_is_a_finding(self):
        (self.base / 'manifests/thing.sync.json').unlink()
        self.finds('thing.sync.json: missing')

    def test_the_hash_files_of_the_manager_fit(self):
        self.assertEqual([], hashes.check(R))


if __name__ == '__main__':
    unittest.main()
