"""Core functions for printing CLI tables."""

from typing import List, Union, Any, Optional
from .params import CliTableParams
from .table import CliTable


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
    params = CliTableParams()
    params.format_edge['color'] = color1
    params.format_data['color'] = color2
    params.format_data['esc'] = format_style
    params.format_data['align'] = 'center' if is_centered else 'left'
    
    if isinstance(colsize, int):
        params.size = colsize
        params.column_count = len(columns)
    else:
        params.column_widths = colsize
        params.column_count = len(columns)

    # Prepare data mode
    params.mode_stack = ['data']
    params.mode_columns['data'] = [[str(col)] for col in columns]
    
    table = CliTable(params)
    table.execute()


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

    params = CliTableParams()
    params.format_edge['color'] = color1
    params.format_data['color'] = color2
    params.format_data['esc'] = format_style
    params.format_data['align'] = 'center' if is_centered else 'left'
    params.format_header['esc'] = format_header
    params.size = colsize
    
    # In CliTableParams, data is stored as columns: List[List[str]]
    # We need to transpose rows to columns
    num_cols = len(rows[0])
    header_row = rows[0]
    data_rows = rows[1:]
    
    params.mode_stack = ['header', 'data']
    
    # Header columns
    params.mode_columns['header'] = [[str(cell)] for cell in header_row]
    
    # Data columns
    data_cols = [[] for _ in range(num_cols)]
    for row in data_rows:
        for i in range(num_cols):
            val = str(row[i]) if i < len(row) else ""
            data_cols[i].append(val)
    params.mode_columns['data'] = data_cols
    
    params.column_count = num_cols
    
    table = CliTable(params)
    table.execute()


def print_table(
    headers: Optional[List[str]] = None,
    data: Optional[List[List[str]]] = None,
    colsize: int = -1
) -> None:
    """
    Print a complete table with optional headers, data, and borders.

    Args:
        headers: List of header strings
        data: List of data rows
        colsize: Column size (-1 for auto)
    """
    rows = []
    if headers:
        rows.append(headers)
    if data:
        rows.extend(data)
    
    if not rows:
        return

    params = CliTableParams()
    params.size = colsize
    params.mode_stack = ['top', 'header', 'data', 'bottom']
    
    num_cols = len(rows[0])
    params.column_count = num_cols
    
    if headers:
        params.mode_columns['header'] = [[str(cell)] for cell in headers]
    
    if data:
        data_cols = [[] for _ in range(num_cols)]
        for row in data:
            for i in range(num_cols):
                val = str(row[i]) if i < len(row) else ""
                data_cols[i].append(val)
        params.mode_columns['data'] = data_cols
    
    table = CliTable(params)
    table.execute()
