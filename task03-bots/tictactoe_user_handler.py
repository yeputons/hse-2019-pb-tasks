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
            return
        if not self.game:
            self.send_message('Game is not started')
            return
        player, col, row = message.split(maxsplit=2)
        if not (player == 'X' or player == 'O'):
            self.send_message('Invalid turn')
            return
        try:
            self.make_turn(player=Player[player], row=int(row), col=int(col))
        except ValueError:
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not 0 <= row < 3 or not 0 <= col < 3 or \
                not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            if winner is None:
                self.send_message('Game is finished, draw')
            elif winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')

            self.game = None

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        assert self.game
        message = '\n'.join([
            ''.join([x.name if x else '.' for x in row])
            for row in self.game.field
        ])
        self.send_message(message)
