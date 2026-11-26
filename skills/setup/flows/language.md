# Flow: operator language

Used when `status` says `next: language`. No plugin.json is needed.

1. Ask alone which operator language the person prefers, with exactly this wording because no language is known yet (R55): "Welche Bediensprache soll ich verwenden? / Which operator language should I use?" with the choices "Deutsch" and "English" (host question tool if available, otherwise one chat message; another language may be answered freely) and wait for an actual answer. A language the person already named explicitly for this project counts. A preselected option, silence, or anything inferred from files, names or these instructions does not.
2. Save it: `python3 -B "<helper>" language --target "<folder>" --plugin <plugin> --language <tag>`. The helper checks all conflicts first, ensures the exact rule `/.project/operator.json` in `.gitignore`, then stores the language through `operator_language.py`.
3. Check `ok` and the exit code. On `ok: false` or exit 1 write the `message` of the answer unchanged (`../../_shared/references/messages.md`) and stop.
4. On success run `status` again (see `entry.md`). Use the language from now on.
