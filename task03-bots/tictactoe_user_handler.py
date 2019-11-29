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
            player, row, col = message.split()
            if player == 'X':
                cur_player = Player.X
            else:
                cur_player = Player.O
            self.make_turn(cur_player, row=int(col), col=int(row))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        print(self.game.can_make_turn(player=player, row=row, col=col))
        if self.game.can_make_turn(player=player, row=row, col=col):
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                message = 'Game is finished, '
                if winner == Player.X:
                    message += 'X wins'
                elif winner == Player.O:
                    message += 'O wins'
                else:
                    message += 'draw'
                self.send_message(message)
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        message = ''
        for row in range(3):
            for col in range(3):
                if self.game.field[row][col]:
                    if self.game.field[row][col] == Player.X:
                        message += 'X'
                    else:
                        message += 'O'
                else:
                    message += '.'
            message += '\n'
        self.send_message(message)
