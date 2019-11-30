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
            player, row, col = message.rstrip('\n').split(maxsplit=2)
            now_player = Player.X if player == 'X' else Player.O
            self.make_turn(now_player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
        else:
            self.send_message('Invalid turn')
            return
        self.send_field()
        if self.game.is_finished():
            if self.game.winner():
                message = 'Game is finished, '
                win = self.game.winner()
                message += 'X wins' if win == Player.X else 'O wins'
                self.send_message(message)
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        message = ''
        for i in self.game.field:
            for j in i:
                if j:
                    message += j.name
                elif j == 2:
                    message += 'O'
                else:
                    message += '.'
            if len(message) < 8:
                message += '\n'
        self.send_message(message)
