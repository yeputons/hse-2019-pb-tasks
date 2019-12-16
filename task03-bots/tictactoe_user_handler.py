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
        elif self.game is None:
            self.send_message('Game is not started')
            return
        player, col, row = message.split()
        self.make_turn(player=Player[player], row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if not 0 <= row < 3 or not 0 <= col < 3 or self.game is None:
            self.send_message('Invalid turn')
            return
        if not self.game.can_make_turn(player=player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if not self.game.is_finished():
            return
        winner = self.game.winner()
        if winner is None:
            self.send_message('Game is finished, draw')
        else:
            self.send_message('Game is finished, {0} wins'.format(winner.name))
        self.game = None

    def send_field(self) -> None:
        assert self.game
        field = ''
        for line in self.game.field:
            for col in line:
                field += col.name if col else '.'
            field += '\n'
        field = field.rstrip('\n')
        self.send_message(field)
