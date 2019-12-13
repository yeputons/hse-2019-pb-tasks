#!/usr/bin/env python3

import sys
import traceback
from tictactoe_user_handler import TicTacToeUserHandler


def main() -> None:
    bot = TicTacToeUserHandler(send_message=print)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            bot.handle_message(message)
        except ValueError:
            traceback.print_exc()


if __name__ == '__main__':
    main()
