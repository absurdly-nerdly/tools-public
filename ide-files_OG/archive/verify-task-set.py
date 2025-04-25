import argparse
import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor

def run_command(command, capture=True, check=True, suppress_output=False):
    """Runs a shell command, captures output, and handles errors."""
    command_str = ' '.join(command)
    if not suppress_output:
        print(f"Executing: {command_str}")
    try:
        process = subprocess.run(command_str, shell=True, check=check, 
                               capture_output=capture, text=True, 
                               cwd=os.getcwd(), encoding='utf-8', 
                               errors='replace')
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
        print(f"Error executing command: {command_str}")
        print(f"Return code: {e.returncode}")
        if stdout:
            print(f"Output:\n{stdout}")
        if stderr:
            print(f"Error output:\n{stderr}")
        return e
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def run_tests_parallel(branch_name, url, log_prompt=None):
    """Run Playwright test and verification suite in parallel"""
    with ThreadPoolExecutor() as executor:
        # Run Playwright test
        playwright_future = executor.submit(
            run_command,
            ["npx", "playwright", "test", "tests/models-page_rendering.spec.ts", "--reporter=list"],
            suppress_output=True
        )
        
        # Build verification suite command
        verification_cmd = ["python", "_20_user-scripts/verification-suite.py", "--url", url]
        if log_prompt:
            verification_cmd.extend(["--log-prompt", f'"{log_prompt}"'])
        
        # Run verification suite
        verification_future = executor.submit(
            run_command,
            verification_cmd,
            suppress_output=True
        )
        
        # Get results
        playwright_result = playwright_future.result()
        verification_result = verification_future.result()
        
        return {
            "playwright": playwright_result,
            "verification": verification_result
        }

def main():
    parser = argparse.ArgumentParser(description="Verify changes on a branch.")
    parser.add_argument(
        "-b", "--branch",
        type=str,
        required=True,
        help="The branch name being verified."
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL to test against (e.g. http://localhost:5173/models)"
    )
    parser.add_argument(
        "--log-prompt",
        type=str,
        default=None,
        help="Optional custom prompt for console log analysis"
    )
    args = parser.parse_args()
    branch_name = args.branch

    print(f"\n--- Verifying Branch {branch_name} ---")

    # Print initial git status
    print("\nInitial git status:")
    run_command(["git", "status"], suppress_output=False)

    # Stage changes
    print("\nStep 1: Staging changes...")
    stage_result = run_command(["git", "add", "."], suppress_output=True)
    if isinstance(stage_result, subprocess.CalledProcessError) or stage_result is None:
        print("Error: Failed to stage changes. Verification cannot proceed reliably.")
        if hasattr(stage_result, 'stderr') and stage_result.stderr:
            print(f"Staging Error Output:\n{stage_result.stderr.strip()}")
        return

    # Run tests in parallel
    print("\nStep 2: Running tests in parallel...")
    test_results = run_tests_parallel(branch_name, args.url, args.log_prompt)

    print("\n--- Test Execution Complete ---")
    print("\nPlaywright render test output:")
    if test_results['playwright'].stdout:
        print(test_results['playwright'].stdout)
    if test_results['playwright'].stderr:
        print("Errors:", test_results['playwright'].stderr)
    
    print("\nVerification suite output:")
    if test_results['verification'].stdout:
        print(test_results['verification'].stdout)
    if test_results['verification'].stderr:
        print("Errors:", test_results['verification'].stderr)

    # Print final git status
    print("\nFinal git status:")
    run_command(["git", "status"], suppress_output=False)

if __name__ == "__main__":
    main()