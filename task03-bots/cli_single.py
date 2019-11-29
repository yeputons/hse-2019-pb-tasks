#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler


def send_message(message: str) -> None:
    print(message)


def main() -> None:
    user_handler = AlarmUserHandler(send_message=send_message)
    for line in sys.stdin:
        try:
            user_handler.handle_message(line.rstrip('\n'))
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    main()
