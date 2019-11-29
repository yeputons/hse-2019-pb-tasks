#!/usr/bin/env python3
import sys
import traceback
from bot import UserIndependentBot
from tictactoe_user_handler import TicTacToeUserHandler


def send_message(to_user_id: int, message: str) -> None:
    print(message)


def main() -> None:
    bot = UserIndependentBot(send_message=send_message, user_handler=TicTacToeUserHandler)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            bot.handle_message(1, message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
