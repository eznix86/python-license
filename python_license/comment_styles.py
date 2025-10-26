# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Comment style definitions for different file types."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CommentStyle:
    line_prefix: Optional[str] = None
    block_start: Optional[str] = None
    block_end: Optional[str] = None

    def format_single_line(self, text: str) -> str:
        if self.line_prefix:
            return f"{self.line_prefix} {text}"
        return f"# {text}"

    def format_block_header(self, lines: List[str]) -> List[str]:
        if self.block_start and self.block_end:
            formatted = [self.format_single_line(line) for line in lines]
            return [self.block_start] + formatted + [self.block_end]
        return [self.format_single_line(line) for line in lines]


# Common comment styles
COMMENT_STYLE_GROUPS = {
    "hash": CommentStyle(line_prefix="#"),
    "slash": CommentStyle(line_prefix="//"),
    "dash": CommentStyle(line_prefix="--"),
    "quote": CommentStyle(line_prefix='"'),
    "css_block": CommentStyle(block_start="/*", block_end="*/"),
    "html_block": CommentStyle(block_start="<!--", block_end="-->"),
}

EXTENSION_STYLES = {
    **{
        ext: COMMENT_STYLE_GROUPS["hash"]
        for ext in (
            ".sh",
            ".bash",
            ".zsh",
            ".fish",
            ".py",
            ".rb",
            ".pl",
            ".r",
            ".yaml",
            ".yml",
            ".toml",
            ".cmake",
        )
    },
    **{
        ext: COMMENT_STYLE_GROUPS["slash"]
        for ext in (
            ".go",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".c",
            ".cpp",
            ".cc",
            ".cxx",
            ".h",
            ".hpp",
            ".hh",
            ".hxx",
            ".java",
            ".scala",
            ".kt",
            ".swift",
            ".cs",
            ".rs",
            ".php",
            ".m",
            ".mm",
            ".gradle",
            ".groovy",
            ".scss",
            ".sass",
            ".less",
        )
    },
    **{ext: COMMENT_STYLE_GROUPS["dash"] for ext in (".sql", ".lua", ".hs", ".elm")},
    ".vim": COMMENT_STYLE_GROUPS["quote"],
    ".css": COMMENT_STYLE_GROUPS["css_block"],
    **{ext: COMMENT_STYLE_GROUPS["html_block"] for ext in (".html", ".xml", ".svg")},
}

SPECIAL_FILES = {
    "Dockerfile": COMMENT_STYLE_GROUPS["hash"],
    "Makefile": COMMENT_STYLE_GROUPS["hash"],
    "Jenkinsfile": COMMENT_STYLE_GROUPS["slash"],
    "Vagrantfile": COMMENT_STYLE_GROUPS["hash"],
    "Rakefile": COMMENT_STYLE_GROUPS["hash"],
    "Gemfile": COMMENT_STYLE_GROUPS["hash"],
    "Podfile": COMMENT_STYLE_GROUPS["hash"],
    "Fastfile": COMMENT_STYLE_GROUPS["hash"],
    "CMakeLists.txt": COMMENT_STYLE_GROUPS["hash"],
}
