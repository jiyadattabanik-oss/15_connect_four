ROWS, COLS = 6, 7
EMPTY = "."


class Board:
    def __init__(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]

    def is_valid_column(self, col):
        return 0 <= col < COLS and self.grid[0][col] == EMPTY

    def legal_columns(self):
        return [c for c in range(COLS) if self.grid[0][c] == EMPTY]

    def drop(self, col, token):
        if not self.is_valid_column(col):
            return None
        for r in range(ROWS - 1, -1, -1):
            if self.grid[r][col] == EMPTY:
                self.grid[r][col] = token
                return r
        return None

    def undo(self, col):
        """Remove the top disc in a column (used by the AI to test moves)."""
        for r in range(ROWS):
            if self.grid[r][col] != EMPTY:
                self.grid[r][col] = EMPTY
                return

    def full(self):
        return all(self.grid[0][c] != EMPTY for c in range(COLS))

    def winner(self, token):
        # right, down, down-right diagonal, down-left diagonal
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] != token:
                    continue
                for dr, dc in directions:
                    if all(
                        0 <= r + i * dr < ROWS
                        and 0 <= c + i * dc < COLS
                        and self.grid[r + i * dr][c + i * dc] == token
                        for i in range(4)
                    ):
                        return True
        return False

    def print(self):
        print("\n " + " ".join(str(i + 1) for i in range(COLS)))
        for row in self.grid:
            print(" " + " ".join(row))
