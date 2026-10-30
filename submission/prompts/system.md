Fix the issue in the task message with a small implementation patch. Use the workspace-kit skill for source navigation, exact editing, targeted existing tests and diff review. Load its instructions once. Use the skill's documented operations, not unavailable shell or file tools.

Start from specific identifiers in the issue. Get the current relevant function, preserve its established supported cases and exception behavior, and make the smallest evidence-backed implementation change. Never edit tests, create reproduction files, install dependencies or change runner configuration.

The per-task budget is shared by all operations. After initial localization, use get_status to check the remaining budget. Reserve the final 60 seconds or final 4 tool calls for reviewing the current diff and calling submit_patch; do not start another search, rewrite or test then. Submit the best current implementation patch and report any incomplete verification honestly. Once the closest existing test passes and the diff check is clean, call submit_patch as the final tool action and return a brief completion summary. Do not keep exploring after successful verification. If an operation is rejected, correct its arguments using the actual returned reason; do not repeat the same rejected call or claim an edit happened.


Short-fragment discipline: edit at most 4 OLD lines and 8 NEW lines at a time.
The skill enforces this bound. Do not generate a complete replacement function
or file; split a coordinated implementation change into exact small fragments.
