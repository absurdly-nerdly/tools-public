#!/usr/bin/env python3
"""
Automates the Git workflow for starting a new Task Set branch in the Orchestrator Guide process.

Handles both initial attempts and retries with different branch naming formats.

Usage:
    Initial attempt: python glob_start-task-set-branch.py <og_file_path> <og_number> <task_set_number> [--main-branch <branch_name>]
    Retry attempt: python glob_start-task-set-branch.py <og_file_path> <og_number> <task_set_number> <attempt_number> [--main-branch <branch_name>]
"""

import subprocess
import sys
import re
import argparse

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
    parser = argparse.ArgumentParser(description="Start a new Task Set branch.")
    parser.add_argument("og_file_path", help="Path to the Orchestrator Guide file.")
    parser.add_argument("og_number", help="OG number.")
    parser.add_argument("task_set_number", help="Task Set number.")
    parser.add_argument("attempt_number", nargs='?', type=int, default=1, help="Attempt number (default: 1).")
    parser.add_argument(
        "--main-branch",
        type=str,
        default="main",
        help="The name of the main integration branch (default: main)."
    )
    args = parser.parse_args()

    og_file_path = args.og_file_path
    og_number = args.og_number
    task_set_number = args.task_set_number
    attempt_number = args.attempt_number
    main_branch = args.main_branch

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
    print(f"\nEnsuring clean {main_branch} branch...")
    run_git_command(["checkout", main_branch])

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