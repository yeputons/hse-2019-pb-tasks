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
            player, row, col = message.split()

            players = {'X': Player.X, 'O': Player.O}

            if self.game.can_make_turn(player=players[player], row=int(row), col=int(col)):
                self.make_turn(player=players[player], row=int(row), col=int(col))
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
            assert winner
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
        game_field = []
        assert self.game
        field = self.game.field
        assert field
        for col in range(3):
            message = ''
            for row in range(3):
                cell = field[row][col]
                if cell is None:
                    message += '.'
                else:
                    assert cell
                    message += cell.name
            game_field.append(message)
        self.send_message('\n'.join(game_field))
