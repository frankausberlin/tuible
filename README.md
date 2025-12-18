This is a little vibe-coding-test with kilocode / x-ai code fast 1


# clitable

A Python package for printing formatted CLI tables with ANSI colors.

## Features

- Print single table lines or multi-row table blocks
- ANSI color support for borders and data
- Customizable column widths and alignment
- Header formatting with underline styles
- Auto-sizing based on content
- Command-line interface with rich help

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
from clitable import print_line, print_block

# Print a single line
print_line(['Name', 'Age', 'City'], colsize=15, color1='36', color2='35')

# Print a table block
rows = [
    ['Name', 'Age', 'City'],
    ['John', '25', 'New York'],
    ['Jane', '30', 'London']
]
print_block(rows, colsize=-1)  # Auto-size columns
```

### Command Line

```bash
# Print a single line
clitable line "Name" "Age" "City"

# Print a table block
clitable block --rows "Name Age City" "John 25 New York" "Jane 30 London"

# With custom colors and formatting
clitable line -c1 31 -c2 32 -centered "Centered Text"
```

## API Reference

### `print_line(columns, colsize=25, color1='36', color2='35', format_style='', is_centered=False)`

Print a single line of table columns.

- `columns`: List of column values to print
- `colsize`: Column width(s) - int for uniform, list for per-column
- `color1`: ANSI color code for borders (default: '36' cyan)
- `color2`: ANSI color code for data (default: '35' magenta)
- `format_style`: Additional ANSI style (e.g., '1;' for bold)
- `is_centered`: Center-align data

### `print_block(rows, colsize=-1, color1='36', color2='35', format_style='', format_header='4;', is_centered=False)`

Print a block of table rows.

- `rows`: List of rows, each row is a list of columns
- `colsize`: Column width (-1 for auto-size)
- `color1`: ANSI color code for borders
- `color2`: ANSI color code for data
- `format_style`: Style for data rows
- `format_header`: Style for header row (default: '4;' underline)
- `is_centered`: Center-align data

### ANSI Colors

Common ANSI color codes:
- 30: Black
- 31: Red
- 32: Green
- 33: Yellow
- 34: Blue
- 35: Magenta
- 36: Cyan
- 37: White

Style codes:
- 0: Reset
- 1: Bold
- 4: Underline
- 7: Reverse

## Examples

### Basic Table

```bash
clitable block --rows "Product Price Stock" "Laptop 999 5" "Mouse 25 20" "Keyboard 75 8"
```

### Colored Output

```bash
clitable line -c1 32 -c2 33 "Success" "Operation completed"
```

### Centered Text

```bash
clitable line -centered -sz 20 "Centered Title"
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/clitable.git
cd clitable
uv sync
```

### Testing

```bash
uv run pytest
```

### Building

```bash
uv build
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.