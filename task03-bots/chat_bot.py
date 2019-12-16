from typing import Callable, List
from bot import Bot


class ChatBot(Bot):
    def __init__(self, send_message: Callable[[int, str], None]) -> None:
        super(ChatBot, self).__init__(send_message)
        self.users: List[int] = []

    def handle_message(self, from_user_id: int, message: str) -> None:
        if from_user_id not in self.users:
            self.users.append(from_user_id)
        for user_id in self.users:
            self.send_message(user_id, f'#{from_user_id}: {message}')
