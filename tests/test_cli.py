import io

from sudokuq.__main__ import classify, run

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
SINGLE_BLANK_UNIQUE = "0" + SOLVED_GRID[1:]
BLANK_GRID = "0" * 81
NO_SOLUTION_GRID = (
    "012900000"
    "345000000"
    "678000000"
    + "000000000" * 6
)


def test_classify_unique():
    assert classify(SINGLE_BLANK_UNIQUE) == "unique"


def test_classify_multiple():
    assert classify(BLANK_GRID) == "multiple"


def test_classify_no_solution():
    assert classify(NO_SOLUTION_GRID) == "no-solution"


def test_classify_malformed():
    assert classify("1" * 80) == "malformed: expected 81 characters, got 80"


def test_run_numbers_lines_and_writes_tab_separated_verdicts():
    lines = [SINGLE_BLANK_UNIQUE, BLANK_GRID, NO_SOLUTION_GRID, "1" * 80]
    out = io.StringIO()
    run(lines, out=out)
    assert out.getvalue() == (
        "1\tunique\n"
        "2\tmultiple\n"
        "3\tno-solution\n"
        "4\tmalformed: expected 81 characters, got 80\n"
    )


def test_run_skips_blank_lines_but_keeps_original_line_numbers():
    lines = [SINGLE_BLANK_UNIQUE, "\n", "   \n", BLANK_GRID]
    out = io.StringIO()
    run(lines, out=out)
    assert out.getvalue() == "1\tunique\n4\tmultiple\n"
