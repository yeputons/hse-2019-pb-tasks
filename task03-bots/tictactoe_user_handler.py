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
        if not (message == 'start') and self.game is None:
            self.send_message('Game is not started')
        if message == 'start':
            self.start_game()
        if not (message == 'start') and self.game is not None:
            tmpl: List[str] = message.split(' ')
            player: Player = Player.X
            if tmpl[0] == 'X':
                player = Player.X
            if tmpl[0] == 'O':
                player = Player.O
            col = int(tmpl[2])
            row = int(tmpl[1])
            self.make_turn(player, row=row, col=col)

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        if self.game is not None and self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                pl = self.game.winner()
                if pl is None:
                    self.send_message('Game is finished, draw')
                elif pl == Player.X:
                    self.send_message('Game is finished, X wins')
                elif pl == Player.O:
                    self.send_message('Game is finished, O wins')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        answ: str = ''
        if self.game is not None:
            for row in self.game.field:
                for place in row:
                    if place is None:
                        answ += '.'
                    elif place == Player.X:
                        answ += 'X'
                    elif place == Player.O:
                        answ += 'O'
                answ += '\n'
            answ = answ.rstrip('\n')
            self.send_message(answ)
