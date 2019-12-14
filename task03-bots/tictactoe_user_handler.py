from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        message_words = message.rstrip('\n').split()
        if not self.game and not message_words[0] == 'start':
            self.send_message('Game is not started')
            return
        elif message_words[0] == 'start':
            self.start_game()
            return
        players = {'X': Player.X, 'O': Player.O}
        self.make_turn(
            player=players[message_words[0]],
            row=int(message_words[1]),
            col=int(message_words[2]))

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
        else:
            self.send_message('Invalid turn')
        winner = self.game.winner()
        if winner:
            self.send_message(
                f'Game is finished, {winner.name} wins')
            self.game = None
        else:
            if self.game.is_finished():
                self.send_message('Game is finished, draw')
                self.game = None

    def send_field(self) -> None:
        assert self.game
        field = []
        for row in self.game.field:
            field.append(''.join([cell.name if cell else '.' for cell in row]))
        self.send_message('\n'.join(field))
