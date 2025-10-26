# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Tests for file_utils module."""

from pathlib import Path
from tempfile import TemporaryDirectory


from python_license.file_utils import find_files


class TestFindFiles:
    """Tests for find_files function."""

    def test_find_files_in_empty_directory(self):
        """Test finding files in an empty directory."""
        with TemporaryDirectory() as tmpdir:
            result = list(find_files(Path(tmpdir)))
            assert result == []

    def test_find_files_non_recursive(self):
        """Test finding files non-recursively."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "file1.py").touch()
            (tmp_path / "file2.js").touch()
            subdir = tmp_path / "subdir"
            subdir.mkdir()
            (subdir / "file3.py").touch()

            result = list(find_files(tmp_path, recursive=False))
            assert len(result) == 2
            assert tmp_path / "file1.py" in result
            assert tmp_path / "file2.js" in result
            assert subdir / "file3.py" not in result

    def test_find_files_recursive(self):
        """Test finding files recursively."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "file1.py").touch()
            (tmp_path / "file2.js").touch()
            subdir = tmp_path / "subdir"
            subdir.mkdir()
            (subdir / "file3.py").touch()
            nested_dir = subdir / "nested"
            nested_dir.mkdir()
            (nested_dir / "file4.go").touch()

            result = list(find_files(tmp_path, recursive=True))
            assert len(result) == 4
            assert tmp_path / "file1.py" in result
            assert tmp_path / "file2.js" in result
            assert subdir / "file3.py" in result
            assert nested_dir / "file4.go" in result

    def test_find_files_ignores_directories(self):
        """Test that find_files only returns files, not directories."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "file.py").touch()
            (tmp_path / "subdir").mkdir()
            (tmp_path / "subdir" / "nested").mkdir()

            result = list(find_files(tmp_path, recursive=True))
            assert len(result) == 1
            assert tmp_path / "file.py" in result
            assert all(p.is_file() for p in result)

    def test_find_files_with_various_extensions(self):
        """Test finding files with various extensions."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            extensions = [".py", ".js", ".go", ".rs", ".java", ".cpp"]
            for i, ext in enumerate(extensions):
                (tmp_path / f"file{i}{ext}").touch()

            result = list(find_files(tmp_path))
            assert len(result) == len(extensions)

    def test_find_files_with_no_extension(self):
        """Test finding files with no extension."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "Makefile").touch()
            (tmp_path / "Dockerfile").touch()
            (tmp_path / "README").touch()

            result = list(find_files(tmp_path))
            assert len(result) == 3
            assert tmp_path / "Makefile" in result
            assert tmp_path / "Dockerfile" in result
            assert tmp_path / "README" in result

    def test_find_files_deeply_nested(self):
        """Test finding files in deeply nested directories."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            current = tmp_path
            for i in range(5):
                current = current / f"level{i}"
                current.mkdir()
                (current / f"file{i}.py").touch()

            result = list(find_files(tmp_path, recursive=True))
            assert len(result) == 5

    def test_find_files_returns_iterator(self):
        """Test that find_files returns an iterator."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "file.py").touch()

            result = find_files(tmp_path)
            assert hasattr(result, "__iter__")
            assert hasattr(result, "__next__")

    def test_find_files_multiple_files_same_name(self):
        """Test finding multiple files with the same name in different directories."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "test.py").touch()
            dir1 = tmp_path / "dir1"
            dir1.mkdir()
            (dir1 / "test.py").touch()
            dir2 = tmp_path / "dir2"
            dir2.mkdir()
            (dir2 / "test.py").touch()

            result = list(find_files(tmp_path, recursive=True))
            assert len(result) == 3
            assert all(p.name == "test.py" for p in result)

    def test_find_files_hidden_files(self):
        """Test finding hidden files (files starting with dot)."""
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / ".hidden").touch()
            (tmp_path / "visible.py").touch()

            result = list(find_files(tmp_path))
            assert len(result) == 2
            assert tmp_path / ".hidden" in result
            assert tmp_path / "visible.py" in result
