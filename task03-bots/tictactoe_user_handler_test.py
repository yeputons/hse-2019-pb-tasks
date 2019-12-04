import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_O_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # O wins
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('.X.\nOX.\n...'),
        mocker.call('.X.\nOX.\nO..'),
        mocker.call('.X.\nOX.\nO.X'),
        mocker.call('OX.\nOX.\nO.X'),
        mocker.call('Game is finished, O wins'),
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # O wins
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


def test_game_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # Start
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


def test_X_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # X wins
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('.X.\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('.X.\nOX.\nO..'),
        mocker.call('.X.\nOX.\nOX.'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
    ]


def test_imapcient_X(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # Impacient X
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
