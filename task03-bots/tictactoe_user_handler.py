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
            return
        if not self.game:
            self.send_message('Game is not started')
            return

        try:
            new_turn = message.split()

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

        except InvalidTurnException:
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            if winner is None:
                self.send_message('Game is finished, draw')
            elif winner == Player.X:
                self.send_message('Game is finished, X wins')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')

            self.game = None

    def send_field(self) -> None:
        assert self.game
        field_str = ''
        for row in self.game.field:
            for cell in row:
                if cell is None:
                    field_str += '.'
                elif cell == Player.X:
                    field_str += 'X'
                elif cell == Player.O:
                    field_str += 'O'
            field_str += '\n'
        self.send_message(field_str[:-1])
        # without last '\n', because send_message adds '\n'
