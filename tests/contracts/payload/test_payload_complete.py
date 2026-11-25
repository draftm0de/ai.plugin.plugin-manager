"""R44: what a host installs from the local development package holds every template of the Manager."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'skills/_shared/templates/marketplace/sync/scripts'))
import plugin_payload  # noqa: E402


class PayloadHoldsEveryTemplate(unittest.TestCase):
    def test_both_host_payloads_contain_every_template_file(self):
        expected = {path.relative_to(ROOT).as_posix() for path in (ROOT / 'skills/_shared/templates').rglob('*')
                    if path.is_file() and '__pycache__' not in path.parts
                    and path.name != '.gitattributes'}  # repository setting for the hashes, not a template
        previous = plugin_payload.ROOT
        self.addCleanup(setattr, plugin_payload, 'ROOT', previous)
        plugin_payload.ROOT = ROOT
        _, portable, claude = plugin_payload.payload()
        for host, files in (('claude', claude), ('codex', plugin_payload.codex_payload(portable))):
            with self.subTest(host=host):
                self.assertEqual(sorted(expected - set(files)), [])


if __name__ == '__main__':
    unittest.main()
