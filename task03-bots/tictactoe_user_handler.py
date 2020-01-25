from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe
import sys


class TicTacToeUserHandler(UserHandler):
    """Реализация логики боты для игры в крестики-нолики с одним пользователем."""

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            player, input_col, input_row = message.split(maxsplit=2)
            col, row = int(input_col), int(input_row)
            if not self.game.can_make_turn(Player[player], row=row, col=col):
                self.send_message('Invalid turn')
            else:
                self.make_turn(Player[player], row=row, col=col)

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self) -> None:
        assert self.game
        winner = self.game.winner()
        if not winner:
            message = 'Game is finished, draw'
        elif winner == Player.X:
            message = 'Game is finished, X wins'
        else:
            message = 'Game is finished, O wins'
        self.send_message(message)
        self.game = None

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        rows = []
        for row in self.game.field:
            rows.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(rows))

bot = TicTacToeUserHandler(send_message=print)
for line in sys.stdin:
    bot.handle_message(line.rstrip('\n'))
