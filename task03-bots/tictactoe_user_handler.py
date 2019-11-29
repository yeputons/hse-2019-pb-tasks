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
            who, col, row = message.split()
            player = Player.X if who == 'X' else Player.O
            self.make_turn(player=player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game.can_make_turn(player=player, row=row, col=col):
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() == Player.X:
                    result = 'Game is finished, X wins'
                elif self.game.winner() == Player.O:
                    result = 'Game is finished, O wins'
                else:
                    result = 'Game is finished, draw'
                self.send_message(result)
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        output = ''
        for rows in self.game.field:
            for cell in rows:
                if cell == Player.X:
                    output += 'X'
                elif cell == Player.O:
                    output += 'O'
                else:
                    output += '.'
            output += '\n'
        output = output.rstrip('\n')
        self.send_message(output)
