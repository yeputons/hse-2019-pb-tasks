from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        if self.game is None:
            if message != 'start':
                self.send_message('Game is not started')
                return
            else:
                self.start_game()
                return
        data_message = message.rstrip('\n').split(' ')
        if len(data_message) != 3:
            self.send_message('Invalid turn')
        else:
            try:
                player = Player[data_message[0]]
            except KeyError:
                self.send_message('There is no such player')
                return
            try:
                row = int(data_message[1])
                col = int(data_message[2])
            except ValueError:
                self.send_message('Please send correct turn: Player row col')
                return
            self.make_turn(player=player, row=row, col=col)

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        if self.game is None:
            self.send_message('Invalid turn')
            return
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner = self.game.winner()
            if not winner:
                self.send_message('Game is finished, draw')
            else:
                self.send_message(f'Game is finished, {winner.name} wins')
            self.game = None

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        if self.game is None:
            return
        resline = ''
        for line in self.game.field:
            for el in line:
                if el is not None:
                    resline += el.name
                else:
                    resline += '.'
            resline += '\n'
        resline = resline.rstrip('\n')
        self.send_message(resline)
