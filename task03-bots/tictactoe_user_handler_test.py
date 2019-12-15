import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\n.O.\n..O'),
        mocker.call('Game is finished, X wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('HMMM')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 1')
    bot.handle_message('Kikoriki')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('.X.\nXO.\n...'),
        mocker.call('OX.\nXO.\n...'),
        mocker.call('OX.\nXO.\n..X'),
        mocker.call('OXO\nXO.\n..X'),
        mocker.call('OXO\nXO.\nX.X'),
        mocker.call('OXO\nXO.\nXOX'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started')
    ]


def test_o_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Who')
    bot.handle_message('start ')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 0')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XXO\nXO.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Game is finished, O wins')
    ]


def test_invalid_turns(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Who')
    bot.handle_message('start')
    bot.handle_message('O 1 2')
    bot.handle_message('X00')
    bot.handle_message('X 1 3')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]
