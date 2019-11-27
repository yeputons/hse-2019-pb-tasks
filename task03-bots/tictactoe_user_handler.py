from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == 'start':
            self.start_game()
        else:
            if not self.game:
                self.send_message('Game is not started')
                return

            player, row, col = message.split()
            try:
                row = int(row)
                col = int(col)
            except ValueError:
                self.send_message('Please send number of row and col. Ex: X 0 2')
                return

            if player not in ('X', 'O'):
                self.send_message('Player should be only X or O')
                return

            pl = Player.X if player == 'X' else Player.O
            try:
                if self.game.can_make_turn(pl, row=row, col=col):
                    self.make_turn(pl, row=row, col=col)
                else:
                    print(f'Cannot make this turn {row}:{col} by {pl}')
                    # debug  - change to Invalid turn message
            except AssertionError:
                self.send_message('Invalid values of col or row')


    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()
        self.send_message("Game is started!")
        #debug delete print later

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            self.send_message(f'{player} wins')
            #change to smth better

    def send_field(self) -> None:
        for row in range(3):
            for col in range(3):
                if self.game.field[row][col]:
                    print(self.game.field[row][col], end=' ')
                else:
                    print('.', end=' ')
            print()



