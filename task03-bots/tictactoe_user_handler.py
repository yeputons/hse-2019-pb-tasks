from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        message = message.rstrip('\n')
        if message == 'start':
            self.start_game()
        elif self.game is None:
            self.send_message('Game is not started')
        else:
            player_by_symbol, col, row = message.split()
            if player_by_symbol in ('X', 'O'):
                player = Player.X if player_by_symbol == 'X' else Player.O
                self.make_turn(player, row=int(row), col=int(col))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() == Player.X:
                    self.send_message('Game is finished, X wins')
                elif self.game.winner() == Player.O:
                    self.send_message('Game is finished, O wins')
                else:
                    self.send_message('Game is finished, draw')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с состоянием игры."""
        field_message = ''
        for row in self.game.field:
            for player in row:
                field_message += player.name if player else '.'
            field_message += '\n'
        self.send_message(field_message.rstrip('\n'))
