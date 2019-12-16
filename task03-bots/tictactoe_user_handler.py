from typing import Callable, Optional, List
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
        if not self.game:
            self.send_message('Game is not started')
            return
        player_name, col, row = message.split()
        self.make_turn(Player[player_name], row=int(row), col=int(col))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if not self.game.can_make_turn(player=player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        field: List[str] = []
        for row in self.game.field:
            field.append(''.join([col.name if col else '.' for col in row]))
        self.send_message('\n'.join(field))

    def finish_game(self) -> None:
        assert self.game
        winner: Optional[Player] = self.game.winner()
        result: str = '{} wins'.format(winner.name) if winner else 'draw'
        self.send_message('Game is finished, {}'.format(result))
        self.game = None
