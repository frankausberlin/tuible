"""Core functions for printing CLI tables."""

from typing import List, Union, Any
from .colors import ansi_color_code, reset_color


def print_line(
    columns: List[Any],
    colsize: Union[int, List[int]] = 25,
    color1: str = '36',
    color2: str = '35',
    format_style: str = '',
    is_centered: bool = False
) -> None:
    """
    Print a single line of table columns with formatting.

    Args:
        columns: List of column values to print.
        colsize: Column size(s). If int, applies to all columns. If list, per column.
        color1: ANSI color code for borders (default: '36' cyan).
        color2: ANSI color code for data (default: '35' magenta).
        format_style: Additional style for data (e.g., '4;' for underline).
        is_centered: Whether to center-align the data.
    """
    if isinstance(colsize, int):
        col_sizes = [colsize] * len(columns)
    else:
        col_sizes = colsize

    edge_format = ansi_color_code(color1)
    data_format = ansi_color_code(color2, format_style)

    for i, col in enumerate(columns):
        if is_centered:
            data_centered = str(col).center(col_sizes[i])
        else:
            data_centered = str(col).ljust(col_sizes[i])
        # First column
        if i == 0:
            print(f"{edge_format}┃", end='')
        print(f"{data_format}{data_centered}{edge_format}┃{reset_color()}", end='')
    print()


def print_block(
    rows: List[List[Any]],
    colsize: int = -1,
    color1: str = '36',
    color2: str = '35',
    format_style: str = '',
    format_header: str = '4;',
    is_centered: bool = False
) -> None:
    """
    Print a block of table rows with formatting.

    Args:
        rows: List of rows, each row is a list of columns.
        colsize: Column size. -1 for auto-size based on longest entry.
        color1: ANSI color code for borders (default: '36' cyan).
        color2: ANSI color code for data (default: '35' magenta).
        format_style: Additional style for data rows.
        format_header: Style for header row (default: '4;' underline).
        is_centered: Whether to center-align the data.
    """
    if not rows:
        return

    num_cols = len(rows[0])
    if colsize == -1:
        col_sizes = [0] * num_cols
        for row in rows:
            for i, col in enumerate(row):
                col_sizes[i] = max(col_sizes[i], len(str(col)))
        col_sizes = [s + 2 for s in col_sizes]  # Add padding
    else:
        col_sizes = [colsize] * num_cols

    for idx, row in enumerate(rows):
        fmt = format_header if idx == 0 else format_style
        print_line(row, col_sizes, color1, color2, fmt, is_centered)