"""ANSI color utilities for CLI table formatting."""

from typing import Optional


def ansi_color_code(color: Optional[str] = None, style: str = '') -> str:
    """
    Generate ANSI escape code for color and style.

    Args:
        color: ANSI color code (e.g., '36' for cyan, '35' for magenta).
        style: Additional style code (e.g., '4;' for underline).

    Returns:
        ANSI escape sequence string.
    """
    if color is None:
        return '\x1b[0m'  # Reset
    return f'\x1b[0m\x1b[{style}{color}m'


def reset_color() -> str:
    """Return ANSI reset code."""
    return '\x1b[0m'