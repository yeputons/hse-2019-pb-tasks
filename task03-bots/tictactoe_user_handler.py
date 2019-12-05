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
            return
        if self.game:
            player, coord_y, coord_x = message.split(' ')
            players = {'X': Player.X, 'O': Player.O}
            if self.game.can_make_turn(player=players[player], row=int(coord_x), col=int(coord_y)):
                self.make_turn(players[player], row=int(coord_x), col=int(coord_y))
                return
            if not self.game.can_make_turn(player=players[player], row=int(coord_x),
                                           col=int(coord_y)):
                self.send_message('Invalid turn')
                return
        else:
            self.send_message('Game is not started')
            return

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game
        game_winner = ''
        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            if self.game.winner() == Player.X:
                game_winner = 'X wins'
            if self.game.winner() == Player.O:
                game_winner = 'O wins'
            if self.game.winner() is None:
                game_winner = 'draw'
            self.send_message(f'Game is finished, {game_winner}')
            self.game = None

    def send_field(self) -> None:
        assert self.game
        field = []
        for i in range(3):
            s = ''
            for j in range(3):
                if not self.game.field[i][j]:
                    s = s + '.'
                if self.game.field[i][j] == Player.X:
                    s = s + 'X'
                if self.game.field[i][j] == Player.O:
                    s = s + 'O'
            field.append(s)
        self.send_message('\n'.join(field))
