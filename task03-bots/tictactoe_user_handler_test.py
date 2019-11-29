import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_before_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Initial message')
    bot.handle_message('Not start')
    bot.handle_message('Also not start')
    bot.handle_message('Start will be in following message')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
    ]


def test_correct_turns(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\n..X'),
    ]


def test_invalid_turns(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hi')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 1')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n..O'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
    ]


def test_multiple_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hi')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('start')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n..O'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n..O'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...'),
    ]


def test_x_wins_and_message_after(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hi')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 2')
    bot.handle_message('Game is not started')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\n..X'),
        mocker.call('XO.\nXOO\n..X'),
        mocker.call('XO.\nXOO\nX.X'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')
    ]


def test_o_wins_and_message_after(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hi')
    bot.handle_message('start')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('More message')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('..O\n...\n.X.'),
        mocker.call('..O\n...\n.XX'),
        mocker.call('..O\n.O.\n.XX'),
        mocker.call('.XO\n.O.\n.XX'),
        mocker.call('.XO\n.O.\nOXX'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
    ]


def test_draw_and_message_after(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    bot.handle_message('More massage')
    bot.handle_message('More massage')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\nO..\n...'),
        mocker.call('XOX\nOX.\n...'),
        mocker.call('XOX\nOX.\nO..'),
        mocker.call('XOX\nOXX\nO..'),
        mocker.call('XOX\nOXX\nO.O'),
        mocker.call('XOX\nOXX\nOXO'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')
    ]


def test_invalid_format(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1')
    bot.handle_message('G 2 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 2 1')
    bot.handle_message('More massage')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\nO..\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n..X\n...'),
        mocker.call('Invalid turn')
    ]
