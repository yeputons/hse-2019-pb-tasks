from abc import ABC, abstractmethod
from typing import Callable, Dict, Type, TypeVar


class Bot(ABC):
    def __init__(self, send_message: Callable[[int, str], None]) -> None:
        self.send_message = send_message

    @abstractmethod
    def handle_message(self, from_user_id: int, message: str) -> None:
        pass


T = TypeVar('T', bound='UserHandler')


class UserIndependentBot(Bot):
    def __init__(self, send_message: Callable[[int, str], None], user_handler: Type[T]) -> None:
        super(UserIndependentBot, self).__init__(send_message)
        self.user_handler = user_handler
        self.users: Dict[int, T] = {}

    def handle_message(self, from_user_id: int, message: str) -> None:
        if from_user_id not in self.users:
            self.users[from_user_id] = self.user_handler(
                lambda out_msg: self.send_message(from_user_id, out_msg)
            )
        self.users[from_user_id].handle_message(message)


class UserHandler(ABC):
    def __init__(self, send_message: Callable[[str], None]) -> None:
        self.send_message = send_message

    @abstractmethod
    def handle_message(self, message: str) -> None:
        pass
