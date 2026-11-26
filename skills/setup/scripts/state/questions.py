"""The one catalogue of the questions the Manager skills ask, in German and English (R55).

A flow shows a question and its choices unchanged and only replaces the {placeholders}. The same wording stands in the
documentation pages of the skills; a test compares them. The question before writing and the failure messages are built
in messages.py."""
from .messages import pick

# id -> (German question, German choices, English question, English choices); no choices means free text
QUESTIONS = {
    'kind': ('Plugin oder Marketplace?', ('Plugin', 'Marketplace'),
             'Plugin or marketplace?', ('Plugin', 'Marketplace')),
    'name': ('Wie lautet der technische Name? Vorschlag: {suggestion}', (),
             'What is the technical name? Suggestion: {suggestion}', ()),
    'display_name': ('Wie lautet der Anzeigename? Vorschlag: {suggestion}', (),
                     'What is the display name? Suggestion: {suggestion}', ()),
    'publisher': ('Wer ist der Herausgeber?', (), 'Who is the publisher?', ()),
    'description': ('Was tut das Plugin, in ein bis zwei Sätzen? Du kannst auch „Noch offen“ antworten.', (),
                    'What does the plugin do, in one or two sentences? You may also answer "Still open".', ()),
    'documentation_languages': (
        'Welche Doku-Sprachen?',
        ('Deutsch und Englisch (Standard Deutsch)', 'Deutsch und Englisch (Standard Englisch)', 'Nur Deutsch', 'Nur Englisch'),
        'Which documentation languages?',
        ('German and English (default German)', 'German and English (default English)', 'German only', 'English only')),
    'license': ('Welche Lizenz?', ('MIT', 'Andere Lizenz', 'Später entscheiden'),
                'Which licence?', ('MIT', 'Another licence', 'Decide later')),
    'copyright_year': ('Welches Jahr steht im Copyright?', ('{year}', 'Anderes Jahr'),
                       'Which year goes into the copyright notice?', ('{year}', 'Another year')),
    'rights_holder': ('Wer ist Rechteinhaber?', ('{publisher}', 'Jemand anderes'),
                      'Who holds the rights?', ('{publisher}', 'Someone else')),
    'marketplace': ('In welchen Marketplace gehört das Plugin?', ('{folder}', 'Anderer Marketplace-Ordner'),
                    'Which marketplace does the plugin belong to?', ('{folder}', 'Another marketplace folder')),
    'differs': ('{file} weicht von der Vorlage ab.', ('Meine Datei behalten', 'Vorlage übernehmen'),
                '{file} differs from the template.', ('Keep my file', 'Adopt template')),
    'template_gone': ('Die Vorlage zu {file} ist entfallen.', ('Datei behalten', 'Datei löschen'),
                      'The template of {file} is gone.', ('Keep file', 'Delete file')),
    'run_setup': ('Soll ich /plugin-manager:setup jetzt ausführen?', ('Ja, ausführen', 'Nein, abbrechen'),
                  'Run /plugin-manager:setup now?', ('Yes, run it', 'No, stop')),
    'new_value': ('Wie lautet der neue Wert für {field}?', (), 'What is the new value for {field}?', ()),
    'change': ('Was soll sich ändern?', ('Technischer Name', 'Anzeigename', 'Beschreibung'),
               'What should change?', ('Technical name', 'Display name', 'Description')),
}
# asked before any language is known, therefore in both
LANGUAGE_QUESTION = ('Welche Bediensprache soll ich verwenden? / Which operator language should I use?', ('Deutsch', 'English'))
YES_NO = {'de': ('Ja', 'Nein'), 'en': ('Yes', 'No')}


def questions(language=None):
    """Every question in one language: {id: {question, choices}}, plus the two fixed choices of a write question."""
    german = pick(language) == 'de'
    found = {key: {'question': value[0 if german else 2], 'choices': list(value[1 if german else 3])} for key, value in QUESTIONS.items()}
    found['language'] = {'question': LANGUAGE_QUESTION[0], 'choices': list(LANGUAGE_QUESTION[1])}
    found['write'] = {'question': '{write_request}', 'choices': list(YES_NO[pick(language)])}
    return found
