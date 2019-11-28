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
        elif not self.game:
            self.send_message('Game is not started')
        else:
            move, row, col = message.rstrip('\n').split(maxsplit=2)
            if self.game.current_player:
                self.make_turn(self.game.current_player, row=int(row), col=int(col))
            else:
                return



    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        raise NotImplementedError

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        raise NotImplementedError

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        raise NotImplementedError
