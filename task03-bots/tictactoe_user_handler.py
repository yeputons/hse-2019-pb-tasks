from typing import Callable, Optional, Pattern
import re
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    turn_pattern: Pattern = re.compile(r'([XO])\s+([0-2])\s+([0-2])')

    """Реализация логики бота для игры в крестики-нолики с одним пользователем."""
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
            return
        if self.game is None:
            self.send_message('Game is not started')
            return
        turn_match = self.turn_pattern.fullmatch(message)
        if not turn_match:
            self.send_message('Invalid turn')
            return
        self.make_turn(Player[turn_match.group(1)],
                       col=int(turn_match.group(2)), row=int(turn_match.group(3)))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game is None:
            raise ValueError('Game is not started, when make_turn is called')
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message('Invalid turn')
            return
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self._handle_victory()

    def send_field(self) -> None:
        if self.game is None:
            raise ValueError('Game is not started, when send_field is called')
        msg = ''
        for i in range(3):
            for j in range(3):
                cell = self.game.field[i][j]
                if cell is Player.X:
                    msg += 'X'
                elif cell is Player.O:
                    msg += 'O'
                elif cell is None:
                    msg += '.'
            msg += '\n'
        self.send_message(msg.rstrip('\n'))

    def _handle_victory(self):
        winner = self.game.winner()
        if winner == Player.X:
            self.send_message('Game is finished, X wins')
        elif winner == Player.O:
            self.send_message('Game is finished, O wins')
        else:
            self.send_message('Game is finished, draw')
        self.game = None
