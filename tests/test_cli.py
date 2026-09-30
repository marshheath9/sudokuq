import gzip
import io

from sudokuq.__main__ import classify, main, open_text, run

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


def _buffered(data):
    return io.BufferedReader(io.BytesIO(data))


def test_open_text_reads_plain_input():
    data = (SINGLE_BLANK_UNIQUE + "\n" + BLANK_GRID + "\n").encode()
    assert list(open_text(_buffered(data))) == [
        SINGLE_BLANK_UNIQUE + "\n",
        BLANK_GRID + "\n",
    ]


def test_open_text_reads_gzip_input():
    data = gzip.compress((SINGLE_BLANK_UNIQUE + "\n" + BLANK_GRID + "\n").encode())
    assert list(open_text(_buffered(data))) == [
        SINGLE_BLANK_UNIQUE + "\n",
        BLANK_GRID + "\n",
    ]


def test_open_text_handles_empty_input():
    assert list(open_text(_buffered(b""))) == []


def test_main_reads_gzip_file_regardless_of_name(tmp_path, capsys):
    path = tmp_path / "puzzles.dat"
    path.write_bytes(gzip.compress((SINGLE_BLANK_UNIQUE + "\n" + BLANK_GRID + "\n").encode()))
    assert main([str(path)]) == 0
    assert capsys.readouterr().out == "1\tunique\n2\tmultiple\n"


def test_run_skips_blank_lines_but_keeps_original_line_numbers():
    lines = [SINGLE_BLANK_UNIQUE, "\n", "   \n", BLANK_GRID]
    out = io.StringIO()
    run(lines, out=out)
    assert out.getvalue() == "1\tunique\n4\tmultiple\n"


def test_run_without_progress_writes_nothing_to_progress_out():
    lines = [SINGLE_BLANK_UNIQUE]
    out = io.StringIO()
    progress_out = io.StringIO()
    run(lines, out=out, progress=False, progress_out=progress_out)
    assert progress_out.getvalue() == ""


def test_run_with_progress_reports_final_count_even_below_threshold():
    lines = [SINGLE_BLANK_UNIQUE, BLANK_GRID, NO_SOLUTION_GRID]
    out = io.StringIO()
    progress_out = io.StringIO()
    run(lines, out=out, progress=True, progress_out=progress_out)
    report = progress_out.getvalue()
    assert report.startswith("done: 3 lines, ")
    assert report.count("\n") == 1


def test_run_with_progress_reports_at_threshold_and_at_end():
    lines = [SINGLE_BLANK_UNIQUE] * 200_000
    out = io.StringIO()
    progress_out = io.StringIO()
    run(lines, out=out, progress=True, progress_out=progress_out)
    reported_lines = progress_out.getvalue().splitlines()
    assert reported_lines[0].startswith("... 100000 lines, ")
    assert reported_lines[1].startswith("... 200000 lines, ")
    assert reported_lines[2].startswith("done: 200000 lines, ")
