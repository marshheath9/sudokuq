from sudokuq.board import parse_line
from sudokuq.solver import count_solutions

# Hand-verified complete, valid 9x9 solution.
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

# Blank first cell of SOLVED_GRID. Row 0, column 0 and box 0 already contain
# every digit except 5, so the cell has exactly one candidate.
SINGLE_BLANK_UNIQUE = "0" + SOLVED_GRID[1:]

BLANK_GRID = "0" * 81

# Box 0 is filled with givens 1-8 across its 8 non-blank cells, leaving one
# cell (row 0, col 0) that can only take 9 by box constraint. Row 0 already
# has a given 9 elsewhere, so that cell has zero valid candidates and the
# puzzle has no solution.
NO_SOLUTION_GRID = (
    "012900000"
    "345000000"
    "678000000"
    + "000000000" * 6
)


def test_fully_solved_grid_has_exactly_one_solution():
    grid = parse_line(SOLVED_GRID)
    assert count_solutions(grid) == 1


def test_single_forced_blank_has_exactly_one_solution():
    grid = parse_line(SINGLE_BLANK_UNIQUE)
    assert count_solutions(grid) == 1


def test_blank_grid_has_multiple_solutions():
    grid = parse_line(BLANK_GRID)
    assert count_solutions(grid) == 2


def test_contradictory_grid_has_no_solutions():
    grid = parse_line(NO_SOLUTION_GRID)
    assert count_solutions(grid) == 0


def test_limit_caps_the_count_even_when_more_solutions_exist():
    grid = parse_line(BLANK_GRID)
    assert count_solutions(grid, limit=1) == 1
