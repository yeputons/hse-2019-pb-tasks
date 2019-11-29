#!/usr/bin/env python3
from alarm_user_handler import AlarmUserHandler
import sys
import traceback


def send_message(message: str) -> None:
    print('==========')
    print(message)
    print('==========')


def main() -> None:
    bot = AlarmUserHandler(send_message)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            bot.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
