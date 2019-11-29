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
        elif self.game is None:
            self.send_message('Game is not started')
        else:
            player_char, row, col = message.split()
            self.make_turn(
                player=Player.X if player_char == 'X' else Player.O, col=int(col), row=int(row))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self) -> None:
        assert self.game
        winner = self.game.winner()
        if winner:
            self.send_message(f'Game is finished, {winner.name} wins')
        else:
            self.send_message('Game is finished, draw')
        self.game = None

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                self.finish_game()
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        output = '\n'
        for row in self.game.field:
            for c in row:
                if c:
                    output += c.name
                else:
                    output += '.'
            output += '\n'
        self.send_message(output)
