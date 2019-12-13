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
            step, col, row = message.split(maxsplit=2)
            if step not in ['X', 'O']:
                self.send_message('Invalid turn')
            self.make_turn(player={'X': Player.X, 'O': Player.O}[step],
                           row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game:
            if not self.game.can_make_turn(player, row=row, col=col):
                self.send_message('Invalid turn')
            else:
                self.game.make_turn(player, row=int(row), col=int(col))
                self.send_field()
                if self.game.is_finished():
                    self.finish_game()

    def finish_game(self):
        assert self.game
        player = self.game.winner()
        if player:
            self.send_message(f'Game is finished, {player.name} wins')
        else:
            self.send_message('Game is finished, draw')
        self.game = None

    def send_field(self) -> None:
        assert self.game
        field = []
        for row in self.game.field:
            field.append(''.join([col.name if col else '.' for col in row]))
        self.send_message('\n'.join(field))
