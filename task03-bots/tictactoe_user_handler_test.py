import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler

def test_TicTacToeUserHandler_winX(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...'),
	mocker.call('...'),
	mocker.call('...'),
	mocker.call('...'),
        mocker.call('.X.'),
	mocker.call('...'),
        mocker.call('..O'),
        mocker.call('.X.'),
	mocker.call('...'),
	mocker.call('Invalid turn'),
        mocker.call('.XO'),
        mocker.call('.X.'),
	mocker.call('...'),
        mocker.call('.XO'),
        mocker.call('.X.'),
	mocker.call('O..'),
        mocker.call('.XO'),
        mocker.call('.X.'),
	mocker.call('OX.'),
        mocker.call('Game is finished, X wins'),
	]


def test_TicTacToeUserHandler_winO(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...'),
	mocker.call('...'),
	mocker.call('...'),
	mocker.call('X..'),
        mocker.call('...'),
	mocker.call('...'),
        mocker.call('X.O'),
        mocker.call('...'),
	mocker.call('...'),
	mocker.call('Invalid turn'),
        mocker.call('XXO'),
        mocker.call('...'),
	mocker.call('...'),
        mocker.call('XXO'),
        mocker.call('..O'),
	mocker.call('...'),
        mocker.call('XXO'),
        mocker.call('.XO'),
	mocker.call('...'),
	mocker.call('XXO'),
        mocker.call('.XO'),
	mocker.call('..O'),
        mocker.call('Game is finished, O wins'),
	]


def test_TicTacToeUserHandler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...'),
	mocker.call('...'),
	mocker.call('...'),
	mocker.call('X..'),
        mocker.call('...'),
	mocker.call('...'),
        mocker.call('X.O'),
        mocker.call('...'),
	mocker.call('...'),
	mocker.call('Invalid turn'),
        mocker.call('X.O'),
        mocker.call('...'),
	mocker.call('X..'),
        mocker.call('X.O'),
        mocker.call('O..'),
	mocker.call('X..'),
        mocker.call('X.O'),
        mocker.call('OX.'),
	mocker.call('X..'),
        mocker.call('X.O'),
        mocker.call('OX.'),
	mocker.call('X.O'),
	mocker.call('X.O'),
        mocker.call('OXX'),
	mocker.call('X.O'),
	mocker.call('XOO'),
        mocker.call('OXX'),
	mocker.call('X.O'),
	mocker.call('XOO'),
        mocker.call('OXX'),
	mocker.call('XXO'),
        mocker.call('Game is finished, draw'),
	]
