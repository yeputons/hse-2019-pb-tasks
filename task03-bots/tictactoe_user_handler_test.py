import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_game_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hello')
    assert send_message.call_args_list == [
        mocker.call('Game is not started')
    ]


def test_start_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...')
    ]


def test_win_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('...\nO..\nX..'),
        mocker.call('...\nOX.\nX..'),
        mocker.call('O..\nOX.\nX..'),
        mocker.call('O.X\nOX.\nX..'),
        mocker.call('Game is finished, X wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('...\n...\nXO.'),
        mocker.call('...\n...\nXOX'),
        mocker.call('...\n.O.\nXOX'),
        mocker.call('...\nXO.\nXOX'),
        mocker.call('O..\nXO.\nXOX'),
        mocker.call('O..\nXOX\nXOX'),
        mocker.call('O.O\nXOX\nXOX'),
        mocker.call('OXO\nXOX\nXOX'),
        mocker.call('Game is finished, draw')
    ]


def test_make_new(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('...\n...\nXO.'),
        mocker.call('...\n.X.\nXO.'),
        mocker.call('...\n.X.\nXOO'),
        mocker.call('...\n...\n...')
    ]


def test_invalid_move_in_same_cell(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('Invalid turn')
    ]


def test_invalid_move_twice_same_player(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('Invalid turn')
    ]


def test_message_after_go(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    bot.handle_message('wow')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('...\nO..\nX..'),
        mocker.call('...\nOX.\nX..'),
        mocker.call('O..\nOX.\nX..'),
        mocker.call('O.X\nOX.\nX..'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')
    ]
