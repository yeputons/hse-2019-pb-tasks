from typing import Callable, Optional
import traceback
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:  # add try,exept
        """Обрабатывает очередное сообщение от пользователя."""
        players_signs = {'O': Player.O, 'X': Player.X}
        try:
            if message == 'start':
                self.start_game()
                return
            if self.game is None:
                self.send_message('Game is not started')
                return
            player_sign, column, row = message.split()
            self.make_turn(players_signs[player_sign], row=int(row), col=int(column))

        except Exception:  # pylint: disable=W0703
            traceback.print_exc()

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        inverse_player_signs = {Player.O: 'O', Player.X: 'X'}
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                if winner is None:
                    self.send_message('Game is finished, draw')
                else:
                    self.send_message(f'Game is finished, {inverse_player_signs[winner]} wins')
            return
        self.send_message('Invalid turn')
        return

    def send_field(self) -> None:
        assert self.game
        str_of_game = ''
        for i in range(3):
            for j in range(3):
                if self.game.field[i][j] is None:
                    str_of_game += '.'
                else:
                    str_of_game += 'X' if self.game.field[i][j] == Player.X else 'O'
            str_of_game += '\n'
        self.send_message(str_of_game[:-1])
