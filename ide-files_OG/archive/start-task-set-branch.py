#!/usr/bin/env python3
"""
Automates the Git workflow for starting a new Task Set branch in the Orchestrator Guide process.

Handles both initial attempts and retries with different branch naming formats.

Usage:
    Initial attempt: python start-task-set-branch.py <og_file_path> <og_number> <task_set_number>
    Retry attempt: python start-task-set-branch.py <og_file_path> <og_number> <task_set_number> <attempt_number>
"""

import subprocess
import sys
import re

def run_git_command(cmd, check=True):
    """Run a Git command and return its output."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(cmd)}")
        print(e.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) not in [4, 5]:
        print("Usage (initial attempt): python start-task-set-branch.py <og_file_path> <og_number> <task_set_number>")
        print("Usage (retry attempt): python start-task-set-branch.py <og_file_path> <og_number> <task_set_number> <attempt_number>")
        sys.exit(1)

    og_file_path = sys.argv[1]
    og_number = sys.argv[2]
    task_set_number = sys.argv[3]
    attempt_number = int(sys.argv[4]) if len(sys.argv) == 5 else 1

    # Validate number formats
    if not re.match(r'^\d+$', og_number):
        print("Error: OG number must be numeric")
        sys.exit(1)
    if not re.match(r'^\d+$', task_set_number):
        print("Error: Task Set number must be numeric")
        sys.exit(1)
    if attempt_number < 1:
        print("Error: Attempt number must be 1 or greater")
        sys.exit(1)

    # Show initial status
    print("\nInitial git status:")
    print(run_git_command(["status"]))
    
    # Ensure we're on main branch
    print("\nEnsuring clean main branch...")
    run_git_command(["checkout", "main"])
    
    # Check git status
    status_output = run_git_command(["status", "--porcelain"])
    status_lines = status_output.split('\n') if status_output else []
    has_og_file = False
    has_other_files = False

    for line in status_lines:
        file_path = line[3:]
        if file_path == og_file_path:
            has_og_file = True
        else:
            has_other_files = True

    # Commit all changes if any exist
    if status_lines:
        print("Staging all changes...")
        run_git_command(["add", "."])
        
        commit_msg = f"OG-{og_number} TS-{task_set_number}: Doc update before Attempt-{attempt_number}"
        run_git_command(["commit", "-m", commit_msg])
        
        if has_og_file and has_other_files:
            print(f"Committed {og_file_path} and other files.")
        elif has_og_file:
            print(f"Committed {og_file_path}.")
        else:
            print("Committed other files (no OG file changes).")

    # Create new branch with appropriate format
    if attempt_number > 1:
        branch_name = f"OG-{og_number}_TS-{task_set_number}_attempt-{attempt_number}"
        print(f"Creating retry branch (attempt {attempt_number}): {branch_name}")
    else:
        branch_name = f"OG-{og_number}_TS-{task_set_number}"
        print(f"Creating initial branch: {branch_name}")
    
    run_git_command(["checkout", "-b", branch_name])
    
    # Show final status
    print("\nTask Set branch created successfully. Current status:")
    print(run_git_command(["status"]))

if __name__ == "__main__":
    main()