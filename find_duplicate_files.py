#!/usr/bin/env python3
"""
Find duplicate files across subdirectories based on filename and filesize.
Duplicates are defined as files with identical names AND sizes.
"""

import os
from collections import defaultdict
from typing import Dict, List, Tuple
import sys
from pathlib import Path


def format_size(size_bytes: int) -> str:
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def find_duplicate_files(root_dir: str) -> Dict[Tuple[str, int], List[str]]:
    """
    Scan directory tree for files with matching names and sizes.
    
    Args:
        root_dir: Starting directory path to scan
    
    Returns:
        Dictionary mapping (filename, size) to list of directory paths
    """
    file_map = defaultdict(list)
    root_dir = os.path.abspath(root_dir)

    try:
        # Walk directory tree
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                try:
                    filepath = os.path.join(dirpath, filename)
                    # Get file size
                    file_size = os.path.getsize(filepath)
                    # Store directory path for this filename+size combination
                    file_map[(filename, file_size)].append(dirpath)
                except (OSError, PermissionError) as e:
                    print(f"Error accessing {filepath}: {e}", file=sys.stderr)
                    continue

    except (OSError, PermissionError) as e:
        print(f"Error scanning directory {root_dir}: {e}", file=sys.stderr)
        return {}

    # Filter out non-duplicates (files that only appear once)
    return {k: v for k, v in file_map.items() if len(v) > 1}


def print_duplicates(duplicates: Dict[Tuple[str, int], List[str]]) -> None:
    """
    Print formatted report of duplicate files, grouped by category.
    Include summary of directory pairs containing duplicates.
    
    Args:
        duplicates: Dictionary mapping (filename, size) to list of directory paths
    """
    if not duplicates:
        print("\nNo duplicate files found.")
        return

    # Track directory pairs that contain duplicates
    dir_pairs: Dict[Tuple[str, str], List[Tuple[str, int]]] = defaultdict(list)
    
    # Group files by category
    categories: Dict[str, List[Tuple[Tuple[str, int], List[str]]]] = defaultdict(list)
    total_wasted_space = 0
    
    for (filename, size), directories in duplicates.items():
        # Identify category based on filename pattern
        if "_depth_" in filename:
            category = "Depth Maps"
        elif "_main_" in filename:
            category = "Main Images"
        else:
            category = "Other Files"
            
        # Calculate wasted space (size * (num_copies - 1))
        total_wasted_space += size * (len(directories) - 1)
        categories[category].append(((filename, size), directories))
        
        # Track directory pairs containing duplicates
        sorted_dirs = sorted(directories)
        for i in range(len(sorted_dirs)):
            for j in range(i + 1, len(sorted_dirs)):
                dir_pair = (sorted_dirs[i], sorted_dirs[j])
                dir_pairs[dir_pair].append((filename, size))

    # Print summary by category
    print(f"\nFound {len(duplicates)} sets of duplicate files:\n")
    
    # Flatten list of all directories for common prefix calculation
    all_dirs = []
    for dirs in duplicates.values():
        all_dirs.extend(dirs)
    common_prefix = os.path.commonpath(all_dirs)
    
    for category, items in sorted(categories.items()):
        print(f"=== {category} ===")
        for (filename, size), directories in sorted(items):
            print("\nDuplicate Found:")
            print(f"  File Name: {filename}")
            print(f"  File Size: {format_size(size)}")
            print("  Locations:")
            for directory in sorted(directories):
                # Show relative path from common prefix for readability
                rel_path = os.path.relpath(directory, common_prefix)
                print(f"    - .../{rel_path}")
        print("-" * 80)
    
    # Print space savings summary
    print(f"\nTotal space that could be saved by removing duplicates: {format_size(total_wasted_space)}")
    
    # Print directory pairs summary
    print("\nDirectory Pairs Containing Duplicates:")
    print("-" * 80)
    
    common_prefix = os.path.commonpath([d for dirs in duplicates.values() for d in dirs])
    
    for (dir1, dir2), files in sorted(dir_pairs.items(), key=lambda x: len(x[1]), reverse=True):
        # Show relative paths from common prefix
        rel_dir1 = os.path.relpath(dir1, common_prefix)
        rel_dir2 = os.path.relpath(dir2, common_prefix)
        
        total_size = sum(size for _, size in files)
        print(f"\nPair containing {len(files)} duplicate files (Total: {format_size(total_size)}):")
        print(f"  - .../{rel_dir1}")
        print(f"  - .../{rel_dir2}")


def main():
    # Hardcoded path - can be modified or made into a command line argument
    target_dir = r"C:\Users\Casey\OneDrive\CSM\CD\_WIP\.Next\_3Dnext\_DOWNselect"
    
    if not os.path.exists(target_dir):
        print(f"Error: Directory not found: {target_dir}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Scanning directory: {target_dir}")
    print("This may take a while depending on the number of files...")
    
    duplicates = find_duplicate_files(target_dir)
    print_duplicates(duplicates)


if __name__ == "__main__":
    main()