from typing import Callable, Optional, List
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.rstrip('\n')
        if message == 'start':
            self.start_game()
            return
        if not self.game:
            self.send_message('Game is not started')
            return
        symbol, col, row = message.split(maxsplit=2)
        if symbol in ['X', 'O'] and 0 <= int(row) < 3 and 0 <= int(col) < 3:
            self.make_turn(player={'X': Player.X, 'O': Player.O}[symbol],
                           col=int(col), row=int(row))
        else:
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not self.game.can_make_turn(player=player, row=row, col=col):
            self.send_message('Invalid turn')
        else:
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        assert self.game
        field: List[str] = []
        for row in self.game.field:
            field.append(''.join([col.name if col else '.' for col in row]))
        self.send_message('\n'.join(field))

    def finish_game(self) -> None:
        assert self.game
        winner = self.game.winner()
        result: str = '{} wins'.format(winner.name) if winner else 'draw'
        self.send_message('Game is finished, {}'.format(result))
        self.game = None
