from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.rstrip('\n')
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            symbol, col, row = message.rstrip('\n').split(maxsplit=2)
            if symbol == 'X':
                player = Player.X
            else:
                player = Player.O
            self.make_turn(player, row=int(row), col=int(col))

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
        field = ''
        for row in self.game.field:
            for col in row:
                if col == Player.X:
                    field += 'X'
                elif col == Player.O:
                    field += 'O'
                else:
                    field += '.'
            field += '\n'
        self.send_message(field.rstrip('\n'))
        