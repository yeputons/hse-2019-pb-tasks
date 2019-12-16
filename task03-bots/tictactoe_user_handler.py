from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            side, col, row = message.split(maxsplit=2)
            if side == 'X':
                player = Player.X
            if side == 'O':
                player = Player.O
            self.make_turn(player=player, row=int(row), col=int(col))

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
        field = '\n'.join([''.join([
            cell.name if cell else '.' for cell in row]) for row in self.game.field])
        self.send_message(field)
