#!/usr/bin/env python3
import threading
import time
from bot import UserHandler


class AlarmUserHandler(UserHandler):
    def handle_message(self, message: str) -> None:
        try:
            alarm_after = int(message)
        except ValueError:
            self.send_message('Please send number of seconds: pause before new alarm')
            return

        def alarm() -> None:
            time.sleep(alarm_after)  # Untestable! Inject `time.sleep`.
            self.send_message('Alarm!')
        threading.Thread(target=alarm).start()  
