from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == "start":
            self.start_game()
            return
        if self.game:
            symbol, coord_y, coord_x = message.split(' ')
            if symbol == "X":
                symbol = Player.X
            if symbol == "O":
                symbol = Player.O
            self.make_turn(symbol, row=int(coord_x), col=int(coord_y))
        else:
            self.send_message("Game is not started")
            return

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() == Player.X:
                    self.send_message("Game is finished, X wins")
                    self.game = None
                    return
                if self.game.winner() == Player.O:
                    self.send_message("Game is finished, O wins")
                    self.game = None
                    return
                if self.game.winner() is None:
                    self.send_message("Game is finished, draw")
                    self.game = None
                    return
        else:
            self.send_message("Invalid turn")
            return

    def send_field(self) -> None:
        for i in range(3):
            s = ''
            for j in range(3):
                if not self.game.field[i][j]:
                    s = s+'.'
                if self.game.field[i][j] == Player.X:
                    s = s+'X'
                if self.game.field[i][j] == Player.O:
                    s = s+'O'
            self.send_message(s)
