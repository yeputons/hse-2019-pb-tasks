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
            return
        if not self.game:
            self.send_message('Game is not started')
            return
        player, col, row = message.split(' ')
        if not self.game.can_make_turn(player=Player[player], row=int(row), col=int(col)):
            self.send_message('Invalid turn')
            return
        self.make_turn(Player[player], row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if self.game.winner() is not None:
                result = f'{player.name} wins'
            if self.game.winner() is None:
                result = 'draw'
            self.send_message(f'Game is finished, {result}')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = [''.join([col.name if col else '.' for col in row]) for row in self.game.field]
        self.send_message('\n'.join(field))
