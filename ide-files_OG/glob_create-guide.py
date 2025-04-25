import argparse
import os
import re
import shutil
import sys

def create_guide(guide_type, description):
    """Creates a new OG file from the global template."""

    templates_dir = "ide-files_OG" # Assuming global templates are downloaded here
    target_dir = "_00_user-docs"
    template_file = os.path.join(templates_dir, "glob_OG-template.md") # Use the global template

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
        # Only print the path on full success
        print(f"Successfully created guide: {new_filepath}")
    except FileNotFoundError:
        print(f"Error: Global template file '{template_file}' not found.")
        print("Please ensure you have downloaded the global Orchestrator assets.")
    except Exception as e:
        print(f"Error copying template file '{template_file}' to '{new_filepath}': {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new OG file from the global template.")
    parser.add_argument("guide_type", help="Type of guide (OG)") # Only OG relevant now
    parser.add_argument("description", nargs='+', help="Description of the guide (used in filename)")
    # Removed --url and --log-prompt arguments

    args = parser.parse_args()

    if args.guide_type.upper() != "OG":
        print("Error: This script now only supports creating 'OG' guides.")
        sys.exit(1)

    create_guide(args.guide_type, args.description)