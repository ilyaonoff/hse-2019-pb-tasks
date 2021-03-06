from typing import List, Optional
from enum import Enum


class Player(Enum):
    X = 1
    O = 2  # noqa: disable=E741


class TicTacToe:
    def __init__(self) -> None:
        self.field: List[List[Optional[Player]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def winner(self) -> Optional[Player]:
        if self.field[0][0] and (self.field[0][0] ==
                                 self.field[1][1] ==
                                 self.field[2][2]):
            return self.field[1][1]
        if self.field[2][0] and (self.field[2][0] ==
                                 self.field[1][1] ==
                                 self.field[0][2]):
            return self.field[1][1]
        for row in range(3):
            if self.field[row][0] and (self.field[row][0] ==
                                       self.field[row][1] ==
                                       self.field[row][2]):
                return self.field[row][1]
        for col in range(3):
            if self.field[0][col] and (self.field[0][col] ==
                                       self.field[1][col] ==
                                       self.field[2][col]):
                return self.field[1][col]
        return None

    def is_finished(self) -> bool:
        if self.winner():
            return True
        return all(None not in row for row in self.field)

    def current_player(self) -> Optional[Player]:
        cnt_x = sum(sum(c == Player.X for c in row) for row in self.field)
        cnt_o = sum(sum(c == Player.O for c in row) for row in self.field)
        if cnt_x + cnt_o == 9:
            return None
        if cnt_x == cnt_o:
            return Player.X
        elif cnt_x - 1 == cnt_o:
            return Player.O
        else:
            assert False

    def can_make_turn(self, player: Player, *, row: int, col: int) -> bool:
        assert 0 <= row < 3
        assert 0 <= col < 3
        if self.field[row][col]:
            return False
        if self.is_finished():
            return False
        return player == self.current_player()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.can_make_turn(player, row=row, col=col)
        self.field[row][col] = player
