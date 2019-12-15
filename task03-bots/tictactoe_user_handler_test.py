import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('START THE GAME, STUPID BOT')
    assert send_message.call_args_list == mocker.call('Game not started')


def test_tictactoe_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('...\n.O.\n..X'),
        mocker.call('X..\n.O.\n..X'),
        mocker.call('X..\n.O.\n.OX'),
        mocker.call('X.X\n.O.\n.OX'),
        mocker.call('XOX\n.O.\n.OX'),
        mocker.call('Game is finished, O wins')
    ]


def test_x_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('X..\n.X.\n.O.'),
        mocker.call('XO.\n.X.\n.O.'),
        mocker.call('XO.\n.X.\n.OX'),
        mocker.call('Game is finished, X wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\n.O.\nX..'),
        mocker.call('XXO\nOO.\nX..'),
        mocker.call('XXO\nOOX\nX..'),
        mocker.call('XXO\nOOX\nXO.'),
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw')
    ]
