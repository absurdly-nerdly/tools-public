# Orchestrator Guide: Debrief Template & Instructions

## 1. Purpose

This document provides a template and instructions for Orchestrators to document suggestions and debug findings in dedicated files and generate the final `attempt_completion` response after successfully completing all High-Level Objectives defined in an Orchestrator Guide (OG).

## 2. Orchestrator Instructions: OG Completion Workflow

Upon successful completion of all High-Level Objectives in an OG:

1.  **Finalize OG State:** Before proceeding, ensure the completed OG file on the `main` branch accurately reflects the final state of execution. Verify all Task Set statuses (✅/❌/✖️), individual task statuses, validation step statuses, Failure Attempts counts, Problem Report lists, and TSx Log sections are complete and accurate.

2.  **Read Final OG State:** Read the final, merged state of the completed OG file from the `main` branch.
3.  **Read All PRs:** Read all Problem Report (PR) files created during the OG's execution.
4.  **Generate & Append Tree Diagram:** Generate the OG execution flow tree diagram (following the format in `_00_user-docs/OG Flows.md`) and append it to the `_00_user-docs/OG Flows.md` file.
5.  **Consolidate Information:** Gather the following information from the final OG state and all associated PRs:
    *   Deviations from the original plan.
    *   Important notes recorded during execution.
    *   Suggestions for codebase improvements for maintainability.
    *   Suggestions for other significant codebase improvements.
    *   Suggestions for automation improvements (e.g. testing, improvements to scripts, etc.).
    *   Suggestions for rule enhancements (Orchestrator, O-Coder, Debug, Analyst, etc.).
    *   Confirmed, helpful debugging steps and findings.
6.  **Update Dedicated Files:**
    *   **`_00_user-docs\continuous-improvement.md`:**
        *   Add consolidated codebase suggestions.
        *   Mark `complete` (✅) any existing/past items that are now resolved.
        *   Mark `new info` (🎁) any existing/past items that may potentially now be resolved based on new info/code state.
    *   **`_00_user-docs/debug_history.md`:**
        *   Add confirmed, helpful debug findings under a new heading `## Findings from OG-{OG_Number}`.
        *   **Format:** Document the symptom, the successful diagnostic step/tool usage, and the confirmed finding. Prepend each finding set with `- [OG-{OG_Number}/PR-{PR_Number or TS-X}]`. Add the commit hash of the final merge commit if relevant.
        *   **Location/Sort:** Add new OG sections chronologically.
7.  **Prepare & Create Debrief File:** Use the template below (`## 3. OG Debrief Template`) to structure the full completion report. Create a *new file* named `_00_user-docs/_{OG_Number}_OG_Debrief.md`. Write the fully populated report content (including Suggested Next Steps) into this new file using `write_to_file`.
8.  **Execute Brief `attempt_completion`:** Use the `attempt_completion` tool with a summarized result message referencing the Debrief file and it's contents.

---

## 3. OG Debrief Template

**(Copy and populate the following structure for the `_00_user-docs/_{OG_Number}_OG_Debrief.md` file, and summarize this in `attempt_completion`)**

**OG Completion Report**

**Orchestrator Guide:** `[Path to the completed OG file]`
**High-Level Objectives:**
*   [List the HLOs from the OG]
*   [...]

**Outcome:** [State whether all HLOs were met, e.g., "All High-Level Objectives were successfully achieved."]

**Execution Summary:**
*   [Provide a brief narrative summary of the execution flow, mentioning key successes, failures, and resolutions. Reference Task Set numbers and PRs.]
*   [...]

**Generated Artifacts:**
*   **Problem Reports:**
    *   `[Path to PR-1]` ([Briefly note status, e.g., Resolved, Root cause addressed])
    *   `[Path to PR-2]` ([Briefly note status])
    *   [...]

**Consolidated Deviations (from High-Level Plan):**
*   [List significant deviations from the original OG plan encountered during execution. Reference TS/PR numbers.]
*   [...]

**Consolidated Important Notes:**
*   [List key observations, environment issues, tool behaviors, or critical findings recorded during execution. Reference TS/PR numbers.]
*   [...]

**Documentation Updates Summary:**

*   **Suggestions for Codebase Maintainability (`_00_user-docs\continuous-improvement.md`):**
    *   [List 1-3 (minimum 1) key suggestions added, or state "N suggestions added."]
*   **Rule Suggestions (Refer to relevant rules files):**
    *   [List 1-5 (minimum 1) key suggestions added, or state "N suggestions added."]
*   **Debug History (`_00_user-docs/debug_history.md`):**
    *   [List 1-3 key findings added, or state "N findings added."]

**OG Flow Diagram:**

*   Show the diagram added to the OG Flow file.

**Suggested Next Steps:**
1.  Address any specific critical issues or major deviations noted during execution that require immediate attention.
2.  Consider implementing specific high-priority suggestions documented in `_00_user-docs\continuous-improvement.md`.