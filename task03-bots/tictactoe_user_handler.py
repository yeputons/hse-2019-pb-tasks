from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message_bot = message.rstrip('\n').split()
        if message_bot[0] == 'start':
            self.start_game()
        if not self.game:
            self.send_message('Game is not started')
        else:
            players = {'X': Player.X, 'O': Player.O}
            self.make_turn(
                player=players[message_bot[0]],
                row=int(message_bot[1]),
                col=int(message_bot[2]))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
        else:
            self.send_message('Invalid turn')
        winner = self.game.winner()
        if winner is not None:
            if winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None
        field = ''
        for row in self.game.field:
            for col in row:
                if col:
                    field += col.name
                else:
                    field += '.'
            field += '\n'
        self.send_message(field.rstrip('\n'))
