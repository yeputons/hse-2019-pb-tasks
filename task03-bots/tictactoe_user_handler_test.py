import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handler_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('well')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\nXX.\n.O.'),
        mocker.call('...\nXXO\n.O.'),
        mocker.call('...\n...\n...')
    ]


def test_tictactoe_user_handler_winner_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('well')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 1')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\nXX.\n.O.'),
        mocker.call('...\nXX.\n.OO'),
        mocker.call('...\nXXX\n.OO'),
        mocker.call('Game is finished, X wins')
    ]


def test_tictactoe_user_handler_winner_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X.O\n...\n...'),
        mocker.call('XXO\n...\n...'),
        mocker.call('XXO\n..O\n...'),
        mocker.call('XXO\n.XO\n...'),
        mocker.call('XXO\n.XO\n..O'),
        mocker.call('Game is finished, O wins'),
    ]


def test_tictactoe_user_handler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('started')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 0')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('...\nXX.\nO..'),
        mocker.call('...\nXXO\nO..'),
        mocker.call('...\nXXO\nO.X'),
        mocker.call('O..\nXXO\nO.X'),
        mocker.call('OX.\nXXO\nO.X'),
        mocker.call('OX.\nXXO\nOOX'),
        mocker.call('OXX\nXXO\nOOX'),
        mocker.call('Game is finished, draw')
    ]


def test_tictactoe_user_handler_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('O 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X.O\n...\n...'),
        mocker.call('Invalid turn'),
    ]
