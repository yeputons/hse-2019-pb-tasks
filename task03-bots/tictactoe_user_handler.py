import traceback
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
            return
        if self.game is None:
            self.send_message('Game is not started')
            return
        try:
            player, col, row = message.split(maxsplit=2)
            players = {'X': Player.X, 'O': Player.O}
            self.make_turn(players[player], row=int(row), col=int(col))
        except Exception:
            print('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return

        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if not self.game.is_finished():
            return

        winner = self.game.winner()
        if winner is None:
            self.send_message('Game is finished, draw')
            self.game = None
            return

        self.send_message(f'Game is finished, {winner.name} wins')
        self.game = None

    def send_field(self) -> None:
        try:
            result_line = ''
            for row in self.game.field:
                for val in row:
                    result_line += '' + val.name if val else '.'
                result_line += '\n'
            self.send_message(result_line.rstrip('\n'))
        except Exception:
            traceback.print_exc()
