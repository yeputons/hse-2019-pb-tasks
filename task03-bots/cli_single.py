#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def main() -> None:
    alarm_bot = AlarmUserHandler(print)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            alarm_bot.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
