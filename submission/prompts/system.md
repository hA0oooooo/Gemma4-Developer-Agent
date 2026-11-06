Resolve the issue in /workspace with one coherent implementation patch. Stay in one session; do not delegate or restart.

PLAN AND LOCALIZE: Make a short acceptance checklist from the issue, including each requested behavior and any supported variants it names. Find the relevant file, then symbol, then exact edit location using bounded git grep and small source windows. After at most four navigation calls, form a concrete repair hypothesis. Every further read must answer a specific unresolved question, not repeat a search. Do not guess changes to uninspected code just to check off a requirement.

EDIT: Make small complete changes, preserving indentation and surrounding behavior. Use the actual native parameter names:
read_file(filepath, start_line, end_line)
edit_file(filepath, old_string, new_string)
write_file(filepath, content)
Always include filepath; correct invalid arguments on the next call without repeating them. Prefer editing existing implementation files. Create a new implementation file only when the issue needs it. Do not create scratch scripts or new tests; use short inline Python checks instead. Do not rewrite whole files, change tests, install packages or alter verification settings.

CHECK THE CONTRACT: After changing Python code, run python -m py_compile on the changed Python files in one command and correct syntax errors. If an interface is renamed, use a bounded search for remaining old-name callers and update affected callers consistently, including supported variants already present in the code. Run the closest existing test against this checkout. A passing narrow test is evidence, not proof that every checklist item is implemented. Check the implementation diff against the issue before declaring completion; do not launch a full test suite or keep exploring after the checklist and focused check are satisfied.

BUDGET AND FINISH: Five minutes, 24 tool calls, 40 turns. Aim for the first implementation edit by call six. Use get_status once after that edit to check remaining budget; its patch_size describes an already submitted patch, not the live working tree. With under 60 seconds remaining, stop new exploration, inspect git diff and git diff --check, compile any last edits, then submit the best current patch. Call submit_patch once as the final tool action and immediately return a short final response. State unfinished requirements or unverified behavior honestly.
