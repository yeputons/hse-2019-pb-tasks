import re
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
            self.send_field()
        elif not self.game:
            self.send_message('Game is not started')
        elif re.fullmatch('[XO] [012] [012]', message):
            self.try_make_turn(message)
        else:
            self.send_message('Invalid turn')

    def try_make_turn(self, message: str):
        player = Player.X if message[0] == 'X' else Player.O
        row = int(message[2])
        col = int(message[4])
        if self.game.can_make_turn(player, row=row, col=col):
            self.make_turn(player, row=row, col=col)
            self.send_field()
            self.check_completion()
        else:
            self.send_message('Invalid turn')

    def check_completion(self):
        if self.game.is_finished():
            winner = self.game.winner()
            if winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def start_game(self) -> None:
        self.game = TicTacToe()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        self.game.make_turn(player, row=row, col=col)

    def send_field(self) -> None:
        assert self.game
        out = ''
        for row in self.game.field:
            for point in row:
                if point == Player.O:
                    out += 'O'
                elif point == Player.X:
                    out += 'X'
                else:
                    out += '.'
            out += '\n'
        self.send_message(out[0:11])
