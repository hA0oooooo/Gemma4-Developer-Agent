---
name: workspace-kit
description: Bounded source navigation, short exact edits and existing-test feedback
---

Call run_skill_script with skill_name="workspace-kit" and
file_path="scripts/workspace.py". Both args formats below are supported by
the same script and perform exactly the same operations.

Prefer the named-map args format for every operation, including source editing.

Array arguments:
- search: ["search", "QUERY"]
- show: ["show", "FILEPATH", "SYMBOL"] (SYMBOL may be omitted)
- edit: ["edit", "FILEPATH", "OLD", "NEW"]
- test: ["test", "EXISTING_TEST_PATH_OR_NODE"]
- diff: ["diff"]

Named-map arguments:
- search: {"operation":"search", "query":"QUERY"}
- show: {"operation":"show", "filepath":"FILEPATH", "symbol":"SYMBOL"}
- edit: {"operation":"edit", "filepath":"FILEPATH", "old":"OLD", "new":"NEW"}
- test: {"operation":"test", "target":"EXISTING_TEST_PATH_OR_NODE"}
- diff: {"operation":"diff"}

Pass actual source strings, including newlines, not a shell command, a JSON
string containing the whole args value, or an extra source-escaping layer.
Do not combine an args array with short_options or positional_args.

Each edit permits at most 4 OLD lines and 8 NEW lines. OLD must match exactly
once. Only a new implementation file permits an empty OLD. Invalid Python is
rejected without modifying the original. Search/show return bounded source.
Use relative paths inside the task checkout. Never edit tests or configuration,
install packages or create reproduction files. Correct errors from actual
feedback, review diff, then submit_patch rather than repeating exploration.
