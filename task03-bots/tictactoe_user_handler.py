from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if self.game is not None:
            datamess = message.rstrip('\n').split(' ')
            if len(datamess) != 3:
                self.send_message("Invalid turn")
            else:
                if datamess[0] == 'X':
                    player = Player.X
                elif datamess[0] == 'O':
                    player = Player.O
                else:
                    self.send_message('There is no such player')
                    return
                try:
                    row = int(datamess[1])
                    col = int(datamess[2])
                except ValueError:
                    self.send_message('Please send correct turn: Player row col')
                    return
                self.make_turn(player=player, row=row, col=col)
        else:
            if message != "start":
                self.send_message("Game is not started")
            else:
                self.start_game()

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() is None:
                    self.send_message("Game is finished, draw")
                    self.game = None
                else:
                    self.send_message(f"Game is finished, {str(self.game.winner()).split('.')[1]} wins")
                    self.game = None
        else:
            self.send_message("Invalid turn")

    def send_field(self) -> None:
        if self.game is not None:
            for line in self.game.field:
                lineres = ""
                for el in range(0, 3):
                    if line[el] is not None:
                        lineres += (str(line[el]).split('.'))[1]
                    else:
                        lineres += '.'
                self.send_message(lineres)
