import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXO.\nO..'),
        mocker.call('X.X\nXO.\nO..'),
        mocker.call('XOX\nXO.\nO..'),
        mocker.call('XOX\nXO.\nOX.'),
        mocker.call('XOX\nXOO\nOX.'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw')
    ]


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\nX..'),
        mocker.call('X..\nOO.\nX..'),
        mocker.call('X..\nOOX\nX..'),
        mocker.call('XO.\nOOX\nX..'),
        mocker.call('XO.\nOOX\nXX.'),
        mocker.call('XOO\nOOX\nXX.'),
        mocker.call('XOO\nOOX\nXXX'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\nX..'),
        mocker.call('X..\nOO.\nX..'),
        mocker.call('X..\nOOX\nX..'),
        mocker.call('XO.\nOOX\nX..'),
        mocker.call('XOX\nOOX\nX..'),
        mocker.call('XOX\nOOX\nXO.'),
        mocker.call('Game is finished, O wins')
    ]


def test_invalid_turns(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XOO\n.X.\n...'),
        mocker.call('XOO\n.X.\n..X'),
        mocker.call('Game is finished, X wins')
    ]


def test_game_is_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 0 0')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\nX..'),
        mocker.call('X..\nOO.\nX..'),
        mocker.call('X..\nOOX\nX..'),
        mocker.call('XO.\nOOX\nX..'),
        mocker.call('XOX\nOOX\nX..'),
        mocker.call('XOX\nOOX\nXO.'),
        mocker.call('Game is finished, O wins')
    ]
