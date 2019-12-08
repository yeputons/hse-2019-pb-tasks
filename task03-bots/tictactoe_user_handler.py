from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            player, col, row = message.rstrip(' ').split(maxsplit=2)
            player = Player.X if player == 'X' else Player.O
            self.make_turn(player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if not self.game.winner():
                self.send_message('Game is finished, draw')
            elif self.game.winner() == Player.X:
                self.send_message('Game is finished, X wins')
            else:
                self.send_message('Game is finished, O wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        msg = ''
        for row in self.game.field:
            for element in row:
                if element is None:
                    msg += '.'
                elif element == Player.X:
                    msg += 'X'
                else:
                    msg += 'O'
            msg += '\n'
        self.send_message(msg[:-1])
