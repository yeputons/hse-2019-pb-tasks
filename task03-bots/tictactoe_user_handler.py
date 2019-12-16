from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        else:
            if self.game is None:
                self.send_message('Game is not started')
            else:
                sign, col, row = message.split()
                self.make_turn(
                    player=Player.X if sign == 'X' else Player.O, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.winner():
                self.send_message('Game is finished, ' + player.name + ' wins')
            else:
                if self.game.is_finished():
                    self.send_message('Game is finished, draw')
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        next_field = ''
        for line in self.game.field:
            for element in line:
                if element is None:
                    next_field += '.'
                else:
                    next_field += element.name
            next_field += '\n'
        self.send_message(next_field[:-1])
