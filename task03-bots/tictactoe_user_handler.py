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
            player, col, row=message.rstrip(' ').split(maxsplit=2)
            if player == 'X':
                self.make_turn(Player.X, row=row, col=col)
            else:
                self.make_turn(Player.O, row=row, col=col)


    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()


    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if not self.game.can_make_turn(Player, row=int(row), col=int(col)):
            print('Invalid turn')
            return
        self.game.make_turn(Player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if not self.game.winner():
                self.send_message('Game is finished, draw')
            elif self.game.winner() == Player.X:
                self.send_message('Game is finished, X wins')
            else:
                self.send_message('Game is finished, O wins')
            self.game = None



    def send_field(self) -> None:
        msg = ''
        for row in range(3):
            for col in range(3):
                if self.game.field[row][col] == None:
                    msg += '.'
                elif self.game.field[row][col] == Player.X:
                    msg += 'X'
                else:
                    msg += 'O'
            msg += '\n'
        self.send_message(msg)
