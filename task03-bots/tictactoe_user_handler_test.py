import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('START THE GAME, STUPID BOT')
    assert send_message.call_args_list == [
        mocker.call('Game is not started')
    ]


def test_tictactoe_various_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
    ]


def test_tictactoe_wrong_arguments(mocker: pytest_mock.MockFixture) -> None:
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


def test_tictactoe_winner_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n.X.\n...'),
        mocker.call('XOO\n.X.\n...'),
        mocker.call('XOO\n.X.\n..X'),
        mocker.call('Game is finished, X wins'),
    ]


def test_tictactoe_winner_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...'),
        mocker.call('OX.\n.X.\n...'),
        mocker.call('OX.\nOX.\n...'),
        mocker.call('OX.\nOXX\n...'),
        mocker.call('OX.\nOXX\nO..'),
        mocker.call('Game is finished, O wins'),
    ]


def test_tictactoe_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n..O'),
        mocker.call('X..\n.X.\n..O'),
        mocker.call('XO.\n.X.\n..O'),
        mocker.call('XO.\n.X.\n.XO'),
        mocker.call('XO.\n.XO\n.XO'),
        mocker.call('XOX\n.XO\n.XO'),
        mocker.call('XOX\n.XO\nOXO'),
        mocker.call('XOX\nXXO\nOXO'),
        mocker.call('Game is finished, draw'),
    ]
