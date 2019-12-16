from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.rstrip(' ')
	 if message == 'start':
	    self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            player, col, row = message.rstrip(' ').split(maxsplit=2)
            right_player = Player.X if player == 'X' else Player.O
            self.make_turn(right_player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
        else:
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                message = 'Game is finished, '
                winner = self.game.winner()
                if not winner:
                    message += 'draw'
                else:
                    message += 'X' if winner == Player.X else 'O'
                    message += ' wins'
		    self.send_message(message)
                    self.game = None

    def send_field(self) -> None:
        assert self.game
        message = ''
        for row in range(3):
            for col in range(3):
                if not self.game.field[row][col]:
                    message += '.'
                else:
                    message += 'X' if self.game.field[row][col] == Player.X else 'O'
            if row < 2:
                message += '\n'
	    self.send_message(message)