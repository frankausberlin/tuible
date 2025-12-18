"""Unit tests for CLI interface in clitable."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from clitable.cli import main


class TestCLILine:
    """Test cases for CLI line subcommand."""

    @patch('clitable.cli.print_line')
    def test_line_basic(self, mock_print_line):
        """Test basic line command."""
        test_args = ['clitable', 'line', 'col1', 'col2', 'col3']
        with patch('sys.argv', test_args):
            main()
        mock_print_line.assert_called_once_with(
            ['col1', 'col2', 'col3'], [25, 25, 25], '36', '35', '', False
        )

    @patch('clitable.cli.print_line')
    def test_line_with_options(self, mock_print_line):
        """Test line command with all options."""
        test_args = [
            'clitable', 'line',
            '-c1', '31',
            '-c2', '32',
            '-sz', '20',
            '-fmt', '1;',
            '-centered',
            'data1', 'data2'
        ]
        with patch('sys.argv', test_args):
            main()
        mock_print_line.assert_called_once_with(
            ['data1', 'data2'], [20, 20], '31', '32', '1;', True
        )

    @patch('clitable.cli.print_line')
    def test_line_custom_colors(self, mock_print_line):
        """Test line command with custom colors."""
        test_args = ['clitable', 'line', '-c1', '33', '-c2', '34', 'test']
        with patch('sys.argv', test_args):
            main()
        mock_print_line.assert_called_once_with(
            ['test'], [25], '33', '34', '', False
        )

    @patch('clitable.cli.print_line')
    def test_line_no_columns(self, mock_print_line):
        """Test line command with no columns (should fail)."""
        test_args = ['clitable', 'line']
        with patch('sys.argv', test_args):
            main()
        # argparse prints usage on stderr; ensure we didn't call print_line
        mock_print_line.assert_not_called()


class TestCLIBlock:
    """Test cases for CLI block subcommand."""

    @patch('clitable.cli.print_block')
    def test_block_basic(self, mock_print_block):
        """Test basic block command."""
        test_args = [
            'clitable', 'block',
            '--rows', 'Header1 Header2', 'Data1 Data2'
        ]
        with patch('sys.argv', test_args):
            main()
        expected_rows = [['Header1', 'Header2'], ['Data1', 'Data2']]
        mock_print_block.assert_called_once_with(
            expected_rows, -1, '36', '35', '', '4;', False
        )

    @patch('clitable.cli.print_block')
    def test_block_with_options(self, mock_print_block):
        """Test block command with all options."""
        test_args = [
            'clitable', 'block',
            '-c1', '31',
            '-c2', '32',
            '-sz', '15',
            '-fmt', '1;',
            '-fmt-header', '4;1;',
            '-centered',
            '--rows', 'H1 H2', 'D1 D2'
        ]
        with patch('sys.argv', test_args):
            main()
        expected_rows = [['H1', 'H2'], ['D1', 'D2']]
        mock_print_block.assert_called_once_with(
            expected_rows, 15, '31', '32', '1;', '4;1;', True
        )

    @patch('clitable.cli.print_block')
    def test_block_multiple_rows(self, mock_print_block):
        """Test block command with multiple rows."""
        test_args = [
            'clitable', 'block',
            '--rows', 'A B C', '1 2 3', 'X Y Z'
        ]
        with patch('sys.argv', test_args):
            main()
        expected_rows = [['A', 'B', 'C'], ['1', '2', '3'], ['X', 'Y', 'Z']]
        mock_print_block.assert_called_once_with(
            expected_rows, -1, '36', '35', '', '4;', False
        )

    @patch('clitable.cli.print_block')
    def test_block_no_rows(self, mock_print_block):
        """Test block command with no rows (should fail)."""
        test_args = ['clitable', 'block']
        with patch('sys.argv', test_args):
            main()
        # argparse prints usage on stderr; ensure we didn't call print_block
        mock_print_block.assert_not_called()

    @patch('clitable.cli.print_block')
    def test_block_inconsistent_columns(self, mock_print_block):
        """Test block command with inconsistent column counts."""
        test_args = [
            'clitable', 'block',
            '--rows', 'A B', 'C'  # Second row has fewer columns
        ]
        with patch('sys.argv', test_args):
            main()
        # Should still call print_block, but it will raise IndexError internally
        expected_rows = [['A', 'B'], ['C']]
        mock_print_block.assert_called_once()
        # The call should have been made with the parsed rows
        args, kwargs = mock_print_block.call_args
        assert args[0] == expected_rows


class TestCLIHelp:
    """Test cases for CLI help and invalid commands."""

    @patch('sys.stdout', new_callable=StringIO)
    def test_no_command(self, mock_stdout):
        """Test running without subcommand shows help."""
        test_args = ['clitable']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'usage:' in output.lower()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_invalid_command(self, mock_stderr, mock_stdout):
        """Test invalid subcommand shows help."""
        test_args = ['clitable', 'invalid']
        with patch('sys.argv', test_args):
            main()
        output = mock_stderr.getvalue()
        assert 'usage:' in output.lower()

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    def test_help_flag(self, mock_stderr, mock_stdout):
        """Test --help flag."""
        test_args = ['clitable', '--help']
        with patch('sys.argv', test_args):
            main()
        output = mock_stdout.getvalue()
        assert 'usage:' in output.lower()
        assert 'line' in output
        assert 'block' in output


# Integration tests with actual output
def test_cli_line_integration():
    """Integration test for line command."""
    test_args = ['clitable', 'line', 'Test', 'Data']
    with patch('sys.argv', test_args), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main()
    output = mock_stdout.getvalue()
    assert '┃' in output
    assert 'Test' in output
    assert 'Data' in output


def test_cli_block_integration():
    """Integration test for block command."""
    test_args = ['clitable', 'block', '--rows', 'Name Age', 'John 25']
    with patch('sys.argv', test_args), patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        main()
    output = mock_stdout.getvalue()
    assert '┃' in output
    assert 'Name' in output
    assert 'John' in output