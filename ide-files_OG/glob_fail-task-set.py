import subprocess
import argparse
import sys
import os
import shutil
import tempfile
import re
# Removed: from components.confirmation_popup import show_confirmation

def get_current_branch():
    """Gets the current git branch name."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                               capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error detecting current branch: {e}")
        sys.exit(1)

def get_all_changed_files():
    """Gets a list of all modified (tracked) and untracked files."""
    try:
        # Get modified tracked files
        modified_result = subprocess.run(['git', 'ls-files', '-m'],
                                         capture_output=True, text=True, check=True)
        # Get untracked files
        untracked_result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'],
                                          capture_output=True, text=True, check=True)

        all_files = modified_result.stdout.splitlines() + untracked_result.stdout.splitlines()
        return all_files
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        sys.exit(1)

def format_fail_commit_message(branch_name, reason):
    """Formats the commit message based on branch name and failure reason."""
    # Regex to match branch name format OG-XX_TS-YY or OG-XX_TS-YY_attempt-ZZ
    match = re.match(r'^OG-(\d+)_TS-(\d+)(_attempt-(\d+))?$', branch_name)

    if match:
        og_number = match.group(1)
        task_set_number = match.group(2)
        attempt_number = match.group(4) if match.group(4) else '1'
        return f'❌ OG-{og_number} post-TS-{task_set_number}_attempt-{attempt_number}: Task failed: {reason}'
    else:
        # Fallback for branches not matching the pattern (e.g., main)
        return f'❌ Cleanup after task failure: {reason}'

def filter_needed_files(files):
    """Filters the list for .md files NOT matching the _##_OG_ pattern."""
    # Pattern matches filenames starting with _##_OG_ and ending with .md
    # Anchored to the start (^) of the basename.
    og_pattern = re.compile(r'^_(\d{2})_OG_.*\.md$')
    needed = []
    print("  Filtering needed files:") # Added for clarity
    for f in files:
        basename = os.path.basename(f)
        # Check if it's an MD file and its basename does NOT match the OG pattern
        if basename.endswith('.md') and not og_pattern.match(basename):
             needed.append(f) # Keep the original full path 'f'
             print(f"    -> Preserving: {f}") # Debug print
        elif basename.endswith('.md'):
             print(f"    -> Skipping (OG pattern): {f}") # Debug print
        # else: # Optional: print files skipped for not being .md
        #    print(f"    -> Skipping (not .md): {f}")
    return needed

def move_files_to_temp(files, temp_root):
    """Moves files to a temporary directory, preserving structure. Returns mapping."""
    original_to_temp_map = {}
    for original_path in files:
        try:
            # Create the same directory structure within the temp folder
            temp_path = os.path.join(temp_root, original_path)
            temp_dir = os.path.dirname(temp_path)
            os.makedirs(temp_dir, exist_ok=True)

            # Move the file
            if os.path.exists(original_path): # Ensure file exists before moving
                shutil.move(original_path, temp_path)
                original_to_temp_map[original_path] = temp_path
                print(f"  Moved: {original_path} -> {temp_path}")
            else:
                 print(f"  Skipping move (already moved or deleted?): {original_path}")

        except Exception as e:
            print(f"Error moving {original_path} to temp: {e}")
            # Attempt to restore any files already moved in this batch if error occurs?
            # For now, just report error and continue.
    return original_to_temp_map

def restore_files_from_temp(original_to_temp_map):
    """Moves files back from the temporary directory to their original locations."""
    for original_path, temp_path in original_to_temp_map.items():
        try:
            # Ensure the original destination directory exists
            original_dir = os.path.dirname(original_path)
            os.makedirs(original_dir, exist_ok=True)

            # Move the file back
            if os.path.exists(temp_path): # Ensure temp file exists
                shutil.move(temp_path, original_path)
                print(f"  Restored: {temp_path} -> {original_path}")
            else:
                print(f"  Skipping restore (temp file missing?): {temp_path}")

        except Exception as e:
            print(f"Error restoring {original_path} from {temp_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Clean up after failed task')
    parser.add_argument('--r', required=False, default="No reason provided", help='Failure Reason: (default: "No reason provided")')
    parser.add_argument('--delete-branch', action='store_true', help='Delete the branch after cleanup (default is to preserve)')
    parser.add_argument(
        "--main-branch",
        type=str,
        default="main",
        help="The name of the main integration branch (default: main)."
    )
    args = parser.parse_args()

    try:
        current_branch = get_current_branch()
        main_branch = args.main_branch # Use the provided main branch name
        branch_to_delete = current_branch if current_branch != main_branch else None

        print("1. Getting list of all changed files...")
        all_changed_files = get_all_changed_files()
        if not all_changed_files:
            print("No modified or untracked files found.")
        else:
            print(f"  Found changed files: {all_changed_files}")

        print("2. Committing all changes...")
        if all_changed_files:
             # Check if there's anything to commit (git status --porcelain)
            status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
            if status_result.stdout.strip():
                print("  Staging all changes...")
                subprocess.run(['git', 'add', '.'], check=True)
                print("  Creating commit...")
                commit_message = format_fail_commit_message(current_branch, args.r)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                print(f"  Committed with message: '{commit_message}'")
            else:
                print("  No changes staged for commit.")
        else:
            print("  No changes detected, skipping commit.")

        print("3. Identifying needed files to preserve...")
        needed_files = filter_needed_files(all_changed_files)
        if needed_files:
            print(f"  Needed files: {needed_files}")
        else:
            print("  No specific .md files need preservation.")

        temp_dir = None
        original_to_temp_map = {}
        if needed_files:
            print("4. Moving needed files to temporary location...")
            temp_dir = tempfile.mkdtemp(prefix='git_fail_')
            print(f"  Created temp directory: {temp_dir}")
            original_to_temp_map = move_files_to_temp(needed_files, temp_dir)

        print(f"5. Checking out {main_branch} branch...")
        subprocess.run(['git', 'checkout', main_branch], check=True)
        print(f"  Successfully checked out '{main_branch}'.")

        if args.delete_branch and branch_to_delete:
            print(f"6. Deleting branch {branch_to_delete} (--delete-branch flag set)...")
            subprocess.run(['git', 'branch', '-D', branch_to_delete], check=True)
            print(f"  Successfully deleted branch '{branch_to_delete}'.")
        elif args.delete_branch:
             print(f"6. Skipping branch deletion (already on '{main_branch}' or no branch to delete, despite --delete-branch flag).")
        else:
             print("6. Preserving branch (default behavior).")

        if original_to_temp_map:
            print("7. Restoring needed files...")
            restore_files_from_temp(original_to_temp_map)
            print("  Finished restoring files.")
        else:
            print("7. No files to restore.")

        print("8. Committing restored files on main branch...")
        # Stage any restored files (or other changes if any)
        subprocess.run(['git', 'add', '.'], check=True)
        # Check if there's anything staged to commit
        status_result_after_restore = subprocess.run(['git', 'diff', '--staged', '--quiet'], check=False) # check=False as it returns 1 if there are staged changes
        if status_result_after_restore.returncode == 1:
            # Use branch name to get OG/TS/Attempt numbers
            match = re.match(r'^OG-(\d+)_TS-(\d+)(_attempt-(\d+))?$', branch_to_delete or '')
            if match:
                og_number = match.group(1)
                task_set_number = match.group(2)
                attempt_number = match.group(4) if match.group(4) else '1'
                # Count preserved PR files
                pr_count = len(original_to_temp_map)
                commit_message_restore = f"OG-{og_number} TS-{task_set_number} Attempt-{attempt_number}: ❌ Failed. [{pr_count}] PRs preserved."
            else:
                # Fallback if not on a task branch
                commit_message_restore = "❌ Failed. Generic branch cleanup complete."
            subprocess.run(['git', 'commit', '-m', commit_message_restore], check=True)
            print(f"  Successfully committed restored files with message: '{commit_message_restore}'")
        else:
            print("  No restored files staged for commit.")

        # Clean up temp directory if it was created
        if temp_dir and os.path.exists(temp_dir):
            print(f"9. Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)
        else:
            print("9. No temporary directory to clean up.")

        print("\nOperation completed successfully!")

        # Removed: Confirmation Popup

        # Show final git status
        print("\nFinal git status:")
        subprocess.run(['git', 'status'], check=False)

        sys.exit(0)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()