from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    START_COMMAND = 'start'
    GAME_IS_NOT_STARTED = 'Game is not started'
    INVALID_TURN = 'Invalid turn'
    GAME_FINISHED = 'Game is finished,'

    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        if message == self.START_COMMAND:
            self.start_game()
            return
        if self.game is None:
            self.send_message(self.GAME_IS_NOT_STARTED)
            return
        try:
            player, col, row = message.split(maxsplit=2)
            self.make_turn(Player[player], row=int(row), col=int(col))
        except ValueError:
            self.send_message(self.INVALID_TURN)

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        assert self.game is not None
        if not self.game.can_make_turn(player, row=row, col=col):
            self.send_message(self.INVALID_TURN)
            return

        self.game.make_turn(player, row=row, col=col)
        self.send_field()
        if self.game.is_finished():
            winner: Optional[Player] = self.game.winner()
            if winner is None:
                self.send_message(f'{self.GAME_FINISHED} draw')
                return
            self.send_message(f'{self.GAME_FINISHED} {winner.name} wins')
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None

        def get_char(player: Optional[Player]) -> str:
            if player is None:
                return '.'
            if player is Player.X:
                return 'X'
            return 'O'

        message = ''
        for row in range(0, 3):
            for col in range(0, 3):
                message += get_char(self.game.field[row][col])
            message += '\n'
        self.send_message(message[:-1])
