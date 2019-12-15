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
        message = message.rstrip(' ')
        if message == 'start':
            self.start_game()
        elif not self.game:
            self.send_message('Game is not started')
        else:
            player, col, row = message.rstrip(' ').split(maxsplit=2)
            current_player = Player[player]
            self.make_turn(current_player, row=int(row), col=int(col))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if self.game.winner():
                win = self.game.winner()
                result = 'Game is finished, X wins' if win == Player.X \
                    else 'Game is finished, O wins'
                self.send_message(result)
            else:
                self.send_message('Game is finished, draw')
            self.game = None

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        playing_field = ''
        for row in range(3):
            for col in range(3):
                if not self.game.field[row][col]:
                    playing_field += '.'
                else:
                    playing_field += 'X' if self.game.field[row][col] == Player.X else 'O'
            playing_field += '\n'
        self.send_message(playing_field[:11])
