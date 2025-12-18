"""CLI interface for clitable using argparse."""

import argparse
import sys
from .core import print_line, print_block
from . import __version__


def main():
    """Main CLI entry point for clitable."""
    parser = argparse.ArgumentParser(
        prog='clitable',
        description='Print formatted CLI tables with ANSI colors',
        epilog='For more information, visit: https://github.com/yourusername/clitable'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'clitable {__version__}'
    )

    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND'
    )

    # Line subcommand
    line_parser = subparsers.add_parser(
        'line',
        help='Print a single table line',
        description='Print a single line of table columns with optional formatting.'
    )
    line_parser.add_argument(
        '-c1', '--color1',
        default='36',
        help='ANSI color code for borders (default: 36 cyan)'
    )
    line_parser.add_argument(
        '-c2', '--color2',
        default='35',
        help='ANSI color code for data (default: 35 magenta)'
    )
    line_parser.add_argument(
        '-sz', '--colsize',
        type=int,
        default=25,
        help='Column width (default: 25)'
    )
    line_parser.add_argument(
        '-fmt', '--format',
        default='',
        help='Additional ANSI format style (e.g., "1;" for bold)'
    )
    line_parser.add_argument(
        '-centered',
        action='store_true',
        help='Center-align the data in columns'
    )
    line_parser.add_argument(
        'columns',
        nargs='+',
        help='Column values to display'
    )

    # Block subcommand
    block_parser = subparsers.add_parser(
        'block',
        help='Print a table block with multiple rows',
        description='Print a block of table rows with optional header formatting.'
    )
    block_parser.add_argument(
        '-c1', '--color1',
        default='36',
        help='ANSI color code for borders (default: 36 cyan)'
    )
    block_parser.add_argument(
        '-c2', '--color2',
        default='35',
        help='ANSI color code for data (default: 35 magenta)'
    )
    block_parser.add_argument(
        '-sz', '--colsize',
        type=int,
        default=-1,
        help='Column width (-1 for auto-size, default: -1)'
    )
    block_parser.add_argument(
        '-fmt', '--format',
        default='',
        help='ANSI format style for data rows'
    )
    block_parser.add_argument(
        '-fmt-header', '--format-header',
        default='4;',
        help='ANSI format style for header row (default: "4;" underline)'
    )
    block_parser.add_argument(
        '-centered',
        action='store_true',
        help='Center-align the data in columns'
    )
    block_parser.add_argument(
        '--rows',
        nargs='+',
        required=True,
        help='Rows as space-separated columns, e.g., "Name Age" "John 25" "Jane 30"'
    )

    # Parse arguments
    try:
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        if args.command == 'line':
            try:
                colsize = [args.colsize] * len(args.columns) if isinstance(args.colsize, int) else args.colsize
                print_line(args.columns, colsize, args.color1, args.color2, args.format, args.centered)
            except Exception as e:
                print(f"Error printing line: {e}", file=sys.stderr)
                sys.exit(1)

        elif args.command == 'block':
            try:
                rows = [row.split() for row in args.rows]
                print_block(rows, args.colsize, args.color1, args.color2, args.format, args.format_header, args.centered)
            except Exception as e:
                print(f"Error printing block: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            parser.print_help()

    except SystemExit:
        # argparse handles --help and --version
        pass
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()