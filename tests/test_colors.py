"""Unit tests for color utilities in clitable."""

import pytest
from clitable.colors import ansi_color_code, reset_color


class TestAnsiColorCode:
    """Test cases for ansi_color_code function."""

    def test_ansi_color_code_basic(self):
        """Test basic ANSI color code generation."""
        result = ansi_color_code('36')
        assert result == '\x1b[0m\x1b[36m'

    def test_ansi_color_code_with_style(self):
        """Test ANSI color code with style."""
        result = ansi_color_code('35', '1;')
        assert result == '\x1b[0m\x1b[1;35m'

    def test_ansi_color_code_none_color(self):
        """Test ANSI color code with None color (reset)."""
        result = ansi_color_code(None)
        assert result == '\x1b[0m'

    def test_ansi_color_code_none_color_with_style(self):
        """Test ANSI color code with None color and style."""
        result = ansi_color_code(None, '4;')
        assert result == '\x1b[0m'

    def test_ansi_color_code_empty_color(self):
        """Test ANSI color code with empty string color."""
        result = ansi_color_code('')
        assert result == '\x1b[0m\x1b[m'

    def test_ansi_color_code_empty_style(self):
        """Test ANSI color code with empty style."""
        result = ansi_color_code('31', '')
        assert result == '\x1b[0m\x1b[31m'

    def test_ansi_color_code_multiple_styles(self):
        """Test ANSI color code with multiple styles."""
        result = ansi_color_code('32', '1;4;')
        assert result == '\x1b[0m\x1b[1;4;32m'

    def test_ansi_color_code_invalid_color(self):
        """Test ANSI color code with invalid color (should still work)."""
        result = ansi_color_code('invalid')
        assert result == '\x1b[0m\x1b[invalidm'

    def test_ansi_color_code_numeric_color(self):
        """Test ANSI color code with numeric color string."""
        result = ansi_color_code('31')
        assert result == '\x1b[0m\x1b[31m'


class TestResetColor:
    """Test cases for reset_color function."""

    def test_reset_color(self):
        """Test reset_color returns correct ANSI reset code."""
        result = reset_color()
        assert result == '\x1b[0m'

    def test_reset_color_consistency(self):
        """Test reset_color consistency."""
        result1 = reset_color()
        result2 = reset_color()
        assert result1 == result2 == '\x1b[0m'


# Integration tests
def test_color_functions_integration():
    """Test that color functions work together."""
    color_code = ansi_color_code('36', '1;')
    reset = reset_color()
    combined = f"{color_code}Text{reset}"
    assert '\x1b[0m\x1b[1;36m' in combined
    assert combined.endswith('\x1b[0m')


def test_color_reset_combination():
    """Test combining color codes and reset."""
    start = ansi_color_code('35')
    end = reset_color()
    assert start != end
    assert start.endswith('m')
    assert end == '\x1b[0m'


# Edge cases and error handling
def test_ansi_color_code_none_style():
    """Test ansi_color_code with None style."""
    result = ansi_color_code(None, '')
    assert result == '\x1b[0m'


def test_ansi_color_code_various_colors():
    """Test ansi_color_code with various color strings."""
    result = ansi_color_code('42', '7;')
    assert result == '\x1b[0m\x1b[7;42m'