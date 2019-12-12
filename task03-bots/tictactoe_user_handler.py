from typing import Callable, Optional, List
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
            player_by_symbol, col, row = message.split()
            if player_by_symbol in ('X', 'O'):
                self.make_turn(player=Player[player_by_symbol], row=int(row), col=int(col))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self):
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
            return

    def send_field(self) -> None:
        assert self.game
        field: List[str] = []
        for row in self.game.field:
            field.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(field))
