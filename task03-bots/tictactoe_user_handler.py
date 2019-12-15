from typing import Callable, Optional, Dict
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        """Обрабатывает очередное сообщение от пользователя."""
        try:
            if message == 'start':
                self.start_game()
                return
            if self.game is None:
                self.send_message('Game is not started')
                return
            players = {'X': Player.X, 'O': Player.O}
            player_sgn, column, row = message.split()
            self.make_turn(players[player_sgn], col=int(column), row=int(row))
        except Exception:  # pylint: disable=W0703
            self.send_message('Invalid turn')

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        player_sgn = {Player.X: 'X', Player.O: 'O'}
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                winner = self.game.winner()
                if winner is None:
                    self.send_message('Game is finished, draw')
                else:
                    self.send_message(f'Game is finished, {player_sgn[winner]} wins')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        assert self.game
        player_sgn: Dict[Optional[Player], str] = {None: '.', Player.X: 'X', Player.O: 'O'}
        string_field = ''
        for row in self.game.field:
            for cell in row:
                string_field += player_sgn[cell]
            string_field += '\n'
        self.send_message(string_field[:-1])
