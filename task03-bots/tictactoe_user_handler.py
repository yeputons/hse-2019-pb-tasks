from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        command = message.rstrip('\n')
        if command == 'start':
            self.start_game()
            return
        if not self.game:
            self.send_message('Game is not started')
            return
        name, col, row = command.rstrip('\n').split(maxsplit=2)
        if name == 'O':
            self.make_turn(player=Player.O, row=int(row), col=int(col))
        elif name == 'X':
            self.make_turn(player=Player.X, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = None
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        else:
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.current_player() == Player.X:
                    self.send_message('Game is finished, O wins')
                elif self.game.current_player() == Player.O:
                    self.send_message('Game is finished, X wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None

    def send_field(self) -> None:
        assert self.game
        field_print = ''
        for column in self.game.field:
            for row in column:
                if row:
                    field_print += row.name
                else:
                    field_print += '.'
            field_print += '\n'
        self.send_message(field_print.rstrip('\n'))
