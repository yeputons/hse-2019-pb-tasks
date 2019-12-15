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
            now_player = Player.X if player == 'X' else Player.O
            self.make_turn(now_player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if self.game.winner():
                win = self.game.winner()
                result = 'Game is finished, X wins' if win == Player.X \
                    else 'Game is finished, O wins'
                self.send_message(result)
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        playing_field = ''
        for row in range(3):
            for col in range(3):
                if not self.game.field[row][col]:
                    playing_field += '.'
                else:
                    playing_field += 'X' if self.game.field[row][col] == Player.X else 'O'
            playing_field += '\n'
        self.send_message(playing_field[:11])
