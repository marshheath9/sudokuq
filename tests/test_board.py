import pytest

from sudokuq.board import MalformedLine, find_conflict, parse_line

# A hand-verified complete, valid 9x9 solution (every row/column/box has 1-9).
SOLVED_GRID = (
    "534678912"
    "672195348"
    "198342567"
    "859761423"
    "426853791"
    "713924856"
    "961537284"
    "287419635"
    "345286179"
)


def test_parses_solved_grid_to_ints():
    grid = parse_line(SOLVED_GRID)
    assert len(grid) == 81
    assert grid[0] == 5
    assert grid[-1] == 9
    assert all(1 <= v <= 9 for v in grid)


def test_dot_and_zero_both_mean_blank():
    line = "." * 40 + "0" * 41
    grid = parse_line(line)
    assert grid == (0,) * 81


def test_strips_surrounding_whitespace_and_newline():
    grid = parse_line(SOLVED_GRID + "\n")
    assert grid == parse_line(SOLVED_GRID)


def test_ignores_everything_after_first_comma():
    line = SOLVED_GRID + "," + SOLVED_GRID[::-1]
    assert parse_line(line) == parse_line(SOLVED_GRID)


def test_wrong_length_is_malformed():
    with pytest.raises(MalformedLine, match="expected 81 characters, got 80"):
        parse_line("1" * 80)


def test_extra_length_before_comma_is_malformed():
    with pytest.raises(MalformedLine, match="expected 81 characters, got 82"):
        parse_line("1" * 82)


def test_unexpected_character_is_malformed():
    line = "0" * 80 + "x"
    with pytest.raises(MalformedLine, match=r"unexpected character 'x'"):
        parse_line(line)


def test_empty_line_is_malformed():
    with pytest.raises(MalformedLine, match="empty line"):
        parse_line("")
    with pytest.raises(MalformedLine, match="empty line"):
        parse_line("   \n")


def test_duplicate_given_in_row_is_malformed():
    line = "55" + "0" * 79
    with pytest.raises(MalformedLine, match="duplicate given in row 0"):
        parse_line(line)


def test_duplicate_given_in_column_is_malformed():
    # index 0 and index 9 are both column 0 (row 0 and row 1).
    line = "5" + "0" * 8 + "5" + "0" * 71
    with pytest.raises(MalformedLine, match="duplicate given in column 0"):
        parse_line(line)


def test_duplicate_given_in_box_is_malformed():
    # index 0 (row 0, col 0) and index 10 (row 1, col 1) share box 0.
    line = "5" + "0" * 9 + "5" + "0" * 70
    with pytest.raises(MalformedLine, match="duplicate given in box 0"):
        parse_line(line)


def test_find_conflict_returns_none_for_valid_grid():
    assert find_conflict(parse_line(SOLVED_GRID)) is None
