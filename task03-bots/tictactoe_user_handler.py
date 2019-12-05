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
        elif self.game is not None:
            try:
                char, row, col = message.split()
                if char == 'X':
                    player = Player.X
                else:
                    player = Player.O
                self.make_turn(player, row=int(row), col=int(col))
            except ValueError:
                self.send_message('Invalid turn\n')
        else:
            self.send_message('Game is not started\n')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        if self.game.can_make_turn(player, row=row, col=col) is True:
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                if winner is None:
                    self.send_message('Game is finished, draw\n')
                else:
                    self.send_message(f'Game is finished, {winner.name} wins\n')
                self.game = None
        else:
            self.send_message('Invalid turn\n')

    def send_field(self) -> None:
        field = ''
        assert self.game is not None
        for row in self.game.field:
            for dot in row:
                if dot is None:
                    field += '.'
                elif dot == Player.X:
                    field += 'X'
                elif dot == Player.O:
                    field += 'O'
            field += '\n'
        self.send_message(field)
