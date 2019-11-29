import re
from bot import UserHandler


class CalculatorUserHandler(UserHandler):
    def handle_message(self, message: str) -> None:
        m = re.match(r'(\d+)\s*([+\-*/])\s*(\d+)', message)
        if not m:
            self.send_message("Invalid expression,try smth 112*2")
            return
        a = int(m.group(1))
        op = m.group(2)
        b = int(m.group(3))
        self.send_message(str(self.calculate(a, op, b)))

    @staticmethod
    def calculate(a: int, op: str, b: int) -> int:
        if op == '+':
            return a + b
        if op == '-':
            return a - b
        if op == '*':
            return a * b
        if op == '/':
            return a // b
