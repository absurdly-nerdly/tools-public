# How to Split an Orchestrator Guide (OG)

This document outlines the process for splitting a large Orchestrator Guide (OG) into two separate files to manage context size and improve usability for subtask modes.

**Scenario:** An OG (`_XX_OG_Original-Description.md`) has become too large, potentially exceeding context limits or making it difficult for subtask modes to process efficiently.

**Goal:** Split the OG into two parts:
1.  **Part 1:** Contains the introduction (Objectives, Files, Initial State) and all *completed* Task Sets.
2.  **Part 2:** Contains the introduction (Objectives, Files, Initial State), a few *recent* completed Task Sets for context, and all *remaining* (⚪ NOT STARTED) Task Sets.

**Procedure:**

1.  **Ensure `main` Branch:** Before starting, make sure you are on the `main` branch and the working directory is clean (`git checkout main; git status`).
2.  **Read Original OG:** Use the `read_file` tool to get the complete content of the original OG file (`_XX_OG_Original-Description.md`).
3.  **Create Part 1 File:**
    *   Identify the line number where the first *remaining* (⚪ NOT STARTED) Task Set begins in the original OG content.
    *   Copy all content from the beginning of the original OG up to (but *not* including) the start of the first remaining Task Set.
    *   Use the `write_to_file` tool to create a new file (e.g., `_XX_OG_Part1_Completed_TS1-Y.md`, where Y is the last completed Task Set number). Paste the copied content into this file.
4.  **Create Part 2 File:**
    *   Identify the line number where the *context* Task Sets should begin (e.g., 1-3 Task Sets *before* the first remaining one).
    *   Copy the introduction sections (Objectives, Files, Initial State) from the beginning of the original OG.
    *   Append the content of the context Task Sets and *all* remaining Task Sets (from the identified line number in the previous step to the end of the original OG).
    *   Use the `write_to_file` tool to create a second new file (e.g., `_XX_OG_Part2_Remaining_TSZ-N.md`, where Z is the first context Task Set number and N is the last Task Set number). Paste the combined introduction and relevant Task Set content into this file.
5.  **Commit New Files:**
    *   Add both new Part 1 and Part 2 files using `git add`.
    *   Commit the changes to the `main` branch with a descriptive message (e.g., `git commit -m "OG-XX: 📜 Split OG-XX into Part 1 (TS1-Y) and Part 2 (TSZ-N)"`).
6.  **Update Workflow:**
    *   When creating subtasks for the remaining Task Sets, provide the path to the **Part 2** OG file (`_XX_OG_Part2_Remaining_TSZ-N.md`) in the `new_task` message. This ensures the subtask mode receives only the relevant, manageable context.
    *   The original full OG (`_XX_OG_Original-Description.md`) can optionally be archived or kept for historical reference, but should *not* be used for subsequent subtasks. The Part 1 file serves as the historical record of completed work.
7.  **Initiate Workflow:** After successfully verifying the state and potentially adjusting the OG on `main`, `suggest` creating a new subtask in Orchestrator Mode to formally begin execution of Task Set {X}. If approved, at minimum, provide to the subtask the path to the original OG (`[Relative Path to the Original OG File]`) and confirm the starting Task Set number ({X}) as context for the new task. If more context is helpful, provide it.
8.  **Refer to Global Rules:** The subsequent steps for resuming execution and updating the OG during execution are defined in the global Orchestrator rules (.roo/rules-orche-global/rules.md).

**Example (Based on OG-44):**

*   Original File: `_44_OG_Fix-TanStack-Table-SKU-Pagination-and-Validate-MCP.md`
*   Split Point: Task Set 10 was the next to start.
*   Context Sets for Part 2: Task Sets 8 and 9.
*   Part 1 File Created: `_44_OG_Part1_Completed_TS1-9.md` (Intro + TS1 through TS9)
*   Part 2 File Created: `_44_OG_Part2_Remaining_TS8-11.md` (Intro + TS8, TS9, TS10, TS11)
*   Commit Message: `OG-44: 📜 Split OG-44 into Part 1 (TS1-9) and Part 2 (TS8-11)`
*   Subsequent Subtasks (for TS10, TS11) should reference `_44_OG_Part2_Remaining_TS8-11.md`.