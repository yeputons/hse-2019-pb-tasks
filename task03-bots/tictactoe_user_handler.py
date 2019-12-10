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
            player, row, col = message.split()
            self.make_turn(Player.X if player == 'X' else Player.O, row=int(row), col=int(col))
        except Exception:  # pylint: disable=W0703
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
        else:
            self.send_message('Invalid turn')
            return

        if self.game.is_finished():
            winner = self.game.winner()
            if winner:
                self.send_message(f'Game is finished, {winner} wins')
                return
            else:
                self.send_message('Game is finished, draw')
                return

    def send_field(self) -> None:
        if self.game is not None:
            field = ''
            for row in range(3):
                for col in range(3):
                    if self.game.field[row][col] is None:
                        field += '.'
                    else:
                        field += 'X' if self.game.field[row][col] == Player.X else 'O'
                if row < 2:
                    field += '\n'
            self.send_message(field)
