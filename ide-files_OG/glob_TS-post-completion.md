# POST-COMPLETION STEPS (PCS) FOR TASK SETS

This document outlines the mandatory steps to perform after completing all assigned tasks and validation steps for a Task Set within an Orchestrator Guide (OG).

## 1. Update the Orchestrator Guide (OG) Document

Carefully update the relevant Task Set section in the OG document:

**A. Update Task Set End State:**
   - Follow the specific instructions within the OG document for updating the "Task Set End State" section.
   - **Critical:** If new issues (e.g., console errors, Firebase problems) are discovered during this update that indicate the Task Set *actually failed*, **STOP** updating the OG. Switch to Debug Mode immediately to address these new issues.

**B. Update Status Markers:**
   - Update the status marker (e.g., `⚪`) for each *individual Task* and *Validation step* within the *completed* Task Set.
   - **DO NOT** update the overall Task Set status line (e.g., `**Status:** ⚪`) at this stage.
   - **Status Markers:**
     - Tasks/Task Sets: `⚪` NOT STARTED, `✅` COMPLETED, `✖️` SKIPPED, `❌` FAILED
     - Validation Steps: `⚪` NOT STARTED, `✅` PASSED, `✖️` SKIPPED, `❌` FAILED

**C. Update the Task Set Log:**
   - Ensure the log provides sufficient detail for subsequent teammates to understand the work performed and proceed with future tasks, as there is no direct contact between teammates.
   - **Document Actual Validation Results:** Record the *actual* outcomes of validation steps in the log. **DO NOT** alter the *expected* outcomes (e.g., `Expect PASS`) listed in the OG's `Validation` section.
   - **Add Log Sections:**
     - **Results Summary:** 1-4 concise sentences summarizing the Task Set outcome.
     - **Deviations:** Note any deviations from the original plan and the reasons for them.
     - **Important Notes (Optional):** Max 3 notes, ranked by importance.
     - **Suggestions for Codebase (Optional):** Max 3 high-level, impactful recommendations for codebase maintainability improvements. Avoid overlap with Rules suggestions. Do not repeat previous suggestions.
     - **Suggestions for Rules (Optional):** Max 5 suggestions for improving rules files (`.roo/rules/rules.md`, mode-specific `.roo\rules-*\rules.md` files) to enhance maintainability or automation. Rank by importance. Mark critical suggestions with `🛑`. Avoid overlap with Codebase suggestions. Do not repeat previous suggestions.
      - **Problem Reports (PRs):** If any PR files were created during *this* Task Set implementation, list their file paths here. For each PR listed, indicate whether the core issue documented within it was resolved.

## 2. Report Completion

- Once all OG updates (Steps 1A-1C) are complete, use the `attempt_completion` tool.

    *   Your `attempt_completion` response MUST contain, in this order:

        a.  **Auth-Icon-A:** (from `_guide-instructions.md`)
        b.  **Auth-Icon-B:** 🪃
        c.  A **brief** completion message. Do NOT report 'SUCCESS' or 'FAILURE'. 
        -   **DO NOT** include the entire content of the Problem Report or the OG Task Set in the `attempt_completion`. Be brief.
        d.  If any Problem Reports were created during the Task Set, list their file paths and state if the underlying issue was resolved.  Be brief.
