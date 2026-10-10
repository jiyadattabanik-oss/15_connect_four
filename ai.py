import random

from board import COLS


class AI:
    def choose_column(self, board, me="O", opponent="X"):
        legal = board.legal_columns()
        if not legal:
            return None

        # 1) take an immediate win, 2) otherwise block the opponent's immediate win
        for token in (me, opponent):
            for col in legal:
                board.drop(col, token)
                wins = board.winner(token)
                board.undo(col)
                if wins:
                    return col

        # 3) otherwise prefer columns closest to the centre (random tie-break)
        centre = COLS // 2
        return min(legal, key=lambda c: (abs(c - centre), random.random()))
