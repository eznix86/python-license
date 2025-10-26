# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025  Bruno Bernard

"""Tests for constants module."""

from python_license.constants import EXCLUDE_DIRS, EXCLUDE_PATTERNS


def test_exclude_dirs_contains_common_vcs():
    """Test that EXCLUDE_DIRS includes common version control directories."""
    assert ".git" in EXCLUDE_DIRS
    assert ".svn" in EXCLUDE_DIRS
    assert ".hg" in EXCLUDE_DIRS


def test_exclude_dirs_contains_build_artifacts():
    """Test that EXCLUDE_DIRS includes common build artifact directories."""
    assert "build" in EXCLUDE_DIRS
    assert "dist" in EXCLUDE_DIRS
    assert "target" in EXCLUDE_DIRS
    assert "__pycache__" in EXCLUDE_DIRS


def test_exclude_dirs_contains_dependencies():
    """Test that EXCLUDE_DIRS includes dependency directories."""
    assert "node_modules" in EXCLUDE_DIRS
    assert "vendor" in EXCLUDE_DIRS
    assert "third_party" in EXCLUDE_DIRS


def test_exclude_dirs_contains_virtual_environments():
    """Test that EXCLUDE_DIRS includes virtual environment directories."""
    assert "venv" in EXCLUDE_DIRS
    assert ".venv" in EXCLUDE_DIRS
    assert "env" in EXCLUDE_DIRS
    assert ".env" in EXCLUDE_DIRS


def test_exclude_dirs_is_set():
    """Test that EXCLUDE_DIRS is a set for efficient lookups."""
    assert isinstance(EXCLUDE_DIRS, set)


def test_exclude_patterns_contains_minified_files():
    """Test that EXCLUDE_PATTERNS includes minified file patterns."""
    assert "*.min.js" in EXCLUDE_PATTERNS
    assert "*.min.css" in EXCLUDE_PATTERNS


def test_exclude_patterns_contains_generated_files():
    """Test that EXCLUDE_PATTERNS includes generated file patterns."""
    assert "*.generated.*" in EXCLUDE_PATTERNS
    assert "*.pb.go" in EXCLUDE_PATTERNS
    assert "*.pb.cc" in EXCLUDE_PATTERNS
    assert "*_pb2.py" in EXCLUDE_PATTERNS


def test_exclude_patterns_contains_config_files():
    """Test that EXCLUDE_PATTERNS includes configuration file patterns."""
    assert "*.json" in EXCLUDE_PATTERNS
    assert "*.toml" in EXCLUDE_PATTERNS
    assert "*.yml" in EXCLUDE_PATTERNS
    assert "*.yaml" in EXCLUDE_PATTERNS


def test_exclude_patterns_contains_lock_files():
    """Test that EXCLUDE_PATTERNS includes lock file patterns."""
    assert "*.lock" in EXCLUDE_PATTERNS
    assert "*.sum" in EXCLUDE_PATTERNS


def test_exclude_patterns_contains_special_files():
    """Test that EXCLUDE_PATTERNS includes special files."""
    assert "LICENSE" in EXCLUDE_PATTERNS
    assert "NOTICE" in EXCLUDE_PATTERNS
    assert ".gitignore" in EXCLUDE_PATTERNS
    assert ".licenseignore" in EXCLUDE_PATTERNS


def test_exclude_patterns_is_set():
    """Test that EXCLUDE_PATTERNS is a set for efficient lookups."""
    assert isinstance(EXCLUDE_PATTERNS, set)


def test_exclude_dirs_no_duplicates():
    """Test that EXCLUDE_DIRS has no duplicate values."""
    assert len(EXCLUDE_DIRS) == len(set(EXCLUDE_DIRS))


def test_exclude_patterns_no_duplicates():
    """Test that EXCLUDE_PATTERNS has no duplicate values."""
    assert len(EXCLUDE_PATTERNS) == len(set(EXCLUDE_PATTERNS))
