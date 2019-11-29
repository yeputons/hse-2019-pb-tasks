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
        player, row, col = message.rstrip('\n').split(maxsplit=2)
        self.make_turn(Player[player], row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game is None:
            return
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                game_result = 'Game is finished, '
                if self.game.winner() is None:
                    game_result += 'draw'
                elif self.game.winner() == Player.X:
                    game_result += 'X wins'
                else:
                    game_result += 'O wins'
                self.send_message(game_result)
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        if self.game is not None:
            field_in_chars = ''
            i = 0
            for row in self.game.field:
                for cell in row:
                    if cell == Player.X:
                        field_in_chars += 'X'
                    elif cell == Player.O:
                        field_in_chars += 'O'
                    else:
                        field_in_chars += '.'
                if i != 2:
                    field_in_chars += '\n'
                i += 1
            self.send_message(field_in_chars)
