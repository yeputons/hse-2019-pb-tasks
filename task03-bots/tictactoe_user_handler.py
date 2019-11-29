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
        if message == 'start':
            self.start_game()
        else:
            try:
                player, row, col = message.split()

                player_ = Player.X if player == 'X' else Player.O

                self.make_turn(player=player_, row=int(row), col=int(col))
            except Exception:  # pylint: disable=W0703
                if self.game is None:
                    self.send_message('Game is not started')
                else:
                    self.send_message('Invalid turn')
                return

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        if self.game is not None:
            if self.game.can_make_turn(player=player, row=row, col=col):
                self.game.make_turn(player=player, row=row, col=col)
                if self.game.is_finished():
                    if self.game.winner() is None:
                        self.send_message('Game is finished, draw')
                    else:
                        who = 'X' if self.game.winner() is Player.X else 'O'
                        self.send_message(f'Game is finished, {who} wins')
                    self.game = None
                    return
                else:
                    self.send_field()
            else:
                self.send_message('Invalid turn')
        else:
            self.send_message('Game is not started')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        message = ''
        for col in range(3):
            for row in range(3):
                if self.game is not None:
                    if self.game.field[col][row] is Player.X:
                        message += 'X'
                    elif self.game.field[col][row] is Player.O:
                        message += 'O'
                    else:
                        message += '.'
            if col != 2:
                message += '\n'
        self.send_message(message)
