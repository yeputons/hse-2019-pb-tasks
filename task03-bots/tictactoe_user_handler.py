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
        player, col, row = message.rstrip('\n').split(maxsplit=2)
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
            game_result = 'Game is finished, {}'.format('draw' if winner is None else
                                                        '{} wins'.format(winner.name))
            self.send_message(game_result)
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None
        field_in_lines = []
        for row in self.game.field:
            row_line = ''
            for cell in row:
                row_line += '{}'.format('.' if cell is None else cell.name)
            field_in_lines.append(row_line)
        self.send_message('\n'.join(field_in_lines))
