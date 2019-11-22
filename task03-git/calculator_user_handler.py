from bot import UserHandler

class CalculatorUserHandler(UserHandler):
	# def __init__(self, send_messgae: Callable[[str], None]) -> None:
	# 	super(CalculatorUserHandler, self).__init__(send_message)

	def handle_message(self, message: str) -> None:
		left, op, right = message.split()
		a = int(left)
		b = int(right)
		res = self.calculate(a, op, b)
		self.send_message(str(res))

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