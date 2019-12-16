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
        player, col, row = message.split()
        if self.game.can_make_turn(Player[player], row=int(row), col=int(col)):
            self.make_turn(Player[player], row=int(row), col=int(col))
        else:
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            game_end_message = 'Game is finished, {}{}'.format(winner.name if winner else
                                                               'draw', ' wins' if winner
                                                               else '')
            self.send_message(game_end_message)
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None
        field_in_lines = [''.join(cell.name if cell else '.' for cell in row)
                          for row in self.game.field]
        self.send_message('\n'.join(field_in_lines))
