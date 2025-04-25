# Guide Instructions and Task Set Implementation Rules

## Task Set Execution Steps

1.   Read the *entire* Orchestrator Guide (`{OG-filepath}`) before starting. *(**DO NOT** read ide-files_OG/glob_TS-post-completion.md at this point. Follow the steps in order)*

2.   Complete all tasks listed within the assigned Task Set (`{X}`).

3.   Execute all validation steps defined within the Task Set's "Validation & End State" section.

*   **Rerun on Edit:** If *any* validation step leads to code edits, you MUST restart and rerun *all* validation steps from the beginning of the validation section for that Task Set. All validation steps must pass consecutively after the final edit.

*   **End State Verification:** After validation, verify the actual end state matches the expected end state defined in the "Validation & End State" section, including exact commands, flags, and arguments.

*   **Scope Control:** Only complete the tasks and validations in the *assigned Task Set*. Do NOT proceed to the next Task Set.

4.  **Document Key Outputs:** Before proceeding to the PCS, document any key outputs or information generated during the Task Set execution (e.g., lists of SKUs, configuration values, test results summaries) in the `#### TS-X Log:` section of the OG file. Ensure this information is clear and easily accessible for subsequent task sets.

5.   **Read, understand, and execute** the instructions/rules in the "Post Completion Steps" by fetching and reading ide-files_OG/glob_TS-post-completion.md.


## Implementation Rules
*   **Scope Control:** Only complete the tasks and validations in the *assigned Task Set*. Do NOT proceed to the next Task Set.
*   **Mode Switching:** Use `switch_mode` to proceed to and complete tasks that are assigned to other modes within the same TS. Do not read PCS and do not `attempt_completion` when tasks have not yet been attempted (due to being in incorrect mode) - just switch modes.
*   **OG Task Issues:** If an OG task needs clarification, has a conflict, or cannot be completed as planned, do not improvise or deviate. Use `attempt_completion` to query the user with progress and suggestions.
*   **Task Set Status:** Never update the overall Task Set status (e.g., `**TS-X Status:** ⚪`). Only update the status of individual tasks and validation steps within the Task Set.
*   **Context Limit:** If `Current Context Size (Tokens)` > 250,000, immediately `switch_mode` to Analyst, conduct a Root Cause Analysis to identify the issue (don't resolve it at this time), create a PR, and then `attempt_completion` to report the failure of the task set and the PR path.
*   **Mode Tracking:** In *every* response, state the mode you are in *currently*.
*   **Missing Components:** If a component needed for a test doesn't exist, `attempt_completion` to report the issue.
*   **Test Strategy Documentation:** Document successful strategies and helper functions for interacting with complex or non-standard UI components, including any workarounds developed, in `continuous-improvement.md` for future reference.

## **Auth-Icon-A:** 🦘
---





























## Task Set Branch & Subtask Workflow (Executed by Laborer)

*Follow steps in this exact order. Do not `switch_mode` under any circumstances.*
*:

1.  **Start Task Set Branch:** Create/switch to the feature branch.
    *   **Script:** `python ide-files_OG/glob_start-task-set-branch.py <OG_file_path> <OG_Number> <TS-number> <NextAttemptNumber>`
        *   *(Use variables provided by Orchestrator in the initial `new_task` message: `{OG_file_path}`, `{OG_Number}`, `{TS-number}`, `{attempt_number}`)*
    *   **Action:** The script prints `git status`, checks out `main`, commits pending changes, creates the branch (`OG-{OG_Number}_TS-{TS-number}_attempt-{N}`), checks it out, and runs `git status` again.
    *   **Verify:** Confirm branch creation/checkout using `git status` or `git branch --show-current`. **CRITICAL:** Do *not* assume success based on script exit code if undefined or no response is returned. Retry twice on failure. If third attempt fails, report via `attempt_completion` with error. Do not proceed until branch checkout is confirmed successful.

2.  **Identify Mode & Create Subtask:** Delegate the Task Set implementation.
    *   **Identify:** Use the `{Mode}` variable provided by Orchestrator in the initial `new_task` message.
    *   **Create `new_task`:** Use the following message **VERBATIM**, replacing placeholders with variables provided by Orchestrator in the initial `new_task` message:
        ```
        🌿 {Mode}: OG-{OG_Number}_TS-{TS-number}_Attempt-{NextAttemptNumber}
        *Follow steps in this exact order*:
        1.  **FIRST**, review the rules in the global Task Set Instructions file (ide-files_OG/glob_TS-instructions.md, lines 1-50).
        2.  **SECOND**, read the file `{OG-filepath}`. Within this OG file, locate and read the Task Set {TS-number} section.
        3.  **THIRD**, complete Task Set {TS-number} from `{OG-filepath}`, adhering to the rules reviewed in Step 1 (lines 1-50 of ide-files_OG/glob_TS-instructions.md).
        4.  **FOURTH**, After completion of Task Set {TS-number} (*not before*) read the *entire* global Task Set Post Completion instructions file: ide-files_OG/glob_TS-post-completion.md.
        5.  **FIFTH**, Adhering to the rules in the post-completion file read in Step 4, update `{OG-filepath}`.
        6.  **SIXTH**, `attempt_completion` with exactly the following:
            a.  **Auth-Icon-A:** 🦘 (from ide-files_OG/glob_TS-instructions.md).
            b.  **Auth-Icon-B:** 🪃
            c.  A **brief** completion message, including any output or information required for subsequent Task Sets.
        ```
        *(Replace `{Mode}`, `{OG_Number}`, `{TS-number}`, `{OG-filepath}` using variables provided by Orchestrator. NO additional content.)*
    *   **Action:** The subtask will use `attempt_completion` with the specified format.
    *   **Verify:** Ensure the `attempt_completion` message includes any required information for subsequent Task Sets.
3.  **Await Subtask Completion:** Wait for the assigned mode to finish and provide its `attempt_completion` response.

4.  **Validate Subtask Execution:** Verify the work done in the subtask.
    *   **Run Verification Steps:** Execute the project-specific verification steps defined in the OG's 'Validation & End State' section for this Task Set.
        *   **Command:** [Refer to the OG for the specific commands/tool usage]
        *   *(Use variables provided by Orchestrator in the initial `new_task` message: `{CurrentBranchName}`, `{URL_from_OG}`, `{LogPrompt_from_OG}`, `{ImagePrompt_from_OG}`. Source URL and prompts directly from the OG's `Validation & End State` section for TS-{TS-number}. Only include prompt args if specified there.)*
        *   **Action:** Perform the specified verification steps using `execute_command` or appropriate MCP tools.
        *   **Review:** Examine the output for critical errors/warnings and compare against expected results in the OG.
    *   **Perform Unique Check:** Execute at least one *unique* validation step specific to the Task Set's goal (e.g., Playwright MCP interaction, specific `read_file` check, `firebase-emulator-mcp` query, custom project script analysis, `playwright_mcp` screenshot + `any-vision-mcp` analysis, etc.) to confirm the core change.

5.  **Report completion via `attempt_completion`:** Use `attempt_completion` to report a comprehensive result. This result MUST include: a) The outcome of the verification steps (Step 4a), b) The outcome of the unique validation check (Step 4b), and c) The completion message received from the Assigned Mode's subtask (Step 3). Ensure all details are captured.