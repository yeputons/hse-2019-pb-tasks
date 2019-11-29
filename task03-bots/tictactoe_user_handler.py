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
            try:
                assert self.game is not None
                if message[0] == 'X':
                    player = Player.X
                else:
                    player = Player.O
                row = int(message[2])
                col = int(message[4])
                try:
                    self.make_turn(player, row=row, col=col)
                except Exception:
                    self.send_message('Invalid turn')
            except Exception:
                self.send_message('Game is not started')
                return

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        TicTacToe.make_turn(self.game, player, row=row, col=col)
        self.send_field()
        if TicTacToe.is_finished(self.game) or TicTacToe.is_finished(self.game) == 9:
            winner = TicTacToe.winner(self.game)
            if winner is not None:
                self.send_message('Game is finished, X wins'
                                  if winner == Player.X else 'Game is finished, O wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None
        for i in range(3):
            for j in range(3):
                if self.game.field[j][i] is None:
                    print('.', end='')
                else:
                    if self.game.field[j][i] == Player.X:
                        print('X', end='')
                    else:
                        print('O', end='')
            print()
