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
            dude = message.split(maxsplit=2)[0]
            if dude == 'X':
                player = Player.X
            else:
                player = Player.O
            i = int(message.split(maxsplit=2)[1])
            j = int(message.split(maxsplit=2)[2])
            self.make_turn(player=player, row=i, col=j)

    def start_game(self) -> None:
        self.game = TicTacToe()
        for i in range(3):
            for j in range(3):
                self.game.field[i][j] = None
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        try:
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
        except AssertionError:
            self.send_message('Invalid turn')
            return
        if self.game.is_finished():
            if not self.game.winner():
                self.send_message('Game is finished, draw')
            else:
                if self.game.winner() == Player.X:
                    self.send_message('Game is finished, X wins')
                else:
                    self.send_message('Game is finished, O wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        a = []
        for row in self.game.field:
            for j in row:
                if j:
                    a.append(j.name)
                else:
                    a.append('.')
            a.append('\n')
        del a[len(a) - 1]
        field = ''.join(a)
        self.send_message(field)
