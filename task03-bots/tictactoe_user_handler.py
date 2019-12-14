from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        bot_message = message.rstrip('\n').split()
        if bot_message[0] != 'start' and not self.game:
            self.send_message('Game is not started')
        elif bot_message[0] == 'start':
            self.start_game()
        else:
            if bot_message[0] == 'X':
                cur_player = Player.X
            else:
                cur_player = Player.O
            self.make_turn(cur_player, row=int(bot_message[2]), col=int(bot_message[1]))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, col=col, row=row):
            self.game.make_turn(player, col=col, row=row)
            self.send_field()
        else:
            self.send_message('Invalid turn')
        if self.game.is_finished():
            finish_str = 'Game is finished, '
            winner = self.game.winner()
            if not winner:
                self.send_message(finish_str + 'draw')
            else:
                self.send_message(finish_str + str(winner.name) + ' wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = []
        for row in self.game.field:
            field.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(field))
