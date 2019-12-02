#!/usr/bin/env python3
import sys
import traceback
from tictactoe_user_handler import TicTacToeUserHandler


def main() -> None:
    obj = TicTacToeUserHandler(send_message=print)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            obj.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
