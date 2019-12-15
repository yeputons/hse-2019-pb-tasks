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
        if not self.game:
            self.send_message('Game is not started')
            return
        turn, column, row = message.split(maxsplit=2)
        if turn == 'O':
            player = Player.O
        elif turn == 'X':
            player = Player.X
        else:
            self.send_message('Invalid turn')
            return
        try:
            self.make_turn(player=player, row=int(row), col=int(column))
        except ValueError:
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if not (0 <= row < 3 and 0 <= col < 3) or not self.game.can_make_turn(
                player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            if not winner:  # Sad story
                self.send_message('Game is finished, draw')
            elif winner == Player.O:
                self.send_message('Game is finished, O wins')
            else:
                self.send_message('Game is finished, X wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = ''
        for row in self.game.field:
            for cell in row:
                if not cell:
                    field += '.'
                elif cell == Player.O:
                    field += 'O'
                else:
                    field += 'X'
            field += '\n'
        self.send_message(field[:-1])
