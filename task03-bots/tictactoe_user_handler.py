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
        message = message.rstrip()
        if message == 'start':
            self.start_game()
        elif self.game:
            how, id_column, id_line = message.split()
            player = Player.X if how == 'X' else Player.O
            self.make_turn(player, row=int(id_line), col=int(id_column))
        else:
            self.send_message('Game is not started')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner():
                    winner = 'X' if self.game.winner() == Player.X else 'O'
                    self.send_message(f'Game is finished, {winner} wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        field = ''
        for line in self.game.field:
            for symbol in line:
                if symbol == Player.X:
                    field += 'X'
                elif symbol == Player.O:
                    field += 'O'
                else:
                    field += '.'
            field += '\n'
        self.send_message(field[:len(field) - 1])
