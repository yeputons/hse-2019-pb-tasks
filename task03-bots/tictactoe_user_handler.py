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
        else:
            try:
                player, r, c = message.split()
                row = int(r)
                col = int(c)
            except ValueError:
                self.send_message('Invalid turn')
                return

            if not self.game or self.game.is_finished():
                self.send_message('Game is not started')
                return

            if player not in ('X', 'O'):
                self.send_message('Incorrect choice (X|O)')
                return

            pl = Player.X if player == 'X' else Player.O
            try:
                assert self.game is not None
                if self.game and self.game.can_make_turn(pl, row=row, col=col):
                    self.make_turn(pl, row=row, col=col)
                else:
                    self.send_message('Invalid turn')
            except AssertionError:
                self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if not self.game.winner():
                self.send_message('Game is finished, draw')
                return
            winner = 'X' if player == Player.X else 'O'
            self.send_message(f'Game is finished, {winner} wins')

    def send_field(self) -> None:
        assert self.game is not None
        output = ''
        for row in range(3):
            for col in range(3):
                symbol = '.'
                if self.game.field[row][col]:
                    symbol = 'X' if self.game.field[row][col] == Player.X else 'O'
                output += symbol
            if row != 2:
                output += '\n'
        self.send_message(output)
