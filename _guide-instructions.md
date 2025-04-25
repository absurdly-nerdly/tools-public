# Guide Instructions and Task Set Implementation Rules

## Task Set Execution Steps

1.   Read the *entire* Orchestrator Guide (`{OG-filepath}`) before starting. *(**DO NOT** read `_10_templates/_PCS.md` at this point. Follow the steps in order)*

2.   Complete all tasks listed within the assigned Task Set (`{X}`).

3.   Execute all validation steps defined within the Task Set's "Validation & End State" section.

*   **Rerun on Edit:** If *any* validation step leads to code edits, you MUST restart and rerun *all* validation steps from the beginning of the validation section for that Task Set. All validation steps must pass consecutively after the final edit.

*   **End State Verification:** After validation, verify the actual end state matches the expected end state defined in the "Validation & End State" section, including exact commands, flags, and arguments.

*   **Scope Control:** Only complete the tasks and validations in the *assigned Task Set*. Do NOT proceed to the next Task Set.

4.  **Document Key Outputs:** Before proceeding to the PCS, document any key outputs or information generated during the Task Set execution (e.g., lists of SKUs, configuration values, test results summaries) in the `#### TS-X Log:` section of the OG file. Ensure this information is clear and easily accessible for subsequent task sets.

5.   **Read, understand, and execute** the instructions/rules in the "Post-Completion Steps" (PCS) in `_10_templates/_PCS.md`.



## Implementation Rules
*   **Scope Control:** Only complete the tasks and validations in the *assigned Task Set*. Do NOT proceed to the next Task Set.
*   **Mode Switching:** Use `switch_mode` to proceed to and complete tasks that are assigned to other modes within the same TS. Do not read PCS and do not `attempt_completion` when tasks have not yet been attempted (due to being in incorrect mode) - just switch modes.
*   **OG Task Issues:** If an OG task needs clarification, has a conflict, or cannot be completed as planned, do not improvise or deviate. Use `attempt_completion` to query the orchestrator with progress and suggestions.
*   **Task Set Status:** Never update the overall Task Set status (e.g., `**TS-X Status:** ⚪`). Only update the status of individual tasks and validation steps within the Task Set.
*   **Context Limit:** If `Current Context Size (Tokens)` > 250,000, immediately `switch_mode` to Analyst, conduct a Root Cause Analysis to identify the issue (don't resolve it at this time), create a PR, and then `attempt_completion` to report the failure of the task set and the PR path.
*   **Mode Tracking:** In *every* response, state the mode you are in *currently*.
*   **Missing Components:** If a component needed for a test doesn't exist, `attempt_completion` to report the issue.
*   **Test Strategy Documentation:** Document successful strategies and helper functions for interacting with complex or non-standard UI components, including any workarounds developed, in `continuous-improvement.md` for future reference.

## **Auth-Icon-A:** 🦘