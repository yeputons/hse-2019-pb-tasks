import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 3 1')
    bot.handle_message('X 1 3')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.XO\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_player_x_wins_and_game_is_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Hello')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    bot.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n...\n.O.'),
        mocker.call('X..\n.X.\n.O.'),
        mocker.call('X..\n.XO\n.O.'),
        mocker.call('X..\n.XO\n.OX'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
    ]


def test_player_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('.X.\n.X.\n.O.'),
        mocker.call('.X.\n.X.\n.OO'),
        mocker.call('.XX\n.X.\n.OO'),
        mocker.call('.XX\n.X.\nOOO'),
        mocker.call('Game is finished, O wins')

    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('...\nO..\n..X'),
        mocker.call('X..\nO..\n..X'),
        mocker.call('X..\nOO.\n..X'),
        mocker.call('X..\nOOX\n..X'),
        mocker.call('X.O\nOOX\n..X'),
        mocker.call('X.O\nOOX\nX.X'),
        mocker.call('X.O\nOOX\nXOX'),
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw')

    ]
