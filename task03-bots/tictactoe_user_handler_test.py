import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_game_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hi')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('Invalid turn'),
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\n.X.'),
        mocker.call('OO.\n.X.\n.X.'),
        mocker.call('OO.\n.X.\n.XX'),
        mocker.call('OOO\n.X.\n.XX'),
        mocker.call('Game is finished, O wins'),
    ]


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXO.\n..O'),
        mocker.call('X..\nXO.\nX.O'),
        mocker.call('Game is finished, X wins'),
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\nO..\n...'),
        mocker.call('XOX\nO.X\n...'),
        mocker.call('XOX\nOOX\n...'),
        mocker.call('XOX\nOOX\nX..'),
        mocker.call('XOX\nOOX\nX.O'),
        mocker.call('XOX\nOOX\nXXO'),
        mocker.call('Game is finished, draw'),
    ]


def test_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.O.\n...'),
    ]
