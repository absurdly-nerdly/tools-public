# Guide Instructions and Task Set Implementation Rules



## Task Set Branch Workflow (Executed by Laborer) (approx. lines 3-50)

*Follow steps in this exact order. Do not `switch_mode` under any circumstances.*

1.  **Start Task Set Branch:** Create/switch to the feature branch.
    *   **Script:** `python ide-files_OG/glob_start-task-set-branch.py <OG_file_path> <OG_Number> <TS-number> <AttemptNumber>`
        *   *(Use variables provided: `{OG_file_path}`, `{OG_Number}`, `{TS-number}`, `{AttemptNumber}`)*
    *   **Action:** The script prints `git status`, checks out `main`, commits pending changes, creates the branch (`OG-{OG_Number}_TS-{TS-number}_attempt-{N}`), checks it out, and runs `git status` again.
    *   **Verify:** Confirm branch creation/checkout using `git status` or `git branch --show-current`. Retry twice on failure. If third attempt fails, report via `ask_followup_question` with error. Do not proceed until successful.

2.  **Identify Mode & Create Subtask:** Delegate the Task Set implementation.
    *   **Identify:** Use the `{Mode}` variable provided.
    *   **Create `new_task` for Laborer:** Use the following message **VERBATIM**, replacing placeholders with variables provided:
        ```
        🌿 {Mode}: OG-{OG_Number}_TS-{TS-number}_Attempt-{AttemptNumber}
        *Starting in Laborer mode. Follow instructions precisely:*
        *In `ide-files_OG/glob_TS-instructions.md`, `read_file` only lines 60-120, find the 'Task Set Subtask Workflow' section, and follow those instructions exactly.*
        *Use these variables:*
        - OG File Path: {OG-filepath}
        - Task Set Number: {TS-number}
        - Assigned Mode: {Mode}
        ```
        *(Replace `{Mode}`, `{OG_Number}`, `{TS-number}`, `{AttemptNumber}`, `{OG-filepath}`. NO additional content.)*
    *   **Action:** The subtask will start in Laborer mode and follow the workflow, and respond with the specified format (Auth Icons + message).
    *   **Verify:** Ensure the message from the subtask includes any required information for subsequent Task Sets.

3.  **Await Subtask Completion:** Wait for the subtask's response.

4.  **Validate Subtask Execution:** Verify the work done in the subtask.
    *   **Run Verification Steps:** Execute the project-specific verification steps defined in the OG's 'Validation & End State' section for this Task Set.
        *   **Command:** [Refer to the OG for the specific commands/tool usage]
        *   *(Use variables provided: `{CurrentBranchName}`, `{URL_from_OG}`, `{LogPrompt_from_OG}`, `{ImagePrompt_from_OG}`. Source URL/prompts from OG's `Validation & End State` for TS-{TS-number}. Only include prompt args if specified.)*
        *   **Action:** Perform the specified verification steps using `execute_command` or appropriate MCP tools.
        *   **Review:** Examine the output for critical errors/warnings and compare against expected results in the OG.
    *   **Perform Unique Check:** Execute at least one *unique* validation step specific to the Task Set's goal (e.g., Playwright MCP interaction, `read_file` check, `firebase-emulator-mcp` query, `playwright_mcp` screenshot + `any-vision-mcp` analysis, etc.) to confirm the core change.

5.  **Respond via `attempt_completion`:** Report comprehensive results: a) verification script outcome, b) unique validation type and outcome, c) subtask completion message. Ensure all details are captured.
-- -- --


























## Task Set Execution Instructions (Executed by Assigned Mode, starting in Laborer) (approx. lines 60-120)

### Task Set Execution Workflow
*Follow these steps precisely. The initial mode is Laborer.*

**Phase 1: Preparation (Laborer -> Architect)**

1.  **Read OG & Context (Laborer):**
    *   Read the *entire* Orchestrator Guide (`{OG-filepath}`).
    *   Read all files listed in the assigned Task Set's (`{X}`) `Files to Edit` and `Resources` sections.
    *   Read any other files necessary per OG instructions.
    *   *(Do NOT read `_10_ide/TS-post-completion.md` yet).*
2.  **Switch to Architect:** Use `switch_mode`.
3.  **Plan (Architect):**
    *   State current mode (`Architect Mode`).
    *   Formulate and state a detailed, step-by-step execution plan based on the OG Task Set (`{X}`) and gathered context.

**Phase 2: Execution & Wrap-up (Architect -> Assigned Mode)**

4.  **Switch to Assigned Mode:** Use `switch_mode` to the mode specified in the OG (`{Mode}`).
5.  **Execute (Assigned Mode - `{Mode}`):**
    *   State current mode (`{Mode} Mode`).
    *   Execute the Architect's plan, completing all tasks in the assigned Task Set (`{X}`). 
    *   Adhere strictly to the Task Set Execution Rules below and OG/user instructions.
6.  **Validate:**
    *   Execute *all* validation steps defined in the Task Set's "Validation & End State".
    *   **Rerun on Edit:** If any validation leads to code edits, restart and rerun *all* validation steps consecutively. Debug and iterate until all validations pass consecutively.
    *   **Verify End State:** Confirm actual state matches expected state (commands, flags, args).
    *   **Scope:** Complete *only* the assigned Task Set.
7.  **Post Completion:** Read `_10_ide/TS-post-completion.md`** and execute all instructions within it. This includes exact instructions for updating the OG document and reporting completion.  *Auth-Icon-A:* 🦘


### Task Set Execution Rules

*   **Scope Control:** Only complete the assigned Task Set. Do not proceed to the next.
*   **Mode Switching:** Use `switch_mode` if tasks within the *same* TS require different modes. Do not read `TS-post-completion.md` or `attempt_completion` if tasks remain in the current TS for another mode.
*   **OG Task Issues:** If unable to complete a task as planned, use `attempt_completion` to query the user with progress and suggestions. Do not improvise unless a success path is clear and it does not deviate from the High Level Objectives and Execution Notes in the OG.
*   **Task Set Status:** *Never* update the overall Task Set status (e.g., `**TS-X Status:** ⚪`). Only update individual task/validation statuses.
*   **Context Limit (>200k tokens):** Immediately `switch_mode` to Analyst, perform RCA, create PR, then `attempt_completion` reporting failure and PR path.
*   **Mode Tracking:** State current mode in *every* response.
*   **Missing Components:** Report via `attempt_completion` if components expected to exist don't exist.
*   **Test Strategy Docs:** Add clear docstrings for complex UI interaction strategies/helpers.
*   **Laborer Restrictions:** Laborer MUST NOT use `switch_mode` except as directed by workflow (to Architect, then Assigned Mode). Laborer MUST NOT switch to any other mode. If issues are encountered while in Laborer mode, report them via `ask_followup_question` or `attempt_completion`. 
-- -- --
