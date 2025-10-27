# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""SPDX header management for source files."""

import fnmatch
import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from .comment_styles import COMMENT_STYLE_GROUPS, EXTENSION_STYLES, SPECIAL_FILES, CommentStyle
from .constants import EXCLUDE_DIRS, EXCLUDE_PATTERNS
from .ignore import IgnoreRule


class SPDXHeader:
    """Manages SPDX license headers in files."""

    def __init__(
        self,
        license_id: str,
        author: str,
        year: Optional[str] = None,
        ignore_rules: Optional[List[IgnoreRule]] = None,
        notice_template: Optional[Path] = None,
    ):
        self.license_id = license_id
        self.author = author
        self.year = year or str(datetime.now().year)
        self.ignore_rules = ignore_rules or []
        self.notice_lines = []

        if notice_template and notice_template.exists():
            try:
                content = notice_template.read_text(encoding="utf-8").strip()
                self.notice_lines = [line for line in content.splitlines() if line.strip()]
            except Exception:
                pass

        self.spdx_pattern = re.compile(
            r"SPDX-License-Identifier:\s*(.+?)(?:\s*(?:-->|\*/|$))"
        )
        self.copyright_pattern = re.compile(
            r"Copyright\s*(?:\(C\)|©)?\s*(\d{4})(?:\s*-\s*(\d{4}))?\s+(.+?)(?:\s*(?:-->|\*/|$))"
        )

    def get_comment_style(self, filepath: Path) -> Optional[CommentStyle]:
        """Determine the appropriate comment style for a file."""
        if filepath.name in SPECIAL_FILES:
            return SPECIAL_FILES[filepath.name]
        if filepath.suffix.lower() in EXTENSION_STYLES:
            return EXTENSION_STYLES[filepath.suffix.lower()]
        if not filepath.suffix:
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    first_line = f.readline().strip()
                    if first_line.startswith("#!"):
                        if any(
                            lang in first_line
                            for lang in ("python", "sh", "bash", "ruby")
                        ):
                            return COMMENT_STYLE_GROUPS["hash"]
                        elif any(lang in first_line for lang in ("node", "javascript")):
                            return COMMENT_STYLE_GROUPS["slash"]
            except (IOError, UnicodeDecodeError):
                pass
        return None

    def should_skip_file(self, filepath: Path) -> bool:
        """Check if a file should be skipped based on exclusion rules."""
        if any(part in EXCLUDE_DIRS for part in filepath.parts):
            return True

        name = filepath.name
        if any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_PATTERNS):
            return True

        try:
            rel_path = str(filepath.relative_to(Path.cwd()))
        except ValueError:
            rel_path = str(filepath)

        skip = False
        for rule in self.ignore_rules:
            matched = (
                fnmatch.fnmatch(rel_path, rule.pattern) or rule.pattern in rel_path
            )
            if matched:
                skip = not rule.negate
        return skip

    def format_header(self, style: CommentStyle) -> List[str]:
        """Format a license header using the given comment style."""
        lines = [
            f"SPDX-License-Identifier: {self.license_id}",
            f"Copyright (C) {self.year}  {self.author}",
        ]

        if self.notice_lines:
            lines.append("")
            lines.extend(self.notice_lines)

        return style.format_block_header(lines)

    def update_copyright_year(self, line: str, style: CommentStyle) -> str:
        """Update the copyright year in an existing copyright line."""
        match = self.copyright_pattern.search(line)
        if not match:
            return line
        start_year, end_year, author_name = match.groups()
        author_name = author_name.strip()
        if not end_year:
            if start_year != self.year:
                new_text = f"Copyright (C) {start_year}-{self.year}  {author_name}"
            else:
                return line
        else:
            if end_year != self.year:
                new_text = f"Copyright (C) {start_year}-{self.year}  {author_name}"
            else:
                return line
        return style.format_single_line(new_text)

    def process_file(self, filepath: Path, fix: bool = False) -> Tuple[bool, str]:
        """Process a file to check or update its license header."""
        style = self.get_comment_style(filepath)
        if not style:
            return False, f"Unsupported file type: {filepath}"

        try:
            lines = filepath.read_text(encoding="utf-8", errors="ignore").splitlines(
                True
            )
        except Exception as e:
            return False, f"Error reading {filepath}: {e}"

        if not lines:
            return False, f"Empty file: {filepath}"

        start_idx = 1 if lines and lines[0].startswith("#!") else 0
        has_spdx = False
        has_copyright = False
        spdx_line_idx = -1
        copyright_idx = -1

        for i in range(start_idx, min(start_idx + 20, len(lines))):
            line = lines[i]
            if "SPDX-License-Identifier" in line:
                has_spdx = True
                spdx_line_idx = i
            if self.copyright_pattern.search(line):
                has_copyright = True
                copyright_idx = i

        needs_update = False
        new_lines = lines.copy()

        if has_spdx:
            match = self.spdx_pattern.search(lines[spdx_line_idx])
            if match and match.group(1).strip() != self.license_id:
                needs_update = True
                if fix:
                    new_lines[spdx_line_idx] = (
                        style.format_single_line(
                            f"SPDX-License-Identifier: {self.license_id}"
                        )
                        + "\n"
                    )
            if has_copyright:
                updated = self.update_copyright_year(lines[copyright_idx], style)
                if updated != lines[copyright_idx]:
                    needs_update = True
                    if fix:
                        new_lines[copyright_idx] = updated + "\n"
            elif fix:
                new_lines.insert(
                    spdx_line_idx + 1,
                    style.format_single_line(
                        f"Copyright (C) {self.year}  {self.author}"
                    )
                    + "\n",
                )
                needs_update = True
        else:
            needs_update = True
            if fix:
                header_lines = [line + "\n" for line in self.format_header(style)]
                insert_pos = start_idx
                if insert_pos < len(new_lines) and new_lines[insert_pos].strip():
                    header_lines.append("\n")
                new_lines[insert_pos:insert_pos] = header_lines

        if fix and needs_update:
            try:
                filepath.write_text("".join(new_lines), encoding="utf-8")
                return True, f"Updated: {filepath}"
            except Exception as e:
                return False, f"Error writing {filepath}: {e}"

        if needs_update:
            return True, f"Needs update: {filepath}"
        return False, f"OK: {filepath}"
