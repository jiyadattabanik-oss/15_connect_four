from board import Board, COLS, ROWS
from ai import AI


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.turn = "X"

    def read_human_column(self):
        """Return a valid 0-based column, or None if the player quits."""
        while True:
            try:
                raw = input(f"Column (1-{COLS}), or q: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if raw == "q":
                return None
            try:
                col = int(raw) - 1
            except ValueError:
                print("Enter a column number.")
                continue
            if not 0 <= col < COLS:
                print(f"Column must be between 1 and {COLS}.")
                continue
            if not self.board.is_valid_column(col):
                print("That column is full. Choose another.")
                continue
            return col

    def run(self):
        print("Connect Four — you are X.")
        while True:
            self.board.print()

            if self.turn == "X":
                col = self.read_human_column()
                if col is None:
                    print("Game ended by player.")
                    return
            else:
                col = self.ai.choose_column(self.board)
                if col is None or not self.board.is_valid_column(col):
                    print("No valid move available. Game over.")
                    return

            row = self.board.drop(col, self.turn)
            print(f"{self.turn} placed a disc in column {col + 1} (row {ROWS - row} from the bottom).")

            if self.board.winner(self.turn):
                self.board.print()
                print(f"{self.turn} wins!")
                return

            if self.board.full():
                self.board.print()
                print("Draw.")
                return

            self.turn = "O" if self.turn == "X" else "X"
