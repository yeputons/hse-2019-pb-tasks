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
            self.start_game()
            return
        if not self.game:
            self.send_message('Game is not started')
            return
        try:
            player_str, id_column, id_row = message.rstrip(' ').split(maxsplit=2)
            if player_str == 'X':
                player = Player.X
            else:
                player = Player.O
            self.make_turn(player, row=int(id_row), col=int(id_column))
        except ValueError:
            self.send_message('Invalid turn')

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
                if self.game.winner() == Player.X:
                    winner = 'X'
                else:
                    winner = 'O'
                self.send_message(f'Game is finished, {winner} wins')
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        message = ''
        for line in self.game.field:
            for symbol in line:
                if symbol == Player.X:
                    message += 'X'
                elif symbol == Player.O:
                    message += 'O'
                else:
                    message += '.'
            message += '\n'
        self.send_message(message[:-1])
