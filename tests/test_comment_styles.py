"""Tests for comment_styles module."""


from python_license.comment_styles import (
    COMMENT_STYLE_GROUPS,
    EXTENSION_STYLES,
    SPECIAL_FILES,
    CommentStyle,
)


class TestCommentStyle:
    """Tests for CommentStyle dataclass."""

    def test_format_single_line_with_prefix(self):
        """Test formatting a single line with a custom prefix."""
        style = CommentStyle(line_prefix="#")
        result = style.format_single_line("SPDX-License-Identifier: MIT")
        assert result == "# SPDX-License-Identifier: MIT"

    def test_format_single_line_with_slash_prefix(self):
        """Test formatting a single line with slash prefix."""
        style = CommentStyle(line_prefix="//")
        result = style.format_single_line("Copyright 2025")
        assert result == "// Copyright 2025"

    def test_format_single_line_default_fallback(self):
        """Test that format_single_line falls back to # when no prefix."""
        style = CommentStyle()
        result = style.format_single_line("Test line")
        assert result == "# Test line"

    def test_format_block_header_with_line_comments(self):
        """Test formatting block header with line-style comments."""
        style = CommentStyle(line_prefix="#")
        lines = ["SPDX-License-Identifier: MIT", "Copyright 2025"]
        result = style.format_block_header(lines)
        assert result == ["# SPDX-License-Identifier: MIT", "# Copyright 2025"]

    def test_format_block_header_with_block_comments(self):
        """Test formatting block header with block-style comments."""
        style = CommentStyle(block_start="/*", block_end="*/")
        lines = ["SPDX-License-Identifier: MIT", "Copyright 2025"]
        result = style.format_block_header(lines)
        assert result[0] == "/*"
        assert result[-1] == "*/"
        assert len(result) == 4

    def test_format_block_header_html_style(self):
        """Test formatting block header with HTML-style comments."""
        style = CommentStyle(block_start="<!--", block_end="-->")
        lines = ["SPDX-License-Identifier: MIT"]
        result = style.format_block_header(lines)
        assert result[0] == "<!--"
        assert result[-1] == "-->"


class TestCommentStyleGroups:
    """Tests for COMMENT_STYLE_GROUPS."""

    def test_hash_style_exists(self):
        """Test that hash style is defined."""
        assert "hash" in COMMENT_STYLE_GROUPS
        assert COMMENT_STYLE_GROUPS["hash"].line_prefix == "#"

    def test_slash_style_exists(self):
        """Test that slash style is defined."""
        assert "slash" in COMMENT_STYLE_GROUPS
        assert COMMENT_STYLE_GROUPS["slash"].line_prefix == "//"

    def test_dash_style_exists(self):
        """Test that dash style is defined."""
        assert "dash" in COMMENT_STYLE_GROUPS
        assert COMMENT_STYLE_GROUPS["dash"].line_prefix == "--"

    def test_css_block_style_exists(self):
        """Test that CSS block style is defined."""
        assert "css_block" in COMMENT_STYLE_GROUPS
        style = COMMENT_STYLE_GROUPS["css_block"]
        assert style.block_start == "/*"
        assert style.block_end == "*/"

    def test_html_block_style_exists(self):
        """Test that HTML block style is defined."""
        assert "html_block" in COMMENT_STYLE_GROUPS
        style = COMMENT_STYLE_GROUPS["html_block"]
        assert style.block_start == "<!--"
        assert style.block_end == "-->"

    def test_quote_style_exists(self):
        """Test that quote style is defined."""
        assert "quote" in COMMENT_STYLE_GROUPS
        assert COMMENT_STYLE_GROUPS["quote"].line_prefix == '"'


class TestExtensionStyles:
    """Tests for EXTENSION_STYLES mapping."""

    def test_python_uses_hash(self):
        """Test that Python files use hash comments."""
        assert ".py" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".py"].line_prefix == "#"

    def test_javascript_uses_slash(self):
        """Test that JavaScript files use slash comments."""
        assert ".js" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".js"].line_prefix == "//"

    def test_typescript_uses_slash(self):
        """Test that TypeScript files use slash comments."""
        assert ".ts" in EXTENSION_STYLES
        assert ".tsx" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".ts"].line_prefix == "//"
        assert EXTENSION_STYLES[".tsx"].line_prefix == "//"

    def test_go_uses_slash(self):
        """Test that Go files use slash comments."""
        assert ".go" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".go"].line_prefix == "//"

    def test_rust_uses_slash(self):
        """Test that Rust files use slash comments."""
        assert ".rs" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".rs"].line_prefix == "//"

    def test_c_cpp_use_slash(self):
        """Test that C/C++ files use slash comments."""
        assert ".c" in EXTENSION_STYLES
        assert ".cpp" in EXTENSION_STYLES
        assert ".h" in EXTENSION_STYLES
        assert ".hpp" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".c"].line_prefix == "//"

    def test_sql_uses_dash(self):
        """Test that SQL files use dash comments."""
        assert ".sql" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".sql"].line_prefix == "--"

    def test_shell_scripts_use_hash(self):
        """Test that shell scripts use hash comments."""
        assert ".sh" in EXTENSION_STYLES
        assert ".bash" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".sh"].line_prefix == "#"

    def test_ruby_uses_hash(self):
        """Test that Ruby files use hash comments."""
        assert ".rb" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".rb"].line_prefix == "#"

    def test_yaml_uses_hash(self):
        """Test that YAML files use hash comments."""
        assert ".yaml" in EXTENSION_STYLES
        assert ".yml" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".yaml"].line_prefix == "#"

    def test_css_uses_block(self):
        """Test that CSS files use block comments."""
        assert ".css" in EXTENSION_STYLES
        style = EXTENSION_STYLES[".css"]
        assert style.block_start == "/*"
        assert style.block_end == "*/"

    def test_html_uses_block(self):
        """Test that HTML files use block comments."""
        assert ".html" in EXTENSION_STYLES
        assert ".xml" in EXTENSION_STYLES
        style = EXTENSION_STYLES[".html"]
        assert style.block_start == "<!--"
        assert style.block_end == "-->"

    def test_vim_uses_quote(self):
        """Test that Vim files use quote comments."""
        assert ".vim" in EXTENSION_STYLES
        assert EXTENSION_STYLES[".vim"].line_prefix == '"'


class TestSpecialFiles:
    """Tests for SPECIAL_FILES mapping."""

    def test_dockerfile_uses_hash(self):
        """Test that Dockerfile uses hash comments."""
        assert "Dockerfile" in SPECIAL_FILES
        assert SPECIAL_FILES["Dockerfile"].line_prefix == "#"

    def test_makefile_uses_hash(self):
        """Test that Makefile uses hash comments."""
        assert "Makefile" in SPECIAL_FILES
        assert SPECIAL_FILES["Makefile"].line_prefix == "#"

    def test_jenkinsfile_uses_slash(self):
        """Test that Jenkinsfile uses slash comments."""
        assert "Jenkinsfile" in SPECIAL_FILES
        assert SPECIAL_FILES["Jenkinsfile"].line_prefix == "//"

    def test_ruby_files_use_hash(self):
        """Test that Ruby special files use hash comments."""
        assert "Vagrantfile" in SPECIAL_FILES
        assert "Rakefile" in SPECIAL_FILES
        assert "Gemfile" in SPECIAL_FILES
        assert SPECIAL_FILES["Vagrantfile"].line_prefix == "#"

    def test_cmake_uses_hash(self):
        """Test that CMakeLists.txt uses hash comments."""
        assert "CMakeLists.txt" in SPECIAL_FILES
        assert SPECIAL_FILES["CMakeLists.txt"].line_prefix == "#"


class TestBlockCommentFormatting:
    """Tests for block comment formatting (CSS, HTML, Vue)."""

    def test_css_block_formatting(self):
        """Test that CSS uses proper block comment formatting with asterisk prefix."""
        style = COMMENT_STYLE_GROUPS["css_block"]
        lines = ["SPDX-License-Identifier: MIT", "Copyright (C) 2025  Test"]
        result = style.format_block_header(lines)

        assert result[0] == "/*"
        assert result[1] == " * SPDX-License-Identifier: MIT"
        assert result[2] == " * Copyright (C) 2025  Test"
        assert result[3] == "*/"
        # Ensure no hash symbols
        assert all("#" not in line for line in result)

    def test_html_block_formatting(self):
        """Test that HTML uses proper block comment formatting with no prefix."""
        style = COMMENT_STYLE_GROUPS["html_block"]
        lines = ["SPDX-License-Identifier: MIT", "Copyright (C) 2025  Test"]
        result = style.format_block_header(lines)

        assert result[0] == "<!--"
        assert result[1] == "SPDX-License-Identifier: MIT"
        assert result[2] == "Copyright (C) 2025  Test"
        assert result[3] == "-->"
        # Ensure no hash symbols
        assert all("#" not in line for line in result)

    def test_css_block_with_blank_lines(self):
        """Test that CSS handles blank lines correctly in notice blocks."""
        style = COMMENT_STYLE_GROUPS["css_block"]
        lines = ["SPDX-License-Identifier: MIT", "", "This is a notice."]
        result = style.format_block_header(lines)

        assert result[0] == "/*"
        assert result[1] == " * SPDX-License-Identifier: MIT"
        assert result[2] == " * "
        assert result[3] == " * This is a notice."
        assert result[4] == "*/"

    def test_vue_uses_html_block(self):
        """Test that Vue files use HTML block comment style."""
        assert EXTENSION_STYLES[".vue"] == COMMENT_STYLE_GROUPS["html_block"]
