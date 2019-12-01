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
        symbol, col, row = message.rstrip('\n').split(maxsplit=2)
        if symbol != 'X' and symbol != 'O':
            self.send_message('Invalid turn')
            return
        self.make_turn(player={'X': Player.X, 'O': Player.O}[symbol],
                       row=int(row), col=int(col))

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
            self.finish_game()

    def send_field(self) -> None:
        assert self.game
        rows: List[str] = []
        for row in self.game.field:
            rows.append(''.join([col.name if col else '.' for col in row]))
        self.send_message('\n'.join(rows))

    def finish_game(self):
        assert self.game
        player = self.game.winner()
        if not player:
            self.send_message('Game is finished, draw')
        else:
            self.send_message(f'Game is finished, {player.name} wins')
        self.game = None
