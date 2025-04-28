## Procedure: Sync Local Orchestrator Rules to Global

This procedure outlines the steps to check for recent changes in the local Orchestrator rules and associated IDE files within the `site_CD` project and apply relevant updates to the global rules in the `tools-public` repository.

**Local Project Files:**
- Rules: `c:/Users/lg3580/CSM/dev_cd/site_CD/.roo/rules-orchestrator/rules.md`
- Associated IDE Files: `C:\Users\lg3580\CSM\dev_cd\site_CD\_10_ide\`

**Global Repository Files:**
- Rules: `C:\Users\lg3580\CSM\dev_cd\tools-public\.roo\rules-global-orche\rules.md`
- Associated IDE Files: `C:\Users\lg3580\CSM\dev_cd\tools-public\ide-files_OG\`

**Steps:**

1.  **Navigate to Local Project:**
    *   Open a terminal and change directory to the local project:
        ```powershell
        cd 'c:/Users/lg3580/CSM/dev_cd/site_CD/'
        ```

2.  **Check Git Status:**
    *   Ensure your local repository is up-to-date:
        ```powershell
        git pull origin main ; git status # Or the relevant branch
        ```
    *   Commit or stash any local changes if necessary before proceeding.

3.  **Identify Recent Changes:**
    *   Use `git log` to review recent commits affecting the Orchestrator rules and IDE files. Focus on changes since the last sync.
        ```powershell
        # View log for the rules file
        git log --pretty=format:"%h - %an, %ar : %s" -- .roo/rules-orchestrator/rules.md

        # View log for the IDE directory
        git log --pretty=format:"%h - %an, %ar : %s" -- _10_ide/
        ```
    *   Alternatively, use `git diff` to compare specific commits or branches if you know the relevant range.

4.  **Compare Local and Global Content:**
    *   Read the content of the local and global rules files and associated IDE directories.
    *   Compare the actual content to identify specific differences and determine which changes from the local repository have not yet been applied to the global repository.
    *   Do not rely solely on commit messages to determine what has been updated.

5.  **Summarize Changes & Request Confirmation:**
    *   Based on the `git log` or `git diff` output, create a summarized outline of the changes made to the local rules and IDE files.
    *   Present this summary to the user.
    *   Ask the user to confirm which specific changes should be applied to the global repository files.

6.  **Apply Approved Changes to Global Files:**
    *   Carefully review the approved changes.
    *   Manually apply the *exact* equivalent changes (or as close as possible, adapting for global context if necessary) to:
        *   `C:\Users\lg3580\CSM\dev_cd\tools-public\.roo\rules-global-orche\rules.md`
        *   Files within `C:\Users\lg3580\CSM\dev_cd\tools-public\ide-files_OG\` corresponding to the modified local IDE files.
    *   Use appropriate tools (`read_file`, `apply_diff`, `write_to_file`) for editing.

7.  **Verify Global Changes:**
    *   User should verify that the changes made to the global files are correct and complete.