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
        if not self.game:
            self.send_message('Game is not started')
            return
        tokens = message.split()
        assert len(tokens) == 3
        char, col, row = tokens[0], int(tokens[1]), int(tokens[2])
        player = Player.X if char == 'X' else Player.O
        self.make_turn(player, row=row, col=col)

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
            winner = self.game.winner()
            if winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        message = '\n'.join([
            ''.join(['.XO' [x.value if x else 0] for x in row])
            for row in self.game.field
        ])
        self.send_message(message)
