#!/usr/bin/env python3
"""Inspect skill sources and scaffold/validate evidence-based GitHub documentation.

This helper never generates factual claims or executes the input skill.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify.docs import (FORMER_PAGES, KINDS, MANAGED_PAGES, SECTION_LABELS, anchors, check_policy, kind_of,  # noqa: E402,F401
                        language_policy, outline, page_layout, read_manifest, repository_address, safe_target, slug, strict_json, validate)

SKILL = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL / 'templates'


def one_line(text):
    return ' '.join(str(text).split()).replace('|', '\\|')


def skills_info(skills):
    """[(name, description)] from the frontmatter of each skill directory, in the order of the directories."""
    result = []
    for skill in skills:
        text = (Path(skill) / 'SKILL.md').read_text(encoding='utf-8')
        front = text.split('---', 2)[1] if text.startswith('---') and text.count('---') >= 2 else ''
        found = {key: re.search('^' + key + r':\s*(.+)$', front, re.MULTILINE) for key in ('name', 'description')}
        name = found['name'].group(1).strip().strip('"\'') if found['name'] else Path(skill).name
        description = found['description'].group(1).strip().strip('"\'') if found['description'] else ''
        result.append((name, description))
    return result


def plugins_info(root):
    """[(name, description, link)] of the plugins a marketplace lists."""
    data = strict_json((Path(root) / 'marketplace.json').read_text(encoding='utf-8'))
    result = []
    for entry in data.get('plugins', []):
        link = entry.get('repository') or entry.get('homepage') or ''
        if not link and isinstance(entry.get('source'), dict):
            link = entry['source'].get('url', '')
        result.append((entry.get('name', ''), entry.get('description', ''), link))
    return result


def skill_page(skill, number, policy, language, base=None, text=None):
    """The subpage of one skill; `text` fills its sections, else placeholders to author."""
    page = ((base or TEMPLATES / 'documentation' / 'plugin') / 'docs' / language / 'skill.md').read_text(encoding='utf-8')
    if len(policy['languages']) == 1:
        page = '\n'.join(line for line in page.split('\n') if not ('Deutsch' in line and 'English' in line and ' | ' in line))
    if policy['default_language'] == 'en':
        page = page.replace('(../../../README.en.md)', '(../../../__EN__)').replace('(../../../README.md)', '(../../../README.de.md)').replace('__EN__', 'README.md')
    page = page.replace('{{SKILL_NAME}}', skill)
    for part in range(1, len(SECTION_LABELS[language]) + 1):
        page = page.replace('{{SECTION_%d}}' % part, text or '{{SKILL_%d_%d}}' % (number, part))
    return page


def origin_of(folder):
    """The GitHub address of the origin of a checkout, or None (read-only)."""
    if not Path(folder).is_dir():
        return None
    try:
        out = subprocess.run(['git', '-C', str(folder), 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, check=False)
    except OSError:
        return None
    return repository_address(out.stdout) if out.returncode == 0 else None


def local_json(path):
    try:
        data = strict_json(Path(path).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def installation_facts(root, recorded=None, marketplace=None):
    """What the installation page states (R35): marketplace address and name, plugin id and label; None where unknown.
    The address is the recorded one, else the origin of the marketplace checkout (a plugin: the associated or given one;
    a marketplace: its own). Nothing is invented."""
    root = Path(root)
    facts = {'url': repository_address(recorded), 'market': None, 'id': None, 'label': None}
    if kind_of(root) == 'marketplace':
        facts['market'] = local_json(root / 'marketplace.json').get('name')
        facts['url'] = facts['url'] or origin_of(root)
        facts['id'] = '<plugin>@' + facts['market'] if facts['market'] else None
        facts['label'] = None
        return facts
    manifest = local_json(root / 'plugin.json')
    name = manifest.get('name')
    interface = manifest.get('extensions', {}).get('com.openai', {}) if isinstance(manifest.get('extensions'), dict) else {}
    facts['label'] = (interface.get('interface') or {}).get('displayName') or name
    for config in sorted((root / '.project/plugins').glob('*/config.json')):
        identity = local_json(config).get('marketplace')
        if isinstance(identity, dict) and identity.get('name'):
            facts['market'] = identity['name']
            checkout = local_json(config.parent / 'local.json').get('marketplace_path')
            marketplace = marketplace or (root / checkout if checkout else None)
    if marketplace:
        facts['market'] = facts['market'] or local_json(Path(marketplace) / 'marketplace.json').get('name')
        facts['url'] = facts['url'] or origin_of(marketplace)
    facts['id'] = name + '@' + facts['market'] if name and facts['market'] else None
    return facts


def fill_installation(text, facts, language):
    """Replace the variables whose fact is known; an unknown one stays as a placeholder that validate reports."""
    marketplace_text = {'de': 'das gewünschte Plugin', 'en': 'the plugin you want'}[language]
    values = {'MARKETPLACE_URL': facts.get('url'), 'MARKETPLACE_NAME': facts.get('market'), 'PLUGIN_ID': facts.get('id'),
              'PLUGIN_LABEL': facts.get('label') or (marketplace_text if facts.get('id', '') and facts['id'].startswith('<plugin>@') else None)}
    for key, value in values.items():
        if value:
            text = text.replace('{{' + key + '}}', value)
    return text


def fill_listings(text, language, skills=(), plugins=(), section_text=None):
    text = text.replace('{{SKILL_ROWS}}', '\n'.join('| [%s](skills/%s.md) | %s |' % (name, name, one_line(description)) for name, description in skills))
    text = text.replace('{{SKILL_FEATURES}}', '\n\n'.join('### :%s\n\n%s\n\n📖 [:%s – %s](docs/%s/skills/%s.md)' % (
        name, section_text or '{{FEATURE_%d}}' % number, name, {'de': 'Mehr dazu', 'en': 'More'}[language], language, name)
        for number, (name, _) in enumerate(skills, 1)))
    return text.replace('{{PLUGIN_ROWS}}', '\n'.join('| %s | %s | %s |' % (one_line(name), one_line(description), '[' + name + '](' + link + ')' if link else '')
                                                    for name, description, link in plugins))


def template_text(template, policy, base=None, kind='plugin'):
    if template.endswith(MANAGED_PAGES):  # managed pages (R36, R42): identical in every repository of the kind, never varied
        page = (TEMPLATES / kind / 'sync' / template).read_text(encoding='utf-8')
        return page if len(policy['languages']) > 1 else '\n'.join(
            line for line in page.split('\n') if not ('Deutsch' in line and 'English' in line and ' | ' in line)).replace('\n\n\n', '\n\n')
    text = ((base or TEMPLATES / 'documentation' / kind) / template).read_text(encoding='utf-8')
    if len(policy['languages']) == 1:
        text = '\n'.join(line for line in text.split('\n') if not ('Deutsch' in line and 'English' in line and ' | ' in line))
    if policy['default_language'] == 'en':
        # Rewrite only root README links; localized guide filenames remain stable.
        text = text.replace('(README.en.md)', '(__EN_ROOT__)').replace('(README.md)', '(README.de.md)') if template.startswith('README') else text.replace('(../../README.en.md)', '(../../__EN_ROOT__)').replace('(../../README.md)', '(../../README.de.md)')
        text = text.replace('__EN_ROOT__', 'README.md')
    return text


def source_skills(source):
    """Every skill directory the documentation reads: the skill folder itself when `source` is a standalone skill,
    else all skills of the repository (skills/*/SKILL.md). Documentation is never tied to one skill."""
    root = Path(source).expanduser().resolve()
    if not root.is_dir():
        raise ValueError('Source must be an accessible local directory')
    if any((root / old).exists() or (root / old).is_symlink() for old in ('.claude/skills', '.agents/skills')):
        raise ValueError('Unsupported source layout: repository skills must be under skills/')
    read_manifest(root)
    if (root / 'SKILL.md').is_file():
        if any((root / name).exists() for name in ('plugin.json', 'marketplace.json')):
            raise ValueError('Unsupported root SKILL.md in product repository; use skills/')
        if (root / 'SKILL.md').read_text(encoding='utf-8').startswith('---\n'):
            return [root]
        raise ValueError('Unsupported root SKILL.md pointer; select a current skill directory')
    found = []
    for path in sorted((root / 'skills').glob('*/SKILL.md')):
        resolved = path.parent.resolve()
        if path.parent.is_symlink() or not resolved.is_relative_to((root / 'skills').resolve()):
            raise ValueError('Unsupported source layout: symlink source pointer')
        if resolved not in found:
            found.append(resolved)
    if not found:
        raise ValueError('No skill found: a repository needs skills/<name>/SKILL.md')
    return found


EVIDENCE_FOLDERS = ('references', 'flows', 'scripts')
EVIDENCE_SUFFIXES = ('.md', '.py', '.sh', '.json', '.yaml', '.yml')


# what a marketplace has instead of skills; the files that exist are its documentation sources
MARKETPLACE_SOURCES = ('marketplace.json', 'SCOPE.md', 'Makefile', 'CUSTOM.mk')


def inspect_marketplace(root):
    paths = [root / name for name in MARKETPLACE_SOURCES] + sorted((root / '.github/workflows').glob('*.y*ml'))
    evidence = [path.relative_to(root).as_posix() for path in paths
                if path.is_file() and not any((root / part).is_symlink() for part in (path.relative_to(root), *path.relative_to(root).parents))]
    data = strict_json((root / 'marketplace.json').read_text(encoding='utf-8'))
    return {'skills': [], 'name': data.get('name') or root.name, 'evidence_files': evidence, 'source_executed': False}


def inspect(source):
    root = Path(source).expanduser().resolve()
    if kind_of(root) == 'marketplace':
        return inspect_marketplace(root)
    skills = source_skills(root)
    standalone = skills == [root]
    base = root
    evidence = []
    for skill in skills:
        prefix = skill.relative_to(base)
        evidence.append(str(prefix / 'SKILL.md') if not standalone else 'SKILL.md')
        for folder in EVIDENCE_FOLDERS:
            if not (skill / folder).is_dir():
                continue
            for path in sorted((skill / folder).rglob('*')):
                relative = path.relative_to(skill)
                if (path.is_file() and not path.is_symlink()
                        and not any(part.startswith('.') or part == '__pycache__' for part in relative.parts)
                        and path.suffix in EVIDENCE_SUFFIXES):
                    evidence.append(str(relative) if standalone else str(prefix / relative))
    if not standalone and (root / 'SCOPE.md').is_file() and not (root / 'SCOPE.md').is_symlink():
        evidence.append('SCOPE.md')  # the goal of the plugin is a documentation source too
    name = skills[0].name
    if standalone:
        match = re.search(r'^name:\s*(.+)$', (root / 'SKILL.md').read_text(encoding='utf-8'), re.MULTILINE)
        name = match.group(1).strip('"\'') if match else root.name
    elif (root / 'plugin.json').is_file():
        try:
            name = strict_json((root / 'plugin.json').read_text(encoding='utf-8')).get('name') or root.name
        except (ValueError, OSError, AttributeError):
            name = root.name
    else:
        name = root.name if len(skills) > 1 else skills[0].name
    return {'skills': [str(skill) for skill in skills], 'name': name, 'evidence_files': evidence, 'source_executed': False}


def scaffold(source, output, title=None, languages=None, default_language=None):
    root = Path(output).expanduser().resolve()
    source_root = Path(source).expanduser().resolve()
    kind = kind_of(source_root)
    skills, plugins = [], []
    if kind == 'marketplace':
        data = strict_json((source_root / 'marketplace.json').read_text(encoding='utf-8'))
        info = {'name': data.get('displayName') or data.get('name') or source_root.name, 'skills': []}
        plugins = plugins_info(source_root)
    else:
        info = inspect(source)
        skills = skills_info(info['skills'])
    if any(root.is_relative_to(Path(skill)) for skill in info['skills']):
        raise ValueError('Write documentation outside the distributable source skill')
    for skill in info['skills']:  # a skill inside the output repository must lie under skills/
        inside = Path(skill).relative_to(root).parts if Path(skill).is_relative_to(root) else None
        if inside is not None and (not inside or inside[0] != 'skills' or '..' in inside):
            raise ValueError('Unsupported source layout: repository skills must be under skills/')
    plans = []
    manifest_path = safe_target(root, 'docs/documentation.json')
    manifest = read_manifest(root)
    policy = language_policy(root, languages, default_language)
    facts = installation_facts(source_root, (manifest or {}).get('marketplace_url'))
    if not manifest:
        manifest = {'schema_version': 1, 'extra_sources': [], 'open_questions': [], 'documentation': policy}
        if facts['url']:
            manifest['marketplace_url'] = facts['url']
        plans.append((manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()))
    for name, (template, _, language) in page_layout(policy, kind).items():
        target = safe_target(root, name)
        if target.exists() and not target.is_file():
            raise ValueError(f'Expected a file: {target}')
        if not target.exists():
            text = template_text(template, policy, kind=kind)
            text = fill_listings(text.replace('{{TITLE}}', title or info['name']), language, skills, plugins)
            if name.endswith('/installation.md'):
                text = fill_installation(text, facts, language)
            plans.append((target, text.encode('utf-8')))
    for language in policy['languages'] if kind == 'plugin' else ():
        for number, (name, _) in enumerate(skills, 1):
            target = safe_target(root, f'docs/{language}/skills/{name}.md')
            if not target.exists():
                plans.append((target, skill_page(name, number, policy, language).encode('utf-8')))
    for target, content in plans:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(content)
    return {'created': [str(p.relative_to(root)) for p, _ in plans],
            'existing_pages_preserved': True,
            'missing_facts': sorted(key for key in ('url', 'market', 'id') if not facts.get(key)),
            'next': 'Author evidence-based content, replace placeholders, then validate. Scaffold is not finished documentation.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    scan = sub.add_parser('inspect')
    scan.add_argument('--source', type=Path, required=True)
    create = sub.add_parser('scaffold')
    create.add_argument('--source', type=Path, required=True)
    create.add_argument('--output', type=Path, required=True)
    create.add_argument('--title')
    create.add_argument('--languages', nargs='+', choices=('de','en'))
    create.add_argument('--default-language', choices=('de','en'))
    verify = sub.add_parser('validate')
    verify.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'inspect':
            result = inspect(args.source)
        elif args.command == 'scaffold':
            result = scaffold(args.source, args.output, args.title, args.languages, args.default_language)
        else:
            errors = validate(args.output)
            result = {'valid': not errors, 'errors': errors,
                      'scope': 'Structure, branding and local links only; content and host claims require review.'}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return int(bool(errors))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
