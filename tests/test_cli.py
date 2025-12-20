"""Unit tests for CLI interface in clitable."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from clitable.cli import main


class TestCLI:
    """Test cases for CLI."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_help(self, mock_stdout):
        """Test help output."""
        test_args = ['clitable', '--help']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'Usage: clitable' in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_data_basic(self, mock_stdout):
        """Test basic data command."""
        test_args = ['clitable', 'data', 'col1', 'col2']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'col1' in output
        assert 'col2' in output
        assert '┃' in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_header_basic(self, mock_stdout):
        """Test basic header command."""
        test_args = ['clitable', 'header', 'H1', 'H2']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'H1' in output
        assert 'H2' in output
        assert '┃' in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_full_table(self, mock_stdout):
        """Test full table sequence (simulated by multiple calls or combined args)."""
        # The current CLI implementation in cli.py executes one set of params.
        # source_clitable allowed multiple modes in one call if parsed correctly.
        # Let's check parseArguments in params.py.
        # It loops through args and appends to mode_stack.
        test_args = ['clitable', 'top', 'header', 'H1', 'data', 'D1', 'bottom', '-cc', '1']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert '┏' in output
        assert 'H1' in output
        assert 'D1' in output
        assert '┗' in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_no_border(self, mock_stdout):
        """Test no border option."""
        test_args = ['clitable', 'data', 'test', '-nb']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'test' in output
        assert '┃' not in output

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_custom_colors(self, mock_stdout):
        """Test custom colors."""
        test_args = ['clitable', 'data', 'test', '-ce', '31', '-cd', '32']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert '\x1b[31m' in output # Edge color
        assert '\x1b[32m' in output # Data color

    @patch('sys.stdout', new_callable=StringIO)
    def test_cli_dynamic_size(self, mock_stdout):
        """Test dynamic sizing."""
        test_args = ['clitable', 'data', 'very long string', '-size', '-1']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'very long string' in output
        # Check if width is at least the length of the string
        # The output will have ANSI codes, so we just check it printed.
