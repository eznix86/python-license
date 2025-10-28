# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Tests for cli module."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest

from python_license.cli import main


class TestCLIBasicFunctionality:
    """Tests for basic CLI functionality."""

    def test_help_flag(self):
        """Test that --help flag works."""
        with patch("sys.argv", ["license", "--help"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.args[0] == 0

    def test_missing_required_args(self):
        """Test that missing required arguments causes error."""
        with patch("sys.argv", ["license"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.args[0] != 0

    def test_check_and_fix_both_error(self):
        """Test that using both --check and --fix causes error."""
        with patch("sys.argv", ["license", "MIT", "Test", "--check", "--fix"]):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.args[0] != 0


class TestCLICheckMode:
    """Tests for CLI check mode."""

    def test_check_mode_default(self):
        """Test that check mode is the default."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--dir", tmpdir]):
                with pytest.raises(SystemExit) as excinfo:
                    main()
                # Should exit with 1 because files need update
                assert excinfo.value.args[0] == 1

    def test_check_mode_explicit(self):
        """Test explicit check mode."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--check", "--dir", tmpdir]):
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.args[0] == 1

    def test_check_mode_files_ok(self):
        """Test check mode when files already have headers."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text(
                "# SPDX-License-Identifier: MIT\n"
                "# Copyright (C) 2025  Test\n\n"
                "def hello():\n    pass\n"
            )

            with patch("sys.argv", ["license", "MIT", "Test", "--check", "--dir", tmpdir, "--year", "2025"]):
                # Should not raise SystemExit because files are OK
                try:
                    main()
                except SystemExit:
                    pytest.fail("Should not exit when files are OK")


class TestCLIFixMode:
    """Tests for CLI fix mode."""

    def test_fix_mode_adds_headers(self):
        """Test that fix mode adds headers to files."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--fix", "--dir", tmpdir]):
                try:
                    main()
                except SystemExit:
                    pass

            content = filepath.read_text()
            assert "SPDX-License-Identifier: MIT" in content
            assert "Copyright (C)" in content
            assert "Test" in content

    def test_fix_mode_updates_year(self):
        """Test that fix mode updates copyright year."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text(
                "# SPDX-License-Identifier: MIT\n"
                "# Copyright (C) 2020  Test\n\n"
                "def hello():\n    pass\n"
            )

            with patch("sys.argv", ["license", "MIT", "Test", "--fix", "--dir", tmpdir, "--year", "2025"]):
                try:
                    main()
                except SystemExit:
                    pass

            content = filepath.read_text()
            assert "2020-2025" in content


class TestCLIOptions:
    """Tests for CLI options."""

    def test_custom_year_option(self):
        """Test using custom year option."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("def hello():\n    pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--fix", "--dir", tmpdir, "--year", "2023"]):
                try:
                    main()
                except SystemExit:
                    pass

            content = filepath.read_text()
            assert "Copyright (C) 2023" in content

    def test_specific_files_option(self):
        """Test processing specific files instead of directory."""
        with TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.py"
            file2 = Path(tmpdir) / "file2.py"
            file3 = Path(tmpdir) / "file3.py"
            file1.write_text("pass\n")
            file2.write_text("pass\n")
            file3.write_text("pass\n")

            with patch("sys.argv", ["license", "--fix", "MIT", "Test", str(file1), str(file2)]):
                try:
                    main()
                except SystemExit:
                    pass

            assert "SPDX-License-Identifier" in file1.read_text()
            assert "SPDX-License-Identifier" in file2.read_text()
            assert "SPDX-License-Identifier" not in file3.read_text()

    def test_no_recursive_option(self):
        """Test --no-recursive option."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "root.py").write_text("pass\n")
            subdir = tmp_path / "subdir"
            subdir.mkdir()
            (subdir / "nested.py").write_text("pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--fix", "--dir", tmpdir, "--no-recursive"]):
                try:
                    main()
                except SystemExit:
                    pass

            assert "SPDX-License-Identifier" in (tmp_path / "root.py").read_text()
            # Nested file should not be processed
            assert "SPDX-License-Identifier" not in (subdir / "nested.py").read_text()

    def test_verbose_option(self, capsys):
        """Test verbose option shows all files."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text(
                "# SPDX-License-Identifier: MIT\n"
                "# Copyright (C) 2025  Test\n\n"
                "def hello():\n    pass\n"
            )

            with patch("sys.argv", ["license", "MIT", "Test", "--check", "--dir", tmpdir, "--verbose", "--year", "2025"]):
                try:
                    main()
                except SystemExit:
                    pass

            captured = capsys.readouterr()
            assert "test.py" in captured.out or "OK" in captured.out


class TestCLIIgnoreFile:
    """Tests for ignore file handling."""

    def test_custom_ignore_file(self):
        """Test using custom ignore file."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "test.py").write_text("pass\n")
            (tmp_path / "ignore.py").write_text("pass\n")

            ignore_file = tmp_path / ".customignore"
            ignore_file.write_text("ignore.py\n")

            with patch("sys.argv", [
                "license", "MIT", "Test", "--fix", "--dir", tmpdir,
                "--ignore-file", str(ignore_file)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            assert "SPDX-License-Identifier" in (tmp_path / "test.py").read_text()
            assert "SPDX-License-Identifier" not in (tmp_path / "ignore.py").read_text()

    def test_licenseignore_auto_detection(self):
        """Test that .licenseignore is automatically detected."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "test.py").write_text("pass\n")
            (tmp_path / "skip.py").write_text("pass\n")
            (tmp_path / ".licenseignore").write_text("skip.py\n")

            # Change to tmpdir so .licenseignore is found
            import os
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                with patch("sys.argv", ["license", "MIT", "Test", "--fix"]):
                    try:
                        main()
                    except SystemExit:
                        pass
            finally:
                os.chdir(old_cwd)

            assert "SPDX-License-Identifier" in (tmp_path / "test.py").read_text()
            assert "SPDX-License-Identifier" not in (tmp_path / "skip.py").read_text()


class TestCLIExitCodes:
    """Tests for CLI exit codes."""

    def test_exit_code_check_needs_update(self):
        """Test exit code when files need update in check mode."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--check", "--dir", tmpdir]):
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.args[0] == 1

    def test_exit_code_fix_success(self):
        """Test exit code when fix succeeds."""
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.py"
            filepath.write_text("pass\n")

            with patch("sys.argv", ["license", "MIT", "Test", "--fix", "--dir", tmpdir]):
                try:
                    main()
                except SystemExit:
                    pytest.fail("Should not exit with error on successful fix")


class TestCLINoticeTemplate:
    """Tests for notice template functionality."""

    def test_notice_template_basic(self):
        """Test that notice template is added to headers."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.py"
            test_file.write_text("def hello():\n    pass\n")

            template_file = tmp_path / "NOTICE.template"
            template_file.write_text(
                "This file is part of Test Project.\n"
                "See the NOTICE and LICENSE files for details."
            )

            with patch("sys.argv", [
                "license", "MIT", "Test Author", "--fix", "--dir", tmpdir,
                "--notice-template", str(template_file)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            content = test_file.read_text()
            assert "SPDX-License-Identifier: MIT" in content
            assert "Copyright (C)" in content
            assert "This file is part of Test Project." in content
            assert "See the NOTICE and LICENSE files for details." in content

    def test_notice_template_with_different_comment_styles(self):
        """Test notice template works with different comment styles."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            template_file = tmp_path / "NOTICE.template"
            template_file.write_text("This is a notice block.")

            # Test with JavaScript (// comments)
            js_file = tmp_path / "test.js"
            js_file.write_text("console.log('hello');\n")

            with patch("sys.argv", [
                "license",
                "--fix",
                "--notice-template", str(template_file),
                "MIT", "Test",
                str(js_file)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            js_content = js_file.read_text()
            assert "// SPDX-License-Identifier: MIT" in js_content
            assert "// This is a notice block." in js_content

    def test_notice_template_missing_file(self):
        """Test handling of missing template file."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.py"
            test_file.write_text("pass\n")

            missing_template = tmp_path / "nonexistent.template"

            with patch("sys.argv", [
                "license", "MIT", "Test", "--fix", "--dir", tmpdir,
                "--notice-template", str(missing_template)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            content = test_file.read_text()
            assert "SPDX-License-Identifier: MIT" in content
            assert "Copyright (C)" in content

    def test_notice_template_blank_line_separator(self):
        """Test that blank line separates copyright from notice."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.py"
            test_file.write_text("pass\n")

            template_file = tmp_path / "NOTICE.template"
            template_file.write_text("Notice text here.")

            with patch("sys.argv", [
                "license", "MIT", "Test", "--fix", "--dir", tmpdir,
                "--notice-template", str(template_file)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            lines = test_file.read_text().splitlines()
            spdx_idx = next(i for i, line in enumerate(lines) if "SPDX-License-Identifier" in line)
            copyright_idx = next(i for i, line in enumerate(lines) if "Copyright" in line)
            notice_idx = next(i for i, line in enumerate(lines) if "Notice text" in line)

            # Check there's a blank comment line between copyright and notice
            assert copyright_idx < notice_idx
            assert lines[copyright_idx + 1].strip() in ["#", "//"]

    def test_notice_template_preserves_blank_lines(self):
        """Test that blank lines in template are preserved."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            test_file = tmp_path / "test.py"
            test_file.write_text("pass\n")

            template_file = tmp_path / "NOTICE.template"
            template_file.write_text(
                "First paragraph.\n"
                "\n"
                "Second paragraph after blank line.\n"
                "\n"
                "Third paragraph."
            )

            with patch("sys.argv", [
                "license", "MIT", "Test", "--fix", "--dir", tmpdir,
                "--notice-template", str(template_file)
            ]):
                try:
                    main()
                except SystemExit:
                    pass

            content = test_file.read_text()
            # Check that all paragraphs are present
            assert "First paragraph." in content
            assert "Second paragraph after blank line." in content
            assert "Third paragraph." in content

            # Check that blank lines are preserved (appears as "# " in Python files)
            lines = content.splitlines()
            blank_comment_lines = [i for i, line in enumerate(lines) if line.strip() == "#"]
            # Should have at least 3 blank comment lines: one after copyright, and two between paragraphs
            assert len(blank_comment_lines) >= 3
