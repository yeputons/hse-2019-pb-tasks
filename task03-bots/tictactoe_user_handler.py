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
        message = message.rstrip('\n')
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            try:
                character, col, row = message.split(maxsplit=2)
                player = self.char_to_player(character)
                if not player:
                    self.send_message('Invalid turn')
                    return
                self.make_turn(Player(player), row=int(row), col=int(col))
            except ValueError:
                self.send_message('Invalid turn')
                return

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def char_to_player(self, char: str) -> Optional[Player]:
        return {
            'O': Player.O,
            'X': Player.X
        }.get(char, None)

    def finish_game(self) -> None:
        assert self.game
        winner = self.game.winner()
        message_end = f'{winner.name} wins' if winner else 'draw'
        self.send_message(f'Game is finished, {message_end}')
        self.game = None

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not (0 <= row < 3 and 0 <= col < 3 and
                self.game.can_make_turn(player, row=row, col=col)):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        str_field = ''
        for row in self.game.field:
            for cell in row:
                character = cell.name if cell else '.'
                str_field += character
            str_field += '\n'
        self.send_message(str_field[:11])
