import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_valid_play_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('X..\nOX.\n..O'),
        mocker.call('X..\nOX.\n.XO'),
        mocker.call('X..\nOX.\nOXO'),
        mocker.call('XX.\nOX.\nOXO'),
        mocker.call('Game is finished, X wins')
    ]
    assert bot.game is None


def test_valid_play_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('O..\nXXO\n...'),
        mocker.call('O..\nXXO\n.X.'),
        mocker.call('OO.\nXXO\n.X.'),
        mocker.call('OO.\nXXO\n.XX'),
        mocker.call('OOO\nXXO\n.XX'),
        mocker.call('Game is finished, O wins')
    ]
    assert bot.game is None


def test_valid_play_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('O..\nXXO\n...'),
        mocker.call('O..\nXXO\n.X.'),
        mocker.call('OO.\nXXO\n.X.'),
        mocker.call('OOX\nXXO\n.X.'),
        mocker.call('OOX\nXXO\nOX.'),
        mocker.call('OOX\nXXO\nOXX'),
        mocker.call('Game is finished, draw')
    ]
    assert bot.game is None


def test_invalid_play(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 1 1')
    bot.handle_message('Hello, Nadya!')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('O..\nXXO\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\nXXO\n.X.'),
        mocker.call('OO.\nXXO\n.X.'),
        mocker.call('OOX\nXXO\n.X.'),
        mocker.call('OOX\nXXO\nOX.'),
        mocker.call('OOX\nXXO\nOXX'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started')
    ]
    assert bot.game is None
