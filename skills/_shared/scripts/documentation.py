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
from verify.docs import (FORMER_PAGES, KINDS, SECTION_LABELS, anchors, check_policy, kind_of,  # noqa: E402,F401
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
        result.append((entry.get('displayName') or entry.get('name', ''), entry.get('description', ''), link))
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


def file_tree(paths):
    root = {}
    for path in paths:
        node = root
        for part in path.split('/'):
            node = node.setdefault(part, {})
    lines = ['.']
    def walk(node, prefix):
        entries = sorted(node, key=lambda name: (not node[name], name.lower()))  # folders first
        for index, name in enumerate(entries):
            last = index == len(entries) - 1
            lines.append(prefix + ('└── ' if last else '├── ') + name + ('/' if node[name] else ''))
            walk(node[name], prefix + ('    ' if last else '│   '))
    walk(root, '')
    return '```text\n' + '\n'.join(lines) + '\n```'


def shared_files(kind, part):
    """The files a kind receives: `sync` from its hash file, `seed` from its folder; languages as <lang>."""
    if part == 'sync':
        names = strict_json((SKILL / 'manifests' / (kind + '.sync.json')).read_text(encoding='utf-8'))['files']
    else:
        base = TEMPLATES / kind / 'seed'
        names = [path.relative_to(base).as_posix() for path in base.rglob('*') if path.is_file() and '__pycache__' not in path.parts]
    return {'.gitignore' if name == 'gitignore.txt' else re.sub(r'^docs/(de|en)/', 'docs/<lang>/', name) for name in names}


# written anew by docs; the installation page of a plugin also carries the facts of its repository (R35)
GENERATED_PAGES = {'plugin': ('installation.md', 'skills.md', 'concepts.md', 'development.md', 'files.md'),
                   'marketplace': ('installation.md', 'concepts.md', 'development.md')}


def description_of(page, language):
    """The text of the section "Description" of a skill page up to the first sub-heading, with links as seen from skills.md."""
    section = re.split(r'(?m)^## %s$' % SECTION_LABELS[language][0], page, maxsplit=1)
    if len(section) != 2:
        return ''
    text = re.split(r'(?m)^(?:##|###) |^---$|^<hr>$', section[1], maxsplit=1)[0].strip()
    return re.sub(r'\]\((?!https?:|#|\.\./)', '](skills/', text).replace('](../', '](')


def skill_entries(root, language, plugin, skills):
    """One entry per skill: heading, call, its description and the link to its page. A plugin with one skill is called bare."""
    entries = []
    for number, name in enumerate(skills, 1):
        page = safe_target(root, f'docs/{language}/skills/{name}.md')
        text = description_of(page.read_text(encoding='utf-8'), language) if page.is_file() else ''
        call = f'/{plugin}' if len(skills) == 1 else f'/{plugin}:{name}'
        more = {'de': 'Mehr dazu', 'en': 'More'}[language]
        entries.append(f'### {name}\n\n`{call}`\n\n{text or "{{SKILL_%d_1}}" % number}\n\n📖 [{call} – {more}](skills/{name}.md)')
    return '\n\n'.join(entries)


def generated_page(policy, language, kind, name, facts=None, unknown=False, root=None, skills=()):
    """A page docs creates itself: fixed text per kind; "Shared files" also gets the trees of what the Manager delivers, the
    installation page the facts. A missing fact stays a placeholder (verify reports it) unless `unknown` states it as open."""
    page = template_text(f'docs/{language}/{name}', policy, kind=kind)
    if name == 'skills.md':
        manifest = local_json(root / 'plugin.json')
        plugin = manifest.get('name') or root.name
        label = (facts or {}).get('label') or plugin
        page = page.replace('{{PLUGIN_LABEL}}', label).replace('{{SKILL_ENTRIES}}', skill_entries(root, language, plugin, skills))
    if name == 'installation.md':
        page = fill_installation(page, facts or {}, language)
        if unknown:
            page = re.sub(r'\{\{[A-Z_]+\}\}', {'de': '(noch nicht festgelegt)', 'en': '(not set yet)'}[language], page)
    for name in ('plugin', 'marketplace'):
        for part in ('sync', 'seed'):
            page = page.replace('{{%s_%s_TREE}}' % (name.upper(), part.upper()), file_tree(shared_files(name, part)))
    return page


def write_generated_pages(output, policy=None, facts=None, unknown=False, skills=None):
    """Create or refresh the generated pages in every selected language; returns the files written."""
    root = Path(output).expanduser().resolve()
    policy = policy or language_policy(root)
    kind = kind_of(root)
    facts = facts or installation_facts(root, (read_manifest(root) or {}).get('marketplace_url'))
    if skills is None:
        skills = [name for name, _ in skills_info(sorted(p.parent for p in (root / 'skills').glob('*/SKILL.md')))] if kind == 'plugin' else []
    written = []
    for language in policy['languages']:
        for number, skill in enumerate(skills, 1):  # a missing page of a skill is created once and then belongs to the person
            target = safe_target(root, f'docs/{language}/skills/{skill}.md')
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(skill_page(skill, number, policy, language), encoding='utf-8')
                written.append(str(target.relative_to(root)))
        for name in GENERATED_PAGES[kind]:
            target = safe_target(root, f'docs/{language}/{name}')
            content = generated_page(policy, language, kind, name, facts, unknown, root, skills).encode('utf-8')
            if not target.is_file() or target.read_bytes() != content:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                written.append(str(target.relative_to(root)))
    return written


def fill_listings(text, language, skills=(), plugins=(), section_text=None):
    text = text.replace('{{SKILL_FEATURES}}', '\n\n'.join('### :%s\n\n%s\n\n📖 [:%s – %s](docs/%s/skills/%s.md)' % (
        name, section_text or '{{FEATURE_%d}}' % number, name, {'de': 'Mehr dazu', 'en': 'More'}[language], language, name)
        for number, (name, _) in enumerate(skills, 1)))
    more = {'de': 'Mehr dazu', 'en': 'More'}[language]
    return text.replace('{{PLUGIN_FEATURES}}', '\n\n'.join('### %s\n\n%s\n\n📖 [%s – %s](%s#readme)' % (
        name, one_line(description) or '{{PLUGIN_%d}}' % number, name, more, re.sub(r'\.git$', '', link))
        for number, (name, description, link) in enumerate(plugins, 1)))


def template_text(template, policy, base=None, kind='plugin'):
    text = ((base or TEMPLATES / 'documentation' / kind) / template).read_text(encoding='utf-8')
    if len(policy['languages']) == 1:
        text = '\n'.join(line for line in text.split('\n') if not ('Deutsch' in line and 'English' in line and ' | ' in line))
        text = re.sub(r'\n{3,}', '\n\n', text)
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
        if name.endswith(tuple('/' + page for page in GENERATED_PAGES[kind])):
            continue  # generated below, also when it already exists
        if not target.exists():
            text = template_text(template, policy, kind=kind)
            text = fill_listings(text.replace('{{TITLE}}', title or info['name']), language, skills, plugins)
            if name.endswith('/installation.md'):
                text = fill_installation(text, facts, language)
            plans.append((target, text.encode('utf-8')))
    for target, content in plans:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(content)
    generated = write_generated_pages(root, policy, facts, unknown=True, skills=[name for name, _ in skills])
    return {'created': [str(p.relative_to(root)) for p, _ in plans] + generated,
            'existing_pages_preserved': True,
            'missing_facts': sorted(key for key in ('url', 'market', 'id') if not facts.get(key)),
            'next': 'Run validate and report what it names together with missing_facts as warnings. The texts are written by the person.'}


REPORT = {
    'en': {'updated': 'Rewritten:', 'created': 'Created:', 'open': 'Still to be written:', 'facts': 'Missing facts:', 'notes': 'Warnings:',
           'complete': '{kind} {name} docs: complete', 'one': '{kind} {name} docs: 1 warning', 'many': '{kind} {name} docs: {count} warnings'},
    'de': {'updated': 'Neu geschrieben:', 'created': 'Neu angelegt:', 'open': 'Noch zu schreiben:', 'facts': 'Fehlende Angaben:', 'notes': 'Warnungen:',
           'complete': '{kind} {name} Doku: vollständig', 'one': '{kind} {name} Doku: 1 Warnung', 'many': '{kind} {name} Doku: {count} Warnungen'},
}
FACT_NAMES = {'en': {'url': 'marketplace address', 'market': 'marketplace name', 'id': 'plugin id'},
              'de': {'url': 'Adresse des Marketplace', 'market': 'Name des Marketplace', 'id': 'Plugin-Kennung'}}
# the warnings of the check are English (they also show in CI); the answer of docs speaks the language of the person
GERMAN = [(re.compile(pattern, re.DOTALL), text) for pattern, text in (
    (r'Features lacks the entry (.+)', r'unter Features fehlt der Eintrag \1'),
    (r'Features names (.+), which is no skill of the plugin', r'unter Features steht \1, das ist kein Skill des Plugins'),
    (r'the feature (.+) needs a link to (.+)', r'beim Feature \1 fehlt der Link auf \2'),
    (r'the feature (.+) has no explanation', r'beim Feature \1 fehlt die Erklärung'),
    (r'the explanation of (.+) has (\d+) characters, at most (\d+)', r'die Erklärung zu \1 hat \2 Zeichen, erlaubt sind höchstens \3'),
    (r'Plugins lacks the entry (.+)', r'unter Plugins fehlt der Eintrag \1'),
    (r'Plugins names (.+), which marketplace\.json does not list', r'unter Plugins steht \1, das marketplace.json nicht listet'),
    (r'the entry (.+) needs a link to the README of the plugin \((.*)\)', r'beim Eintrag \1 fehlt der Link auf die README des Plugins (\2)'),
    (r'no skill of the plugin has this name', r'kein Skill des Plugins heißt so'),
    (r'page of the former structure; remove it \(nothing is converted\)', r'Seite der früheren Struktur; bitte entfernen (umgewandelt wird nichts)'),
    (r'missing page', r'Seite fehlt'),
    (r'unresolved template placeholders', r'enthält noch Platzhalter'),
    (r'unclosed fenced block', r'ein Codeblock ist nicht geschlossen'),
    (r'the headings must be exactly those of the generated page; run /plugin-manager:docs',
     r'die Überschriften weichen von der erzeugten Seite ab; führe /plugin-manager:docs aus'),
    (r'(.+) is not linked to its page (.+)', r'\1 ist nicht mit seiner Seite \2 verlinkt'),
    (r'level-two headings must match outline order', r'die ##-Überschriften stimmen nicht (Namen oder Reihenfolge)'),
    (r'expected exactly one page title', r'genau eine #-Überschrift ist erforderlich'),
    (r'machine-specific path', r'enthält einen Pfad deines Rechners'),
    (r'missing language counterpart link', r'der Link zur anderen Sprache fehlt'),
    (r'link escapes repository: (.+)', r'Link führt aus dem Repository hinaus: \1'),
    (r'missing link target: (.+)', r'Linkziel fehlt: \1'),
    (r'missing heading anchor: (.+)', r'Sprungmarke fehlt: \1'),
    (r'public link to ignored test artifacts', r'verlinkt auf ignorierte Testergebnisse'),
    (r'the icon assets/icon\.png must be referenced', r'das Logo assets/icon.png ist nicht eingebunden'),
)]
ICON_MISSING = 'assets/icon.png is missing (the single icon of the plugin)'


def translate(warning, language):
    # A warning of the check in the language of the person; an unknown text stays as it is.
    if language != 'de':
        return warning
    if warning == ICON_MISSING:
        return 'assets/icon.png fehlt (das eine Logo des Repositorys)'
    page, separator, text = warning.partition(': ')
    for pattern, german in GERMAN:
        found = pattern.fullmatch(text)
        if separator and found:
            return page + ': ' + found.expand(german)
    return warning


def operator_language(root, requested=None):
    """The requested language, else the one saved in the repository, else English; never guessed."""
    if requested in REPORT:
        return requested
    saved = local_json(Path(root) / '.project/operator.json').get('operator_language')
    return saved if saved in REPORT else 'en'


def result_message(root, created, updated, warnings, missing_facts, language):
    """The finished answer of docs: only what happened and what is open, then one status line."""
    words, kind = REPORT[language], kind_of(root)
    # skills.md only repeats what is open on a skill page of the same language; without such a page its own warning stays
    still_open = {found[1] for found in (re.match(r'^docs/(\w+)/skills/.+: ".+" is still to be written', warning) for warning in warnings) if found}
    warnings = [warning for warning in warnings
                if not any(warning == f'docs/{code}/skills.md: unresolved template placeholders' for code in still_open)]
    manifest = local_json(root / ('plugin.json' if kind == 'plugin' else 'marketplace.json'))
    sections, notes = {}, []
    for warning in warnings:
        found = re.match(r'^(.+?): "(.+?)" is still to be written', warning)
        sections.setdefault(found[1], []).append('"%s"' % ('Einleitung' if language == 'de' and found[2] == 'introduction' else found[2])) if found else notes.append(warning)
    blocks = [words[key] + '\n' + '\n'.join('- ' + line for line in lines) for key, lines in (
        ('updated', sorted(updated)), ('created', sorted(created)),
        ('open', [page + ': ' + ', '.join(names) for page, names in sections.items()]),
        ('facts', [FACT_NAMES[language].get(fact, fact) for fact in missing_facts]), ('notes', [translate(note, language) for note in notes])) if lines]
    count = len(warnings) + len(missing_facts)
    status = words['complete' if not count else 'one' if count == 1 else 'many']
    blocks.append(status.format(kind=kind.title(), name=manifest.get('name') or root.name, count=count))
    return '\n\n'.join(blocks)


def run(source, output, title=None, languages=None, default_language=None, message_language=None):
    """What the docs skill does in one call: generate and create, check, and say it in one finished message."""
    root = Path(output).expanduser().resolve()
    before = {path.relative_to(root).as_posix() for path in [*root.glob('*.md'), *(root / 'docs').rglob('*.md')]}
    result = scaffold(source, output, title, languages, default_language)
    pages = [name for name in result['created'] if name.endswith('.md')]
    warnings = validate(root)
    facts = result['missing_facts'] if kind_of(root) == 'plugin' else [fact for fact in result['missing_facts'] if fact != 'id']
    message = result_message(root, [name for name in pages if name not in before], [name for name in pages if name in before],
                             warnings, facts, operator_language(root, message_language))
    return dict(result, warnings=warnings, result_message=message)


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
    create.add_argument('--message-language', choices=('de','en'), help='Language of result_message; default the saved operator language, else English')
    verify = sub.add_parser('validate')
    verify.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'inspect':
            result = inspect(args.source)
        elif args.command == 'scaffold':
            result = run(args.source, args.output, args.title, args.languages, args.default_language, args.message_language)
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
