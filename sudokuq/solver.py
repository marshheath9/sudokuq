"""Backtracking solver used only to count solutions, not to find one.

Counting stops as soon as it has seen `limit` solutions, since the query
this tool answers ("is the solution unique?") never needs more than two:
one to prove a solution exists, a second to prove it isn't the only one.
"""

SIZE = 9
BOX_SIZE = 3
FULL_MASK = (1 << SIZE) - 1


def _peers(index):
    r, c = divmod(index, SIZE)
    b = (r // BOX_SIZE) * BOX_SIZE + (c // BOX_SIZE)
    return r, c, b


def count_solutions(grid, limit=2):
    """Count solutions of `grid` (tuple of 81 ints, 0 = blank), up to `limit`."""
    row_used = [0] * SIZE
    col_used = [0] * SIZE
    box_used = [0] * SIZE
    cells = list(grid)

    empties = []
    for i, value in enumerate(cells):
        r, c, b = _peers(i)
        if value:
            bit = 1 << (value - 1)
            row_used[r] |= bit
            col_used[c] |= bit
            box_used[b] |= bit
        else:
            empties.append(i)

    found = 0

    def backtrack(pos):
        nonlocal found
        if found >= limit:
            return
        if pos == len(empties):
            found += 1
            return

        # Fill in the emptiest cell first (fewest candidates) so dead
        # branches get pruned as early as possible.
        best_at = pos
        best_candidates = -1
        for j in range(pos, len(empties)):
            i = empties[j]
            r, c, b = _peers(i)
            used = row_used[r] | col_used[c] | box_used[b]
            candidates = FULL_MASK & ~used
            count = bin(candidates).count("1")
            if best_candidates == -1 or count < best_candidates:
                best_candidates = count
                best_at = j
                if count == 0:
                    break
        if best_candidates == 0:
            return

        empties[pos], empties[best_at] = empties[best_at], empties[pos]
        i = empties[pos]
        r, c, b = _peers(i)
        used = row_used[r] | col_used[c] | box_used[b]
        candidates = FULL_MASK & ~used

        remaining = candidates
        while remaining:
            bit = remaining & (-remaining)
            remaining ^= bit
            value = bit.bit_length()

            row_used[r] |= bit
            col_used[c] |= bit
            box_used[b] |= bit
            cells[i] = value

            backtrack(pos + 1)

            row_used[r] &= ~bit
            col_used[c] &= ~bit
            box_used[b] &= ~bit
            cells[i] = 0

            if found >= limit:
                break

        empties[pos], empties[best_at] = empties[best_at], empties[pos]

    backtrack(0)
    return found
