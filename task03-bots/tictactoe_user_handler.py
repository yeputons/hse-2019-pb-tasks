import traceback
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
            if self.game:
                how, id_column, id_line = message.split()
                if how == 'X':
                    player = Player.X
                else:
                    player = Player.O
                self.make_turn(player, row=int(id_line), col=int(id_column))
            else:
                self.send_message('Game is not started')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not none
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner():
                    if self.game.winner() == Player.X:
                        winner = 'X'
                    else:
                        winner = 'O'
                    self.send_message(f'Game is finished, {winner} wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game is not none
        message = ''
        for line in self.game.field:
            for symbol in line:
                if symbol == Player.X:
                    message += 'X'
                else:
                    if symbol == Player.O:
                        message += 'O'
                    else:
                        message += '.'
            message += '\n'
        self.send_message(field[:len(field) - 1])
