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
            return
        if message == 'start':
            self.start_game()
            return
        assert self.game
        if not (message == 'start'):
            tmpl: List[str] = message.split(' ')
            player: Player = Player[tmpl[0]]
            col = int(tmpl[1])
            row = int(tmpl[2])
            self.make_turn(player, row=row, col=col)
            return

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        """Обрабатывает ход игрока player в клетку (row, col)."""
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                player_win: Optional[Player] = self.game.winner()
                if player_win is None:
                    self.send_message('Game is finished, draw')
                elif player_win == Player.X:
                    self.send_message('Game is finished, X wins')
                elif player_win == Player.O:
                    self.send_message('Game is finished, O wins')
                self.game = None
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        """Отправляет пользователю сообщение с текущим состоянием игры."""
        answer: str = ''
        assert self.game
        for row in self.game.field:
            for element in row:
                if element is None:
                    answer += '.'
                elif element == Player.X:
                    answer += 'X'
                elif element == Player.O:
                    answer += 'O'
            answer += '\n'
        answer = answer.rstrip('\n')
        self.send_message(answer)
