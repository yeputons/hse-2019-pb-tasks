#!/usr/bin/env python3
import sys
import traceback
from tictactoe_user_handler import TicTacToeUserHandler
from bot import UserHandler


def send_message(message: str) -> None:
    print(message)


def main() -> None:
    handler: UserHandler = TicTacToeUserHandler(send_message=send_message)
    for line in sys.stdin:
        try:
            handler.handle_message(line.rstrip('\n'))
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
