# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""File discovery utilities."""

from pathlib import Path
from typing import Iterator


def find_files(root_dir: Path, recursive: bool = True) -> Iterator[Path]:
    """Find all files in a directory, optionally recursively."""
    yield from (
        (p for p in root_dir.rglob("*") if p.is_file())
        if recursive
        else (p for p in root_dir.glob("*") if p.is_file())
    )
