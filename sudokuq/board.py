"""Parsing and representation of a single sudoku grid line."""

GRID_CELLS = 81
BOX_SIZE = 3
SIZE = 9

BLANK_CHARS = frozenset("0.")


class MalformedLine(ValueError):
    """Raised when a line cannot be parsed as an 81-cell sudoku grid."""


def parse_line(line):
    """Parse one line of input into a tuple of 81 ints (0 = blank).

    Accepts the common single-line format used by most public sudoku
    datasets: 81 characters, digits 1-9 for givens, '0' or '.' for blanks.
    Anything after the 81st character (e.g. a comma-separated solution
    column some datasets append) is ignored.
    """
    stripped = line.strip()
    if not stripped:
        raise MalformedLine("empty line")

    grid_part = stripped.split(",", 1)[0]

    if len(grid_part) != GRID_CELLS:
        raise MalformedLine(
            f"expected {GRID_CELLS} characters, got {len(grid_part)}"
        )

    cells = []
    for ch in grid_part:
        if ch in BLANK_CHARS:
            cells.append(0)
        elif ch.isdigit() and ch != "0":
            cells.append(int(ch))
        else:
            raise MalformedLine(f"unexpected character {ch!r}")

    grid = tuple(cells)
    conflict = find_conflict(grid)
    if conflict is not None:
        raise MalformedLine(f"duplicate given in {conflict}")
    return grid


def _row(i):
    return i // SIZE


def _col(i):
    return i % SIZE


def _box(i):
    r, c = _row(i), _col(i)
    return (r // BOX_SIZE) * BOX_SIZE + (c // BOX_SIZE)


def find_conflict(grid):
    """Return a description of the first row/column/box conflict, or None.

    Datasets sometimes contain garbage rows; catching this up front means
    the solver never has to reason about an already-contradictory grid.
    """
    rows = [set() for _ in range(SIZE)]
    cols = [set() for _ in range(SIZE)]
    boxes = [set() for _ in range(SIZE)]

    for i, value in enumerate(grid):
        if value == 0:
            continue
        r, c, b = _row(i), _col(i), _box(i)
        if value in rows[r]:
            return f"row {r}"
        if value in cols[c]:
            return f"column {c}"
        if value in boxes[b]:
            return f"box {b}"
        rows[r].add(value)
        cols[c].add(value)
        boxes[b].add(value)
    return None
