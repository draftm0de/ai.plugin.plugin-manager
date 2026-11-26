"""The one place that turns a failure into the message shown to the person (R25, R26).

Pure text: no file access except the optional operator language, no state. A failure with a known code gets its
catalogue wording, anything else the "cause not known" wording; the raw error text is only returned as detail.
Layout (two paragraphs of running text, no labels) and wording live here and nowhere else."""
import json
from pathlib import Path

LANGUAGES = ('en', 'de')
DEFAULT_LANGUAGE = 'en'

# action names as the person knows them; the headline names what was asked for, never a helper or flow
ACTIONS = {'setup': 'setup', 'docs': 'docs', 'modify': 'modify', 'verify': 'verify'}

HEADLINE = {
    'en': 'The {action} action could not be completed, because {cause}.',
    'de': 'Die Aktion {action} konnte nicht abgeschlossen werden, weil {cause}.',
}
STOPPED = {
    'en': 'The {action} action was stopped, because {cause}.',
    'de': 'Die Aktion {action} wurde abgebrochen, weil {cause}.',
}
STOPPED_ANY = {
    'en': 'The requested action was stopped, because {cause}.',
    'de': 'Die angefragte Aktion wurde abgebrochen, weil {cause}.',
}
PLEASE = {'en': 'Please {way}.', 'de': 'Bitte {way}.'}
REPEAT = {'en': 'Then call /plugin-manager:{skill} (in Codex: $plugin-manager:{skill}) again.', 'de': 'Rufe danach /plugin-manager:{skill} (in Codex: $plugin-manager:{skill}) erneut auf.'}
CHANGED = {
    'none': {'en': 'Nothing was changed.', 'de': 'Es wurde nichts geändert.'},
    'language': {'en': 'The language you chose was saved.', 'de': 'Die Sprache, die du gewählt hast, wurde gespeichert.'},
}

# code -> cause (after "because") and way (after "Please"), per language; {facts} are filled from the failure
CATALOGUE = {
    'git_missing': {
        'en': ('Git is not installed or cannot be found', 'install Git'),
        'de': ('Git nicht installiert ist oder nicht gefunden wird', 'installiere Git'),
    },
    'not_a_repository': {
        'en': ('the folder {path} is not recognised as a Git repository',
               'either initialise a Git repository in an IDE (for example VS Code) or run `git init` in a terminal in that folder'),
        'de': ('der Ordner {path} nicht als Git-Repository erkannt wird',
               'initialisiere entweder in einer IDE (zum Beispiel VS Code) ein Git-Repository oder führe in einem Terminal in diesem Ordner `git init` aus'),
    },
    'no_repository': {
        'en': ('the folder {path} is not recognised as a Git repository and has no GitHub address yet', 'run this in that folder (in a terminal or an IDE such as VS Code)'),
        'de': ('der Ordner {path} nicht als Git-Repository erkannt wird und noch keine GitHub-Adresse hat', 'führe in diesem Ordner aus (im Terminal oder in einer IDE wie VS Code)'),
    },
    'no_origin': {
        'en': ('the folder {path} has no GitHub address yet', 'run this in that folder (in a terminal or an IDE such as VS Code)'),
        'de': ('der Ordner {path} noch keine GitHub-Adresse hat', 'führe in diesem Ordner aus (im Terminal oder in einer IDE wie VS Code)'),
    },
    'inside_repository': {
        'en': ('the folder {path} lies inside the Git repository {root}', 'choose the folder that is itself the repository'),
        'de': ('der Ordner {path} im Git-Repository {root} liegt', 'wähle den Ordner, der selbst das Repository ist'),
    },
    'address_not_plain': {
        'en': ('the address {address} is not a plain GitHub address',
               'use the form `https://github.com/<owner>/<name>.git`, without user name or password'),
        'de': ('die Adresse {address} keine einfache GitHub-Adresse ist',
               'verwende die Form `https://github.com/<owner>/<name>.git`, ohne Benutzername und Passwort'),
    },
    'address_differs': {
        'en': ('the given address {address} differs from the GitHub address of the folder ({origin})',
               'use the address of the folder, or change the GitHub address of the folder first'),
        'de': ('die angegebene Adresse {address} von der GitHub-Adresse des Ordners ({origin}) abweicht',
               'verwende die Adresse des Ordners oder ändere zuerst die GitHub-Adresse des Ordners'),
    },
    'other_content': {
        'en': ('the folder {path} already holds other files that are not part of a plugin',
               'either start in an empty folder or move the other files out of the folder'),
        'de': ('der Ordner {path} bereits andere Dateien enthält, die nicht zu einem Plugin gehören',
               'beginne entweder in einem leeren Ordner oder verschiebe die anderen Dateien aus dem Ordner'),
    },
    'existing_differs': {
        'en': ('some files in {path} already exist with other content',
               'keep them as they are, or choose by hand which version stays (the setup asks for each file)'),
        'de': ('einige Dateien in {path} bereits mit anderem Inhalt vorhanden sind',
               'behalte sie, wie sie sind, oder entscheide von Hand, welche Fassung bleibt (das Setup fragt bei jeder Datei nach)'),
    },
    'unsupported_format': {
        'en': ('the file {path} has a format this version does not read',
               'move or rename the file (the Manager never converts or deletes it)'),
        'de': ('die Datei {path} ein Format hat, das diese Version nicht liest',
               'verschiebe die Datei oder benenne sie um (der Manager wandelt sie nie um und löscht sie nie)'),
    },
    'not_configured': {
        'en': ('this folder is not configured yet', 'run /plugin-manager:setup (in Codex: $plugin-manager:setup) first'),
        'de': ('dieser Ordner noch nicht konfiguriert ist', 'führe zuerst /plugin-manager:setup (in Codex: $plugin-manager:setup) aus'),
    },
    'invalid_name': {
        'en': ('the technical name is not valid', 'give a name in lowercase kebab-case (letters, digits and single hyphens, for example `my-plugin`)'),
        'de': ('der technische Name nicht gültig ist', 'gib einen Namen in Kleinbuchstaben mit Bindestrichen an (Buchstaben, Ziffern und einzelne Bindestriche, zum Beispiel `mein-plugin`)'),
    },
    'empty_display_name': {
        'en': ('the display name is empty', 'give a display name'),
        'de': ('der Anzeigename leer ist', 'gib einen Anzeigenamen an'),
    },
    'empty_description': {
        'en': ('the description is empty', 'give a description'),
        'de': ('die Beschreibung leer ist', 'gib eine Beschreibung an'),
    },
    'nothing_to_change': {
        'en': ('no change was given', 'give a name, a display name or a description'),
        'de': ('keine Änderung angegeben wurde', 'gib einen Namen, einen Anzeigenamen oder eine Beschreibung an'),
    },
    'template_base': {
        'en': ('the installed Plugin Manager is incomplete or damaged: its templates do not fit together',
               'update or reinstall the Plugin Manager and open a new session'),
        'de': ('der installierte Plugin Manager unvollständig oder beschädigt ist: Seine Vorlagen passen nicht zusammen',
               'aktualisiere oder installiere den Plugin Manager neu und öffne eine neue Sitzung'),
    },
    'no_decision': {
        'en': ('there is no open question for the file {path}', 'call /plugin-manager:setup (in Codex: $plugin-manager:setup) and say which kept file you want to take back'),
        'de': ('es zur Datei {path} keine offene Entscheidung gibt', 'rufe /plugin-manager:setup (in Codex: $plugin-manager:setup) auf und nenne die behaltene Datei, die du zurückhaben willst'),
    },
    'stale_decision': {
        'en': ('the file {path} changed after the question was asked', 'answer the question again for the current state'),
        'de': ('sich die Datei {path} geändert hat, seit die Frage gestellt wurde', 'beantworte die Frage für den aktuellen Stand neu'),
    },
    'unknown': {
        'en': ('the cause is not known (an unexpected error)',
               'either call the same skill again (it checks the state first, so repeating is safe) or run `/plugin-manager:verify` (in Codex: `$plugin-manager:verify`) for a read-only check of the folder'),
        'de': ('die Ursache nicht bekannt ist (ein unerwarteter Fehler)',
               'rufe entweder denselben Skill erneut auf (er prüft zuerst den Zustand, Wiederholen ist also sicher) oder führe `/plugin-manager:verify` (in Codex: `$plugin-manager:verify`) für eine reine Lese-Prüfung des Ordners aus'),
    },
}

# fixes that are shell commands: shown in one code block after the request, followed by the sentence in AFTER
_REMOTE = 'git remote add origin https://github.com/<owner>/{repo}.git'
COMMANDS = {'no_repository': ('git init', _REMOTE), 'no_origin': (_REMOTE,)}
_NOT_YET = {'en': 'The repository does not have to exist on GitHub yet.', 'de': 'Das Repository muss auf GitHub noch nicht existieren.'}
AFTER = {'no_repository': _NOT_YET, 'no_origin': _NOT_YET}

# state-helper conflicts (Conflict.code) that are known causes; every other conflict is not known
FILE_CODES = ('no_decision', 'stale_decision')  # their {path} is the file, not the folder
CONFLICT_CODES = {'no_decision': 'no_decision', 'stale_decision': 'stale_decision', 'template_base': 'template_base', 'not_fresh': 'other_content', 'config_format': 'unsupported_format', 'not_configured': 'not_configured'}

# R50: the question before the skeleton flow writes, the answer to "no" and the list of what was written
WRITE = {
    'en': {'ask': 'I would like to change file(s):', 'may': 'May I write?', 'declined': 'Nothing was changed. Call /plugin-manager:setup (in Codex: $plugin-manager:setup) again when I may write.',
           'create': 'create', 'change': 'change', 'delete': 'delete',
           'updated': 'I updated:', 'created': 'I created:', 'removed': 'I removed:'},
    'de': {'ask': 'Ich möchte Datei(en) ändern:', 'may': 'Darf ich schreiben?', 'declined': 'Es wurde nichts geändert. Rufe /plugin-manager:setup (in Codex: $plugin-manager:setup) erneut auf, wenn ich schreiben darf.',
           'create': 'anlegen', 'change': 'ändern', 'delete': 'löschen',
           'updated': 'Aktualisiert habe ich:', 'created': 'Neu angelegt habe ich:', 'removed': 'Entfernt habe ich:'},
}


def write_request(entries, language=None):
    """The question naming every file that is about to be written; `entries` are (path, create|change|delete)."""
    if not entries:
        return None
    words = WRITE[pick(language)]
    lines = ['* %s (%s)' % (path, words[action]) for path, action in sorted(entries)]
    return '\n\n'.join((words['ask'], '\n'.join(lines), words['may']))


def write_declined(language=None):
    return WRITE[pick(language)]['declined']


def write_result(updated=(), created=(), removed=(), language=None):
    """The files that were written, one list per kind of change; None when nothing was written."""
    words = WRITE[pick(language)]
    blocks = [words[key] + '\n' + '\n'.join('- ' + path for path in sorted(paths))
              for key, paths in (('updated', updated), ('created', created), ('removed', removed)) if paths]
    return '\n\n'.join(blocks) or None


# the gate: why a writing skill stops (the reason follows "only partly (...)")
GATE_REASONS = {
    'en': {'stop': 'something in this folder blocks the setup', 'language': 'the language is not set yet',
           'configure': 'this folder is not configured yet', 'skeleton': 'some required files or settings are missing or outdated',
           'sync': 'a shared file needs your decision'},
    'de': {'stop': 'etwas in diesem Ordner blockiert die Einrichtung', 'language': 'die Sprache ist noch nicht gesetzt',
           'configure': 'dieser Ordner ist noch nicht konfiguriert', 'skeleton': 'einige benötigte Dateien oder Einstellungen fehlen oder sind veraltet',
           'sync': 'eine gemeinsame Datei braucht deine Entscheidung'},
}
GATE_CAUSE = {'en': 'this folder is not set up yet, or only partly ({reason})',
              'de': 'dieser Ordner noch nicht oder nur teilweise eingerichtet ist ({reason})'}
GATE_WAY = {'en': 'Please run /plugin-manager:setup (in Codex: $plugin-manager:setup) first.', 'de': 'Führe zuerst /plugin-manager:setup (in Codex: $plugin-manager:setup) aus.'}


class Failure(ValueError):
    """A failure with a catalogue code and the facts the wording needs. Still a ValueError for existing handlers."""

    def __init__(self, code, **facts):
        if code not in CATALOGUE:
            raise KeyError('Unknown failure code: ' + code)
        self.code, self.facts = code, {key: str(value) for key, value in facts.items()}
        super().__init__(render_plain(code, self.facts) + (' [' + self.facts['detail'] + ']' if 'detail' in self.facts else ''))


def pick(language):
    return language if language in LANGUAGES else DEFAULT_LANGUAGE


def saved_language(root):
    """The operator language saved in the folder when the catalogue has it, else None."""
    try:
        text = (Path(root) / '.project' / 'operator.json').read_text(encoding='utf-8')
        saved = json.loads(text).get('operator_language')
    except (OSError, ValueError, AttributeError, TypeError):
        return None
    return saved if saved in LANGUAGES else None


def language_for(root, requested=None):
    """The requested language, else the operator language saved in the folder, else English (never guessed)."""
    return requested if requested in LANGUAGES else pick(saved_language(root))


def render_plain(code, facts, language='en'):
    cause, way = CATALOGUE[code][pick(language)]
    text = cause + ('; please ' if pick(language) == 'en' else '; bitte ') + way
    if code in COMMANDS:
        text += ': ' + ', '.join('`%s`' % line for line in COMMANDS[code])
    return text.format_map(_Facts(facts))


class _Facts(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def render(action, code, facts=None, language=None, changed=None, skill=None, stopped=False, repeat=True):
    """The two-paragraph message; a fix made of shell commands carries them in a code block inside the second part.
    `changed` is one of CHANGED or None (the sentence is then left out)."""
    lang = pick(language)
    cause, way = CATALOGUE[code][lang]
    commands = [line.format_map(_Facts(facts or {})) for line in COMMANDS.get(code, ())]
    return _layout(lang, action, cause.format_map(_Facts(facts or {})), way.format_map(_Facts(facts or {})), changed, skill or action, stopped, repeat,
                   commands, AFTER.get(code, {}).get(lang))


def _layout(lang, action, cause, way, changed, skill, stopped, repeat, commands=(), after=None):
    first = (STOPPED if stopped else HEADLINE)[lang].format(action=ACTIONS.get(action, action), cause=cause)
    if changed in CHANGED:
        first += ' ' + CHANGED[changed][lang]
    rest = [after] if after else []
    if repeat:
        rest.append(REPEAT[lang].format(skill=skill))
    if commands:
        second = PLEASE[lang].format(way=way)[:-1] + ':\n\n```bash\n' + '\n'.join(commands) + '\n```'
        return '\n\n'.join([first, second] + ([' '.join(rest)] if rest else []))
    return first + '\n\n' + ' '.join([PLEASE[lang].format(way=way)] + rest)


def gate_message(action, next_state, language=None):
    """The stop of a writing skill at a closed gate."""
    lang = pick(language)
    reason = GATE_REASONS[lang].get(next_state, GATE_REASONS[lang]['stop'])
    cause = GATE_CAUSE[lang].format(reason=reason)
    first = STOPPED[lang].format(action=action, cause=cause) if action else STOPPED_ANY[lang].format(cause=cause)
    return first + '\n\n' + GATE_WAY[lang]


def classify(error, folder=None):
    """Catalogue code and facts of an error, or ('unknown', {}). Only coded failures are known causes."""
    code = getattr(error, 'code', None)
    if isinstance(error, Failure):
        return error.code, dict({'path': str(folder)} if folder else {}, **error.facts)
    if code in CONFLICT_CODES:
        own = folder if folder and code not in FILE_CODES else getattr(error, 'path', '.')
        return CONFLICT_CODES[code], {'path': str(own)}
    return 'unknown', {}


def explain(action, error, language=None, changed=None, skill=None, folder=None):
    """Message and technical detail for any error. The detail is for the person only on request."""
    code, facts = classify(error, folder)
    return {'message': render(action, code, facts, language, changed, skill),
            'known': code != 'unknown', 'code': code, 'detail': str(error)}
