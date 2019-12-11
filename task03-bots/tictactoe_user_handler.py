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
            self.send_field()
            return
        if not self.game:
            self.send_message('Game is not started')
            return

        player_raw, col_raw, row_raw = message.split()

        if player_raw == 'X':
            player = Player.X
        else:
            player = Player.O
        col, row = int(col_raw), int(row_raw)
        self.make_turn(player, col=col, row=row)

    def start_game(self) -> None:
        self.game = TicTacToe()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert isinstance(self.game, TicTacToe)
        if not self.game.can_make_turn(player, col=col, row=row):
            self.send_message('Invalid turn')
            return

        self.game.make_turn(player, col=col, row=row)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            if winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert isinstance(self.game, TicTacToe)
        msg = ''
        for row in self.game.field:
            for cell in row:
                if cell == Player.X:
                    msg += 'X'
                elif cell == Player.O:
                    msg += 'O'
                else:
                    msg += '.'
            msg += '\n'
        self.send_message(msg[:-1])
