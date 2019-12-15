#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def main() -> None:
    user_handler = AlarmUserHandler(send_message=print)
    for line in sys.stdin:
        try:
            message = line.rstrip('\n')
            user_handler.handle_message(message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
