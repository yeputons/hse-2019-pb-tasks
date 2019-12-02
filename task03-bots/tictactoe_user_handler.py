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
        elif not self.game:
            self.send_message('Game is not started')
        else:
            try:
                character, col, row = message.split(maxsplit=2)
                player = Player({'X': Player.X,
                                 'O': Player.O}.get(character, None))
                assert self.game.can_make_turn(player=player, row=int(row), col=int(col))
                self.make_turn(player=player, row=int(row), col=int(col))
            except (ValueError, AssertionError):
                self.send_message('Invalid turn')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self) -> None:
        """Заканчивает игру в крестики-нолики и сообщает об этом пользователю."""
        assert self.game
        winner = self.game.winner()
        output = '{} wins'.format(winner.name) if winner else 'draw'
        self.send_message('Game is finished, {}'.format(output))
        self.game = None

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        self.game.make_turn(player=player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.finish_game()

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        field = []
        for row in self.game.field:
            field.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(field))
