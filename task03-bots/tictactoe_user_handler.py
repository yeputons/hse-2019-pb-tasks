from __future__ import print_function
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
        else:
            if self.game:
                args = message.split(' ')
                if args[0] == 'X':
                    player = Player.X
                else:
                    player = Player.O
                row = int(args[1])
                col = int(args[2])
                self.make_turn(player, row=row, col=col)
            else:
                self.send_message('Game is not started')
                return

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished() or self.game.is_finished() == 9:
                winner = self.game.winner()
                if winner is not None:
                    self.send_message('Game is finished, X wins'
                                      if winner == Player.X else 'Game is finished, O wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        s = ''
        assert self.game
        for i in range(3):
            for j in range(3):
                if self.game.field[j][i] is None:
                    s += '.'
                else:
                    if self.game.field[j][i] == Player.X:
                        s += 'X'
                    else:
                        s += 'O'
            s += '\n'
        self.send_message(s[0:-1])
