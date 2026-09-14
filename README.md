# sudokuq

Public sudoku datasets are usually one puzzle per line, tens of millions of
lines, gigabytes on disk. Before you train something on a file like that, or
publish one, you often want to know: how many of these puzzles actually have
exactly one solution? Puzzle generators and scrapers get this wrong more
often than you'd expect -- under-constrained grids with multiple solutions,
or garbled rows with none at all.

`sudokuq` answers that one question. It reads puzzles line by line and
prints a verdict for each: `unique`, `multiple`, `no-solution`, or
`malformed: <reason>`.

## Input format

One puzzle per line, 81 characters, row-major. Givens are digits `1`-`9`;
blanks are `0` or `.`. If a line has a comma in it, everything after the
first comma is ignored, so `puzzle,solution` datasets work without
preprocessing.

## Usage

```
$ echo "800000000003600000070090200050007000000045700000100030001000068008500010090000400" > puzzle.txt
$ python -m sudokuq puzzle.txt
1	unique
```

Or from stdin, which is what you want for large files:

```
$ cat puzzles.txt | python -m sudokuq
1	unique
2	multiple
3	no-solution
4	malformed: expected 81 characters, got 80
```

`FILE` can also be `-` to mean stdin explicitly.

## Why streaming matters here

`sudokuq` iterates the input file object (or `sys.stdin`) line by line. It
never calls `.read()` or `.readlines()` on the whole input, so memory use
stays flat whether the file has a hundred lines or a hundred million. Each
line is parsed, solved, and discarded before the next one is read.

## Library use

The pieces are usable on their own:

```python
from sudokuq import parse_line, count_solutions

grid = parse_line("800000000003600000070090200050007000000045700000100030001000068008500010090000400")
count_solutions(grid, limit=2)  # 1
```

`count_solutions` stops as soon as it finds `limit` solutions, so checking
uniqueness on a hard puzzle doesn't mean fully enumerating every solution.

## Status

Early. No test suite yet, no packaging release, solver is plain backtracking
with no advanced pruning beyond minimum-remaining-values ordering. Good
enough for correctness on the puzzle sizes sudoku actually has (9x9), not
yet benchmarked against very large batches.

## License

MIT, see [LICENSE](LICENSE).
