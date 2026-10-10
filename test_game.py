
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from board import Board
from ai import AI
from game import Game


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_horizontal_win(self):
        self.board.grid[5][0:4] = ["X", "X", "X", "X"]
        self.assertTrue(self.board.winner("X"))

    def test_vertical_win(self):
        for r in range(2, 6):
            self.board.grid[r][0] = "X"
        self.assertTrue(self.board.winner("X"))

    def test_diagonal_down_right_win(self):
        for i in range(4):
            self.board.grid[i][i] = "X"
        self.assertTrue(self.board.winner("X"))

    def test_diagonal_down_left_win(self):
        for i in range(4):
            self.board.grid[i][3 - i] = "X"
        self.assertTrue(self.board.winner("X"))

    def test_three_in_a_row_is_not_a_win(self):
        self.board.grid[5][0:3] = ["X", "X", "X"]
        self.assertFalse(self.board.winner("X"))

    def test_draw_position(self):
        # Full board with no four-in-a-row for either player.
        rows = [
            "OXXOXXO",
            "OOXXOOX",
            "XXOOOXX",
            "OOXXXOX",
            "OXXOOXO",
            "XOXOXOO",
        ]
        self.board.grid = [list(row) for row in rows]

        self.assertTrue(self.board.full())
        self.assertFalse(self.board.winner("X"))
        self.assertFalse(self.board.winner("O"))

    def test_dropping_into_full_column(self):
        for _ in range(6):
            self.assertIsNotNone(self.board.drop(0, "X"))

        before = [row[:] for row in self.board.grid]

        self.assertIsNone(self.board.drop(0, "O"))
        self.assertEqual(self.board.grid, before)

    def test_out_of_range_column(self):
        before = [row[:] for row in self.board.grid]

        self.assertIsNone(self.board.drop(-1, "X"))
        self.assertIsNone(self.board.drop(7, "X"))
        self.assertEqual(self.board.grid, before)


class TestAI(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.ai = AI()

    def test_ai_takes_immediate_win(self):
        # O has three horizontal discs and can win in column 4.
        self.board.grid[5][0:3] = ["O", "O", "O"]

        self.assertEqual(self.ai.choose_column(self.board), 3)

        # AI's trial move must not alter the actual board.
        self.assertEqual(self.board.grid[5][0:3], ["O", "O", "O"])
        self.assertEqual(self.board.grid[5][3], ".")

    def test_ai_blocks_player_immediate_win(self):
        # X threatens to win horizontally in column 4.
        self.board.grid[5][0:3] = ["X", "X", "X"]

        self.assertEqual(self.ai.choose_column(self.board), 3)

        # The AI must not leave its trial disc on the board.
        self.assertEqual(self.board.grid[5][3], ".")

    def test_ai_returns_none_only_when_board_is_full(self):
        self.assertIsNotNone(self.ai.choose_column(self.board))

        for c in range(7):
            for r in range(6):
                self.board.grid[r][c] = "X"

        self.assertIsNone(self.ai.choose_column(self.board))


class TestGame(unittest.TestCase):

    def test_invalid_input_does_not_change_board_or_turn(self):
        game = Game()
        before = [row[:] for row in game.board.grid]

        output = StringIO()
        with patch("builtins.input", side_effect=["abc", "0", "8", "q"]):
            with redirect_stdout(output):
                game.run()

        self.assertEqual(game.board.grid, before)
        self.assertEqual(game.turn, "X")
        self.assertIn("Invalid input", output.getvalue())
        self.assertIn("Invalid column", output.getvalue())
        self.assertIn("Game quit", output.getvalue())

    def test_quitting_with_q(self):
        game = Game()
        output = StringIO()

        with patch("builtins.input", return_value="q"):
            with redirect_stdout(output):
                game.run()

        self.assertIn("Game quit by player.", output.getvalue())
        self.assertTrue(
            all(cell == "." for row in game.board.grid for cell in row)
        )

    def test_end_of_input_exits_cleanly(self):
        game = Game()
        output = StringIO()

        with patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(output):
                game.run()

        self.assertIn("Game quit (input closed).", output.getvalue())

    def test_keyboard_interrupt_exits_cleanly(self):
        game = Game()
        output = StringIO()

        with patch("builtins.input", side_effect=KeyboardInterrupt):
            with redirect_stdout(output):
                game.run()

        self.assertIn("Game quit (interrupted).", output.getvalue())


if __name__ == "__main__":
    unittest.main()
