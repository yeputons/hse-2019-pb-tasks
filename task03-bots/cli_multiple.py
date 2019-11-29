#!/usr/bin/env python3
import sys
import traceback
from alarm_user_handler import AlarmUserHandler
from bot import UserIndependentBot

def send_message(to_user_id: int, message: str) -> None:
    print(f'===== Message to {to_user_id} =====')
    print(message)
    print('==========')


def main() -> None:
    #bot = ChatBot(send_message=send_message)
    bot = UserIndependentBot(
        send_message=lambda user_id, message: user_widgets[user_id].received_message(message),
        user_handler=AlarmUserHandler
    )
    for line in sys.stdin:
        try:
            user_id, message = line.rstrip('\n').split(maxsplit=1)
            bot.handle_message(int(user_id), message)
        except Exception:  # pylint: disable=W0703
            traceback.print_exc()


if __name__ == '__main__':
    main()
