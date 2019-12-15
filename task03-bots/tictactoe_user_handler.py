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
        elif self.game is None:
            self.send_message('Game is not started')
        else:
            input_source = message.split()
            if not len(input_source) == 3:
                self.send_message('Invalid turn')
                return

            if (not 0 <= int(input_source[1]) < 3) or (not 0 <= int(input_source[2]) < 3):
                self.send_message('Invalid turn')
                return

            if self.game.can_make_turn(player=Player[input_source[0]],
                                       row=int(input_source[1]), col=int(input_source[2])):
                self.make_turn(player=Player[input_source[0]],
                               row=int(input_source[1]), col=int(input_source[2]))
            else:
                self.send_message('Invalid turn')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        self.game.make_turn(player=player, row=row, col=col)
        if self.game.is_finished():
            winner = self.game.winner()
            if winner is None:
                self.send_message('Game is finished, draw')
            else:
                self.send_message(f'Game is finished, {winner.name} wins')
            self.game = None
            return
        else:
            self.send_field()

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        field = self.game.field
        message = '\n'.join([''.join([cell.name
                                      if cell else '.' for cell in col]) for col in field])
        self.send_message(message)
