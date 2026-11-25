"""R37, R47: the verify copy a repository runs in CI checks the documentation structure and the sync hash files."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

R = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
sys.path.insert(0, str(R / 'skills/_shared/scripts'))
import verify  # noqa: E402


class DocumentationCheck(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()

    def test_without_selected_languages_nothing_is_checked_and_the_result_says_so(self):
        self.assertEqual('not_created', verify.documentation(self.root))

    def test_with_selected_languages_missing_pages_are_findings(self):
        (self.root / 'docs').mkdir()
        (self.root / 'docs/documentation.json').write_text(json.dumps(
            {'schema_version': 1, 'documentation': {'languages': ['en'], 'default_language': 'en'}}))
        with self.assertRaisesRegex(ValueError, 'docs/en/development.md: missing page'):
            verify.documentation(self.root)

    def test_the_copy_in_a_repository_works_without_the_manager_and_writes_nothing(self):
        (self.root / 'scripts').mkdir()
        for name in ('verify.py', 'docs_rules.py'):
            shutil.copyfile(R / 'scripts' / name, self.root / 'scripts' / name)
        code = "import sys; sys.path.insert(0, 'scripts'); import verify, pathlib; print(verify.documentation(pathlib.Path.cwd()))"
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=self.root, capture_output=True, text=True)
        self.assertEqual('not_created\n', result.stdout, result.stderr)
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
        self.write({'rules.md': {'sha256': hashlib.sha256(b'fictional\n').hexdigest(), 'executable': False}})

    def write(self, files, removed=()):
        (self.base / 'manifests/thing.sync.json').write_text(
            json.dumps({'schema_version': 1, 'files': files, 'removed': list(removed)}))

    def finds(self, text):
        with self.assertRaisesRegex(ValueError, text):
            verify.template_hashes(self.root)

    def test_matching_hash_files_pass_and_a_plugin_without_sync_templates_is_untouched(self):
        verify.template_hashes(self.root)
        shutil.rmtree(self.base)
        (self.root / 'skills/other/templates/site').mkdir(parents=True)  # templates without sync/ are not sync structures
        verify.template_hashes(self.root)

    def test_a_changed_template_is_a_finding(self):
        self.template.write_text('changed\n')
        self.finds('rules.md differs from its hash')

    def test_an_unlisted_and_a_missing_file_are_findings(self):
        (self.template.parent / 'new.md').write_text('x')
        self.finds('does not list new.md')
        (self.template.parent / 'new.md').unlink()
        self.template.unlink()
        self.finds('lists the missing file rules.md')

    def test_a_missing_hash_file_is_a_finding(self):
        (self.base / 'manifests/thing.sync.json').unlink()
        self.finds('thing.sync.json is missing')

    def test_the_hash_files_of_the_manager_fit(self):
        verify.template_hashes(R)


if __name__ == '__main__':
    unittest.main()
