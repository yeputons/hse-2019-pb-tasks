#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def send_message(message: str) -> None:
    print(f'===== Message =====')
    print(message)
    print('==========')


def main() -> None:
    raise NotImplementedError
    bot = AlarmUserHandler(send_message=send_message)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            bot.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
