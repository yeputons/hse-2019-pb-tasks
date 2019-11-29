#!/usr/bin/env python3
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
            try:
                if self.game is None:
                    print('Game is not started')
                else:
                    player = message[0]
                    row = int(message[2])
                    col = int(message[4])
                    if player == 'X':
                        player = Player(1)
                    else:
                        player = Player(2)
                    try:
                        self.make_turn(player, row=int(row), col=int(col))
                    except Exception:
                        print('Invalid turn')
            except Exception:
                print('Game is not started')
        if self.game is not None and self.game.winner():
            print('Game is finished, {} wins'.format(self.game.winner()))
            self. game = None
        elif self.game is not None and self.game.is_finished():
            print('Game is finished, draw')
            self. game = None

    def start_game(self) -> None:
        self.game = TicTacToe()
        self.send_field()

    def make_turn(self, player: Player, *, row: int, col: int) -> None:
        self.game.make_turn(player, row=row, col=col)
        self.send_field()

    def send_field(self) -> None:
        field = self.game.field
        for col in range(3):
            for row in range(3):
                if field[row][col] is None:
                    print('.', end='')
                elif field[row][col] == Player(1):
                    print('X', end='')
                else:
                    print('O', end='')
            print()
