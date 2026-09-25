"""Command-line entry point: stream puzzles in, print a verdict per line.

Reads either a file given as an argument or stdin, one puzzle per line.
Iterating a file object (or stdin) yields lines lazily, so this never
holds more than the current line in memory -- what makes it safe to run
over multi-gigabyte puzzle dumps instead of `.read().splitlines()`-ing
the whole thing first.
"""

import sys
import time

from .board import MalformedLine, parse_line
from .solver import count_solutions

HELP_TEXT = (
    "usage: python -m sudokuq [--progress] [FILE]\n"
    "\n"
    "Reads one 81-character sudoku grid per line from FILE (or stdin if\n"
    "FILE is omitted or '-') and prints a tab-separated verdict per line:\n"
    "unique, multiple, no-solution, or malformed: <reason>.\n"
    "\n"
    "--progress    every 100000 lines, write a line count and elapsed\n"
    "              time to stderr so long batch runs show they're alive.\n"
)

PROGRESS_EVERY = 100_000


def classify(line):
    try:
        grid = parse_line(line)
    except MalformedLine as exc:
        return f"malformed: {exc}"

    solutions = count_solutions(grid, limit=2)
    if solutions == 0:
        return "no-solution"
    if solutions == 1:
        return "unique"
    return "multiple"


def run(lines, out=sys.stdout, progress=False, progress_out=sys.stderr):
    start = time.monotonic()
    number = 0
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        out.write(f"{number}\t{classify(line)}\n")
        if progress and number % PROGRESS_EVERY == 0:
            progress_out.write(
                f"... {number} lines, {time.monotonic() - start:.1f}s\n"
            )
            progress_out.flush()

    if progress:
        progress_out.write(f"done: {number} lines, {time.monotonic() - start:.1f}s\n")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if "--help" in argv or "-h" in argv:
        sys.stdout.write(HELP_TEXT)
        return 0

    progress = "--progress" in argv
    positional = [arg for arg in argv if arg != "--progress"]

    if positional and positional[0] != "-":
        with open(positional[0], "r", encoding="utf-8") as handle:
            run(handle, progress=progress)
        return 0

    run(sys.stdin, progress=progress)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
