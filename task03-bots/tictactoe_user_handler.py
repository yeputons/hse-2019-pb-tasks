from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.game = None
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            sign, row, collumn = message.split()
            if sign == 'X':
                current_sign = Player.X
            else:
                current_sign = Player.O
            self.make_turn(current_sign, row=int(row), col=int(collumn))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player=player, row=row, col=col):
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                message = 'Game is finished,'
                if winner == Player.X:
                    message += ' X wins'
                elif winner == Player.O:
                    message += ' O wins'
                else:
                    message += ' draw'
                self.send_message(message)
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        field = ''
        for row in range(3):
            for collumn in range(3):
                if self.game.field[row][collumn]:
                    if self.game.field[row][collumn] == Player.X:
                        field += 'X'
                    else:
                        field += 'O'
                else:
                    field += '.'
            field += '\n'
        self.send_message(field)
