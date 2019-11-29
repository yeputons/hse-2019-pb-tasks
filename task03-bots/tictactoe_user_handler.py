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
        elif self.game:
            player, col, row = message.split()
            player_id = Player.X if player == 'X' else Player.O
            self.make_turn(player_id, row=int(row), col=int(col))
        else:
            self.send_message('Game is not started')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game is not None
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner():
                    game_result = 'X wins' if player == Player.X else 'O wins'
                else:
                    game_result = 'draw'
                self.send_message(f'Game is finished, {game_result}')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game is not None
        field = ''
        for row in self.game.field:
            for player in row:
                if player:
                    field += 'X' if player == Player.X else 'O'
                else:
                    field += '.'
            field += '\n'
        self.send_message(field[:len(field) - 1])
