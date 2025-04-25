import argparse
import subprocess
import sys
import os
import re

def run_command(command, capture=True, check=True, suppress_output=False):
    """Runs a shell command, captures output, and handles errors."""
    if not suppress_output:
        # Display joined command for logging purposes
        print(f"Executing: {' '.join(command)}")
    try:
        # Use utf-8 encoding for better compatibility and shell=False for security/quoting
        process = subprocess.run(command, shell=False, check=check, capture_output=capture, text=True, cwd=os.getcwd(), encoding='utf-8', errors='replace')
        if not suppress_output:
            if process.stdout:
                print("Output:\n", process.stdout.strip())
            if process.stderr:
                print("Errors:\n", process.stderr.strip())
            print(f"Command successful.")
        return process
    except subprocess.CalledProcessError as e:
        stdout = e.stdout.strip() if e.stdout else ""
        stderr = e.stderr.strip() if e.stderr else ""
        # Display joined command for logging purposes
        print(f"Error executing command: {' '.join(command)}")
        print(f"Return code: {e.returncode}")
        if stdout:
            print(f"Output:\n{stdout}")
        if stderr:
            print(f"Error output:\n{stderr}")
        return e # Return the exception object
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_current_branch():
    """Gets the current git branch name."""
    result = run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], suppress_output=True, check=False) # Don't fail script if git command fails
    if result and result.returncode == 0 and not isinstance(result, Exception):
        return result.stdout.strip()
    print("Warning: Could not determine current git branch.")
    return None

def format_complete_commit_message(branch_name, summary):
    """Formats the commit message based on branch name and summary."""
    # Regex to match branch name format OG-XX_TS-YY or OG-XX_TS-YY_attempt-ZZ
    match = re.match(r'^OG-(\d+)_TS-(\d+)(_attempt-(\d+))?$', branch_name)

    if match:
        og_number = match.group(1)
        task_set_number = match.group(2)
        attempt_number = match.group(4) if match.group(4) else '1'
        return f'✔️ OG-{og_number} post-TS-{task_set_number}_attempt-{attempt_number}: Success: {summary}'
    else:
        # Fallback for branches not matching the pattern (e.g., main)
        return f'✔️ Success: {summary}'

def main():
    parser = argparse.ArgumentParser(description="Complete a task set: commit changes, merge to main, and delete the specified branch.")
    parser.add_argument(
        "-s", "--Summary",
        type=str,
        required=True,
        help="A brief summary description for the task set completion commit."
    )
    parser.add_argument(
        "-b", "--branch",
        type=str,
        required=True,
        help="The specific branch name to commit, merge, and delete."
    )
    parser.add_argument(
        "--main-branch",
        type=str,
        default="main",
        help="The name of the main integration branch (default: main)."
    )
    parser.add_argument(
        "--preserve-branch",
        action="store_true",
        help="Preserve the feature branch (do not delete it after merge)"
    )
    args = parser.parse_args()
    summary = args.Summary
    branch_to_merge = args.branch
    main_branch = args.main_branch # Use the provided main branch name

    commit_message = format_complete_commit_message(branch_to_merge, summary)

    print(f"\n--- Completing Task on Branch {branch_to_merge} ---")
    print(f"Summary: {summary}")
    print(f"Main branch is: {main_branch}")

    current_branch = get_current_branch()
    if not current_branch:
        print("Error: Could not determine current git branch. Cannot safely proceed with merge.")
        sys.exit(1)
    print(f"Current branch is: {current_branch}")

    # Ensure we are on the branch to merge before committing
    if current_branch != branch_to_merge:
         print(f"Switching from '{current_branch}' to branch '{branch_to_merge}' before committing...")
         checkout_result = run_command(["git", "checkout", branch_to_merge])
         if isinstance(checkout_result, subprocess.CalledProcessError) or checkout_result is None:
              print(f"Error: Failed to checkout branch '{branch_to_merge}'.")
              # Attempt to switch back if possible
              if current_branch:
                   run_command(["git", "checkout", current_branch], check=False, suppress_output=True)
              sys.exit(1)
         current_branch = branch_to_merge # Update current branch


    # 1. Stage changes on the feature branch
    print(f"\nStep 1: Staging changes on branch '{branch_to_merge}'...")
    stage_result = run_command(["git", "add", "."])
    if isinstance(stage_result, subprocess.CalledProcessError) or stage_result is None:
        print("Error: Failed to stage changes.")
        sys.exit(1)

    # 2. Commit changes on the feature branch
    print(f"\nStep 2: Committing changes on branch '{branch_to_merge}'...")
    # Check if there are changes to commit first
    status_result = run_command(["git", "status", "--porcelain"], suppress_output=True, check=False)
    # Check return code and stdout for reliability
    if status_result and status_result.returncode == 0 and status_result.stdout:
        print("Changes detected, proceeding with commit.")
        # Use separate arguments for -m and the message to avoid shell interpretation issues
        commit_result = run_command(["git", "commit", "-m", commit_message])
        if isinstance(commit_result, subprocess.CalledProcessError) or commit_result is None:
            print("Error: Failed to commit changes.")
            # Check if it failed because there was nothing to commit (less reliable check)
            if commit_result and hasattr(commit_result, 'stderr') and "nothing to commit" in commit_result.stderr.lower():
                 print("Ignoring commit error: Nothing to commit.")
            elif commit_result and hasattr(commit_result, 'stdout') and "nothing to commit" in commit_result.stdout.lower():
                 print("Ignoring commit error: Nothing to commit.")
            else:
                 sys.exit(1)
        else:
            print("Commit successful.")
    elif status_result and status_result.returncode == 0 and not status_result.stdout:
         print("No changes staged to commit.")
    else:
         print("Warning: Could not reliably determine git status before commit.")
         print("Attempting commit anyway...")
         commit_result = run_command(["git", "commit", "-m", commit_message], check=False)
         if commit_result and commit_result.returncode != 0:
              # Check if it failed because there was nothing to commit
              output_text = (commit_result.stdout or "") + (commit_result.stderr or "")
              if "nothing to commit" in output_text.lower():
                   print("Commit attempt confirmed: Nothing to commit.")
              else:
                   print("Error: Commit attempt failed.")
                   sys.exit(1)
         elif commit_result and commit_result.returncode == 0:
              print("Commit successful.")
         else: # Includes None case
              print("Error: Commit attempt failed or status unknown.")
              sys.exit(1)


    # 3. Checkout main branch
    print(f"\nStep 3: Checking out '{main_branch}' branch...")
    checkout_main_result = run_command(["git", "checkout", main_branch])
    if isinstance(checkout_main_result, subprocess.CalledProcessError) or checkout_main_result is None:
        print(f"Error: Failed to checkout {main_branch} branch.")
        # Attempt to switch back to original branch before exiting
        run_command(["git", "checkout", current_branch], check=False, suppress_output=True)
        sys.exit(1)

    # 4. Merge the feature branch into main
    print(f"\nStep 4: Merging '{branch_to_merge}' into '{main_branch}'...")
    # Use --no-ff to ensure a merge commit is always created for task set history
    merge_result = run_command(["git", "merge", "--no-ff", branch_to_merge])
    if isinstance(merge_result, subprocess.CalledProcessError) or merge_result is None:
        print(f"Error: Failed to merge branch '{branch_to_merge}'.")
        # Check for merge conflicts
        output_text = (merge_result.stdout or "") + (merge_result.stderr or "")
        if "conflict" in output_text.lower():
             print("MERGE CONFLICT DETECTED. Aborting merge.")
             run_command(["git", "merge", "--abort"], check=False) # Attempt to abort
             print(f"Merge aborted. Please resolve conflicts manually on branch '{main_branch}'.")
        else:
             print("Merge failed for an unknown reason.")
        # Attempt to switch back to original branch before exiting
        run_command(["git", "checkout", current_branch], check=False, suppress_output=True)
        sys.exit(1)
    else:
        print("Merge successful.")

    # 5. Clean up branches by default (unless --preserve-branch is set)
    if not args.preserve_branch and branch_to_merge != main_branch:
        print(f"\nStep 5: Cleaning up related branches (--cleanup-branch flag set)...")

        # Determine the base branch name (e.g., OG-12_TS-3)
        base_branch_name = re.sub(r'_attempt-\d+$', '', branch_to_merge)
        print(f"Base identifier for cleanup: {base_branch_name}")

        # List all local branches
        list_all_result = run_command(["git", "branch"], capture=True)
        if not list_all_result or list_all_result.returncode != 0:
            print("Warning: Could not list local branches. Skipping cleanup of related branches.")
        else:
            all_local_branches = [b.strip('* ').strip() for b in list_all_result.stdout.splitlines()]
            branches_to_delete = []

            # Identify base branch and all attempt branches for this Task Set
            for local_branch in all_local_branches:
                if local_branch == base_branch_name or re.match(rf"^{re.escape(base_branch_name)}_attempt-\d+$", local_branch):
                     # Ensure we don't try to delete the branch we are currently on (should be main)
                     if local_branch != main_branch: # Check against main_branch variable
                          branches_to_delete.append(local_branch)
                     else:
                          print(f"Skipping deletion of current branch: {local_branch}")

            if branches_to_delete:
                print(f"Found {len(branches_to_delete)} related branches to force delete:")
                all_deleted_successfully = True
                for branch_to_del in branches_to_delete:
                    print(f"Force deleting branch '{branch_to_del}'...")
                    # Use force delete (-D)
                    del_result = run_command(["git", "branch", "-D", branch_to_del])
                    if isinstance(del_result, subprocess.CalledProcessError) or del_result is None:
                        print(f"Warning: Failed to force delete branch '{branch_to_del}'.")
                        if del_result and hasattr(del_result, 'stderr'):
                            # Check if error is just "not found" which is okay
                            if "not found" not in del_result.stderr.lower():
                                 print(f"Error: {del_result.stderr.strip()}")
                                 all_deleted_successfully = False
                            else:
                                 print(f"(Branch '{branch_to_del}' likely already deleted)")
                        else:
                             all_deleted_successfully = False # Unknown error
                    else:
                        print(f"Successfully force deleted branch '{branch_to_del}'.")
                if not all_deleted_successfully:
                     print("Warning: One or more related branches could not be deleted.")
            else:
                print("No related base or attempt branches found for cleanup.")

    print(f"\n--- Completion for Branch {branch_to_merge} Successful ---")
    print(f"Branch '{branch_to_merge}' merged into '{main_branch}'.")
    if not args.preserve_branch:
        if branch_to_merge == main_branch:
            print("Branch cleanup skipped (cannot delete main branch).")
        else:
            print("Branch cleanup completed.")
    else:
        print("Branch preserved (used --preserve-branch flag).")

    # Print final git status
    print("\nFinal git status:")
    run_command(["git", "status"], check=False)
    sys.exit(0)

if __name__ == "__main__":
    main()