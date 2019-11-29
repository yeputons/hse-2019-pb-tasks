from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe   


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def char_by_player(self, player: Optional[Player]) -> chr:
        if player == Player.X:
            return 'X'
        elif player == Player.O:
            return 'O'
        else:
            return '.'

    def player_by_char(self, char: chr) -> Optional[Player]:
        if char == 'X':
            return Player.X
        elif char == 'O':
            return Player.O
        else:
            return None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        elif self.game is None:
            self.send_message('Game is not started');
        else:
            player_char, col, row = message.split()
            self.make_turn(self.player_by_char(player_char), col=int(col), row=int(row))



    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def finish_game(self) -> None:
        if self.game.winner():
            self.send_message(f'Game is finished, {self.char_by_player(self.game.winner())} wins')
        else:
            self.send_message('Game is finished, draw')


    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        if self.game.can_make_turn(player, row=row, col=col):
            self.game.make_turn(player, row=row, col=col)
            self.send_field()
            if self.game.is_finished():
                self.finish_game()
        else:
            self.send_message('Invalid turn')



    def send_field(self) -> None:
        output = ''
        for row in self.game.field:
            for c in row:
                output += self.char_by_player(c)
            output += '\n'
        self.send_message(output)     