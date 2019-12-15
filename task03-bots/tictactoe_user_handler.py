from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message = message.rstrip('\n')
        if message == 'start':
            self.start_game()
            return
        elif not self.game:
            self.send_message('Game not started')
            return
        else:
            player, row, col = message.rstrip('\n').split(maxsplit=2)
            current_player = Player.X if player == 'X' else Player.O
            self.make_turn(current_player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
        else:
            self.send_message('Invalid turn')
            return
        self.send_field()
        if self.game.is_finished():
            if self.game.winner():
                message = 'Game is finished, '
                winner = self.game.winner()
                if winner == Player.X:
                    message += 'X wins'
                else:
                    message += 'O wins'
                self.send_message(message)
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        def get_char(player: Optional[Player]) -> str:

            if player is None:
                return '.'
            if player is Player.X:
                return 'X'
            return 'O'

        message = ''
        for row in range(0, 3):
            for col in range(0, 3):
                message += get_char(self.game.field[row][col])
            message += '\n'
        self.send_message(message[:-1])
