#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def main() -> None:
    bot = AlarmUserHandler(send_message=print)
    for line in sys.stdin:
        try:
            line = line.rstrip()
            bot.handle_message(line)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
