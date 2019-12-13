import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrative_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('why ar u gay?')
    bot.handle_message('who saiz im gay?')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('Invalid turn'),
        mocker.call('O.O\n.X.\nX..'),
        mocker.call('OXO\n.X.\nX..'),
        mocker.call('OXO\n.X.\nXO.'),
        mocker.call('OXO\n.X.\nXOX'),
        mocker.call('OXO\n.XO\nXOX'),
        mocker.call('OXO\nXXO\nXOX'),
        mocker.call('Game is finished, draw'),
    ]


def test_integrative_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello mthfckrs')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\nOX.\n...'),
        mocker.call('..X\nOX.\n...'),
        mocker.call('O.X\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O.X\nOX.\nX..'),
        mocker.call('Game is finished, X wins'),
    ]


def test_integrative_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('GOOOOOD MORNING GAMERS!')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\n.X.'),
        mocker.call('X.O\n.O.\n.X.'),
        mocker.call('X.O\nXO.\n.X.'),
        mocker.call('X.O\nXO.\nOX.'),
        mocker.call('Game is finished, O wins'),
    ]
