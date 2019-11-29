from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class InvalidTurnException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        elif self.game:
            try:
                new_turn = message.split(' ')

                if len(new_turn) != 3:
                    raise InvalidTurnException

                if new_turn[0] == 'X':
                    player = Player.X
                elif new_turn[0] == 'O':
                    player = Player.O
                else:
                    raise InvalidTurnException

                try:
                    col, row = map(int, new_turn[1:3])
                except ValueError:
                    raise InvalidTurnException

                try:
                    self.make_turn(player=player, row=row, col=col)
                except AssertionError:
                    raise InvalidTurnException

                self.send_field()
                if self.game.is_finished():
                    winner = self.game.winner()
                    if winner is None:
                        self.send_message('Game is finished, draw')
                    elif winner == Player.X:
                        self.send_message('Game is finished, X wins')
                    elif winner == Player.O:
                        self.send_message('Game is finished, O wins')
                    else:
                        assert False

                    self.game = None

            except InvalidTurnException:
                self.send_message('Invalid turn')
        else:
            self.send_message('Game is not started')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        self.game.make_turn(player=player, row=row, col=col)

    def send_field(self) -> None:
        assert self.game
        for row in self.game.field:
            for cell in row:
                if cell is None:
                    print('.', end='')
                elif cell == Player.X:
                    print('X', end='')
                elif cell == Player.O:
                    print('O', end='')
                else:
                    assert False
            print('')
