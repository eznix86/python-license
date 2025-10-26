# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Tests for header module."""

from pathlib import Path
from tempfile import TemporaryDirectory


from python_license.comment_styles import CommentStyle
from python_license.header import SPDXHeader
from python_license.ignore import IgnoreRule


class TestSPDXHeaderInit:
    """Tests for SPDXHeader initialization."""

    def test_init_basic(self):
        """Test basic initialization."""
        header = SPDXHeader("MIT", "John Doe")
        assert header.license_id == "MIT"
        assert header.author == "John Doe"
        assert header.year is not None
        assert header.ignore_rules == []

    def test_init_with_year(self):
        """Test initialization with custom year."""
        header = SPDXHeader("Apache-2.0", "Jane Smith", year="2023")
        assert header.year == "2023"

    def test_init_with_ignore_rules(self):
        """Test initialization with ignore rules."""
        rules = [IgnoreRule("*.py")]
        header = SPDXHeader("GPL-3.0", "ACME Corp", ignore_rules=rules)
        assert len(header.ignore_rules) == 1


class TestGetCommentStyle:
    """Tests for get_comment_style method."""

    def test_get_style_python_file(self):
        """Test getting comment style for Python file."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "#"

    def test_get_style_javascript_file(self):
        """Test getting comment style for JavaScript file."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.js"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "//"

    def test_get_style_css_file(self):
        """Test getting comment style for CSS file."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.css"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.block_start == "/*"
            assert style.block_end == "*/"

    def test_get_style_html_file(self):
        """Test getting comment style for HTML file."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.html"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.block_start == "<!--"
            assert style.block_end == "-->"

    def test_get_style_dockerfile(self):
        """Test getting comment style for Dockerfile."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "Dockerfile"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "#"

    def test_get_style_makefile(self):
        """Test getting comment style for Makefile."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "Makefile"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "#"

    def test_get_style_unsupported_extension(self):
        """Test getting comment style for unsupported file type."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.unknown"
            filepath.touch()
            style = header.get_comment_style(filepath)
            assert style is None

    def test_get_style_shebang_python(self):
        """Test getting comment style from Python shebang."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "script"
            filepath.write_text("#!/usr/bin/env python\nprint('hello')\n")
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "#"

    def test_get_style_shebang_bash(self):
        """Test getting comment style from bash shebang."""
        header = SPDXHeader("MIT", "Test")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "script"
            filepath.write_text("#!/bin/bash\necho hello\n")
            style = header.get_comment_style(filepath)
            assert style is not None
            assert style.line_prefix == "#"


class TestShouldSkipFile:
    """Tests for should_skip_file method."""

    def test_skip_git_directory(self):
        """Test that files in .git directory are skipped."""
        header = SPDXHeader("MIT", "Test")
        filepath = Path(".git/config")
        assert header.should_skip_file(filepath) is True

    def test_skip_node_modules(self):
        """Test that files in node_modules are skipped."""
        header = SPDXHeader("MIT", "Test")
        filepath = Path("node_modules/package/index.js")
        assert header.should_skip_file(filepath) is True

    def test_skip_minified_js(self):
        """Test that minified JS files are skipped."""
        header = SPDXHeader("MIT", "Test")
        filepath = Path("app.min.js")
        assert header.should_skip_file(filepath) is True

    def test_skip_lock_files(self):
        """Test that lock files are skipped."""
        header = SPDXHeader("MIT", "Test")
        assert header.should_skip_file(Path("package-lock.json")) is True
        assert header.should_skip_file(Path("yarn.lock")) is True

    def test_do_not_skip_regular_file(self):
        """Test that regular files are not skipped."""
        header = SPDXHeader("MIT", "Test")
        filepath = Path("src/main.py")
        assert header.should_skip_file(filepath) is False

    def test_skip_with_ignore_rules(self):
        """Test skipping files based on ignore rules."""
        rules = [IgnoreRule("test_*.py")]
        header = SPDXHeader("MIT", "Test", ignore_rules=rules)
        assert header.should_skip_file(Path("test_example.py")) is True
        assert header.should_skip_file(Path("example.py")) is False


class TestFormatHeader:
    """Tests for format_header method."""

    def test_format_header_hash_style(self):
        """Test formatting header with hash comments."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        style = CommentStyle(line_prefix="#")
        result = header.format_header(style)
        assert len(result) == 2
        assert "# SPDX-License-Identifier: MIT" in result
        assert "# Copyright (C) 2025  John Doe" in result

    def test_format_header_slash_style(self):
        """Test formatting header with slash comments."""
        header = SPDXHeader("Apache-2.0", "Jane Smith", year="2024")
        style = CommentStyle(line_prefix="//")
        result = header.format_header(style)
        assert len(result) == 2
        assert "// SPDX-License-Identifier: Apache-2.0" in result
        assert "// Copyright (C) 2024  Jane Smith" in result


class TestUpdateCopyrightYear:
    """Tests for update_copyright_year method."""

    def test_update_single_year_to_range(self):
        """Test updating single year copyright to range."""
        header = SPDXHeader("MIT", "Test", year="2025")
        style = CommentStyle(line_prefix="#")
        line = "# Copyright (C) 2023  John Doe"
        result = header.update_copyright_year(line, style)
        assert "2023-2025" in result
        assert "John Doe" in result

    def test_update_year_range(self):
        """Test updating year range."""
        header = SPDXHeader("MIT", "Test", year="2025")
        style = CommentStyle(line_prefix="#")
        line = "# Copyright (C) 2020-2023  John Doe"
        result = header.update_copyright_year(line, style)
        assert "2020-2025" in result

    def test_no_update_if_current_year(self):
        """Test that no update occurs if year is current."""
        header = SPDXHeader("MIT", "Test", year="2025")
        style = CommentStyle(line_prefix="#")
        line = "# Copyright (C) 2025  John Doe"
        result = header.update_copyright_year(line, style)
        assert result == line

    def test_no_update_if_range_current(self):
        """Test that no update occurs if range ends with current year."""
        header = SPDXHeader("MIT", "Test", year="2025")
        style = CommentStyle(line_prefix="#")
        line = "# Copyright (C) 2020-2025  John Doe"
        result = header.update_copyright_year(line, style)
        assert result == line


class TestProcessFile:
    """Tests for process_file method."""

    def test_process_file_without_header(self):
        """Test processing a file without any header."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    print('hello')\n")

            changed, msg = header.process_file(filepath, fix=False)
            assert changed is True
            assert "Needs update" in msg

    def test_process_file_add_header(self):
        """Test adding header to a file."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    print('hello')\n")

            changed, msg = header.process_file(filepath, fix=True)
            assert changed is True
            assert "Updated" in msg

            content = filepath.read_text()
            assert "SPDX-License-Identifier: MIT" in content
            assert "Copyright (C) 2025  John Doe" in content

    def test_process_file_with_existing_header(self):
        """Test processing a file with existing correct header."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text(
                "# SPDX-License-Identifier: MIT\n"
                "# Copyright (C) 2025  John Doe\n\n"
                "def hello():\n    print('hello')\n"
            )

            changed, msg = header.process_file(filepath, fix=False)
            assert changed is False
            assert "OK" in msg

    def test_process_file_update_year(self):
        """Test updating copyright year in existing header."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text(
                "# SPDX-License-Identifier: MIT\n"
                "# Copyright (C) 2023  John Doe\n\n"
                "def hello():\n    print('hello')\n"
            )

            changed, msg = header.process_file(filepath, fix=True)
            assert changed is True

            content = filepath.read_text()
            assert "2023-2025" in content

    def test_process_file_with_shebang(self):
        """Test processing a file with shebang line."""
        header = SPDXHeader("MIT", "John Doe", year="2025")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "script.py"
            filepath.write_text(
                "#!/usr/bin/env python\n"
                "def hello():\n    print('hello')\n"
            )

            changed, msg = header.process_file(filepath, fix=True)
            assert changed is True

            content = filepath.read_text()
            lines = content.splitlines()
            assert lines[0] == "#!/usr/bin/env python"
            assert "SPDX-License-Identifier" in lines[1]

    def test_process_empty_file(self):
        """Test processing an empty file."""
        header = SPDXHeader("MIT", "John Doe")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "empty.py"
            filepath.write_text("")

            changed, msg = header.process_file(filepath, fix=False)
            assert changed is False
            assert "Empty file" in msg

    def test_process_unsupported_file_type(self):
        """Test processing an unsupported file type."""
        header = SPDXHeader("MIT", "John Doe")
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.unknown"
            filepath.write_text("content")

            changed, msg = header.process_file(filepath, fix=False)
            assert changed is False
            assert "Unsupported file type" in msg
