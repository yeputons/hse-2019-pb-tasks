from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self._start_game()
            return
        if self.game is None:
            self.send_message('Game is not started')
            return

        player_char, row, col = message.split()
        player = Player.X if player_char == 'X' else Player.O
        self.make_turn(player=player, col=int(col), row=int(row))

    def _start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self) -> None:
        assert self.game
        winner = self.game.winner()
        self.game = None
        if winner:
            self.send_message(f'Game is finished, {winner.name} wins')
            return

        self.send_message('Game is finished, draw')

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game

        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        assert self.game
        output = ''
        for row in self.game.field:
            for c in row:
                if c:
                    output += c.name
                else:
                    output += '.'
            output += '\n'
        self.send_message(output.rstrip('\n'))
