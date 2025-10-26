# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Ignore file handling for .licenseignore and .gitignore files."""

from pathlib import Path
from typing import List


class IgnoreRule:
    def __init__(self, pattern: str, negate: bool = False, dir_only: bool = False):
        self.pattern = pattern
        self.negate = negate
        self.dir_only = dir_only


def load_ignore_file(path: Path | None) -> List[IgnoreRule]:
    """Load ignore rules from a .licenseignore or .gitignore file."""
    rules: List[IgnoreRule] = []
    if path is None or not path or not path.exists():
        return rules
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            negate = line.startswith("!")
            dir_only = line.endswith("/")
            pattern = line
            if negate:
                pattern = pattern[1:]
            if dir_only:
                pattern = pattern[:-1]
            rules.append(IgnoreRule(pattern, negate, dir_only))
    return rules
