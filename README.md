# clitable

A Python package for printing formatted CLI tables with ANSI colors.

## Features

- Print single table lines or multi-row table blocks
- ANSI color support for borders and data
- Customizable column widths and alignment
- Header formatting with underline styles
- Auto-sizing based on content
- Command-line interface with mode-stack support
- Multi-row cells using colon prefix syntax

## Installation

```bash
pip install clitable
```

Or using uv:

```bash
uv pip install clitable
```

## Usage

### Python API

```python
from clitable import print_line, print_block, print_table

# Print a single line
print_line(['Name', 'Age', 'City'], colsize=15, color1='36', color2='35')

# Print a table block
rows = [
    ['Name', 'Age', 'City'],
    ['John', '25', 'New York'],
    ['Jane', '30', 'London']
]
print_block(rows, colsize=-1)  # Auto-size columns

# Print a full table with borders
print_table(headers=['Name', 'Age'], data=[['John', '25'], ['Jane', '30']])
```

### Command Line

The CLI uses a mode-based approach where you can stack different parts of the table.

```bash
# Print a single data line
clitable data "Name" "Age" "City"

# Print a header and data
clitable header "Name" "Age" data "John" "25"

# Print a full table with borders
clitable top header "Name" "Age" data "John" "25" bottom -cc 2

# With custom colors and formatting
clitable data -ce 31 -cd 32 "Red Border" "Green Data"
```

#### Modes
- `data`: Print data line
- `header`: Print header line
- `top`: Print top border
- `bottom`: Print bottom border

#### Options
- `-ce <color>`: Set edge color (e.g., 34 for blue)
- `-cd <color>`: Set data color (e.g., 32 for green)
- `-ch <color>`: Set header color (e.g., 33 for yellow)
- `-fd <style>`: Set data style (e.g., 4 for underline)
- `-fh <style>`: Set header style
- `-fe <chars>`: Set edge characters (8 chars: left-right, top-bottom, corners, middle)
- `-size <num>`: Set column width (-1 for dynamic)
- `-cc <num>`: Set column count
- `-nb`: No border (left and right)

### Multi-row Cells (Colon Mechanics)
Elements starting with `:` are treated as continuations in the same column, allowing multi-row content within a single table column.

```bash
clitable data "Row 1" ":Row 2" "Other Col"
```

## API Reference

### `print_line(columns, colsize=25, color1='36', color2='35', format_style='', is_centered=False)`
Print a single line of table columns.

### `print_block(rows, colsize=-1, color1='36', color2='35', format_style='', format_header='4;', is_centered=False)`
Print a block of table rows.

### `print_table(headers=None, data=None, colsize=-1)`
Print a complete table with optional headers, data, and borders.

## Development

### Setup

```bash
git clone https://github.com/frank/clitable.git
cd clitable
uv sync
```

### Testing

```bash
PYTHONPATH=src uv run pytest
```

## License

MIT License - see LICENSE file for details.
