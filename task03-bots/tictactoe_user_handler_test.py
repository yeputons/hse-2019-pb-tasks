import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_handle_message(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('kek')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_make_turn_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('O.O\n.X.\nX..'),
        mocker.call('OXO\n.X.\nX..'),
        mocker.call('OXO\n.X.\nXO.'),
        mocker.call('OXO\nXX.\nXO.'),
        mocker.call('OXO\nXXO\nXO.'),
        mocker.call('OXO\nXXO\nXOX'),
        mocker.call('Game is finished, draw'),
    ]


def test_make_turn_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('O..\nOX.\nX..'),
        mocker.call('O.X\nOX.\nX..'),
        mocker.call('Game is finished, X wins'),

    ]


def test_make_turn_y_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('OO.\n.X.\nX..'),
        mocker.call('OO.\n.X.\nXX.'),
        mocker.call('OOO\n.X.\nXX.'),
        mocker.call('Game is finished, O wins'),
    ]


def test_make_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('OO.\n.X.\nX..'),
        mocker.call('OO.\n.X.\nXX.'),
        mocker.call('OOO\n.X.\nXX.'),
        mocker.call('Game is finished, O wins'),
    ]


def test_is_game_finished(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('OO.\n.X.\nX..'),
        mocker.call('OO.\n.X.\nXX.'),
        mocker.call('OOO\n.X.\nXX.'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
    ]


def test_is_game_finished(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('OO.\n.X.\nX..'),
        mocker.call('OO.\n.X.\nXX.'),
        mocker.call('OOO\n.X.\nXX.'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
    ]


def test_is_game_finished(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    bot.handle_message('start')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\nX..'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('..O\n...\n.X.'),
        mocker.call('..O\n.X.\n.X.')
    ]





