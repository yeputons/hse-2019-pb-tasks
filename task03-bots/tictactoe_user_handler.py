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
        self.game = TicTacToe()
        if message == "start":
            self.start_game()

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        raise NotImplementedError

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        message = ''
        for line in self.game.field:
            message += '{0[0]} {0[1]} {0[2]}\n'.format([el.name if el else '.' for el in line])
        message.rstrip('\n')
        self.send_message(message)
