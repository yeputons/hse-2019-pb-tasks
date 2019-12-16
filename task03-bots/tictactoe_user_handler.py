from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.rstrip(' ')
        if message == 'start':
            self.start_game()
            return
        if self.game is None:
            self.send_message('Game is not started')
            return
        player, col, row = message.split()
        self.make_turn(player=Player[player], row=int(row), col=int(col))
        if self.game.is_finished():
            winner = self.game.winner()
            message = 'Game is finished, '
            if winner is None:
                message += 'draw'
            elif winner == Player.X:
                message += 'X wins'
            elif winner == Player.O:
                message += 'O wins'
            self.send_message(message)
            self.game = None

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player=player, row=row, col=col):
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game is not None
        field = [''.join([col.name if col else '.' for col in row])
                 for row in self.game.field]
        self.send_message('\n'.join(field))
