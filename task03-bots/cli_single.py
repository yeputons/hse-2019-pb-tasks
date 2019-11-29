#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def send_message(message: str) -> None:
    print(message)


def main() -> None:
    bot = AlarmUserHandler(send_message=send_message)
    for line in sys.stdin:
        try:
            bot.handle_message(line)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
