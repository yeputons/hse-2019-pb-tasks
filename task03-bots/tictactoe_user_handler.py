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
            mark, col, row = message.split()
            if mark not in ['X', 'O']:
                self.send_message('Invalid turn')
            else:
                player = {'X': Player.X, 'O': Player.O}[mark]
                self.make_turn(player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                self.finish_game()
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        rows = []
        for row in self.game.field:
            rows.append(''.join([col.name if col else '.' for col in row]))
        self.send_message('\n'.join(rows))

    def finish_game(self):
        outcome = {Player.X: 'X wins',
                   Player.O: 'O wins',
                   None: 'draw'}[self.game.winner()]
        # outcome = 'X wins' if self.game.winner() == Player.X else\
        #           'O wins' if self.game.winner() == Player.O else\
        #           'draw'
        self.send_message(f'Game is finished, {outcome}')
        self.game = None
