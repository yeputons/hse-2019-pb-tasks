import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_game_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hi')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started')
    ]


def test_invalid_turn_bad_player(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_invalid_turn_bad_cell(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')
    ]


def test_get_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('.X.\nOX.\n...'),
        mocker.call('...\n...\n...'),
    ]


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('X..\nOXO\n...'),
        mocker.call('X..\nOXO\n..X'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('OO.\n.XX\n...'),
        mocker.call('OO.\n.XX\n..X'),
        mocker.call('OOO\n.XX\n..X'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('O..\nX..\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('OO.\nXX.\n...'),
        mocker.call('OOX\nXX.\n...'),
        mocker.call('OOX\nXXO\n...'),
        mocker.call('OOX\nXXO\n..X'),
        mocker.call('OOX\nXXO\nO.X'),
        mocker.call('OOX\nXXO\nOXX'),
        mocker.call('Game is finished, draw')
    ]