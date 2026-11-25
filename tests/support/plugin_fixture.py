"""Materialize filtered host files in isolation without archives or host registration."""
import importlib.util
from pathlib import Path
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Makefile').is_file())
def materialize(destination, host='codex'):
    spec = importlib.util.spec_from_file_location('fixture_engine', ROOT/'skills/_shared/templates/marketplace/sync/scripts/plugin_payload.py')
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    engine.ROOT = ROOT
    _, portable, claude = engine.payload()
    files = claude if host == 'claude' else engine.codex_payload(portable)
    for relative, content in files.items():
        path = Path(destination)/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return Path(destination)
