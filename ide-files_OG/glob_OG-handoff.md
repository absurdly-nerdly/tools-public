# Orchestrator Handoff

**Purpose:** Facilitates handoff of an in-progress OG execution due to context limits.

##   **Handing Off an OG (single step):**

*   Use `new_task` to initiate the handoff.
*   Provide comprehensive, detailed, and distilled context for the receiving Orchestrator.
*   Include relative paths to:
    *   The original OG file.
    *   The OG Appendix file (if applicable).
    *   Any Problem Reports (PRs) associated with in-progress Task Sets.
*   Instruct to read `_10_ide\OG-handoff.md` and follow the instructions for receiving an OG.
*   Suggest next steps, if applicable.


##   **Receiving an OG:**

1.  Review the original OG provided in the handoff. Use `new_task` to delegate to `Researcher`:
    *   Instruct Researcher to:
        *   Ensure the current branch is `main` and the working directory is clean (`git status`).
        *   Analyze and verify the current project state based on the original OG, the handoff context, and any. 
        *   Review the content of associated PRs relevant to in-progress Task Sets.
    *   Include specific verification steps if needed (e.g., running tests, checking file states).
2.  Await and review the Researcher's report. **Do not proceed if the project state is unclear or verification fails.** If the Researcher's analysis indicates the original OG plan needs adjustments before proceeding with the next Task Set (TS {X}):
    *   **Consultant Review:** Switch mode to `Consultant` to plan the OG adjustments before applying them. The Consultant will provide a single response and switch back to Orchestrator mode.
    *   **(Orchestrator Mode) Update OG:** Apply the planned adjustments directly to the OG file.
3.  Resume the standard Orchestrator Task Set Coordination Workflow, starting from Step 1 (Delegate to Laborer...) for the current/next Task Set ({X}).