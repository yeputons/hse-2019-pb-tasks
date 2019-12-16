import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XX.\n.O.\n..O'),
        mocker.call('XXX\n.O.\n..O'),
        mocker.call('Game is finished, X wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
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
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('.X.\nXO.\n...'),
        mocker.call('OX.\nXO.\n...'),
        mocker.call('OX.\nXO.\n..X'),
        mocker.call('OXO\nXO.\n..X'),
        mocker.call('OXO\nXO.\nX.X'),
        mocker.call('OXO\nXO.\nXOX'),
        mocker.call('OXO\nXOX\nXOX'),
        mocker.call('Game is finished, draw'),
    ]


def test_o_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\nXO.\n...'),
        mocker.call('XXO\nXO.\nO..'),
        mocker.call('Game is finished, O wins')
    ]


def test_invalid_turns(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_game_is_not_started(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start ')
    bot.handle_message('X 1 1')
    bot.handle_message('Who are you?')
    bot.handle_message('Yes')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_restart_game(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X')
    ]
