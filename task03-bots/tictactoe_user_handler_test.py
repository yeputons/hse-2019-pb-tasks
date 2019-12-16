import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\n..X'),
        mocker.call('O..\nOX.\n..X'),
        mocker.call('O..\nOX.\nX.X'),
        mocker.call('O..\nOX.\nXOX'),
        mocker.call('OX.\nOX.\nXOX'),
        mocker.call('OXO\nOX.\nXOX'),
        mocker.call('OXO\nOXX\nXOX'),
        mocker.call('Game is finished, draw'),
    ]


def test_mistakes(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Somebody')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 1')
    bot.handle_message('X 2 2')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\n..X'),
        mocker.call('O..\nOX.\n..X'),
        mocker.call('Invalid turn'),
        mocker.call('O..\nOX.\nX.X'),
        mocker.call('O..\nOX.\nXOX'),
        mocker.call('OX.\nOX.\nXOX'),
        mocker.call('OXO\nOX.\nXOX'),
        mocker.call('OXO\nOXX\nXOX'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started'),
    ]


def test_x_winner(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('..O\n.X.\n..X'),
        mocker.call('.OO\n.X.\n..X'),
        mocker.call('XOO\n.X.\n..X'),
        mocker.call('Game is finished, X wins'),
    ]


def test_o_winner(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('O 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\nOX.\n..X'),
        mocker.call('O..\nOX.\n..X'),
        mocker.call('OX.\nOX.\n..X'),
        mocker.call('OX.\nOX.\nO.X'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
    ]
