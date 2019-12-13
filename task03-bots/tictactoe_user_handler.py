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
        if message == 'start':
            self.start_game()
            return
        if self.game is None or self.game.is_finished():
            self.send_message('Game is not started')
            return
        player, move_col, move_row = message.split(maxsplit=2)
        self.make_turn(player=Player[player], row=int(move_row), col=int(move_col))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not self.game.can_make_turn(player=player, row=row, col=col):
            self.send_message('Invalid turn')
        else:
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                self.__send_winner()
                self.game = None

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        field_str = ''
        for row in self.game.field:
            for cell in row:
                if cell:
                    field_str += 'X' if cell == Player.X else 'O'
                else:
                    field_str += '.'
            field_str += '\n'
        field_str = field_str.rstrip('\n')
        self.send_message(field_str)

    def __send_winner(self) -> None:
        """Отправляет пользователю сообщение с информацией об окончании игры"""
        assert self.game
        game_result = 'draw'
        if self.game.winner() is not None:
            game_result = ('X' if self.game.winner() == Player.X else 'O') + ' wins'
        message = f'Game is finished, {game_result}'
        self.send_message(message)
