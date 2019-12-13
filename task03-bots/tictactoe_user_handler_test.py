import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handler_game_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('world')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started')
    ]


def test_tictactoe_user_handler_game_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_tictactoe_user_handler_X_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...')
    ]


def test_tictactoe_user_handler_O_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...')
    ]


def test_tictactoe_user_handler_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_tictactoe_user_handler_game_over_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...'),
        mocker.call('OX.\n.X.\n...'),
        mocker.call('OXO\n.X.\n...'),
        mocker.call('OXO\n.X.\n.X.'),
        mocker.call('Game is finished, X wins')
    ]


def test_tictactoe_user_handler_game_over_noone_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    bot.handle_message('start')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('..X\n...\n...'),
        mocker.call('..X\n..O\n...'),
        mocker.call('..X\n.XO\n...'),
        mocker.call('..X\n.XO\nO..'),
        mocker.call('..X\n.XO\nO.X'),
        mocker.call('O.X\n.XO\nO.X'),
        mocker.call('O.X\n.XO\nOXX'),
        mocker.call('OOX\n.XO\nOXX'),
        mocker.call('OOX\nXXO\nOXX'),
        mocker.call('Game is finished, draw')
    ]
