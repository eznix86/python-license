# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""
Automatically adds or updates SPDX license and copyright headers in source files.
Designed for use in pre-commit hooks.

Usage:
    license <license> "<author>" [options]

Examples:
    license GPL-2.0-or-later "John Doe" --check
    license MIT "Jane Smith" --fix --dir src/
    license Apache-2.0 "ACME Corp" --ignore-file .licenseignore --fix
"""

import argparse
import sys
from pathlib import Path

from .file_utils import find_files
from .header import SPDXHeader
from .ignore import load_ignore_file


def main():
    parser = argparse.ArgumentParser(
        description="SPDX Header Manager - Add/update license headers"
    )
    parser.add_argument(
        "license", help="SPDX license identifier (e.g., GPL-2.0-or-later)"
    )
    parser.add_argument("author", help="Copyright holder name")
    parser.add_argument(
        "--check", action="store_true", help="Check files without modifying (default)"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Fix files by adding/updating headers"
    )
    parser.add_argument(
        "--dir", type=Path, default=Path("."), help="Root directory to process"
    )
    parser.add_argument("--year", help="Copyright year (default: current year)")
    parser.add_argument(
        "--no-recursive", action="store_true", help="Don't process subdirectories"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all files")
    parser.add_argument(
        "--ignore-file",
        type=Path,
        help="Path to ignore file (.licenseignore or .gitignore). By default uses .licenseignore or .gitignore",
    )
    parser.add_argument(
        "--notice-template",
        type=Path,
        help="Path to notice template file to append after copyright",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Specific files to process (overrides --dir)",
    )
    args = parser.parse_args()

    if args.check and args.fix:
        parser.error("Cannot use both --check and --fix")
    if not args.check and not args.fix:
        args.check = True

    ignore_file = None
    if args.ignore_file and args.ignore_file.exists():
        ignore_file = args.ignore_file
    elif Path(".licenseignore").exists():
        ignore_file = Path(".licenseignore")
    elif Path(".gitignore").exists():
        ignore_file = Path(".gitignore")

    ignore_rules = load_ignore_file(ignore_file)
    manager = SPDXHeader(args.license, args.author, args.year, ignore_rules, args.notice_template)

    files_iter = (
        args.files
        if args.files
        else find_files(args.dir, recursive=not args.no_recursive)
    )
    total, updated, errors = 0, 0, 0

    for filepath in files_iter:
        if manager.should_skip_file(filepath):
            continue
        total += 1
        changed, msg = manager.process_file(filepath, fix=args.fix)
        if "Error" in msg:
            errors += 1
        elif changed:
            updated += 1
        if args.verbose or changed or "Error" in msg:
            print(msg)

    print("=" * 60)
    print(f"Total files processed: {total}")
    if args.check:
        print(f"Files needing update: {updated}")
        if updated > 0:
            print("Run with --fix to update headers")
            sys.exit(1)
    else:
        print(f"Files updated: {updated}")
    if errors > 0:
        print(f"Errors: {errors}")
        sys.exit(1)
