"""The checks of scripts/verify/ as one package for the Manager's own skills and generator (not delivered to repositories,
which call the single scripts)."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import structure  # noqa: E402
from common import NAME, kind_of, read, safe, skeleton_marker, strict_json  # noqa: E402,F401
from conventions import conventions  # noqa: E402
from scope import scope_review  # noqa: E402,F401
from standards import STANDARDS, standards  # noqa: E402,F401
from structure import local_configuration, marketplace  # noqa: E402,F401


def plugin(root):
    """Structure, standards and conventions of one plugin."""
    result = structure.plugin(root)
    standards(root)
    conventions(root)
    return result


def verify(source, kind='auto'):
    def further(root, selected):
        standards(root, selected)
        if selected == 'plugin':
            conventions(root)
    return structure.verify(source, kind, also=(further,))
