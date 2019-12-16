from typing import Callable, Optional, Dict, List
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    START_COMMAND = 'start'
    GAME_IS_NOT_STARTED = 'Game is not started'
    INVALID_TURN = 'Invalid turn'
    GAME_FINISHED_X_WINS = 'Game is finished, X wins'
    GAME_FINISHED_O_WINS = 'Game is finished, O wins'
    GAME_FINISHED_DRAW = 'Game is finished, draw'

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
        except ValueError:
            self.send_message(self.INVALID_TURN)
            return
        try:
            self.make_turn(Player[player], row=int(row), col=int(col))
        except (ValueError, KeyError):
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
                result = self.GAME_FINISHED_DRAW
            elif winner.name == 'X':
                result = self.GAME_FINISHED_X_WINS
            else:
                result = self.GAME_FINISHED_O_WINS
            self.send_message(result)
            self.game = None

    def send_field(self) -> None:
        assert self.game is not None

        player_to_char: Dict[Optional[Player], str] = {
            None: '.',
            Player.X: 'X',
            Player.O: 'O'
        }

        messages: List[str] = [
            ''.join([player_to_char[player] for player in row])
            for row in self.game.field
        ]
        self.send_message('\n'.join(messages))
