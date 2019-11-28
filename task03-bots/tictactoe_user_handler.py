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
            self.send_field()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            chips, col, row = message.split()
            if chips == 'X':
                player = Player.X
            else:
                player = Player.O
            self.make_turn(player, row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert isinstance(self.game, TicTacToe)
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
        else:
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                turn = self.game.current_player()
                if not turn:
                    self.send_message('Game is finished, draw')
                else:
                    if turn == Player.O:
                        win = 'X'
                    else:
                        win = 'O'
                    self.send_message('Game is finished, {} wins'.format(win))
                self.game = None

    def send_field(self) -> None:
        assert isinstance(self.game, TicTacToe)
        board = ''
        for row in self.game.field:
            for col in row:
                if col:
                    board += col.name
                else:
                    board += '.'
            board += '\n'
        self.send_message(board.rstrip('\n'))
