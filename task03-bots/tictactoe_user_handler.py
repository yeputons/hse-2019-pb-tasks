from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def __player_to_str(self, player: Optional[Player]) -> str:
        if not player:
            return '.'
        elif player == Player.X:
            return 'X'
        else:
            return 'O'

    def __str_to_player(self, s: str) -> Player:
        if s == 'X':
            return Player.X
        else:
            return Player.O

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        if message == 'start':
            self.__start_game()
            return
        if not self.game:
            self.send_message('Game is not started')
            return

        str_player, str_row, str_col = message.split(maxsplit=3)

        self.__make_turn(
            self.__str_to_player(str_player),
            row=int(str_row),
            col=int(str_col))

    def __start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.__send_field()

    def __make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return

        self.game.make_turn(player, row=row, col=col)
        self.__send_field()
        self.__try_finish()

    def __send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        if self.game:
            self.send_message('\n'.join(
                [''.join(map(self.__player_to_str, line)) for line in self.game.field]
                ))

    def __try_finish(self) -> None:
        if self.game and self.game.is_finished():
            message = 'Game is finished, '
            winner = self.game.winner()
            if winner:
                message += self.__player_to_str(winner) + ' wins'
            else:
                message += 'draw'
            self.send_message(message)
            self.game = None
