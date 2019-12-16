from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        bot_message = message.split()
        if message != 'start' and not self.game:
            self.send_message('Game is not started')
        elif message == 'start':
            self.start_game()
        else:
            row = int(bot_message[2])
            col = int(bot_message[1])
            players = {'X': Player.X, 'O': Player.O}
            self.make_turn(players[bot_message[0]], row=row, col=col)

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
            return
        if self.game.is_finished():
            finish_str = 'Game is finished, '
            winner = self.game.winner()
            if not winner:
                self.send_message(f'{finish_str}draw')
            else:
                self.send_message(f'{finish_str}{winner.name} wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = []
        for row in self.game.field:
            field.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(field))
