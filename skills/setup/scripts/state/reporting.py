"""Status and gate answers: dispatch priority and the report structure."""
import os
from . import associations
from . import detection
from . import evidence_files
from . import inspection
from . import preferences
from . import messages
from .constants import Conflict, IGNORE_RULE


def next_flow(operation, failed, needs_choice, plan, missing, state):
    """Fixed priority (R17): conflict/error stops; then language, configuration, skeleton, sync decisions, ready.
    Flow operations (setup) only say to run status again; status decides."""
    if failed:
        return 'stop'
    if operation != 'status':
        return 'status'
    if needs_choice:
        return 'language'
    if state == 'unconfigured':
        return 'configure'
    removals = plan['removals']
    if missing or plan['pending'] or plan['updates'] or plan['rule_pending'] or removals['auto'] or removals['lock_cleanup']:
        return 'skeleton'
    if plan['decisions'] or removals['decisions']:
        return 'sync'
    return 'ready'


def pending_writes(ctx, plan):
    """What the skeleton flow is about to write; its own evidence file only when it writes nothing else."""
    entries = [(path, 'create') for path, state in plan['files'].items() if state == 'missing']
    entries += [(path, 'change') for path in plan['updates']]
    entries += [(path, 'delete') for path in plan['removals']['auto']]
    if plan['rule_pending']:
        entries.append(('.gitignore', 'change' if plan['ignore_text'] else 'create'))
    if not entries and (plan['pending'] or plan['removals']['lock_cleanup']):
        entries.append((ctx.lock_path, 'change' if plan['lock_exists'] else 'create'))
    return entries


def written(ctx, root, plan, created_files, updated_files, removed_files, ignore, lock_changed):
    """The list of what the skeleton flow wrote, with the same rule for the evidence file."""
    created, updated = list(created_files), list(updated_files)
    if ignore and ignore.get('changed'):
        (updated if plan['ignore_text'] else created).append('.gitignore')
    if lock_changed and not (created or updated or removed_files):
        (updated if plan['lock_exists'] else created).append(ctx.lock_path)
    return messages.write_result(updated, created, removed_files, messages.language_for(root))


def report(ctx, operation, root, name, plan, created_files=(), created_dirs=(), lock_changed=False,
           ignore=None, saved=False, errors=(), conflicts=(), unverified=(), state='plugin', removed_files=(), removed_dirs=(), updated_files=()):
    files = plan['files']
    preference = plan['preference']
    different = sorted(r for r, s in files.items() if s in ('accepted', 'decision_needed'))
    missing = sorted(r for r, s in files.items() if s == 'missing')
    directories = list(plan['directories'])
    if ('.project' not in directories and not os.path.isdir(root / '.project')
            and (plan['pending'] or preference['needs_choice'])):
        directories.append('.project')  # management folder needed for language and/or lock
    failed = bool(errors or conflicts)
    following = next_flow(operation, failed, preference['needs_choice'], plan, missing, state)
    asks = operation == 'status' and following == 'skeleton'
    return {
        'operation': operation, 'ok': not failed, 'state': state, 'target': str(root), 'plugin': name,
        'plugin_configured': state != 'unconfigured',
        'configuration': {'plugin': ctx.plugin, 'configured': state != 'unconfigured',
                          'kind': state if state in ctx.kinds else None},
        'next': following,
        'write_request': messages.write_request(pending_writes(ctx, plan), messages.language_for(root)) if asks else None,
        'write_declined': messages.write_declined(messages.language_for(root)) if asks else None,
        'result_message': written(ctx, root, plan, created_files, updated_files, removed_files, ignore, lock_changed)
        if operation == 'setup' and not failed else None,
        'updated': list(updated_files), 'outdated': list(plan['updates']),
        'skeleton': {'open': bool(missing or plan['pending'] or plan['updates'] or plan['rule_pending'] or plan['removals']['auto']
                                  or plan['removals']['lock_cleanup']) if operation == 'status' else failed,
                     'missing_files': missing, 'lock_pending': list(plan['pending']) if operation == 'status' else [],
                     'ignore_rule_pending': plan['rule_pending'] if operation == 'status' else False,
                     'different': different,
                     'accepted_deviations': sorted(r for r, s in files.items() if s == 'accepted')},
        'sync': {'needed': bool(plan['decisions'] or plan['removals']['decisions']) if operation == 'status' else False,
                 'decisions': list(plan['decisions']) if operation == 'status' else []},
        'kept': list(plan.get('kept', [])) if operation == 'status' else [],
        'removals': {'auto': list(plan['removals']['auto']), 'decisions': list(plan['removals']['decisions']),
                     'kept': list(plan['removals']['kept']), 'unowned': list(plan['removals']['unowned']),
                     'lock_cleanup': list(plan['removals']['lock_cleanup'])} if operation == 'status'
        else {'auto': [], 'decisions': [], 'kept': [], 'unowned': [], 'lock_cleanup': []},
        'removed': {'files': list(removed_files), 'directories': list(removed_dirs)},
        'conflicts': list(conflicts), 'errors': list(errors),
        'files': dict(files),
        'missing': {'files': missing, 'directories': [d for d in directories if not os.path.isdir(root / d)]},
        'identical': sorted(r for r, s in files.items() if s == 'identical'),
        'different': different,
        'created': {'files': list(created_files), 'directories': list(created_dirs), 'unverified': list(unverified)},
        'language': {'operator_language': preference['operator_language'], 'needs_choice': preference['needs_choice'],
                     'saved': saved},
        'gitignore': ignore or {'rule_present': preferences.has_rule(plan['ignore_text']), 'changed': False},
        'lock': {'path': ctx.lock_path, 'exists': plan['lock_exists'] or lock_changed, 'changed': lock_changed,
                 'pending': [] if operation == 'setup' and not failed else list(plan['pending'])},
        'matches_template': state != 'unconfigured' and all(s in ('identical', 'removed') for s in files.values()) and not failed,
        'target_code_executed': False,
        'limitations': ['Existing regular files are replaced only by an explicit adopt decision (sync); deviations are otherwise only reported.',
                        'Ignore handling checks only the exact line ' + IGNORE_RULE + '; other rules and negations are not evaluated.'],
    }


def status(ctx, target):
    root, name, state = detection.detect_target(ctx, target, allow_unconfigured=True)
    plan = inspection.inspect(ctx, root, None)
    plan['kept'] = inspection.kept_files(ctx, root, plan)
    evidence = evidence_files.read_evidence(ctx, root) if state != 'unconfigured' else None
    return dict(report(ctx, 'status', root, name, plan, state=state), entries=sorted(os.listdir(root)),
                association=associations.association_report(ctx, root, evidence))


def conflict_result(operation, target, conflict):
    entry = {'path': conflict.path, 'reason': conflict.reason}
    if conflict.code:
        entry['code'] = conflict.code
    if conflict.entries:
        entry['entries'] = conflict.entries
    return {'operation': operation, 'ok': False, 'state': 'conflict', 'next': 'stop', 'target': str(target), 'conflicts': [entry],
            'created': {'files': [], 'directories': []}, 'target_code_executed': False}


def gate(ctx, target, action=None, language=None):
    """Write-free answer to: may a writing skill other than setup (docs, modify) start? Open means the
    state is not ready; the caller stops and points to /plugin-manager:setup. Never writes and runs no flow.
    The stop message comes from messages.py, in `language` (else the saved operator language, else English)."""
    lang = messages.language_for(target, language)
    try:
        data = status(ctx, target)
    except Conflict as conflict:
        reason = messages.GATE_REASONS['en']['stop']
        return {'operation': 'gate', 'ok': False, 'ready': False, 'next': 'stop', 'target': str(target),
                'reason': reason, 'detail': str(conflict.reason), 'run': '/plugin-manager:setup',
                'message': messages.gate_message(action, 'stop', lang), 'target_code_executed': False}
    ready = bool(data['ok']) and data['next'] == 'ready'
    reason = '' if ready else messages.GATE_REASONS['en'].get(data['next'], 'the state is not ready')
    detail = '; '.join(str(c.get('reason', '')) for c in data['conflicts']) or None
    return {'operation': 'gate', 'ok': ready, 'ready': ready, 'next': data['next'], 'target': data['target'],
            'reason': reason, 'detail': detail, 'run': None if ready else '/plugin-manager:setup',
            'message': None if ready else messages.gate_message(action, data['next'], lang), 'target_code_executed': False}
