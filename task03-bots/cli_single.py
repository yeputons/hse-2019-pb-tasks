#!/usr/bin/env python3
import sys
import traceback
from bot import UserHandler
from alarm_user_handler import AlarmUserHandler
from bot import UserIndependentBot


def send_message(user_id: int, message: str) -> None:
    print('==========')
    print(message)
    print('==========')


def main() -> None:
    bot = UserIndependentBot(send_message=send_message, user_handler=AlarmUserHandler)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            bot.handle_message(1, message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
