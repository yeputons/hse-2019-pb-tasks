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
            person_now, column, row = message.split()
            player = Player.X if person_now == 'X' else Player.O
            self.make_turn(player=player, row=int(row), col=int(column))

    def start_game(self) -> None:
        """Начинает новую игру в крестики-нолики и сообщает об этом пользователю."""
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player=player, row=row, col=col):
            self.game.make_turn(player=player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                if self.game.winner() == Player.X:
                    result = 'Game is finished,X wins'
                elif self.game.winner() == Player.O:
                    result = 'Game is finished,O wins'
                else:
                    result = 'Game is finished,draw'
                self.game = None
                self.send_message(result)
        else:
            self.send_message('Invalid turn')

    def send_field(self) -> None:
        assert self.game
        output = ''
        for row in self.game.field:
            for cell in row:
                if cell == Player.O:
                    output += ' 0 '
                elif cell == Player.X:
                    output += ' X '
                else:
                    output += ' . '
            output += '\n'
        output = output.rstrip('\n')
        self.send_message(output)
