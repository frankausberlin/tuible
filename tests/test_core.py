"""Unit tests for core functions in clitable."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from clitable.core import print_line, print_block


class TestPrintLine:
    """Test cases for print_line function."""

    @patch('builtins.print')
    def test_print_line_basic(self, mock_print):
        """Test basic print_line functionality."""
        columns = ['Name', 'Age', 'City']
        print_line(columns)
        # Check that print was called: 1 initial ┃ + 3 data prints + 1 newline = 5
        assert mock_print.call_count == 5

    @patch('builtins.print')
    def test_print_line_with_int_colsize(self, mock_print):
        """Test print_line with integer colsize."""
        columns = ['A', 'B']
        print_line(columns, colsize=10)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        # Should have borders and data formatted
        assert '┃' in ''.join(calls)

    @patch('builtins.print')
    def test_print_line_with_list_colsize(self, mock_print):
        """Test print_line with list of colsizes."""
        columns = ['Short', 'Much longer text here']
        print_line(columns, colsize=[10, 20])
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '┃' in ''.join(calls)

    @patch('builtins.print')
    def test_print_line_centered(self, mock_print):
        """Test print_line with centered alignment."""
        columns = ['Test']
        print_line(columns, is_centered=True)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        # Check for centered formatting
        assert any('Test'.center(25) in call for call in calls)

    @patch('builtins.print')
    def test_print_line_custom_colors(self, mock_print):
        """Test print_line with custom colors."""
        columns = ['Data']
        print_line(columns, color1='31', color2='32')
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        # ANSI codes should be present
        assert '\x1b[' in ''.join(calls)

    @patch('builtins.print')
    def test_print_line_format_style(self, mock_print):
        """Test print_line with format style."""
        columns = ['Styled']
        print_line(columns, format_style='1;')  # Bold
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '\x1b[1;35m' in ''.join(calls)  # Bold + magenta

    @patch('builtins.print')
    def test_print_line_empty_columns(self, mock_print):
        """Test print_line with empty columns list."""
        print_line([])
        mock_print.assert_called_once_with()

    @patch('builtins.print')
    def test_print_line_single_column(self, mock_print):
        """Test print_line with single column."""
        columns = ['Single']
        print_line(columns)
        assert mock_print.call_count == 3  # Initial + data + newline

    @patch('builtins.print')
    def test_print_line_non_string_columns(self, mock_print):
        """Test print_line with non-string column values."""
        columns = [123, 45.67, True]
        print_line(columns)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '123' in ''.join(calls)
        assert '45.67' in ''.join(calls)
        assert 'True' in ''.join(calls)


class TestPrintBlock:
    """Test cases for print_block function."""

    @patch('builtins.print')
    def test_print_block_basic(self, mock_print):
        """Test basic print_block functionality."""
        rows = [['Name', 'Age'], ['John', '25'], ['Jane', '30']]
        print_block(rows)
        # Should call print_line for each row
        assert mock_print.call_count > 0

    @patch('builtins.print')
    def test_print_block_auto_colsize(self, mock_print):
        """Test print_block with auto column sizing."""
        rows = [['A', 'BB'], ['CCC', 'D']]
        print_block(rows, colsize=-1)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        # Check that columns are sized appropriately
        assert len([c for c in calls if 'CCC' in c]) > 0

    @patch('builtins.print')
    def test_print_block_fixed_colsize(self, mock_print):
        """Test print_block with fixed column size."""
        rows = [['A', 'B'], ['C', 'D']]
        print_block(rows, colsize=10)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '┃' in ''.join(calls)

    @patch('builtins.print')
    def test_print_block_centered(self, mock_print):
        """Test print_block with centered alignment."""
        rows = [['Header'], ['Data']]
        print_block(rows, is_centered=True)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        # First row should be underlined (header)
        assert any('\x1b[4;35m' in call for call in calls)

    @patch('builtins.print')
    def test_print_block_custom_header_format(self, mock_print):
        """Test print_block with custom header format."""
        rows = [['H1', 'H2'], ['D1', 'D2']]
        print_block(rows, format_header='1;4;')  # Bold underline
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '\x1b[1;4;35m' in ''.join(calls)

    @patch('builtins.print')
    def test_print_block_empty_rows(self, mock_print):
        """Test print_block with empty rows list."""
        print_block([])
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_print_block_single_row(self, mock_print):
        """Test print_block with single row."""
        rows = [['Only', 'Row']]
        print_block(rows)
        assert mock_print.call_count == 4  # 1 initial + 2 data + 1 newline

    @patch('builtins.print')
    def test_print_block_inconsistent_columns(self, mock_print):
        """Test print_block with inconsistent column counts."""
        rows = [['A', 'B'], ['C']]  # Second row has fewer columns
        print_block(rows)  # Should not raise, just print what it can
        assert mock_print.call_count > 0

    @patch('builtins.print')
    def test_print_block_non_string_data(self, mock_print):
        """Test print_block with non-string data."""
        rows = [[1, 2.5], [True, None]]
        print_block(rows)
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        assert '1' in ''.join(calls)
        assert '2.5' in ''.join(calls)
        assert 'True' in ''.join(calls)
        assert 'None' in ''.join(calls)


# Integration tests with captured stdout
def test_print_line_stdout_capture():
    """Test print_line output capture."""
    columns = ['Test', 'Data']
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        print_line(columns, colsize=10)
        output = mock_stdout.getvalue()
        assert '┃' in output
        assert 'Test' in output
        assert 'Data' in output


def test_print_block_stdout_capture():
    """Test print_block output capture."""
    rows = [['Header'], ['Value']]
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        print_block(rows, colsize=10)
        output = mock_stdout.getvalue()
        assert '┃' in output
        assert 'Header' in output
        assert 'Value' in output