from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            move, row, col = message.rstrip('\n').split(maxsplit=2)
            if self.game.can_make_turn(Player.X if move == 'X'
                                       else Player.O, row=int(row), col=int(col)):
                self.make_turn(Player.X if move == 'X' else Player.O, row=int(row), col=int(col))
            else:
                self.send_message('Invalid turn')

    def finish_game(self):
        if self.game.winner() == Player.X:
            self.send_message('Game is finished, X wins')
        elif self.game.winner() == Player.O:
            self.send_message('Game is finished, O wins')
        else:
            self.send_message('Game is finished, draw')
        self.game = None

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        self.game.make_turn(player, row=int(row), col=int(col))
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        field = ''
        assert self.game
        for row in self.game.field:
            for col in row:
                if col:
                    field += col.name
                else:
                    field += '.'
            field += '\n'
        self.send_message(field.rstrip('\n'))
