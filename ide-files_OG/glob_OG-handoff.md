# Orchestrator Handoff Document

**Purpose:** This document facilitates the handoff of an in-progress Orchestrator Guide (OG) execution, typically due to context window limitations. The receiving Orchestrator must use this document in conjunction with the original OG to understand the current state and resume work effectively.

**Original Orchestrator Guide:** [Relative Path to the Original OG File]

---

## 1. High-Level Objectives (from Original OG)

*   Refer to the `## High Level Objectives` section in the original OG: `[Relative Path to the Original OG File]`

---

## 2. Overall Status Summary

*   **Last Successfully Completed Task Set:** [Number of the last TS marked ✅ in the OG]
*   **Current/Next Task Set to Execute:** [Number of the TS to be worked on next]
*   **Total Task Sets in OG:** [Total number of TS defined in the original OG]
*   **Summary of Failed/Incomplete Task Sets:** [List TS numbers with ❌ or ⚪ status. Reference associated PRs, e.g., TS3 (PR-12), TS5 (PR-15). Refer to the OG for full details.]

---

## 3. Status of Current/Next Task Set ({X}) - Refer to OG

*   **Task Set Number:** {X}
*   **Task Set Title:** [Title from Original OG]
*   **Current Status in OG:** [Status: ⚪, ✅, ❌, 🚧 (In Progress/Failed Attempt)]
*   **Key Information/Summary (Optional):**
    *   [Briefly summarize critical outcomes, failures, or points of attention from the last attempt on this TS, if applicable. E.g., "Last attempt failed validation step 3.2 due to render mismatch. See PR-XX."]
    *   [Mention the number of failure attempts and associated PRs for this specific TS, e.g., "Failure Attempts: 2, PRs: [PR-YY, PR-ZZ]"]
*   **Action Required:** The receiving Orchestrator MUST carefully review the full details of Task Set {X} within the original OG: `[Relative Path to the Original OG File]` before proceeding.

---

## 4. Outstanding Issues / Critical Notes / Context

*   [List any known blockers, critical warnings from logs, pending decisions, environment issues, or important context not captured elsewhere. This is crucial for the receiving Orchestrator.]
*   [Example: "A verification step consistently timed out during the last attempt on TS{X-1}. Root cause unknown."]
*   [Example: "User approval is pending for the adjustments made in PR-ZZ."]

---

## 5. Instructions for Receiving Orchestrator

1.  **Thoroughly Review Original OG:** Read the *entire* original Orchestrator Guide: `[Relative Path to the Original OG File]`. Pay close attention to the High-Level Objectives, Initial State, and the specific details of *all* Task Sets up to and including the **Current/Next Task Set ({X})**.
2.  **Review Handoff Document:** Carefully read this entire handoff document to understand the latest summary status, known issues, and critical context.
3.  **Ensure `main` Branch:** Before making *any* file modifications (including OG updates) or starting the Task Set workflow (which involves branching), **ensure you are on the `main` branch** (`git checkout main; git pull`). Verify the working directory is clean (`git status`).
4.  **Analyze & Verify Current State:**
    *   **Crucially:** Based on the OG, this handoff doc, and any associated PRs for failed Task Sets, analyze the state of the project *while on the `main` branch*.
    *   **Verify:** If there are *any* ambiguities, conflicting information, or potential inconsistencies, **perform verification steps**. This might include:
        *   Running project-specific initial state checks (e.g., linting, rendering/console tests).
        *   Verifying specific file contents or data using appropriate tools.
        *   Consulting logs or outputs mentioned in PRs.
    *   Do not proceed if the current state is unclear or seems incorrect. Resolve discrepancies first.
5.  **Consult Problem Reports (PRs):** If failed Task Sets (❌) are indicated, review the associated Problem Report (PR) files for details.
6.  **Adjust Original OG (If Necessary, on `main`):** If your analysis (Step 4) reveals that the plan in the *original* OG needs adjustments *before* proceeding with Task Set {X}, make those adjustments directly to the OG file **while still on the `main` branch**. Commit them with a clear message (e.g., `git add [OG path]; git commit -m "OG-{OG_Number}: Adjust plan before resuming TS{X} based on handoff analysis"`).
7.  **Resume Execution (Branching from `main`):** Once the state is understood, verified, and the OG is adjusted (if needed), continue the Orchestrator workflow as defined in the global Orchestrator rules (.roo/rules-orche-global/rules.md), starting from the step for initiating a Task Set branch. This step explicitly involves creating a *new branch* from the potentially updated `main` branch for the **Current/Next Task Set ({X})**. Use the *original* OG as the primary guide.
8.  **Update Original OG (During Execution on Feature Branch):** Ensure all progress, logs, and status changes *during your execution on the feature branch* are accurately reflected *only* in the *original* OG file (`[Relative Path to the Original OG File]`) as you complete tasks and Task Sets. Do not update this handoff document further.
9.  **Initiate Workflow:** After successfully verifying the state and potentially adjusting the OG on `main`, `suggest` creating a new subtask in Orchestrator Mode to formally begin execution of Task Set {X}. If approved, at minimum, provide to the subtask the path to the original OG (`[Relative Path to the Original OG File]`) and confirm the starting Task Set number ({X}) as context for the new task. If more context is helpful, provide it.