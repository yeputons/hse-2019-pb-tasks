from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        try:
            if message == 'start':
                self.start_game()
                return
            if self.game is None:
                self.send_message('Game is not started')
                return
            player, col, row = message.split(maxsplit=2)
            self.make_turn(Player[player], row=int(row), col=int(col))
        except Exception:  # pylint: disable=W0703
            self.send_message('Invalid format')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                if winner is None:
                    self.send_message('Game is finished, draw')
                else:
                    self.send_message(f'Game is finished, {winner.name} wins')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        field = ''
        for row in self.game.field:
            tmp = ''.join([cell.name if cell else '.' for cell in row])
            field += tmp + '\n'
        self.send_message(field.rstrip('\n'))
