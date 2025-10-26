# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Tests for ignore module."""

from pathlib import Path
from tempfile import NamedTemporaryFile


from python_license.ignore import IgnoreRule, load_ignore_file


class TestIgnoreRule:
    """Tests for IgnoreRule class."""

    def test_basic_rule_creation(self):
        """Test creating a basic ignore rule."""
        rule = IgnoreRule("*.py")
        assert rule.pattern == "*.py"
        assert rule.negate is False
        assert rule.dir_only is False

    def test_negated_rule_creation(self):
        """Test creating a negated ignore rule."""
        rule = IgnoreRule("!important.py", negate=True)
        assert rule.pattern == "!important.py"
        assert rule.negate is True

    def test_directory_only_rule_creation(self):
        """Test creating a directory-only ignore rule."""
        rule = IgnoreRule("build/", dir_only=True)
        assert rule.pattern == "build/"
        assert rule.dir_only is True


class TestLoadIgnoreFile:
    """Tests for load_ignore_file function."""

    def test_load_nonexistent_file(self):
        """Test loading a non-existent ignore file."""
        result = load_ignore_file(Path("/nonexistent/path"))
        assert result == []

    def test_load_none_path(self):
        """Test loading with None path."""
        result = load_ignore_file(None)
        assert result == []

    def test_load_empty_file(self):
        """Test loading an empty ignore file."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert result == []
        finally:
            temp_path.unlink()

    def test_load_file_with_comments(self):
        """Test loading ignore file with comments."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("# This is a comment\n")
            f.write("*.py\n")
            f.write("# Another comment\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 1
            assert result[0].pattern == "*.py"
        finally:
            temp_path.unlink()

    def test_load_file_with_blank_lines(self):
        """Test loading ignore file with blank lines."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("*.py\n")
            f.write("\n")
            f.write("*.js\n")
            f.write("   \n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 2
            assert result[0].pattern == "*.py"
            assert result[1].pattern == "*.js"
        finally:
            temp_path.unlink()

    def test_load_file_with_negated_patterns(self):
        """Test loading ignore file with negated patterns."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("*.py\n")
            f.write("!important.py\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 2
            assert result[0].pattern == "*.py"
            assert result[0].negate is False
            assert result[1].pattern == "important.py"
            assert result[1].negate is True
        finally:
            temp_path.unlink()

    def test_load_file_with_directory_patterns(self):
        """Test loading ignore file with directory patterns."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("build/\n")
            f.write("dist/\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 2
            assert result[0].pattern == "build"
            assert result[0].dir_only is True
            assert result[1].pattern == "dist"
            assert result[1].dir_only is True
        finally:
            temp_path.unlink()

    def test_load_file_with_mixed_patterns(self):
        """Test loading ignore file with mixed pattern types."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("# Comment\n")
            f.write("*.py\n")
            f.write("!important.py\n")
            f.write("build/\n")
            f.write("\n")
            f.write("*.log\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 4
            assert result[0].pattern == "*.py"
            assert result[0].negate is False
            assert result[0].dir_only is False
            assert result[1].pattern == "important.py"
            assert result[1].negate is True
            assert result[2].pattern == "build"
            assert result[2].dir_only is True
            assert result[3].pattern == "*.log"
        finally:
            temp_path.unlink()

    def test_load_file_strips_whitespace(self):
        """Test that whitespace is properly stripped from patterns."""
        with NamedTemporaryFile(mode="w", suffix=".ignore", delete=False) as f:
            f.write("  *.py  \n")
            f.write("\t*.js\t\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 2
            assert result[0].pattern == "*.py"
            assert result[1].pattern == "*.js"
        finally:
            temp_path.unlink()

    def test_load_gitignore_format(self):
        """Test loading a .gitignore-style file."""
        with NamedTemporaryFile(mode="w", suffix=".gitignore", delete=False) as f:
            f.write("# Build outputs\n")
            f.write("build/\n")
            f.write("dist/\n")
            f.write("*.pyc\n")
            f.write("\n")
            f.write("# But keep this file\n")
            f.write("!important.pyc\n")
            temp_path = Path(f.name)

        try:
            result = load_ignore_file(temp_path)
            assert len(result) == 4
            assert result[0].pattern == "build"
            assert result[0].dir_only is True
            assert result[1].pattern == "dist"
            assert result[1].dir_only is True
            assert result[2].pattern == "*.pyc"
            assert result[3].pattern == "important.pyc"
            assert result[3].negate is True
        finally:
            temp_path.unlink()
