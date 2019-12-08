from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        message = message.rstrip('\n')
        if message != 'start' and not self.game:
            self.send_message('Game is not started')
            return
        if message == 'start':
            self.start_game()
            return
        marker, col, row = message.split()
        if marker == 'X':
            player = Player.X
        else:
            player = Player.O
        self.make_turn(player, row=int(row), col=int(col))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() == Player.X:
                    self.send_message('Game is finished, X wins')
                elif self.game.winner() == Player.O:
                    self.send_message('Game is finished, O wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None

        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        field = ''
        for row in self.game.field:
            for col in row:
                if col:
                    field += col.name
                else:
                    field += '.'
            field += '\n'
        self.send_message(field.rstrip('\n'))
