"""The write-free inspection plan of a target folder."""
import json
import re
from . import fsafe
from . import preferences
from . import skeleton_lock
from . import template_sources
from .constants import Conflict, LANGUAGE_PATH


MANAGED_PAGE = re.compile(r'docs/(de|en)/(?:concepts|development|files)\.md')
SWITCH_LINE = re.compile(rb'(?m)^(?:\*\*Deutsch\*\* \| \[English\]|\[Deutsch\])\([^)]*\)(?: \| \*\*English\*\*)?\n\n')


def single_language(templates, selected):
    """With one documentation language there is no other page to switch to: the managed pages lose that line."""
    if len(selected) != 1:
        return templates
    return {relative: entry if entry is None or not MANAGED_PAGE.fullmatch(relative) else (SWITCH_LINE.sub(b'', entry[0]), entry[1])
            for relative, entry in templates.items()}


STYLE_PAGE = 'docs/style.md'


def style_state(ctx, root):
    """R38: the writing style of the documentation is required where the kind ships a template for it."""
    template = ctx.source_root / ctx.template_base.rsplit('/', 1)[0] / 'seed' / STYLE_PAGE
    return {'path': STYLE_PAGE, 'required': template.is_file(), 'present': (root / STYLE_PAGE).is_file(), 'template': str(template)}


def documentation_languages(root):
    """The selected documentation languages of the repository; none when the settings are missing or unreadable."""
    path = root / 'docs/documentation.json'
    try:
        if path.is_symlink():
            return set()
        languages = json.loads(path.read_text(encoding='utf-8'))['documentation']['languages']
        return {value for value in languages if isinstance(value, str)}
    except (OSError, ValueError, KeyError, TypeError):
        return set()


def kept_files(ctx, root, plan):
    """R45: the files kept on purpose (accepted deviation) with the pair that taking one back refers to."""
    return [dict(path=relative, **skeleton_lock.pair(fsafe.sha256(plan['templates'][relative][0]),
                                                      fsafe.sha256(fsafe.read_regular(root, relative))))
            for relative, state in sorted(plan['files'].items()) if state == 'accepted']


def inspect(ctx, root, requested_language):
    """Read-only plan; raises Conflict before any write could happen."""
    language = preferences.load_language_helper(ctx)
    if requested_language is not None:
        try:
            language.validate_language(requested_language)
        except ValueError as exc:
            raise Conflict(LANGUAGE_PATH, str(exc)) from exc
    templates = template_sources.load_templates(ctx)
    fsafe.check_chain(root, '.project', 'dir')
    try:
        preference = language.preference(root)
    except (ValueError, OSError) as exc:  # includes corrupt JSON (JSONDecodeError)
        raise Conflict(LANGUAGE_PATH, str(exc)) from exc
    if requested_language and preference['operator_language'] not in (None, requested_language):
        raise Conflict(LANGUAGE_PATH, 'Operator language is already ' + preference['operator_language']
                       + '; changing it is not part of setup')
    lock, lock_exists, _ = skeleton_lock.read_lock(ctx, root)
    ignore_text = preferences.read_ignore(root)
    files, directories, decisions, updates = {}, [], [], []
    removals = {'auto': [], 'decisions': [], 'kept': [], 'unowned': [], 'lock_cleanup': []}
    needed_dirs = set()
    selected = documentation_languages(root)
    templates = single_language(templates, selected)
    for relative, entry in templates.items():
        page = MANAGED_PAGE.fullmatch(relative)
        if page and page.group(1) not in selected:
            continue  # managed pages exist only in the selected documentation languages
        accepted = lock.get(relative)
        exists = fsafe.check_chain(root, relative, 'file') != 'missing'
        if entry is None:  # source removed in the parent: ownership evidence in the lock decides
            local = fsafe.read_regular(root, relative) if exists else None
            if not exists:
                files[relative] = 'removed'
                if accepted is not None:
                    removals['lock_cleanup'].append(relative)
            elif accepted is None:
                files[relative] = 'unowned'  # no ownership evidence: never touched
                removals['unowned'].append(relative)
            else:
                local_hash = fsafe.sha256(local)
                if accepted['source_hash'] is None and local_hash == accepted['local_hash']:
                    files[relative] = 'removal_kept'
                    removals['kept'].append(relative)
                elif (accepted['source_hash'] is not None
                        and local_hash == accepted['local_hash'] == accepted['source_hash']):
                    files[relative] = 'auto_remove'
                    removals['auto'].append(relative)
                else:
                    files[relative] = 'removal_decision'
                    removals['decisions'].append({
                        'kind': 'removal', 'path': relative, 'source_removed': True,
                        'reason': 'source_removed_local_changed' if accepted['source_hash'] is None else 'source_removed_local_differs',
                        'source_hash': None, 'local_hash': local_hash, 'accepted': accepted,
                        'source_file': None, 'local_file': str(root / relative)})
            continue
        template = entry[0]
        parent = ''
        for part in relative.split('/')[:-1]:
            parent += part
            needed_dirs.add(parent)
            parent += '/'
        if not exists:
            files[relative] = 'missing'
        else:
            local = fsafe.read_regular(root, relative)
            files[relative], reason = skeleton_lock.classify(local, template, accepted)
            if reason == 'source_changed' and accepted['source_hash'] == accepted['local_hash']:
                files[relative], reason = 'auto_update', None  # was an exact copy and is untouched: the new source is taken without a question
                updates.append(relative)
            if reason:
                current = skeleton_lock.pair(fsafe.sha256(template), fsafe.sha256(local))
                decisions.append({
                    'kind': 'content', 'path': relative, 'reason': reason, 'source_hash': current['source_hash'],
                    'local_hash': current['local_hash'], 'accepted': accepted,
                    'source_changed': accepted is None or accepted['source_hash'] != current['source_hash'],
                    'local_changed': accepted is None or accepted['local_hash'] != current['local_hash'],
                    'source_file': str(ctx.source_root / ctx.template_base / relative), 'local_file': str(root / relative)})
        parent = ''
        for part in relative.split('/')[:-1]:
            parent += part
            if fsafe.check_chain(root, parent, 'dir') == 'missing' and parent not in directories:
                directories.append(parent)
            parent += '/'
    pending = [r for r, state in files.items()
               if state in ('missing', 'identical') and lock.get(r) != skeleton_lock.pair(fsafe.sha256(templates[r][0]), fsafe.sha256(templates[r][0]))]
    return {'language': language, 'preference': preference, 'templates': templates, 'lock': lock,
            'lock_exists': lock_exists, 'ignore_text': ignore_text, 'files': files,
            'directories': directories, 'pending': pending, 'decisions': decisions, 'updates': updates, 'removals': removals,
            'needed_dirs': needed_dirs,
            'rule_pending': preference['operator_language'] is not None and not preferences.has_rule(ignore_text)}
