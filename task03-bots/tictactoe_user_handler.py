import traceback
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
        if self.game is None:
            self.send_message('Game is not started')
            return
        try:
            player, col, row = message.split(maxsplit=2)
            if player == 'X':
                self.make_turn(Player.X, row=int(row), col=int(col))
            elif player == 'O':
                self.make_turn(Player.O, row=int(row), col=int(col))
            else:
                print('Invalid turn')
        except Exception:
            print('Invalid turn')

    def start_game(self) -> None:
        try:
            self.game = TicTacToe()
            self.send_field()
        except Exception:
            traceback.print_exc()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() is None:
                    self.send_message('Game is finished, draw')
                    return
                if self.game.winner() == Player.X:
                    self.send_message('Game is finished, X wins')
                    return
                if self.game.winner() == Player.O:
                    self.send_message('Game is finished, O wins')
                    return
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        try:
            for line in self.game.field:
                result_line = ''
                for i in line:
                    if i == Player.X:
                        result_line += 'X'
                    elif i == Player.O:
                        result_line += 'O'
                    else:
                        result_line += '.'
                result_line += '\n'
            self.send_message(result_line.rstrip('\n'))
        except Exception:
            traceback.print_exc()
