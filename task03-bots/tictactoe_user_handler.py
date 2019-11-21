from typing import Callable, Optional
from bot import UserHandler
from tictactoe import Player, TicTacToe


class TicTacToeUserHandler(UserHandler):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        super(TicTacToeUserHandler, self).__init__(send_message)
        self.game: Optional[TicTacToe] = None

    def handle_message(self, message: str) -> None:
        raise NotImplementedError

    def start_game(self) -> None:
        raise NotImplementedError

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        raise NotImplementedError

    def send_field(self) -> None:
        raise NotImplementedError
