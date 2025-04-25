import argparse
import os
import re
import shutil
import subprocess
import sys

def run_verification_suite(url, log_prompt=None):
    """Runs the verification suite script and returns its output."""
    command = ["python", "_20_user-scripts/verification-suite.py", "--url", url]
    if log_prompt:
        # Ensure the prompt is properly quoted for the shell, especially if it contains spaces
        command.extend(["--log-prompt", f'"{log_prompt}"'])

    command_str = ' '.join(command)
    print(f"Running verification suite: {command_str}")
    try:
        # Use shell=True because we might have quoted arguments like --log-prompt
        result = subprocess.run(
            command_str,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        print("Verification suite completed successfully.")
        return command_str, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running verification suite: {command_str}")
        print(f"Return code: {e.returncode}")
        stderr = e.stderr.strip() if e.stderr else "No stderr captured."
        stdout = e.stdout.strip() if e.stdout else "No stdout captured."
        print(f"Stderr:\n{stderr}")
        print(f"Stdout:\n{stdout}")
        # Return the error details so they can be logged in the OG
        error_output = f"ERROR: Verification suite failed!\nStderr:\n{stderr}\nStdout:\n{stdout}"
        return command_str, error_output
    except Exception as e:
        print(f"Unexpected error running verification suite: {e}")
        return command_str, f"UNEXPECTED ERROR: {e}"


def update_og_initial_state(og_filepath, command_run, verification_output, log_prompt_used):
    """Reads the OG file, updates the Initial State section, and writes it back."""
    try:
        with open(og_filepath, 'r', encoding='utf-8') as f:
            og_content = f.read()

        initial_state_marker = "## Initial State"
        task_sets_marker = "## Task Sets"
        start_index = og_content.find(initial_state_marker)
        end_index = og_content.find(task_sets_marker)

        if start_index == -1 or end_index == -1:
            print(f"Error: Could not find '{initial_state_marker}' or '{task_sets_marker}' markers in {og_filepath}")
            return False

        # Construct the new Initial State section content
        new_initial_state_content = f"""{initial_state_marker}

*   **Command:** `{command_run}`
*   **Log Prompt:** {log_prompt_used if log_prompt_used else "none"}
*   **Results:**
    ```
{verification_output}
    ```

- - - - - - - - -
"""
        # Replace the old section (including the marker and separator)
        # Find the start of the content to replace (after the marker)
        content_start = start_index + len(initial_state_marker)
        # Find the end of the content to replace (before the next marker's separator)
        separator_before_task_sets = "- - - - - - - - -"
        content_end = og_content.rfind(separator_before_task_sets, start_index, end_index)
        if content_end == -1:
             print(f"Error: Could not find separator before Task Sets in {og_filepath}")
             return False

        # Build the final content
        final_og_content = og_content[:start_index] + new_initial_state_content + og_content[end_index:] # Keep the Task Sets marker

        with open(og_filepath, 'w', encoding='utf-8') as f:
            f.write(final_og_content)
        print(f"Successfully updated Initial State in {og_filepath}")
        return True

    except FileNotFoundError:
        print(f"Error: OG file not found at {og_filepath}")
        return False
    except Exception as e:
        print(f"Error updating OG file {og_filepath}: {e}")
        return False


def create_guide(guide_type, description, url, log_prompt=None):
    """Creates a new OG file, runs verification, and populates Initial State."""

    templates_dir = "_10_ide"
    target_dir = "_00_user-docs"
    template_file = os.path.join(templates_dir, "OG-template.md") # Always use _OG-template.md

    if guide_type.upper() not in ("OG", "TG"):
        print("Invalid guide type. Must be 'OG' or 'TG'.")
        return

    # Find the next available number
    next_number = 1
    try:
        existing_files = os.listdir(target_dir)
        for filename in existing_files:
            match = re.match(r"_(\d+)_", filename)
            if match:
                number = int(match.group(1))
                next_number = max(next_number, number + 1)
    except FileNotFoundError:
        print(f"Warning: Target directory '{target_dir}' not found. Creating it.")
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(f"Error reading target directory '{target_dir}': {e}")
        return # Cannot safely determine next number

    # Construct the new filename
    description_str = " ".join(description)
    safe_description = re.sub(r'[\\/*?:"<>|]', '', description_str).replace(' ', '-') # Sanitize description
    new_filename = f"_{next_number:02d}_{guide_type.upper()}_{safe_description}.md"
    new_filepath = os.path.join(target_dir, new_filename)

    # Copy the template file
    try:
        shutil.copyfile(template_file, new_filepath)
        print(f"Created new guide file: {new_filepath}")
    except Exception as e:
        print(f"Error copying template file '{template_file}' to '{new_filepath}': {e}")
        return

    # Run verification suite and get output
    command_run, verification_output = run_verification_suite(url, log_prompt)

    # Update the OG file with the initial state
    if not update_og_initial_state(new_filepath, command_run, verification_output, log_prompt):
         print("Failed to update OG with initial state. Please check the file manually.")
         # Still print the path so Orchestrator knows the file exists
         print(f"Guide file created at: {new_filepath}")
    else:
         # Only print the path on full success
         print(f"Successfully created and initialized guide: {new_filepath}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new OG file and capture initial state.")
    parser.add_argument("guide_type", help="Type of guide (OG)") # Only OG relevant now
    parser.add_argument("description", nargs='+', help="Description of the guide (used in filename)")
    parser.add_argument("--url", required=True, help="URL for the verification suite")
    parser.add_argument("--log-prompt", help="Optional custom prompt for verification suite log analysis")
    args = parser.parse_args()

    if args.guide_type.upper() != "OG":
        print("Error: This script now only supports creating 'OG' guides.")
        sys.exit(1)

    create_guide(args.guide_type, args.description, args.url, args.log_prompt)