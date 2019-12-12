#!/usr/bin/env python3
import traceback
import sys
from tictactoe_user_handler import TicTacToeUserHandler


def send_message(message: str) -> None:
    print(message)


def main() -> None:
    user = TicTacToeUserHandler(send_message=send_message)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            user.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()
    raise NotImplementedError


if __name__ == '__main__':
    main()
